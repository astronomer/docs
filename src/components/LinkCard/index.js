import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function LinkCard({
  label,
  description,
  icon,
  href
}) {
  return (
    <Link className={styles.linkCard} id="linkCard" href={href}>
      {icon && (
        <div className={styles.linkCard__icon}>
          <img src={icon} alt='' />
        </div>
      )}
      <div className={styles.linkCard__copy}>
        <p className={styles.linkCard__label}>{label}</p>
        {description && (
          <p className={styles.linkCard__description}>{description}</p>
        )}
      </div>
    </Link>
  )
}