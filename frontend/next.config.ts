import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // ESM packages need to be transpiled for Next.js compatibility
  transpilePackages: ['react-markdown', 'remark-gfm', 'unified', 'remark-parse'],
  images: {
    remotePatterns: [],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', 'recharts', 'framer-motion'],
  },
  devIndicators: {
    buildActivity: false,
    appIsrStatus: false,
  },
}

export default nextConfig
