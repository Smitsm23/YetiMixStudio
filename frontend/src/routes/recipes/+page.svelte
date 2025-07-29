<!-- src/routes/recipes/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { supabase } from '$lib/services/supabaseClient.js';
    import { user } from '$lib/stores/authStore.js';
    import { getAllPaints } from '$lib/services/api.js';
    import SavedRecipeCard from '$lib/components/SavedRecipeCard.svelte';
    import ConfirmDeleteModal from '$lib/components/ConfirmDeleteModal.svelte';

    let savedRecipes = [];
    let allPaints = [];
    let isLoading = true;
    let errorMessage = '';

    // --- State for delete confirmation ---
    let showConfirmDelete = false;
    let recipeToDeleteId = null;

    onMount(async () => {
        try {
            allPaints = await getAllPaints();
        } catch (e) {
            errorMessage = "Could not load the full paint library.";
            console.error(e);
        }

        const unsubscribe = user.subscribe(async (currentUser) => {
            if (currentUser) {
                await getRecipes();
            } else {
                isLoading = false;
                savedRecipes = [];
            }
        });
        return () => unsubscribe();
    });

    async function getRecipes() {
        isLoading = true;
        errorMessage = '';
        try {
            const { data, error } = await supabase
                .from('recipes')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;
            savedRecipes = data || [];
        } catch (error) {
            errorMessage = `Error fetching recipes: ${error.message}`;
        } finally {
            isLoading = false;
        }
    }

    // --- Functions to handle deletion ---
    function promptDelete(event) {
        recipeToDeleteId = event.detail;
        showConfirmDelete = true;
    }

    async function confirmDelete() {
        if (!recipeToDeleteId) return;
        
        try {
            const { error } = await supabase
                .from('recipes')
                .delete()
                .eq('id', recipeToDeleteId);

            if (error) throw error;

            // Remove the deleted recipe from the local list for an instant UI update
            savedRecipes = savedRecipes.filter(r => r.id !== recipeToDeleteId);

        } catch (error) {
            errorMessage = `Error deleting recipe: ${error.message}`;
        } finally {
            // Hide the modal
            recipeToDeleteId = null;
            showConfirmDelete = false;
        }
    }
</script>

<div class="container mx-auto p-4 sm:p-8">
    <h1 class="text-4xl font-bold text-center mb-8 text-gray-800 dark:text-gray-100">My Saved Recipes</h1>

    {#if isLoading}
        <p class="text-center text-gray-500">Loading your recipes...</p>
    {:else if !$user}
        <p class="text-center text-gray-500">
            Please <a href="/login" class="text-blue-600 hover:underline">login</a> to view your saved recipes.
        </p>
    {:else if errorMessage}
        <p class="text-center text-red-500">{errorMessage}</p>
    {:else if savedRecipes.length === 0}
        <p class="text-center text-gray-500">You haven't saved any recipes yet.</p>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {#each savedRecipes as recipe (recipe.id)}
                <SavedRecipeCard {recipe} {allPaints} on:delete={promptDelete} />
            {/each}
        </div>
    {/if}
</div>

<!-- Render the confirmation modal -->
{#if showConfirmDelete}
    <ConfirmDeleteModal 
        on:confirm={confirmDelete}
        on:cancel={() => showConfirmDelete = false}
    />
{/if}
