import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.hybridBadge} id="hybridBadge">
      <div className={styles.hybridBadge}>
        <a target="_blank" href="https://www.astronomer.io/docs/astro/hybrid-overview">
          <img src="/docs/img/Badge_Hybrid.png" alt="This feature is available only on Astro Hybrid." title="This feature is available only on AstroHybrid." />
        </a>
      </div>
    </Link>
  )
}
