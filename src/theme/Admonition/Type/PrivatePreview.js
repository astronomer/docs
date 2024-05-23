import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
import IconWarning from '@theme/Admonition/Icon/Warning';
const infimaClassName = 'alert alert--warning';
const defaultProps = {
  icon: <IconWarning />,
  children: <div class="admonitionContent">This feature is in <a href="https://www.astronomer.io/docs/astro/feature-previews" target="_blank" rel="noopener noreferrer">Private Preview</a>. Please reach out to your account team to enable this feature.</div>,
  title: (
    <Translate
      id="theme.admonition.Warning"
      description="The default label used for the PrivatePreview admonition (:::privatepreview)">
      private preview
    </Translate>
  ),
};
export default function AdmonitionTypePrivatePreview(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {defaultProps.children}
    </AdmonitionLayout>
  );
}
