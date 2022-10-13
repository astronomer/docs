import React from 'react';
import styles from './styles.module.css';

export default function LinkCardGrid({ children, columns = "1" }) {
  return (
    <div className={styles.linkCardGrid} data-columns={columns}>
      {children}
    </div>
  )
}