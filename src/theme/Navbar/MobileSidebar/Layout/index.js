import React from 'react';
import clsx from 'clsx';
import cn from 'clsx';
import styles from './styles.module.css';

export default function NavbarMobileSidebarLayout({
  header,
  primaryMenu,
  secondaryMenu,
}) {
  return (
    <div className="navbar-sidebar">
      {header}
      <div
        className={clsx('navbar-sidebar__items')}>
        <div className="navbar-sidebar__item menu primaryMenu">{primaryMenu}</div>
        <div className="navbar-sidebar__item menu secondaryMenu">{secondaryMenu}</div>
      </div>
      <div className="navbar-sidebar__item menu bottomButtons">
        <a className={cn(styles.button, styles.button__outline)} href="https://www.astronomer.io/?referral=docs-nav-button" target="_blank">
          Learn about Astronomer
        </a>
        <a className={styles.button} href="https://www.astronomer.io/try-astro/?referral=docs-nav-button&utm_medium=docs&utm_content=web&utm_source=top_nav" target="_blank">
          Try Astro
        </a>
      </div>
    </div>
  );
}
