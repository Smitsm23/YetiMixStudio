<script>
    import { onMount } from 'svelte';
    import { selectedPaints } from '$lib/stores/paletteStore.js';
    import { theme } from '$lib/stores/themeStore.js';
    import { getAllPaints } from '$lib/services/api.js';

    import PaintCard from '$lib/components/PaintCard.svelte';
    import FilterControls from '$lib/components/FilterControls.svelte';
    import ControlPanel from '$lib/components/ControlPanel.svelte';
    import BrandedColorModal from '$lib/components/BrandedColorModal.svelte';

    // --- Core State ---
    let allPaints = [];
    let isLoadingPaints = true;
    let errorMessage = '';
    
    // --- UI State ---
    let viewMode = 'setup'; // 'setup' or 'result'
    let recipeResult = [];
    let targetHex = '#87CEEB';
    let showBrandModal = false;

    // --- Filtering State ---
    let filteredPaints = [];
    let showPaintLibrary = false;
    let searchTerm = '', selectedBrand = '', selectedPaintType = '', selectedModel = '', selectedGrade = '';
    let uniqueBrands = [], availablePaintTypes = [], availableModels = [], availableGrades = [], searchSuggestions = [];
    
    // Brands reserved for the modal target picker
    const excludedBrands = ['Sherwin-Williams'];

    onMount(async () => {
        try {
            let rawPaints = await getAllPaints();
            allPaints = rawPaints.filter(p => 
                p && 
                p.productId != null &&
                p.name && p.name.trim() !== ''
            );
            
            uniqueBrands = [...new Set(allPaints.map(p => p.brand).filter(b => !excludedBrands.includes(b)))].sort();
        } catch (error) {
            console.error("Failed to load paint library:", error);
        } finally {
            isLoadingPaints = false;
        }
    });

    // --- Helper Functions ---
    function getParsedType(paint) {
        if (!paint || !paint.paintType) return 'N/A';
        const match = paint.paintType.match(/^(.*?)\s*\(/);
        return match ? match[1].trim() : paint.paintType;
    }

    function getModelLine(paint) {
        if (!paint) return 'N/A';
        const match = paint.paintType?.match(/\((.*?)\)/);
        if (match && match[1]) {
            return match[1].trim();
        }
        if (paint.grade) {
            return paint.grade;
        }
        return getParsedType(paint);
    }

    function capitalize(str) {
        if (!str) return '';
        return str
            .toLowerCase()
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    // --- Event Handlers ---
    function handleRecipeSuccess(event) {
        recipeResult = event.detail;
        viewMode = 'result';
        errorMessage = '';
    }

    function resetView() {
        recipeResult = [];
        viewMode = 'setup';
        errorMessage = '';
    }

    function handleSelectBrandedColor(event) {
        targetHex = event.detail.hexCode;
        showBrandModal = false;
    }

    // --- Reactive Filtering Logic ---
    $: if (selectedBrand) {
        selectedPaintType = '';
        const typesForBrand = allPaints
            .filter(p => p.brand === selectedBrand)
            .map(p => capitalize(getParsedType(p)));
        availablePaintTypes = [...new Set(typesForBrand)].sort();
    }

    $: if (selectedPaintType) {
        selectedModel = '';
        const modelsForType = allPaints
            .filter(p => p.brand === selectedBrand && getParsedType(p).toLowerCase() === selectedPaintType.toLowerCase())
            .map(p => capitalize(getModelLine(p)));
        availableModels = [...new Set(modelsForType)].sort();
    }

    $: if (selectedModel) {
        selectedGrade = '';
        const gradesForModel = allPaints
            .filter(p => 
                p.brand === selectedBrand && 
                getParsedType(p).toLowerCase() === selectedPaintType.toLowerCase() && 
                getModelLine(p).toLowerCase() === selectedModel.toLowerCase()
            )
            .map(p => p.grade || 'N/A');
        availableGrades = [...new Set(gradesForModel)].sort();
    }

    $: {
        let paints = [];
        showPaintLibrary = selectedBrand && selectedPaintType && selectedModel;

        if (showPaintLibrary) {
            paints = allPaints.filter(p => 
                p.brand === selectedBrand && 
                getParsedType(p).toLowerCase() === selectedPaintType.toLowerCase() &&
                getModelLine(p).toLowerCase() === selectedModel.toLowerCase() &&
                (!selectedGrade || (p.grade || 'N/A') === selectedGrade)
            );

            if (searchTerm.length > 1) {
                 paints = paints.filter(p => 
                    p.name.toLowerCase().includes(searchTerm.toLowerCase())
                );
            }
        }
        filteredPaints = showPaintLibrary ? paints.slice(0, 100) : [];
    }
</script>

<svelte:window on:click={() => searchSuggestions = []} />

<main class="bg-gray-50 dark:bg-gray-900 min-h-screen font-sans p-4 sm:p-8">
    <div class="max-w-screen-2xl mx-auto">
        <header class="text-center mb-10 relative">
            <h1 class="text-4xl sm:text-5xl font-bold text-gray-800 dark:text-gray-100">ColorMix Studio 🎨</h1>
            <p class="text-lg text-gray-600 dark:text-gray-400 mt-2">Find the perfect mixing recipe for any color.</p>
            <button on:click={theme.toggle} class="absolute top-0 right-0 p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                {#if $theme === 'light'}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m8.485-8.485l-.707.707M4.222 4.222l-.707.707M21 12h-1M4 12H3m16.778 4.222l-.707-.707M6.343 17.657l-.707-.707M12 5.5A6.5 6.5 0 1012 18.5 6.5 6.5 0 0012 5.5z"></path></svg>
                {/if}
            </button>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-6 gap-8">
            
            <div class="lg:col-span-2 space-y-8">
                <ControlPanel 
                    bind:targetHex
                    on:success={handleRecipeSuccess}
                    on:error={(e) => errorMessage = e.detail}
                    on:browse={() => showBrandModal = true}
                />

                {#if $selectedPaints.size > 0 && viewMode === 'setup'}
                    <section>
                        <div class="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                            <h3 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-4">Selected Paints ({$selectedPaints.size})</h3>
                            <ul class="space-y-3">
                                {#each Array.from($selectedPaints.values()) as paint (paint.productId)}
                                    <li class="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-700 rounded-md">
                                        <div class="flex items-center space-x-4">
                                            <div class="w-8 h-8 rounded border border-gray-300 dark:border-gray-600" style="background-color: {paint.hexCode || '#fff'};"></div>
                                            <div>
                                                <p class="font-semibold text-gray-900 dark:text-gray-100">{paint.name}</p>
                                                <p class="text-sm text-gray-700 dark:text-gray-300">{paint.brand} - {capitalize(getModelLine(paint))}</p>
                                            </div>
                                        </div>
                                        <button aria-label="Remove paint" class="text-red-600 hover:text-red-800 dark:hover:text-red-400" on:click={() => selectedPaints.togglePaint(paint)}>
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </li>
                                {/each}
                            </ul>
                        </div>
                    </section>
                {/if}

                {#if errorMessage && viewMode === 'setup'}
                    <div class="p-4 text-red-800 bg-red-100 dark:bg-red-900/50 dark:text-red-300 rounded-lg">
                        <p>{errorMessage}</p>
                    </div>
                {/if}
            </div>

            <div class="lg:col-span-4 bg-white p-6 rounded-xl shadow-md border border-gray-200 dark:bg-gray-800 dark:border-gray-700">
                {#if viewMode === 'setup'}
                    <section>
                        <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-4">Paint Library</h2>
                        <FilterControls 
                            bind:searchTerm bind:selectedBrand bind:selectedPaintType bind:selectedModel bind:selectedGrade
                            {uniqueBrands} {availablePaintTypes} {availableModels} {availableGrades} {searchSuggestions}
                        />

                        {#if isLoadingPaints}
                            <p class="text-center text-gray-500 dark:text-gray-400 py-10">Loading paint library...</p>
                        {:else if !showPaintLibrary}
                            <div class="text-center py-10 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                                <p class="text-gray-500 dark:text-gray-400">Please select filters to view available paints.</p>
                            </div>
                        {:else}
                            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                                {#each filteredPaints as paint (paint.productId)}
                                    <PaintCard 
                                        {paint} 
                                        modelLine={capitalize(getModelLine(paint))} 
                                        isSelected={$selectedPaints.has(paint.productId)}
                                        on:click={() => selectedPaints.togglePaint(paint)} 
                                    />
                                {:else}
                                    <p class="col-span-full text-center text-gray-500 dark:text-gray-400 py-10">No paints match your filter criteria.</p>
                                {/each}
                            </div>
                        {/if}
                    </section>
                {:else if viewMode === 'result' && recipeResult.length > 0}
    <section>
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Best Recipe Options</h2>
            <p class="text-gray-600 dark:text-gray-400">Comparing your target color to the best mix for each ingredient count.</p>
            <div class="inline-flex flex-col items-center mt-4">
                <div class="w-20 h-20 rounded-full border-4 border-white dark:border-gray-700 shadow-md" style="background-color: {targetHex};"></div>
                <p class="mt-2 font-semibold text-gray-600 dark:text-gray-300">Your Target</p>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
            {#each recipeResult as result}
                {@const numIngredients = Object.keys(result.recipe).length}
                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md border dark:border-gray-700 p-5 flex flex-col">
                            <div class="flex justify-between items-start mb-4">
                                <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100">{numIngredients}-Paint Mix</h3>
                                <span class="text-sm font-semibold text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/50 px-2 py-1 rounded-full">{result.accuracy}% Match</span>
                            </div>
                            <div class="flex items-center gap-4 mb-4">
                                <div class="w-12 h-12 flex-shrink-0 rounded-lg border dark:border-gray-600 shadow-inner" style="background-color: {result.mixedHex};"></div>
                                <div>
                                    <p class="font-semibold text-gray-600 dark:text-gray-300">Mixed Result</p>
                                    <p class="font-mono text-sm text-gray-500">{result.mixedHex}</p>
                                </div>
                            </div>
                            <ul class="space-y-2 text-sm border-t dark:border-gray-700 pt-4">
                                {#each Object.entries(result.recipe) as [paint, ratio]}
                                    <li class="text-gray-700 dark:text-gray-300">
                                        <span class="font-bold text-blue-600 dark:text-blue-400">{ratio} part{ratio > 1 ? 's' : ''}</span> of {paint}
                                    </li>
                                {/each}
                            </ul>
                        </div>
                    {/each}
                </div>
                
                <div class="text-center">
                    <button on:click={resetView} class="mt-8 bg-gray-200 text-gray-800 dark:bg-gray-600 dark:text-gray-200 font-bold py-2 px-6 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">
                        Start Over
                    </button>
                </div>
            </section>
        {/if}
            </div>
        </div>
    </div>

    {#if showBrandModal}
        <BrandedColorModal
            {allPaints} {getParsedType} {getModelLine} {capitalize}
            on:close={() => showBrandModal = false}
            on:select={handleSelectBrandedColor}
        />
    {/if}
</main>