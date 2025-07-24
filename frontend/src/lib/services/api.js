// This file should be located at: frontend/src/lib/services/api.js

// The URL and port where your .NET backend API is running.
const API_BASE_URL = 'http://localhost:5171'; 


/**
 * Fetches the entire library of paints from the backend.
 * @returns {Promise<Array>} A promise that resolves to the array of paint objects.
 */
export async function getAllPaints() {
    const response = await fetch(`${API_BASE_URL}/api/Paints`);
    if (!response.ok) {
        throw new Error(`Failed to fetch paints: ${response.statusText}`);
    }
    return await response.json();
}

/**
 * Sends a request to the backend to generate mixing recipes.
 * @param {string} targetHex - The target color HEX code.
 * @param {Array} availablePaints - An array of the user's selected paint objects.
 * @returns {Promise<Array>} A promise that resolves to an array of recipe results.
 */
export async function generateRecipes(targetHex, availablePaints) {
    // Using camelCase for the request body to match the .NET model
    const requestBody = {
        targetHex: targetHex,
        availablePaints: availablePaints
    };

    const response = await fetch(`${API_BASE_URL}/api/Recipe/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }
    return await response.json();
}
