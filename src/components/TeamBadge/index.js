import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.teamBadge} id="teamBadge">
      <div className={styles.teamBadge}>
        <a target="_blank" href="https://www.astronomer.io/pricing/">
          <img src="/docs/img/Badge_Team.png" alt="This feature is available only if you are on the Team tier or above." title="This feature is available only if you are on the Team tier or above." />
        </a>
      </div>
    </Link>
  )
}
