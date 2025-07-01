import "eslint-plugin-only-warn";
import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import { defineConfig, globalIgnores } from "eslint/config";
import { FlatCompat } from "@eslint/eslintrc";
import pluginQuery from "@tanstack/eslint-plugin-query";

const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

export default defineConfig([
  globalIgnores([".next", "node_modules"]),
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    plugins: { js },
    extends: ["js/recommended"],
  },
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    languageOptions: { globals: { ...globals.browser, ...globals.node } },
  },
  tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,

  ...pluginQuery.configs["flat/recommended"],
  ...compat.config({
    extends: ["next", "next/core-web-vitals", "next/typescript", "prettier"],
    plugins: ["prettier"],
    rules: {
      "prettier/prettier": [
        "error",
        { endOfLine: "auto", plugins: ["prettier-plugin-tailwindcss"] },
      ],
      "no-console": "error",
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          caughtErrors: "none",
          varsIgnorePattern: "^_",
        },
      ],
    },
  }),
]);
