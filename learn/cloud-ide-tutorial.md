---
title: 'Write a simple ML pipeline using the Cloud IDE'
sidebar_label: 'Cloud IDE - Simple ML pipeline'
id: cloud-ide-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

Developing your pipelines has never been easier than using the Cloud IDE on Astro.

This tutorial is for people who are Astro customers and want to create their first simple ML pipeline in the Cloud IDE.

After you complete this tutorial, you'll be able to:



## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).
- Basic SQL. See the [W3 Schools SQL tutorial](https://www.w3schools.com/sql/)


## Step 1: Create your Cloud IDE project

In your Astro Cloud workspace click on the **Cloud IDE** tab in the navigation bar on the left. Create a new Cloud IDE project with the **+ Project** button in the right upper corner of the screen.

![Create a project](/PLACEHOLDER)

PLACEHOLDER (feature not turned on yet)

## Step 2: Create a new pipeline

Click on **+ Pipeline** to create a new pipeline. Give it a name and description and click **Create**.

![Create new pipeline](/img/guides/cloud_ide_new_project.png)

## Step 3: Configure a connection

Navigate to the **Connections** tab in your Cloud IDE project. Here you can define connections to external tools which can be used by all pipelines in your project. Click on **+ Connection** to add a new connection. We will use Snowflake in this tutorial but you can also use Postgres, Bigquery or Redshift. 

In the UI provide your connection credentials as shown in the screenshots below.

![Configure a connection](/img/guides/cloud_ide_new_connection.png)

![Configure a connection 2](/img/guides/cloud_ide_new_connection_2.png)

After entering your credentials click the **Test Connection button** to make sure Astro is able to connect to Snowflake. If your credentials are correct, a green banner will appear above saying "Connection successfully tested". Save the connection by clicking **Create Connection**.

## Step 4: Add required python packages

Navigate to the **Requirements** tab in your Cloud IDE project. Under this tab you can add any Python packages that you are planning to use in Cloud IDE Python cells within this Cloud IDE project. To create our simple ML model we will need the `scikit-learn` package. Add this package by clicking on **+ Requirement** and typing `scikit-learn` into the "package name" field. Select the latest version and click **Add**.

![Add scikit-learn](/img/guides/cloud_ide_add_sklearn.png)

## Step 5: Import a dataset into your database

In this tutorial we will use the try to predict the intelligence of a dog breed based on their upper and lower height and weight limits. Download [this dataset](PLACEHOLDER LINK) and import it into your database. 

If you are using Snowflake follow these steps:

1. Run the following SQL statement in a Snowflake worksheet to create the target table:

```sql 
CREATE TABLE dog_intelligence (
    BREED varchar(50),
    HEIGHT_LOW_INCHES INT,
    HEIGHT_HIGHT_INCHES INT,
    WEIGHT_LOW_LBS INT,
    WEIGHT_HIGH_LBS INT,
    REPS_LOWER INT,
    REPS_UPPER INT
);
```

2. Run this SQL statement to create the file format `my_csv_format`:

```sql
CREATE FILE FORMAT my_csv_format
    TYPE = csv
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = true;
```

3. Use the ["Loading Using the Web Interface" wizard](https://docs.snowflake.com/en/user-guide/data-load-web-ui.html) by navigating to the `dog_intelligence` table in the **Datasets** tab of the Snowflake UI and clicking on **Load Table**. Select the `dog_intelligence.csv` file you downloaded as the "Source File" and `my_csv_format` as the "File Format".

![Load csv Snowflake](/img/guides/cloud_ide_load_csv.png)

## Query your table from the Cloud IDE

Navigate back to your Cloud IDE on Astro.

1. Create your first SQL cell by clicking on **Add Cell** in the topleft corner and selecting **SQL**. 

2. Paste the following SQL code into your cell:

```sql 
SELECT * FROM <your database>.<your schema>.DOG_INTELLIGENCE LIMIT 10 
```

3. Select your Snowflake connection as shown in the screenshot below.

![Load csv Snowflake](/img/guides/cloud_ide_first_cell.png)

4. Run the cell.

With the **Table Expression** box activated by default you should now see the first 10 lines of the dataset below the cell.

## Step 7: Query your Table
Query values from the second table and return a pandas df
Step 8: Train a Random Forest Classifier
python cell (copy paste code) to train a random forest classifier on the first 80% of the data, then use it to predict classes in the last 20%
Step 10: Set up a connection to your github repo
Step 11: Export your DAG to github
Contain info that you can add to an existing project, but build wont be able to read the repo
Step 12: Deploy your DAG to Astro
maybe show the path of pulling from the repo and then using the Astro CLI to deploy, mentioning CI/CD auto deploy options linking to the Astro Module on it and later once we have it linking to the GithubActions tutorial