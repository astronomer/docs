import React from 'react';
import styles from './styles.module.css';
import cn from 'clsx';
import { useThemeConfig } from '@docusaurus/theme-common';

function useAstroCardConfig() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().astroCard;
}

export default function AstroCard(
  {
    title,
    description
  }
) {
  const content = useAstroCardConfig();
  return (
    <div className={styles.astroCard} id="astroCard">
      <h2 className={styles.astroCard__title}>{title || content.title}</h2>
      <p className={styles.astroCard__description}>{description || content.description}</p>
      <div className={styles.astroCard__buttons}>
        <a className={cn(styles.button)} href={content.buttons.primary.href}>{content.buttons.primary.label}</a>
        <a className={cn(styles.button, styles.button__outline)} href={content.buttons.secondary.href}>{content.buttons.secondary.label}</a>
      </div>
    </div>
  )
}
