import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.businessBadge} id="businessBadge">
        <div className={styles.businessBadge}>
        <a target="_blank" href="https://docs.astronomer.io/astro/astro-architecture">
            <img src="/img/Badge_Business.png" alt="This feature is available only if you are on the Business tier or above." title="This feature is available only if you are on the Business tier or above." />
        </a>
        </div>
    </Link>
  )
}