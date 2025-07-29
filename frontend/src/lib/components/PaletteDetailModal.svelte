<!-- src/lib/components/PaletteDetailModal.svelte -->
<script>
    import { createEventDispatcher, onMount, onDestroy } from 'svelte';
    import { supabase } from '$lib/services/supabaseClient.js';

    export let palette;

    const dispatch = createEventDispatcher();

    let editableName = palette.name;
    let isSaving = false;
    let copyStatus = {}; // To track "Copied!" message for each color
    let errorMessage = '';

    // --- NEW: Function to determine text color based on background ---
    function getContrastColor(hex) {
        if (!hex) return '#000000';
        const hexValue = hex.startsWith('#') ? hex.substring(1) : hex;
        const r = parseInt(hexValue.substring(0, 2), 16);
        const g = parseInt(hexValue.substring(2, 4), 16);
        const b = parseInt(hexValue.substring(4, 6), 16);
        // Formula to calculate perceived brightness (luminance)
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        // Return black for light colors, white for dark colors
        return luminance > 0.5 ? '#000000' : '#FFFFFF';
    }

    // --- Function to copy hex code to clipboard ---
    function copyToClipboard(hex) {
        const tempTextArea = document.createElement('textarea');
        tempTextArea.value = hex;
        document.body.appendChild(tempTextArea);
        tempTextArea.select();
        try {
            document.execCommand('copy');
            copyStatus[hex] = true;
            setTimeout(() => {
                copyStatus[hex] = false;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
        document.body.removeChild(tempTextArea);
    }

    // --- Function to save the updated palette name ---
    async function handleUpdatePalette() {
        isSaving = true;
        errorMessage = '';
        try {
            const { data, error } = await supabase
                .from('palettes')
                .update({ name: editableName })
                .eq('id', palette.id)
                .select()
                .single();

            if (error) throw error;
            
            dispatch('update', data);

        } catch (error) {
            errorMessage = `Error: ${error.message}`;
        } finally {
            isSaving = false;
        }
    }

    // --- Handle Escape key to close the modal ---
    const handleKeydown = (e) => {
        if (e.key === 'Escape') {
            dispatch('close');
        }
    };

    onMount(() => {
        window.addEventListener('keydown', handleKeydown);
    });

    onDestroy(() => {
        window.removeEventListener('keydown', handleKeydown);
    });
</script>

<div 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" 
    on:click={(e) => { if (e.target === e.currentTarget) dispatch('close'); }}
    on:keydown={handleKeydown}
    role="dialog" 
    aria-modal="true"
    tabindex="-1"
>
    <div class="w-full max-w-6xl max-h-[90vh] bg-white dark:bg-gray-800 rounded-xl shadow-2xl flex flex-col">
        <header class="p-4 border-b dark:border-gray-700 flex justify-end items-center flex-shrink-0">
            <button on:click={() => dispatch('close')} class="text-gray-500 hover:text-gray-800 dark:hover:text-gray-200 text-3xl" aria-label="Close modal">&times;</button>
        </header>

        <div class="flex-grow overflow-y-auto">
            <div class="p-6">
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                    {#each palette.paints as paint (paint.productId)}
                        <div class="aspect-square rounded-lg flex items-center justify-center relative group" style="background-color: {paint.hexCode};">
                            <button 
                                on:click={() => copyToClipboard(paint.hexCode)}
                                class="absolute bottom-4 px-3 py-2 rounded-full flex items-center gap-2 transition-all duration-200"
                                style="color: {getContrastColor(paint.hexCode)};"
                            >
                                {#if copyStatus[paint.hexCode]}
                                    <!-- UPDATED: Font size changed from text-lg to text-base -->
                                    <span class="font-bold text-base">Copied!</span>
                                {:else}
                                    <!-- UPDATED: Font size changed from text-lg to text-base -->
                                    <span class="font-bold text-base group-hover:hidden">{paint.hexCode}</span>
                                    <!-- UPDATED: Font size changed from text-lg to text-base -->
                                    <span class="hidden group-hover:flex items-center gap-1.5 font-bold text-base">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                        Copy
                                    </span>
                                {/if}
                            </button>
                        </div>
                    {/each}
                </div>
            </div>

            <div class="p-6 pt-0">
                <label for="palette-name" class="block text-sm font-medium text-gray-600 dark:text-gray-300">Palette Name</label>
                <div class="mt-1 flex items-center gap-4">
                    <input 
                        type="text" 
                        id="palette-name"
                        bind:value={editableName}
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    >
                    <button 
                        on:click={handleUpdatePalette}
                        disabled={isSaving || editableName === palette.name}
                        class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex-shrink-0"
                    >
                        {isSaving ? 'Saving...' : 'Save'}
                    </button>
                </div>
                {#if errorMessage}
                    <p class="text-red-500 text-sm mt-2">{errorMessage}</p>
                {/if}
            </div>
        </div>
    </div>
</div>
