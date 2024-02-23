import React from 'react';
import AdmonitionTypeNote from '@theme/Admonition/Type/Note';
import AdmonitionTypeTip from '@theme/Admonition/Type/Tip';
import AdmonitionTypeInfo from '@theme/Admonition/Type/Info';
import AdmonitionTypeWarning from '@theme/Admonition/Type/Warning';
import AdmonitionTypeDanger from '@theme/Admonition/Type/Danger';
import AdmonitionTypeCaution from '@theme/Admonition/Type/Caution';
import AdmonitionTypeCli from '@theme/Admonition/Type/Cli';
import AdmonitionTypeHighlight from '@theme/Admonition/Type/Highlight';
import AdmonitionTypePrivatePreview from '@theme/Admonition/Type/PrivatePreview';
import AdmonitionTypePublicPreview from '@theme/Admonition/Type/PublicPreview';
import AdmonitionTypeCliAstroOnly from '@theme/Admonition/Type/CliAstroOnly';
import AdmonitionTypeCliSoftwareOnly from '@theme/Admonition/Type/CliSoftwareOnly';
import AdmonitionTypeCliAstroAndSoftware from '@theme/Admonition/Type/CliAstroAndSoftware';


const admonitionTypes = {
  note: AdmonitionTypeNote,
  tip: AdmonitionTypeTip,
  info: AdmonitionTypeInfo,
  warning: AdmonitionTypeWarning,
  danger: AdmonitionTypeDanger,
  cli: AdmonitionTypeCli,
  highlight: AdmonitionTypeHighlight,
  privatepreview: AdmonitionTypePrivatePreview,
  publicpreview: AdmonitionTypePublicPreview,
  cliastroonly: AdmonitionTypeCliAstroOnly,
  clisoftwareonly: AdmonitionTypeCliSoftwareOnly,
  cliastroandsoftware: AdmonitionTypeCliAstroAndSoftware
};

// Undocumented legacy admonition type aliases
// Provide hardcoded/untranslated retrocompatible label
// See also https://github.com/facebook/docusaurus/issues/7767
const admonitionAliases = {
  secondary: (props) => <AdmonitionTypeNote title="secondary" {...props} />,
  important: (props) => <AdmonitionTypeInfo title="important" {...props} />,
  success: (props) => <AdmonitionTypeTip title="success" {...props} />,
  caution: AdmonitionTypeCaution,
};
export default {
  ...admonitionTypes,
  ...admonitionAliases,
};
