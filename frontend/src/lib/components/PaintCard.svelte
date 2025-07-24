<script>
    export let paint;
    export let modelLine = '';
    export let isSelected = false;
</script>

<button
    on:click
    class="text-left p-3 rounded-lg transition-all border-2
        {isSelected 
            ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200 dark:bg-blue-900/50 dark:border-blue-400' 
            : 'border-gray-200 bg-white hover:border-blue-400 dark:bg-gray-800 dark:border-gray-600 dark:hover:border-blue-500'}">
    
    <div class="w-full aspect-square rounded-md mb-3 border dark:border-gray-700" style="background-color: {paint.hexCode};"></div>
    
    <div class="h-12"> 
        <h4 class="font-bold text-sm text-gray-800 dark:text-gray-200" title={paint.name}>{paint.name}</h4>
        
        <p class="text-xs text-gray-500 dark:text-gray-400">{paint.brand} - {modelLine}</p>
    </div>
</button>