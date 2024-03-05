import React from 'react';
import clsx from 'clsx';
import Translate from '@docusaurus/Translate';
import AdmonitionLayout from '@theme/Admonition/Layout';
import IconInfo from '@theme/Admonition/Icon/Info';
const infimaClassName = 'alert alert--info';
const defaultProps = {
  icon: <IconInfo />,
  children: <div class="admonitionContent">This command is available for both Astro and Astronomer Software. Any difference in usage will be documented in separate tabs for each product. </div>,
  title: (
    <Translate
      id="theme.admonition.Info"
      description="The default label used for the CliAstroAndSoftware admonition (:::cliastroandsoftware)">
      astro and software
    </Translate>
  ),
};
export default function AdmonitionTypeCliAstroAndSoftware(props) {
  return (
    <AdmonitionLayout
      {...defaultProps}
      {...props}
      className={clsx(infimaClassName, props.className)}>
      {defaultProps.children}
    </AdmonitionLayout>
  );
}
