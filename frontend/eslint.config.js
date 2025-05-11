// eslint.config.js
import js from "@eslint/js";
import react from "eslint-plugin-react";
import prettier from "eslint-plugin-prettier";
import * as prettierConfig from "eslint-config-prettier";
import parser from "@babel/eslint-parser"; // Add Babel parser for JSX

export default [
  js.configs.recommended,
  {
    files: ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser, // Use Babel parser
      parserOptions: {
        requireConfigFile: false, // Avoid needing a separate Babel config
        babelOptions: {
          presets: ["@babel/preset-react"], // Ensure JSX support
        },
      },
    },
    plugins: {
      react,
      prettier,
    },
    rules: {
      ...react.configs.recommended.rules,
      ...prettierConfig.rules,
      "react/jsx-uses-react": "error",
      "react/jsx-uses-vars": "error",
      "prettier/prettier": "error",
      "no-console": "warn",
      "no-unused-vars": "warn",
      "react/prop-types": "off",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
];
