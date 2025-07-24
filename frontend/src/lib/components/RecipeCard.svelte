<script>
    export let result;
    export let index;
</script>

<div class="border border-gray-200 rounded-lg p-4 bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
    <div class="flex justify-between items-center mb-3">
        <h3 class="font-bold text-lg text-gray-800 dark:text-gray-100">Option {index + 1}</h3>
        <span class="text-sm font-semibold text-green-700 bg-green-100 px-2 py-1 rounded-full dark:bg-green-900/50 dark:text-green-300">{result.accuracy}% Match</span>
    </div>
    <div class="flex items-center gap-4 mb-3">
        <div class="w-12 h-12 rounded-md border dark:border-gray-600" style="background-color: {result.mixedHex};"></div>
        <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-300">Mixed Result</p>
            <p class="text-xs font-mono text-gray-500 dark:text-gray-400">{result.mixedHex}</p>
        </div>
    </div>
    <ul class="text-sm">
        {#each Object.entries(result.recipe) as [paint, ratio]}
            <li class="text-gray-700 dark:text-gray-300"><span class="font-semibold">{ratio} part{ratio > 1 ? 's' : ''}</span> {paint}</li>
        {/each}
    </ul>
</div>