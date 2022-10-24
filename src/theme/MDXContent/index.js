import React, { useEffect } from 'react';
import MDXContent from '@theme-original/MDXContent';

export default function MDXContentWrapper(props) {
  useEffect(() => {
    // Check if this is a release-notes page
    let isReleaseNotesPage = document.querySelector('html[class*="release-notes"]') !== null;

    // if it is, then add the "release-header" class to each h2 element
    if (isReleaseNotesPage) {
      let h2s = document.querySelectorAll('h2');
      h2s.forEach((h2) => h2.classList.add('release-header'));
    }
  }, []);
  return (
    <>
      <MDXContent {...props} />
    </>
  );
}
