/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import { useContextualSearchFilters } from '@docusaurus/theme-common';
// Translate search-engine agnostic search filters to Algolia search filters
export default function useAlgoliaContextualFacetFilters() {
  const {locale, tags} = useContextualSearchFilters();

  // seems safe to convert locale->language, see AlgoliaSearchMetadatas comment
  const languageFilter = `language:${locale}`;

  let tagsFilter = tags.map((tag) => `docusaurus_tag:${tag}`);
  const currentPath = typeof window !== 'undefined' ? window.location.pathname : '';
  const currentSoftwareTag = tags.find(tag => tag.includes('software'));
  // limit search results to current docset
 if (currentPath.includes('software')) {
  tagsFilter = [`docusaurus_tag:${currentSoftwareTag}`,`docusaurus_tag:docs-tutorials-current`]
} else if (currentPath.includes('astro')) {
  tagsFilter = ['docusaurus_tag:docs-default-current', 'docusaurus_tag:docs-tutorials-current']
 }
  return [languageFilter, tagsFilter];
}
