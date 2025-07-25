<script>
    import Header from '$lib/components/Header.svelte';
    import Footer from '$lib/components/Footer.svelte';
    import { theme } from '$lib/stores/themeStore.js';
    import { browser } from '$app/environment';
    import '../app.css';

    // This reactive statement ensures the class on the <html> tag
    // always matches the theme store's value.
    $: if (browser) {
        if ($theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        localStorage.setItem('theme', $theme);
    }
</script>

<slot />