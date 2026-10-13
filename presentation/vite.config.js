import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  base: './',
  plugins: [svelte(), viteSingleFile()],
  build: { target: 'es2022', reportCompressedSize: false, emptyOutDir: true },
});
