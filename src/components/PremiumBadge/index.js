import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.premiumBadge} id="premiumBadge">
        <div className={styles.premiumBadge}>
          <img src="/img/PremiumLarge.png" href="https://www.astronomer.io/pricing/" alt='This feature is an Astro Premium-tier service.' />
        </div>
    </Link>
  )
}