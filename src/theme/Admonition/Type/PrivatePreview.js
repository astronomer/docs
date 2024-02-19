import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
import IconWarning from '@theme/Admonition/Icon/Warning';
const infimaClassName = 'alert alert--warning';
const admonitionText = "This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature."
const defaultProps = {
  icon: <IconWarning />,
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
      {admonitionText}
    </AdmonitionLayout>
  );
}
