import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
const infimaClassName = 'alert alert--cli';

const defaultProps = {
  icon: <svg width="1200pt" height="1200pt" version="1.1" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
  <g fill-rule="evenodd">
    <path d="m1106.2 1106.2v-112.5h-1012.5v112.5z" />
    <path d="m168.75 168.75h862.5v750h-862.5zm93.75 93.75v562.5h675v-562.5z" />
    <path d="m337.5 337.5h75v75h-75z" />
    <path d="m412.5 412.5h75v75h-75z" />
    <path d="m337.5 487.5h75v75h-75z" />
    </g>
    </svg>,
  title: (
    <Translate
      id="theme.admonition.cli"
      description="The default label used for the Astro CLI admonition (:::cli)">
      cli
    </Translate>
  ),
};

export default function AdmonitionTypeCli(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {props.children}
    </AdmonitionLayout>
  );
}
