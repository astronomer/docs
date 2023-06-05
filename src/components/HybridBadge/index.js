import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.hybridBadge} id="hybridBadge">
        <div className={styles.hybridBadge}>
        <a target="_blank" href="https://docs.astronomer.io/astro/hybrid-overview"> 
            <img src="/img/Badge_Hybrid.png" alt="This feature is available only on Astro Hybrid." title="This feature is available only on AstroHybrid." /> 
        </a>
        </div>
    </Link>
  )
}