import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';

// @aws-amplify/ui-react-core uses xstate v4 (`{ actions }` export), while the
// project's streaming state machine needs xstate v5 (`setup` / `assign` API).
// `xstate4` is an npm alias ("xstate4": "npm:xstate@4.38.3") installed as a
// direct dependency so it is always present after `npm ci`.
// The Rollup plugin below redirects every `xstate` import that originates from
// inside an `@aws-amplify` package to the `xstate4` alias, letting both
// versions co-exist without conflicts.
const fixAmplifyXstate = {
  name: 'fix-amplify-xstate',
  resolveId(source: string, importer: string | undefined) {
    if (
      source === 'xstate' &&
      importer &&
      importer.includes(path.join('node_modules', '@aws-amplify'))
    ) {
      return 'xstate4';
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
        name: 'AA Bedrock',
        short_name: 'AA Bedrock',
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
