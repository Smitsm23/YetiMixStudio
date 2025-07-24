<script>
	export let searchTerm = '';
	export let selectedBrand = '';
	export let selectedPaintType = '';
	export let selectedModel = '';
    export let selectedGrade = '';
    export let availableGrades = [];
	
	export let uniqueBrands = [];
	export let availablePaintTypes = [];
	export let availableModels = [];

    export let searchSuggestions = []; // For the custom dropdown

    function selectSuggestion(paint) {
        searchTerm = paint.name;
        searchSuggestions = []; // Hide dropdown after selection
    }
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border dark:bg-gray-800 dark:border-gray-700">
    <div class="sm:col-span-4 " role="button" tabindex="0" on:click|stopPropagation on:keydown|stopPropagation on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); /* You can add any click logic here if needed */ } }}>
        <input 
            type="search" 
            placeholder="Filter current selection..." 
            bind:value={searchTerm} 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400">
        
        {#if searchSuggestions.length > 0 && searchTerm.length > 1}
            <ul class="absolute z-10 w-full bg-white dark:bg-gray-700 border dark:border-gray-600 rounded-lg mt-1 max-h-60 overflow-y-auto shadow-lg">
                {#each searchSuggestions as paint (paint.productId)}
                    <li>
                        <button type="button" on:click={() => selectSuggestion(paint)} class="w-full text-left px-4 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white">
                            {paint.name}
                        </button>
                    </li>
                {/each}
            </ul>
        {/if}
    </div>

    <!-- Brand Dropdown -->
    <select bind:value={selectedBrand} class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white">
		<option value="" disabled>Brand</option>
		{#each uniqueBrands as brand}
			<option value={brand}>{brand}</option>
		{/each}
	</select>
	
    <!-- Paint Type Dropdown -->
    <select bind:value={selectedPaintType} disabled={!selectedBrand} class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white disabled:bg-gray-100 disabled:cursor-not-allowed dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:disabled:bg-gray-600">
		<option value="" disabled>Paint Type</option>
		{#each availablePaintTypes as type}
			<option value={type}>{type}</option>
		{/each}
	</select>

    <!-- Model Line Dropdown -->
    <select bind:value={selectedModel} disabled={!selectedPaintType} class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white disabled:bg-gray-100 disabled:cursor-not-allowed dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:disabled:bg-gray-600">
		<option value="" disabled>Model</option>
		{#each availableModels as model}
			<option value={model}>{model}</option>
		{/each}
	</select>

    <!-- Grade Dropdown -->
    <select bind:value={selectedGrade} disabled={!selectedModel || availableGrades.length === 0} class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        <option value="">Grade</option> {#each availableGrades as grade}
            <option value={grade}>{grade}</option>
        {/each}
    </select>
</div>
