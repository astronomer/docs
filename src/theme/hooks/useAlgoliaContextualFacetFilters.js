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
  const currentEnterpriseTag = tags.find(tag => tag.includes('enterprise'));
  // limit search results to current docset
 if (currentPath.includes('enterprise')) {
  tagsFilter = [`docusaurus_tag:${currentEnterpriseTag}`]
 } else if (currentPath.includes('cloud')) {
  tagsFilter = ['docusaurus_tag:docs-default-current']
 }

  return [languageFilter, tagsFilter];
}
