// vite.config.js

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import https from 'https';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/mistral': {
        target: 'https://mistral-7b-instruct-v03-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com',
        changeOrigin: true,
        secure: false, // This will allow self-signed certificates
        agent: new https.Agent({
          rejectUnauthorized: false,
        }),
        rewrite: path => path.replace(/^\/api\/mistral/, ''),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Authorization', `Bearer ${process.env.VITE_HF_ACCESS_TOKEN}`);
          });
        },
      },
      '/api/llama': {
        target: 'https://meta-llama3-8b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com',
        changeOrigin: true,
        secure: false, // This will allow self-signed certificates
        agent: new https.Agent({
          rejectUnauthorized: false,
        }),
        rewrite: path => path.replace(/^\/api\/llama/, ''),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Authorization', `Bearer ${process.env.VITE_HF_ACCESS_TOKEN}`);
          });
        },
      },
      '/api/granite': {
        target: 'https://granite-7b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com',
        changeOrigin: true,
        secure: false, // This will allow self-signed certificates
        agent: new https.Agent({
          rejectUnauthorized: false,
        }),
        rewrite: path => path.replace(/^\/api\/granite/, ''),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Authorization', `Bearer ${process.env.VITE_HF_ACCESS_TOKEN}`);
          });
        },
      },
    },
  },
});
