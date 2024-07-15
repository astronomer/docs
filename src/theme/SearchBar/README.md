## NOTE on custom SearchBar component

This component was created using [Docusaurus swizzle eject](https://docusaurus.io/docs/swizzling#ejecting).

This overwrites the SearchBar component so that we can use our custom `useAlgoliaContextualFacetFilters.js` search hook, which filters results based on the product being viewed (Astro vs Software).

Previously, overwriting `useAlgoliaContextualFacetFilters` sufficed, but the original hook was moved into a different package so that stopped working.

`swizzle eject` automatically created this entire directory for the SearchBar component, which is a copy of the original package(`theme-search-algolia`) component . The only file changed was `index.js`, where on line 17 we're importing our custom hook instead of the original hook.

The caveat to all of this is that our custom component will prevent future changes from being applied. The original component can be [found here](node_modules/@docusaurus/theme-search-algolia/lib/theme/SearchBar) if we ever need to update our custom component.