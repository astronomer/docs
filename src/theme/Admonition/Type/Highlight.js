import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
const infimaClassName = 'alert alert--highlight';

const defaultProps = {
  icon: null,
  title: (
    <Translate
      id="theme.admonition.highlight"
      description="The default label used for the highlight admonition (:::highlight)">
    </Translate>
  ),
};

export default function AdmonitionTypeHighlight(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {props.children}
    </AdmonitionLayout>
  );
}
