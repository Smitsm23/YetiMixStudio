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
    """Represents a single paint color available to the user."""
    product_id: str
    name: str
    cielab_l: float
    cielab_a: float
    cielab_b: float

class RecipeRequest(BaseModel):
    """Defines the structure of an incoming request to the API."""
    target_hex: str = Field(..., example="#87CEEB", description="The target color in HEX format.")
    available_paints: List[PaintInput] = Field(..., description="A list of paints the user has.")

class RecipeOutput(BaseModel):
    """Defines the structure of a single recipe result."""
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
    """Converts a HEX color string to an (R, G, B) tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb_tuple: Tuple[int, int, int]) -> np.ndarray:
    """Converts an RGB tuple (0-255) to a CIE-L*a*b* numpy array."""
    rgb_array = np.array([[rgb_tuple]], dtype=np.uint8)
    return color.rgb2lab(rgb_array)[0][0]

def lab_to_rgb(lab_array: np.ndarray) -> Tuple[int, int, int]:
    """Converts a CIE-L*a*b* numpy array back to an RGB tuple (0-255)."""
    rgb_scaled = color.lab2rgb(lab_array.reshape((1, 1, 3)))
    return tuple((rgb_scaled[0][0] * 255).astype(int))

def rgb_to_hex(rgb_tuple: Tuple[int, int, int]) -> str:
    """Converts an (R, G, B) tuple to a HEX color string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)

def get_color_difference(lab1: np.ndarray, lab2: np.ndarray) -> float:
    """Calculates the Delta E 2000 difference between two L*a*b* colors."""
    return color.deltaE_ciede2000(lab1.reshape((1, 1, 3)), lab2.reshape((1, 1, 3)))[0][0]

def mix_lab_colors(colors_with_ratios: List[Tuple[np.ndarray, int]]) -> np.ndarray:
    """Mixes L*a*b* colors using a weighted average based on ratios."""
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
    """
    This endpoint receives a target color and a list of available paints,
    then calculates and returns the single best mixing recipe for both 
    2-ingredient and 3-ingredient combinations.
    """
    try:
        target_rgb = hex_to_rgb(request.target_hex)
        target_lab = rgb_to_lab(target_rgb)
    except (ValueError, IndexError):
        return []

    available_paints_lab = {
        p.product_id: (p.name, np.array([p.cielab_l, p.cielab_a, p.cielab_b]))
        for p in request.available_paints
    }

    # This dictionary will store the single best recipe for each ingredient count
    best_recipe_by_count = {}
    paint_ids = list(available_paints_lab.keys())

    # --- Test combinations for 2 AND 3 paints ---
    # Loop from 2 ingredients up to 3
    for num_ingredients in range(2, 4):
        # Skip if the user hasn't selected enough paints
        if len(paint_ids) < num_ingredients:
            continue

        # Generate paint combinations (e.g., all 3-paint combos)
        for combo_ids in combinations(paint_ids, num_ingredients):
            combo_paints = [available_paints_lab[pid] for pid in combo_ids]
            
            # Generate ratio combinations (e.g., 1:1:2, 1:2:1, etc.)
            # Using a smaller range for ratios improves performance
            for ratio_combo in product(range(1, 3), repeat=num_ingredients):
                colors_with_ratios = [(paint[1], ratio) for paint, ratio in zip(combo_paints, ratio_combo)]
                mixed_lab = mix_lab_colors(colors_with_ratios)
                delta_e = get_color_difference(target_lab, mixed_lab)
                
                # If we haven't found a recipe for this count yet, or if this one is better, save it
                if num_ingredients not in best_recipe_by_count or delta_e < best_recipe_by_count[num_ingredients]["delta_e"]:
                    recipe_parts = {paint[0]: ratio for paint, ratio in zip(combo_paints, ratio_combo)}
                    best_recipe_by_count[num_ingredients] = {
                        "delta_e": delta_e,
                        "recipe_parts": recipe_parts,
                        "mixed_lab": mixed_lab
                    }

    # --- Format and return the best recipe from each category ---
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

    return output_recipes


# To run this app, save it as main.py and run `uvicorn main:app --reload` in your terminal.
