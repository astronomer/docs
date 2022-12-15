import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.premiumBadge} id="premiumBadge">
        <div className={styles.premiumBadge}>
        <a target="_blank" href="https://www.astronomer.io/get-started/"> 
            <img src="/img/PremiumLarge.png" alt="This feature is an Astro Premium-tier service." title="This feature is an Astro Premium-tier service." /> 
        </a>
        </div>
    </Link>
  )
}
