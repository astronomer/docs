import React from 'react';
import Footer from '@theme-original/DocItem/Footer';
import NewsletterForm from '@site/src/components/NewsletterForm';
import FeedbackWidget from '@site/src/components/FeedbackWidget';
export default function FooterWrapper(props) {
  return (
    <>
      <FeedbackWidget />
      <NewsletterForm />
      <Footer {...props} />
    </>
  );
}
