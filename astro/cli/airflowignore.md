---
title: 'Use `.airflowignore` to ignorre files in your Astro project'
sidebar_label: 'Ignore project files'
id: airflowignore
---

You can create an `.airflowignore` file in the `dags` directory of your Astro project to identify the files to ignore when you deploy to Astro or develop locally. This can be helpful if your team has a single Git repository that contains DAGs for multiple projects.

The `.airflowignore` file and the files listed in it must be in the same `dags` directory of your Astro project. Files or directories listed in `.airflowignore` are not parsed by the Airflow scheduler and the DAGs listed in the file don't appear in the Airflow UI.

For more information about `.airflowignore`, see [`.airflowignore` in the Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#airflowignore). To learn more about the code deploy process, see [What happens during a code deploy](/astro/deploy-code.md#what-happens-during-a-code-deploy).

## Setup

1. In the `dags` directory of your Astro project, create a new file named `.airflowignore`.

2. List the files or sub-directories you want ignored when you push code to Astro or when you are developing locally. You should list the path for each file or directory relative to the `dags` directory. For example: 

    ```text
    mydag.py
    data-team-dags
    some-dags/ignore-this-dag.py
    ```

    You can also use regular expressions to specify groups of files. See the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#airflowignore) for more information about usage.
    
3. Save your changes locally or deploy to Astro.

    Your local Airflow environment automatically updates as soon as you save your changes to `.airflowignore`. To apply your change in Astro, you need to deploy. See [Deploy code](/astro/deploy-code.md).