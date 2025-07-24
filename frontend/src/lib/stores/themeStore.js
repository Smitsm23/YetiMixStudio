import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const createThemeStore = () => {
	const { subscribe, set, update } = writable('light');

	if (browser) {
		const storedTheme = localStorage.getItem('theme');
		const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		set(storedTheme || (prefersDark ? 'dark' : 'light'));
	}

	return {
		subscribe,
		set,
		toggle: () => update(current => (current === 'dark' ? 'light' : 'dark'))
	};
};

export const theme = createThemeStore();