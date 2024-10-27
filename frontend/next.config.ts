import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
    output: "standalone",
    // https://nextjs.org/docs/app/api-reference/next-config-js/serverExternalPackages
    serverExternalPackages: ["@huggingface/transformers"],
    webpack(config, { isServer }) {
        config.resolve.alias['@huggingface/transformers'] = path.resolve(__dirname, 'node_modules/@huggingface/transformers');
        return config;
    }
};

export default nextConfig;
