import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard() {
  return (
    <Link className={styles.enterpriseBadge} id="enterpriseBadge">
        <div className={styles.enterpriseBadge}>
        <a target="_blank" href="https://www.astronomer.io/pricing/">
            <img src="/img/Badge_Enterprise.png" alt="This feature is available only if you are on the Enterprise tier or above." title="This feature is available only if you are on the Enterprise tier or above." />
        </a>
        </div>
    </Link>
  )
}