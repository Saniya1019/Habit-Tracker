import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `npm run build` writes the app into Django's static folder (backend/static/app),
// so Django can serve everything. Only needed if you edit the React code.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://127.0.0.1:8000" } },
  build: {
    outDir: "../static/app",
    emptyOutDir: true,
    assetsDir: "",
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
        entryFileNames: "app.js",
        chunkFileNames: "app.js",
        assetFileNames: "app[extname]",
      },
    },
  },
});
