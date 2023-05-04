import React from 'react';
import Footer from '@theme-original/DocItem/Footer';
import NewsletterForm from '@site/src/components/NewsletterForm';
export default function FooterWrapper(props) {
  return (
    <>
      <NewsletterForm />
      <Footer {...props} />
    </>
  );
}
