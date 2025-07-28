<script>
    import { supabase } from '$lib/services/supabaseClient';

    let loading = false;
    let email = '';
    let password = '';
    let errorMessage = '';

    const handleSignUp = async () => {
        try {
            loading = true;
            errorMessage = '';
            const { error } = await supabase.auth.signUp({ email, password });
            if (error) throw error;
            alert('Check your email for the login link!');
        } catch (error) {
            errorMessage = error.message;
        } finally {
            loading = false;
        }
    };

    const handleLogin = async () => {
        try {
            loading = true;
            errorMessage = '';
            const { error } = await supabase.auth.signInWithPassword({ email, password });
            if (error) throw error;
            // After successful login, you would typically redirect the user
            // or update the UI state to show they are logged in.
            alert('Logged in successfully!');
        } catch (error) {
            errorMessage = error.message;
        } finally {
            loading = false;
        }
    };
</script>

<div class="max-w-md mx-auto p-8 border rounded-lg shadow-lg dark:bg-gray-800 dark:border-gray-700">
    <h2 class="text-2xl font-bold text-center mb-6 dark:text-gray-100">Sign In or Create Account</h2>
    
    <div class="space-y-4">
        <div>
            <label for="email" class="block mb-1 font-medium dark:text-gray-300">Email</label>
            <input type="email" id="email" bind:value={email} class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        </div>
        <div>
            <label for="password" class="block mb-1 font-medium dark:text-gray-300">Password</label>
            <input type="password" id="password" bind:value={password} class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        </div>
    </div>

    {#if errorMessage}
        <p class="text-red-500 text-center my-4">{errorMessage}</p>
    {/if}

    <div class="mt-6 space-y-4">
        <button on:click={handleLogin} disabled={loading} class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400">
            {loading ? 'Loading...' : 'Sign In'}
        </button>
        <button on:click={handleSignUp} disabled={loading} class="w-full bg-gray-600 text-white font-bold py-2 px-4 rounded hover:bg-gray-700 disabled:bg-gray-400">
            {loading ? 'Loading...' : 'Sign Up'}
        </button>
    </div>
</div>