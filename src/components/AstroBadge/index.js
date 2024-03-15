import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.astroBadge} id="astroBadge">
      <div className={styles.astroBadge}>
        <a target="_blank" href="https://docs.astronomer.io/astro">
          <img src="/img/Badge_Astro.png" alt="This feature is available only on Astro." title="This feature is available only on Astro." />
        </a>
      </div>
    </Link>
  )
}