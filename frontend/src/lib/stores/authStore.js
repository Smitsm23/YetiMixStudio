// File: src/lib/stores/authStore.js
import { readable } from 'svelte/store';
import { supabase } from '$lib/services/supabaseClient';

// This creates a readable store that starts with null
// It listens for Supabase auth events and updates the store with the user session
export const user = readable(null, (set) => {
    supabase.auth.onAuthStateChange((event, session) => {
        set(session?.user ?? null);
    });
});