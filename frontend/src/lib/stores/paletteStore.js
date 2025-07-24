import { writable } from 'svelte/store';

function createPaletteStore() {
    const { subscribe, set, update } = writable(new Map());

    return {
        subscribe,
        // UPDATED: Use camelCase 'productId'
        togglePaint: (paint) => update(currentMap => {
            if (currentMap.has(paint.productId)) {
                currentMap.delete(paint.productId);
            } else {
                currentMap.set(paint.productId, paint);
            }
            return currentMap;
        }),
        reset: () => set(new Map())
    };
}

export const selectedPaints = createPaletteStore();