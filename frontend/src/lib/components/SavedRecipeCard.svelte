<!-- src/lib/components/SavedRecipeCard.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    export let recipe;
    export let allPaints = [];

    const dispatch = createEventDispatcher();

    // Create a map for efficient lookups by paint name
    const paintMap = new Map(allPaints.map(p => [p.name, p]));
</script>

<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-gray-800 flex flex-col gap-4 relative">
    <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg text-gray-800 dark:text-gray-100">Saved Recipe</h3>
        <span class="text-sm font-semibold text-green-700 bg-green-100 px-2 py-1 rounded-full dark:bg-green-900/50 dark:text-green-300">{recipe.accuracy}% Match</span>
    </div>

    <div class="flex items-center justify-around gap-4">
        <div class="text-center">
            <div class="w-16 h-16 rounded-md border dark:border-gray-600 mx-auto" style="background-color: {recipe.target_hex};"></div>
            <p class="mt-2 text-sm font-medium text-gray-600 dark:text-gray-300">Target</p>
            <p class="text-xs font-mono text-gray-500 dark:text-gray-400">{recipe.target_hex}</p>
        </div>
        <div class="text-gray-300 dark:text-gray-600 text-2xl">&rarr;</div>
        <div class="text-center">
            <div class="w-16 h-16 rounded-md border dark:border-gray-600 mx-auto" style="background-color: {recipe.mixed_hex};"></div>
            <p class="mt-2 text-sm font-medium text-gray-600 dark:text-gray-300">Result</p>
            <p class="text-xs font-mono text-gray-500 dark:text-gray-400">{recipe.mixed_hex}</p>
        </div>
    </div>

    <ul class="text-sm border-t dark:border-gray-700 pt-3 mt-auto space-y-1 mb-8">
        {#each Object.entries(recipe.recipe) as [paintName, ratio]}
            {@const fullPaint = paintMap.get(paintName)}
            <li class="text-gray-700 dark:text-gray-300">
                <span class="font-bold text-blue-600 dark:text-blue-400">{ratio} part{ratio > 1 ? 's' : ''}</span> of {fullPaint ? `${fullPaint.brand} - ${paintName}` : paintName}
            </li>
        {/each}
    </ul>

    <!-- Delete Button -->
    <button
        on:click|stopPropagation={() => dispatch('delete', recipe.id)}
        class="absolute bottom-3 right-3 p-2 rounded-full text-gray-400 hover:text-red-600 hover:bg-red-100 dark:hover:text-red-400 dark:hover:bg-red-900/30"
        aria-label="Delete recipe"
    >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
    </button>
</div>