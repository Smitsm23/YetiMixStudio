<!-- src/lib/components/ControlPanel.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import { selectedPaints } from '$lib/stores/paletteStore.js';
    import { generateRecipes } from '$lib/services/api.js';
    import { user } from '$lib/stores/authStore.js';
    import { supabase } from '$lib/services/supabaseClient.js';

    export let targetHex;
    export let viewMode = 'setup'; // Receive the viewMode from the parent page
    
    const dispatch = createEventDispatcher();
    let isGeneratingRecipes = false;

    // --- State for saving palettes ---
    let paletteName = '';
    let isSaving = false;
    let saveMessage = '';

    // --- Reactive variables for button state ---
    $: isDisabled = isGeneratingRecipes || $selectedPaints.size < 2 || viewMode === 'result';

    function handleHexInput(event) {
        const rawValue = event.target.value;
        const sanitized = rawValue.replace(/[^0-9a-fA-F]/g, '').slice(0, 6);
        targetHex = '#' + sanitized.toUpperCase();
    }

    async function handleGenerateRecipe() {
        if ($selectedPaints.size < 2) {
            dispatch('error', 'Please select at least two paints to mix.');
            return;
        }
        
        isGeneratingRecipes = true;
        dispatch('error', ''); // Clear previous errors
        try {
            const results = await generateRecipes(targetHex, Array.from($selectedPaints.values()));
            if (results && results.length > 0) {
                dispatch('success', results);
            } else {
                dispatch('error', 'Could not generate a recipe with the selected paints.');
            }
        } catch (error) {
            dispatch('error', `API Error: ${error.message}`);
        } finally {
            isGeneratingRecipes = false;
        }
    }

    async function handleSavePalette() {
        if (!paletteName.trim()) {
            saveMessage = 'Error: Please enter a name for your palette.';
            return;
        }
        if ($selectedPaints.size === 0) {
            saveMessage = 'Error: Please select at least one paint to save.';
            return;
        }

        isSaving = true;
        saveMessage = '';

        const paintsToSave = Array.from($selectedPaints.values());

        try {
            const { error } = await supabase
                .from('palettes')
                .insert({ 
                    name: paletteName, 
                    paints: paintsToSave,
                    user_id: $user.id
                });

            if (error) throw error;

            saveMessage = `Success! Palette "${paletteName}" was saved.`;
            paletteName = '';
        } catch (error) {
            saveMessage = `Error saving palette: ${error.message}`;
            console.error('Error saving palette:', error);
        } finally {
            isSaving = false;
        }
    }
</script>

<div class="bg-white p-6 rounded-xl shadow-md border border-gray-200 dark:bg-gray-800 dark:border-gray-700">
    <h2 class="text-2xl font-semibold text-gray-700 mb-4 border-b pb-2 dark:text-gray-200 dark:border-gray-600">Recipe Generator</h2>
    
    <!-- ... form elements ... -->
    <div class="mb-4">
        <label for="target-color-input" class="block font-medium text-gray-600 mb-2 dark:text-gray-300">1. Pick or Find a Target Color</label>
        <div class="flex items-center gap-4">
            <div class="relative w-16 h-16 flex-shrink-0">
                <div
                    class="w-full h-full rounded-md border-2 border-gray-300 dark:border-gray-600"
                    style="background-color: {targetHex};"
                ></div>
                <input
                    type="color"
                    class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    bind:value={targetHex}
                    aria-label="Pick a target color"
                >
            </div>
            <input 
                type="text"
                id="target-color-input" 
                placeholder="#RRGGBB"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                value={targetHex}
                on:input={handleHexInput}
            >
        </div>
    </div>
    <div class="mb-6">
        <button on:click={() => dispatch('browse')} class="w-full text-center px-4 py-2 border-2 border-dashed rounded-lg text-gray-500 hover:text-blue-600 hover:border-blue-500 dark:border-gray-600 dark:hover:border-blue-400 transition-colors">
            Browse Branded Paints...
        </button>
    </div>
    <div class="mb-6">
        <h3 class="font-medium text-gray-600 mb-2 dark:text-gray-300">2. Your Selected Paints ({$selectedPaints.size})</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
            {#if $selectedPaints.size < 2}
                Select at least 2 paints from the library below.
            {:else}
                Ready to mix!
            {/if}
        </p>
    </div>

    <!-- The button now has a simple class list -->
    <button 
        on:click={handleGenerateRecipe}
        disabled={isDisabled}
        class="w-full text-white font-bold py-3 px-4 rounded-lg transition-colors flex items-center justify-center bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:opacity-75 disabled:cursor-not-allowed"
    >
        {#if isGeneratingRecipes}
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            Mixing...
        {:else if viewMode === 'result'}
            Recipe Generated
        {:else}
            Get Recipe
        {/if}
    </button>

    <!-- Save Palette Section -->
    {#if $user}
    <div class="mt-6 pt-6 border-t dark:border-gray-600">
        <h3 class="font-medium text-gray-600 mb-2 dark:text-gray-300">3. Save Your Palette</h3>
        <div class="flex items-center gap-2">
            <input 
                type="text"
                bind:value={paletteName}
                placeholder="My Living Room Palette"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                disabled={isSaving}
            >
            <button 
                on:click={handleSavePalette}
                disabled={isSaving || $selectedPaints.size === 0}
                class="bg-green-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex-shrink-0"
            >
                {isSaving ? 'Saving...' : 'Save'}
            </button>
        </div>
        {#if saveMessage}
            <p class="text-sm mt-2" 
               class:text-green-600={saveMessage.includes('Success')} 
               class:text-red-500={saveMessage.includes('Error')}>
               {saveMessage}
            </p>
        {/if}
    </div>
    {/if}
</div>

<!-- REMOVED the <style> block to prevent conflicts -->
