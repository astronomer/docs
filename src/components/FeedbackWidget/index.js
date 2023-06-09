import React, { useState } from 'react';
import styles from './styles.module.css';
import cn from 'clsx';
import { useThemeConfig } from '@docusaurus/theme-common';

function useFeedbackWidgetConfig() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().feedbackWidget;
}

function feedbackClick(question, answer) {
  if (window && window.analytics) {
    window.analytics.track("Feedback Button Click", {
      answer: answer,
      page: document.title,
      path: document.location.pathname,
      question: question
    });
  }
}
export default function FeedbackWidget() {
  const [hasAnswered, setHasAnswered] = useState(false);

  const content = useFeedbackWidgetConfig();
  const question = content.question || "Was this helpful?";
  return (
    <div className={styles.feedbackWidget} id="feedbackWidget">
      {!hasAnswered && (
        <>
          <h2 className={styles.feedbackWidget__question}>{question}</h2>
          <div className={styles.feedbackWidget__buttons}>
            <button className={cn(styles.feedbackWidget__button)} onClick={() => { feedbackClick(question, 'yes'); setHasAnswered(true); }} id="feedbackWidget__button--yes"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M313.4 32.9c26 5.2 42.9 30.5 37.7 56.5l-2.3 11.4c-5.3 26.7-15.1 52.1-28.8 75.2h144c26.5 0 48 21.5 48 48 0 18.5-10.5 34.6-25.9 42.6C497 275.4 504 288.9 504 304c0 23.4-16.8 42.9-38.9 47.1 4.4 7.3 6.9 15.8 6.9 24.9 0 21.3-13.9 39.4-33.1 45.6.7 3.3 1.1 6.8 1.1 10.4 0 26.5-21.5 48-48 48h-97.5c-19 0-37.5-5.6-53.3-16.1l-38.5-25.7C176 420.4 160 390.4 160 358.3V247.1c0-29.2 13.3-56.7 36-75l7.4-5.9c26.5-21.2 44.6-51 51.2-84.2l2.3-11.4c5.2-26 30.5-42.9 56.5-37.7zM32 192h64c17.7 0 32 14.3 32 32v224c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32V224c0-17.7 14.3-32 32-32z" /></svg> Yes</button>
            <button className={cn(styles.feedbackWidget__button)} onClick={() => { feedbackClick(question, 'no'); setHasAnswered(true); }} id="feedbackWidget__button--no"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M313.4 479.1c26-5.2 42.9-30.5 37.7-56.5l-2.3-11.4c-5.3-26.7-15.1-52.1-28.8-75.2h144c26.5 0 48-21.5 48-48 0-18.5-10.5-34.6-25.9-42.6C497 236.6 504 223.1 504 208c0-23.4-16.8-42.9-38.9-47.1 4.4-7.3 6.9-15.8 6.9-24.9 0-21.3-13.9-39.4-33.1-45.6.7-3.3 1.1-6.8 1.1-10.4 0-26.5-21.5-48-48-48h-97.5c-19 0-37.5 5.6-53.3 16.1l-38.5 25.7C176 91.6 160 121.6 160 153.7V264.9c0 29.2 13.3 56.7 36 75l7.4 5.9c26.5 21.2 44.6 51 51.2 84.2l2.3 11.4c5.2 26 30.5 42.9 56.5 37.7zM32 384h64c17.7 0 32-14.3 32-32V128c0-17.7-14.3-32-32-32H32c-17.7 0-32 14.3-32 32v224c0 17.7 14.3 32 32 32z" /></svg> No</button>
          </div>
        </>
      )}
      {hasAnswered && (
        <>
          <h2 className={styles.feedbackWidget__question}>{content.thanksText || "Thank you for your feedback!"}</h2>
        </>
      )}
    </div>
  )
}
