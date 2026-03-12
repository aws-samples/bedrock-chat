import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const _require = createRequire(import.meta.url);

// @aws-amplify/ui-react-core has xstate v4 as a direct dependency.  The
// top-level project also has xstate v5.  In a clean CodeBuild environment
// Rollup resolves the `xstate` import inside `@aws-amplify` packages to the
// top-level v5, which does not export `actions`, and the build fails.
// The plugin below forces all `xstate` imports that originate from inside
// `@aws-amplify` packages to resolve to the nested v4 copy so both co-exist.
const xstateV4Path = _require.resolve('xstate', {
  paths: [path.join(__dirname, 'node_modules/@aws-amplify/ui-react-core')],
});

const fixAmplifyXstate = {
  name: 'fix-amplify-xstate',
  resolveId(source: string, importer: string | undefined) {
    if (
      source === 'xstate' &&
      importer &&
      importer.includes(path.join('node_modules', '@aws-amplify'))
    ) {
      return xstateV4Path;
    }
  },
};

// https://vitejs.dev/config/
export default defineConfig({
  resolve: { alias: { './runtimeConfig': './runtimeConfig.browser' } },
  build: {
    rollupOptions: {
      plugins: [fixAmplifyXstate],
    },
  },
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true,
      },
      injectRegister: 'auto',
      workbox: {
        maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
      },
      manifest: {
        name: 'Dylbot',
        short_name: 'Dylbot',
        description: 'AWS-native chatbot using Bedrock',
        start_url: '/index.html',
        display: 'standalone',
        theme_color: '#6C3F99',
        icons: [
          {
            src: '/images/bedrock_icon_72.png',
            sizes: '72x72',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_96.png',
            sizes: '96x96',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_128.png',
            sizes: '128x128',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_144.png',
            sizes: '144x144',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_152.png',
            sizes: '152x152',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_384.png',
            sizes: '384x384',
            type: 'image/png',
          },
          {
            src: '/images/bedrock_icon_512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
          {
            src: '/images/bedrock_icon_512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any',
          },
        ],
      },
    }),
  ],
  server: { host: true },
});
