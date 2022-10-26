/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation
 The sidebars can be generated from the filesystem, or explicitly defined here.
 Create as many sidebars as you want.
 */

module.exports = {
  cloudIde: [
    "overview",
    {
      type: "category",
      label: "Quick Start",
      items: [
        "quick-start/create-project",
        "quick-start/create-pipeline",
        "quick-start/first-cell",
        "quick-start/connecting-to-a-database",
        // "quick-start/create-python-cell",
        // "quick-start/create-sql-cell",
        // "quick-start/running-modes",
        // "quick-start/deploying",
        // "quick-start/next-steps",
      ],
    },
    {
      type: "category",
      label: "Concepts",
      items: [
        "concepts/project",
        "concepts/pipeline",
        "concepts/cell",
        "concepts/connection",
      ],
    },
  ],
};
