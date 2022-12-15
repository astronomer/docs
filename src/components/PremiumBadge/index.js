import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.premiumBadge} id="premiumBadge">
        <div className={styles.premiumBadge}>
        <a target="_blank" href="https://www.astronomer.io/pricing/"> <img src={useBaseUrl(`img/PremiumLarge.png`)} alt='This feature is an Astro Premium-tier service.' /> </a>
        </div>
    </Link>
  )
}