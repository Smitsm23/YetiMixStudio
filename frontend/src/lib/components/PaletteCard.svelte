<!-- src/lib/components/PaletteCard.svelte -->
<script>
    export let palette;

    // The 'paints' property is a JSON array of paint objects
    const colors = palette.paints.map(p => p.hexCode);
</script>

<div class="group cursor-pointer">
    <!-- The visual color bar -->
    <div class="flex h-24 w-full overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 group-hover:shadow-lg transition-shadow">
        {#each colors as color}
            <div class="h-full flex-grow" style="background-color: {color};"></div>
        {/each}
    </div>

    <!-- The palette name -->
    <div class="mt-2 text-center">
        <h3 class="font-semibold text-gray-800 dark:text-gray-200">{palette.name}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">{colors.length} Colors</p>
    </div>
</div>
