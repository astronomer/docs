import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';
import cn from 'clsx';
import { useThemeConfig } from '@docusaurus/theme-common';

function usePromoBannerConfig() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().promoBanner;
}

export default function PromoBanner() {
  const [closed, setClosed] = useState(false);

  const wasBannerClosed =
    typeof window !== "undefined" && window.sessionStorage.getItem("promoBannerClosed");

  function closePromoBanner() {
    typeof window !== "undefined" && window.sessionStorage.setItem("promoBannerClosed", "true");
    setClosed(true);
  }

  useEffect(() => {
    wasBannerClosed && setClosed(true);
  }, [wasBannerClosed]);

  const content = usePromoBannerConfig();
  return (
    <div className={cn(styles.promoBanner, closed && styles.hidden)} id="promoBanner">
      <div className={cn(styles.promoBanner__content)}>
        <div className={cn(styles.promoBanner__copy)}>
          <p className={cn(styles.promoBanner__text)}>{content.text}</p>
          <a href={content.url} className={cn(styles.promoBanner__link)} onClick={() => closePromoBanner()}>{content.buttonText}</a>
        </div>
        <button className={cn(styles.promoBanner__close)} aria-label="Close Banner" onClick={() => closePromoBanner()}> &#10006;</button>
      </div>
    </div>
  );
}