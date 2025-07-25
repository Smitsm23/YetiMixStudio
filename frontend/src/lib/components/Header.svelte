<script>
    import { theme } from '$lib/stores/themeStore.js';
</script>

<header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50">
    <div class="max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            
            <div class="flex-shrink-0">
                <a href="/" class="text-2xl font-bold text-gray-800 dark:text-gray-100 hover:text-blue-600 transition-colors">
                    Pigment
                </a>
            </div>

            <div class="flex items-center space-x-6">
                <nav class="hidden md:flex space-x-6">
                    <a href="/palettes" class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">My Palettes</a>
                    <a href="/inspiration" class="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">Inspiration</a>
                </nav>

                <button on:click={theme.toggle} class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors" aria-label="Toggle theme">
                    {#if $theme === 'light'}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m8.485-8.485l-.707.707M4.222 4.222l-.707.707M21 12h-1M4 12H3m16.778 4.222l-.707-.707M6.343 17.657l-.707-.707M12 5.5A6.5 6.5 0 1012 18.5 6.5 6.5 0 0012 5.5z"></path></svg>
                    {/if}
                </button>
            </div>

        </div>
    </div>
</header>