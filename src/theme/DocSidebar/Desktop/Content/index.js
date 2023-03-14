import React, { useState } from 'react';
import clsx from 'clsx';
import { ThemeClassNames, useThemeConfig } from '@docusaurus/theme-common';
import {
  useAnnouncementBar,
  useScrollPosition,
} from '@docusaurus/theme-common/internal';
import DocSidebarItems from '@theme/DocSidebarItems';
import SelectNav from '@site/src/components/SelectNav';
import NewsletterForm from '@site/src/components/NewsletterForm';
import styles from './styles.module.css';
function useShowAnnouncementBar() {
  const { isActive } = useAnnouncementBar();
  const [showAnnouncementBar, setShowAnnouncementBar] = useState(isActive);
  useScrollPosition(
    ({ scrollY }) => {
      if (isActive) {
        setShowAnnouncementBar(scrollY === 0);
      }
    },
    [isActive],
  );
  return isActive && showAnnouncementBar;
}
function useSoftwareNavItems() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().softwareNav.items;
}
export default function DocSidebarDesktopContent({ path, sidebar, className }) {
  const showAnnouncementBar = useShowAnnouncementBar();
  const softwareNavItems = useSoftwareNavItems();
  return (
    <>
      {path.indexOf('/software') > -1 && (
        <SelectNav items={softwareNavItems} label="Select Software Version" />
      )}
      <nav
        className={clsx(
          'menu thin-scrollbar',
          styles.menu,
          showAnnouncementBar && styles.menuWithAnnouncementBar,
          className,
        )}>
        <ul className={clsx(ThemeClassNames.docs.docSidebarMenu, 'menu__list')}>
          <DocSidebarItems items={sidebar} activePath={path} level={1} />
        </ul>
        <NewsletterForm />
        {!path.indexOf('/software') > -1 && (
          <ul className={clsx(ThemeClassNames.docs.docSidebarMenu, 'menu__list', styles.menu__listBottom)}>
            <li>
              <a href="https://calendly.com/d/yy2-tvp-xtv/astro-data-engineering-office-hours-ade">Book Office Hours</a>
            </li>
            <li>
              <a href="https://www.astronomer.io/events/webinars/?referral=docs-sidebar">Watch a webinar</a>
            </li>
            <li>
              <a href="https://status.astronomer.io/?referral=docs-sidebar">Astro status</a>
            </li>
          </ul>
        )}
      </nav>
    </>
  );
}
