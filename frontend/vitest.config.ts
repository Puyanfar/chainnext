/// <reference types="vitest" />
import react from '@vitejs/plugin-react-swc';
import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

// Node 24.22+ installs an experimental localStorage getter that is undefined
// unless --localstorage-file is set. Vitest then skips copying jsdom's Storage
// onto the test global. Disable Node Web Storage in the test child processes
// so jsdom owns localStorage (browser tests, not Node's file-backed API).
const noWebStorage = '--no-experimental-webstorage';
const nodeOptions = process.env.NODE_OPTIONS ?? '';
if (!nodeOptions.split(/\s+/).includes(noWebStorage)) {
  process.env.NODE_OPTIONS = `${nodeOptions} ${noWebStorage}`.trim();
}

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
    setupFiles: './tests/setup-tests.ts',
    include: ['./**/*.{test,spec}.?(c|m)[jt]s?(x)'],
    // Vitest 0.34 worker_threads ignore NODE_OPTIONS; child processes inherit it.
    threads: false
  }
});
