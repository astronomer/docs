import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
import IconInfo from '@theme/Admonition/Icon/Info';
const infimaClassName = 'alert alert--info';
const defaultProps = {
  icon: <IconInfo />,
  children: <div class="admonitionContent">This command is only available on Astronomer Software.</div>,
  title: (
    <Translate
      id="theme.admonition.Info"
      description="The default label used for the CliSoftwareOnly admonition (:::clisoftwareonly)">
      software only
    </Translate>
  ),
};
export default function AdmonitionTypeCliSoftwareOnly(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {defaultProps.children}
    </AdmonitionLayout>
  );
}
