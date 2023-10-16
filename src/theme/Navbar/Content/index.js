import React from 'react';
import { useThemeConfig } from '@docusaurus/theme-common';
import {
  splitNavbarItems,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import NavbarItem from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';
import cn from "clsx";
import styles from './styles.module.css';
function useNavbarItems() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().navbar.items;
}
function NavbarItems({ items }) {
  return (
    <>
      {items.map((item, i) => (
        <NavbarItem {...item} key={i} />
      ))}
    </>
  );
}
function NavbarContentLayout({ left, right }) {
  return (
    <div className="navbar__inner">
      <div className="navbar__items">{left}</div>
      <div className="navbar__items navbar__items--right">{right}</div>
    </div>
  );
}
export default function NavbarContent() {
  const mobileSidebar = useNavbarMobileSidebar();
  const items = useNavbarItems();
  const [leftItems, rightItems] = splitNavbarItems(items);
  const searchBarItem = items.find((item) => item.type === 'search');
  return (
    <>
      <div className={cn(styles.navbar__wrapper, styles.navbar__top)}>
        <NavbarContentLayout
          left={
            // TODO stop hardcoding items?
            <>
              {!mobileSidebar.disabled && <NavbarMobileSidebarToggle />}
              <NavbarLogo />
              <a href="/" className={styles.navbar__logolink}>Docs</a>
              {!searchBarItem && (
                <NavbarSearch>
                  <SearchBar />
                </NavbarSearch>
              )}
            </>
          }
          right={
            // TODO stop hardcoding items?
            // Ask the user to add the respective navbar items => more flexible
            <>
              <NavbarItems items={rightItems} />
              <NavbarColorModeToggle className={styles.colorModeToggle} />
              <a className={cn(styles.button, styles.button__outline)} href="https://www.astronomer.io/?referral=docs-nav-button" target="_blank">Learn About Astronomer</a>
              <a className={styles.button} href="https://www.astronomer.io/try-astro/?referral=docs-nav-button" target="_blank">Get Started Free</a>
            </>
          }
        />
      </div>
      <div className={cn(styles.navbar__wrapper, styles.navbar__bottom)}>
        <NavbarContentLayout
          left={
            // TODO stop hardcoding items?
            <>
              <NavbarItems items={leftItems} />
            </>
          }
          right={
            // TODO stop hardcoding items?
            // Ask the user to add the respective navbar items => more flexible
            <>
              <NavbarColorModeToggle className={styles.colorModeToggle} />
              <a className={styles.button} href="https://www.astronomer.io/try-astro/?referral=docs-nav-button" target="_blank">Try Astro</a>
            </>
          }
        />
      </div>
    </>
  );
}
