import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.hostedBadge} id="hostedBadge">
        <div className={styles.hostedBadge}>
        <a target="_blank" href="https://docs.astronomer.io/astro/astro-architecture">
            <img src="/img/Badge_Hosted.png" alt="This feature is available only on Astro Hosted." title="This feature is available only on AstroHosted." />
        </a>
        </div>
    </Link>
  )
}