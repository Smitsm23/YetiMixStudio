<!-- src/routes/palettes/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { supabase } from '$lib/services/supabaseClient.js';
    import { user } from '$lib/stores/authStore.js';
    import PaletteCard from '$lib/components/PaletteCard.svelte';
    import PaletteDetailModal from '$lib/components/PaletteDetailModal.svelte'; // Import the modal

    let savedPalettes = [];
    let isLoading = true;
    let errorMessage = '';

    // --- State for the detail modal ---
    let selectedPalette = null;

    onMount(() => {
        const unsubscribe = user.subscribe(async (currentUser) => {
            if (currentUser) {
                await getPalettes();
            } else {
                isLoading = false;
                savedPalettes = [];
            }
        });
        return () => unsubscribe();
    });

    async function getPalettes() {
        isLoading = true;
        errorMessage = '';
        try {
            const { data, error } = await supabase
                .from('palettes')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;
            savedPalettes = data || [];
        } catch (error) {
            errorMessage = `Error fetching palettes: ${error.message}`;
        } finally {
            isLoading = false;
        }
    }

    // --- Function to handle updating the list after a rename ---
    function handlePaletteUpdate(event) {
        const updatedPalette = event.detail;
        const index = savedPalettes.findIndex(p => p.id === updatedPalette.id);
        if (index !== -1) {
            savedPalettes[index] = updatedPalette;
        }
        selectedPalette = null; // Close the modal
    }
</script>

<div class="container mx-auto p-4 sm:p-8">
    <h1 class="text-4xl font-bold text-center mb-8 text-gray-800 dark:text-gray-100">My Saved Palettes</h1>

    {#if isLoading}
        <p class="text-center text-gray-500">Loading your palettes...</p>
    {:else if !$user}
        <p class="text-center text-gray-500">
            Please <a href="/login" class="text-blue-600 hover:underline">login</a> to view your saved palettes.
        </p>
    {:else if errorMessage}
        <p class="text-center text-red-500">{errorMessage}</p>
    {:else if savedPalettes.length === 0}
        <p class="text-center text-gray-500">You haven't saved any palettes yet.</p>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {#each savedPalettes as palette (palette.id)}
                <!-- When a card is clicked, set it as the selectedPalette to open the modal -->
                <button type="button" on:click={() => selectedPalette = palette} class="text-left w-full">
                    <PaletteCard {palette} />
                </button>
            {/each}
        </div>
    {/if}
</div>

<!-- Render the modal if a palette is selected -->
{#if selectedPalette}
    <PaletteDetailModal 
        palette={selectedPalette} 
        on:close={() => selectedPalette = null}
        on:update={handlePaletteUpdate}
    />
{/if}
