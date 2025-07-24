<script>
    import { createEventDispatcher } from 'svelte';
    import PaintCard from './PaintCard.svelte';
    import FilterControls from './FilterControls.svelte';

    export let allPaints = [];
    export let getParsedType, getModelLine, capitalize;

    const dispatch = createEventDispatcher();

    const availableModalBrands = ['Sherwin-Williams']; 

    // Filtering State for the modal
    let filteredPaints = [];
    let showPaintLibrary = false;
    let searchTerm = '', selectedBrand = '', selectedPaintType = '', selectedModel = '', selectedGrade = '';
    let availablePaintTypes = [], availableModels = [], availableGrades = [], searchSuggestions = [];
    
    // Reactive filtering logic
    $: if (selectedBrand) {
        selectedPaintType = '';
        const typesForBrand = allPaints.filter(p => p.brand === selectedBrand).map(p => capitalize(getParsedType(p)));
        availablePaintTypes = [...new Set(typesForBrand)].sort();
    }
    $: if (selectedPaintType) {
        selectedModel = '';
        const modelsForType = allPaints.filter(p => p.brand === selectedBrand && getParsedType(p).toLowerCase() === selectedPaintType.toLowerCase()).map(p => capitalize(getModelLine(p)));
        availableModels = [...new Set(modelsForType)].sort();
    }
    $: if (selectedModel) {
        selectedGrade = '';
        const gradesForModel = allPaints.filter(p => p.brand === selectedBrand && getParsedType(p).toLowerCase() === selectedPaintType.toLowerCase() && getModelLine(p).toLowerCase() === selectedModel.toLowerCase()).map(p => p.grade || 'N/A');
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
            if (searchTerm) {
                 paints = paints.filter(p => p.name.toLowerCase().includes(searchTerm.toLowerCase()));
            }
        }
        filteredPaints = showPaintLibrary ? paints.slice(0, 100) : [];
    }

    function handleSelect(paint) {
        dispatch('select', paint);
    }
</script>

<div 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" 
    on:click={(e) => { if (e.target === e.currentTarget) dispatch('close'); }}
    on:keydown={(e) => { if (e.key === 'Escape') dispatch('close'); }}
    role="dialog" 
    aria-modal="true" 
    aria-labelledby="modal-title"
    tabindex="-1"
>
    <div class="w-full max-w-4xl max-h-[90vh] bg-white dark:bg-gray-800 rounded-xl shadow-lg flex flex-col">
        <header class="p-4 border-b dark:border-gray-700 flex justify-between items-center flex-shrink-0">
            <h2 id="modal-title" class="text-xl font-bold text-gray-800 dark:text-gray-100">Select a Branded Target Color</h2>
            <button on:click={() => dispatch('close')} class="text-gray-500 hover:text-gray-800 dark:hover:text-gray-200 text-2xl" aria-label="Close modal">&times;</button>
        </header>

        <div class="p-4 flex-grow overflow-y-auto">
            <FilterControls
                uniqueBrands={availableModalBrands}
                bind:searchTerm bind:selectedBrand bind:selectedPaintType bind:selectedModel bind:selectedGrade
                {availablePaintTypes} {availableModels} {availableGrades} {searchSuggestions}
            />

            {#if !showPaintLibrary}
                <div class="text-center py-10 text-gray-500">Please select filters to view paints.</div>
            {:else}
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 mt-4">
                    {#each filteredPaints as paint (paint.productId)}
                        <PaintCard 
                            {paint}
                            modelLine={capitalize(getModelLine(paint))}
                            on:click={() => handleSelect(paint)}
                        />
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>