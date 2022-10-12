/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation
 The sidebars can be generated from the filesystem, or explicitly defined here.
 Create as many sidebars as you want.
 */

module.exports = {
  tutorials: [
    'overview',
   {
      type: 'category',
      label: 'Get started with Apache Airflow',
      link: {
            type: 'doc',
            id: 'get-started-with-airflow',
       },
      items: [
        'get-started-with-airflow',
        'get-started-with-airflow-part-2',
      ],
    },
    'astro-python-sdk',
  ],
};
