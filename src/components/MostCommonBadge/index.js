import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.mostCommonBadge} id="MostCommonBadge">
      <div className={styles.mostCommonBadge}>
          <img src="/docs/img/Badge_Most_Common.png" alt="This is the most commonly chosen option." title="This is the most commonly chosen option." />
      </div>
    </Link>
  )
}
