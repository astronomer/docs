import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.softwareBadge} id="softwareBadge">
      <div className={styles.softwareBadge}>
        <a target="_blank" href="https://www.astronomer.io/docs/software">
          <img src="/docs/img/Badge_Software.png" alt="This feature is available only on Astronomer Software." title="This feature is available only on Astronomer Software." />
        </a>
      </div>
    </Link>
  )
}
