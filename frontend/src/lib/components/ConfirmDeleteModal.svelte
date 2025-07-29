<!-- src/lib/components/ConfirmDeleteModal.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" role="dialog" aria-modal="true">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-sm">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">Confirm Deletion</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
            Are you sure you want to delete this recipe? This action cannot be undone.
        </p>
        <div class="mt-6 flex justify-end space-x-4">
            <button on:click={() => dispatch('cancel')} class="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-200 dark:hover:bg-gray-500">
                Cancel
            </button>
            <button on:click={() => dispatch('confirm')} class="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700">
                Delete
            </button>
        </div>
    </div>
</div>