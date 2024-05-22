import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
import IconWarning from '@theme/Admonition/Icon/Warning';
const infimaClassName = 'alert alert--warning';
const defaultProps = {
  icon: <IconWarning />,
  children: <div class="admonitionContent">This feature is in <a href="https://docs.astronomer.io/astro/feature-previews" target="_blank" rel="noopener noreferrer">Public Preview</a>. </div>,
  title: (
    <Translate
      id="theme.admonition.Warning"
      description="The default label used for the PublicPreview admonition (:::publicpreview)">
      public preview
    </Translate>
  ),
};
export default function AdmonitionTypePublicPreview(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {defaultProps.children}
    </AdmonitionLayout>
  );
}
