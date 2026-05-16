/// <reference types="astro/client" />

interface CloudflareEnv {
  DB: D1Database;
}

declare module 'cloudflare:workers' {
  const env: CloudflareEnv;
  export { env };
}
