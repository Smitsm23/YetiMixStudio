# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple
from itertools import combinations
import numpy as np
from skimage import color
from itertools import combinations, product

# --- Pydantic Models for Data Validation ---
class PaintInput(BaseModel):
    product_id: str
    name: str
    cielab_l: float
    cielab_a: float
    cielab_b: float

class RecipeRequest(BaseModel):
    target_hex: str = Field(..., example="#87CEEB", description="The target color in HEX format.")
    available_paints: List[PaintInput]

class RecipeOutput(BaseModel):
    recipe: Dict[str, int]
    accuracy: float
    mixed_hex: str

# --- FastAPI App Initialization ---
app = FastAPI(
    title="ColorMix Studio - Color Logic Service",
    description="A microservice to calculate paint mixing recipes.",
    version="1.0.0"
)

# --- Color Conversion and Calculation Helpers ---
def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb_tuple: Tuple[int, int, int]) -> np.ndarray:
    rgb_array = np.array([[rgb_tuple]], dtype=np.uint8)
    return color.rgb2lab(rgb_array)[0][0]

def lab_to_rgb(lab_array: np.ndarray) -> Tuple[int, int, int]:
    rgb_scaled = color.lab2rgb(lab_array.reshape((1, 1, 3)))
    return tuple((rgb_scaled[0][0] * 255).astype(int))

def rgb_to_hex(rgb_tuple: Tuple[int, int, int]) -> str:
    """Converts an (R, G, B) tuple to a HEX color string."""
    # UPDATED: Use uppercase 'X' for uppercase hex codes
    return '#{:02X}{:02X}{:02X}'.format(*rgb_tuple)

def get_color_difference(lab1: np.ndarray, lab2: np.ndarray) -> float:
    return color.deltaE_ciede2000(lab1.reshape((1, 1, 3)), lab2.reshape((1, 1, 3)))[0][0]

def mix_lab_colors(colors_with_ratios: List[Tuple[np.ndarray, int]]) -> np.ndarray:
    total_ratio = sum(ratio for _, ratio in colors_with_ratios)
    if total_ratio == 0:
        return np.zeros(3)
    
    mixed_lab = np.zeros(3)
    for lab_color, ratio in colors_with_ratios:
        mixed_lab += lab_color * (ratio / total_ratio)
    return mixed_lab

# --- API Endpoint ---
@app.post("/generate-recipe", response_model=List[RecipeOutput])
async def generate_recipe_endpoint(request: RecipeRequest):
    try:
        target_rgb = hex_to_rgb(request.target_hex)
        target_lab = rgb_to_lab(target_rgb)
    except (ValueError, IndexError):
        return []

    available_paints_lab = {
        p.product_id: (p.name, np.array([p.cielab_l, p.cielab_a, p.cielab_b]))
        for p in request.available_paints
    }
    
    best_recipe_by_count = {}
    paint_ids = list(available_paints_lab.keys())
    
    for num_ingredients in range(2, 5):
        if len(paint_ids) < num_ingredients:
            continue
        
        for combo_ids in combinations(paint_ids, num_ingredients):
            combo_paints = [available_paints_lab[pid] for pid in combo_ids]
            
            for ratio_combo in product(range(1, 3), repeat=num_ingredients):
                colors_with_ratios = [(paint[1], ratio) for paint, ratio in zip(combo_paints, ratio_combo)]
                mixed_lab = mix_lab_colors(colors_with_ratios)
                delta_e = get_color_difference(target_lab, mixed_lab)
                
                if num_ingredients not in best_recipe_by_count or delta_e < best_recipe_by_count[num_ingredients]["delta_e"]:
                    recipe_parts = {paint[0]: ratio for paint, ratio in zip(combo_paints, ratio_combo)}
                    best_recipe_by_count[num_ingredients] = {
                        "delta_e": delta_e,
                        "recipe_parts": recipe_parts,
                        "mixed_lab": mixed_lab
                    }

    output_recipes = []
    for num_ingredients in sorted(best_recipe_by_count.keys()):
        recipe = best_recipe_by_count[num_ingredients]
        accuracy = max(0, 100 - recipe['delta_e'])
        mixed_rgb = lab_to_rgb(recipe['mixed_lab'])
        mixed_hex = rgb_to_hex(mixed_rgb)
        
        output_recipes.append(
            RecipeOutput(
                recipe=recipe['recipe_parts'],
                accuracy=round(accuracy, 2),
                mixed_hex=mixed_hex
            )
        )

    output_recipes.sort(key=lambda x: x.accuracy, reverse=True)
    return output_recipes
