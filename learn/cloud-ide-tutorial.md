---
title: 'Write a simple ML pipeline using the Cloud IDE'
sidebar_label: 'Cloud IDE - Simple ML pipeline'
id: cloud-ide-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

Developing your pipelines has never been easier than using the Cloud IDE on Astro.

This tutorial is for people who are Astro customers and want to create their first simple ML pipeline in the Cloud IDE.

After you complete this tutorial, you'll be able to:

- Create a Cloud IDE project with a pipeline.
- Configure connections and requirements in the Cloud IDE.
- Run a query on a table in a database from the Cloud IDE.
- Transform a table in a database from the Cloud IDE.
- Train a simple ML model in the Cloud IDE.
- Export a DAG from the Cloud IDE to GitHub.
- Configure GitHub Secrets to deploy your DAG to Astro.

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

## Step 6: Query your table

Navigate back to your Cloud IDE on Astro.

1. Create your first SQL cell by clicking on **Add Cell** in the topleft corner and selecting **SQL**. 

2. Rename your cell from `cell_1` to `query_table`. This will also change the name of your task in the pipeline view on the right side of the screen.

3. Paste the following SQL code into your cell to select all records that do not contain any NULL values in any column:

```sql 
SELECT * FROM <your database>.<your_schema>.DOG_INTELLIGENCE 
WHERE CONCAT(BREED, HEIGHT_LOW_INCHES, HEIGHT_HIGHT_INCHES, WEIGHT_LOW_LBS, WEIGHT_HIGH_LBS, REPS_UPPER, REPS_LOWER) IS NOT NULL
```

4. Select your Snowflake connection as shown in the screenshot below.

![Select Snowflake Connection](/img/guides/cloud_ide_select_connection.png)

5. Run the cell by either clicking on the play button next to the connection field or by hitting Command + Enter.

Running the cell will create a temporary table in your database containing the output from your query.
With the **Table Expression** box activated you should now see the output containing of 136 rows below the cell.

![Table output](/img/guides/cloud_ide_query_table.png)

Our dataset contains information about the height, weight and how fast dogs of different breeds learned commands in 7 columns:

- breed: the breed of the dogs in the experiement.
- height_low_inches: height of the smallest dog of one specific breed.
- height_high_inches: height of the largest dog of one specific breed.
- weight_low_lbs: weight of the lightest dog of one specific breed.
- weight_high_lbs: weight of the heaviest dog of one specific breed.
- reps_lower: lowest repetitions necessary for a dog of a specific breed to learn a new command.
- reps_higher: highest repetitions necessary for a dog of a specific breed to learn a new command.

## Step 7: Transform your table

1. Create a second SQL cell.

2. Rename the cell from `cell_1` to `transform_table`.

3. Select the same connection as in your `query_table` cell. 

4. Copy the following SQL statement into the cell:

```sql 
SELECT HEIGHT_LOW_INCHES, HEIGHT_HIGHT_INCHES, WEIGHT_LOW_LBS, WEIGHT_HIGH_LBS,
    CASE WHEN reps_upper <= 25 THEN 'very_smart_dog'
    ELSE 'smart_dog'
    END AS INTELLIGENCE_CATEGORY
FROM {{query_table}}
```

You will notice that pasting this SQL statement will automatically create a dependency between `query_table` and `transform_table` in the pipeline view on the right side of the screen (see the screenshot below). This happens because the SQL statement in `transform_table` references the temporary table created by the `query_table` task using Jinja syntax `{{query_table}}`.

![Table output](/img/guides/cloud_ide_cell_dependency.png)

5. Run the cell.

In the output table you can see that this SQL statement created a new transformed temporary table with an binary `INTELLIGENCE_CATEGORY` column we can use as a target for our classification model. All dogs who at most needed 25 repetitions to learn a new command are put in the `very_smart_dog` category. All other dogs in the `smart_dog` category (because of course, all dogs are smart).

The predictors in our model will be the height and weight-related columns.

## Step 8: Train a model on your data

1. Create a new Python cell by clicking on **Add Cell** in the topleft corner and selecting **Python**. 

2. Rename the cell from `cell_1` to `model_task`.

3. Copy the following Python code into your cell:

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# use the table returned from the transform_table cell
df = transform_table

# calculate baseline accuracy
baseline_accuracy = df.iloc[:,-1].value_counts(normalize=True)[0]

# selecting predictors (X) and the target (y)
X = df.iloc[:,:-1]
y = df.iloc[:,-1]

# split the data into training data (80%) and testing data (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=23
)

# standardize features
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# train a RandomForestClassifier on the training data
model = RandomForestClassifier(max_depth=3, random_state=19)
model.fit(X_train_s, y_train)

# score the trained model on the testing data
score = model.score(X_test_s, y_test)

return f"baseline accuracy: {baseline_accuracy}", f"model accuracy: {score}"
```

You will notice again how the Cloud IDE will automatically create a dependency between the `transform_table` task and the `model_task` task. The Python code above references the `transform_table` object returned from the `tranform_table` cell directly (without Jinja syntax) on line 6. 

The Python code:

- imports necessary functions and classes from the scikit-learn package.
- calculates the baseline accuracy, which is the accuracy you would get if you always guessed the most common outcome (in our data `smart_dog`).
- separates out predictors (height and weight information) and the target (the intelligence category).
- splits the data into a training and testing set.
- standardizes the predicting features.
- trains a [RandomForestClassifier model](https://scikit-learn.org/stable/modules/ensemble.html#forest) on the training data.
- scores the trained model on the testing data.

4. Run the cell.

The output of the cell will show you both the baseline and the model accuracy. With the model accuracy being higher than baseline we can conclude that height and weight of dogs have a correlation (but not necessarily causation!) with how many repetitions they need to learn a new command. 

![Model output](/img/guides/cloud_ide_model_output.png)

The feature importances give you an idea which of the predictor columns were most important in the model to predict the intelligence category. The `weight_low_lbs`, the lower end of the weights of the dogs examined for a breed, gave the most information to the model for our small dataset.

:::info

To learn more about random forests check out this [MLU explain article](https://mlu-explain.github.io/random-forest/).

:::

## Step 9: Connect your GitHub to the Cloud IDE

1. Click on the GitHub **Configure** button in the topright corner of your screen to connect your Cloud IDE Project to your GitHub account.

![Connect to GitHub](/img/guides/cloud_ide_github_conn.png)

2. Enter your personal access token and the name of an existing GitHub repository that contains an Astro project. 

3. Click update to save your connection details.

:::info

If you do not have a GitHub account, you can create one for free on the [GitHub website](https://github.com/signup). To create a personal access token, see the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

:::

## Step 10: Commit your DAG to GitHub

Export your DAG by commiting it to your connected GitHub repository. 

Click the branch you want to commit to and provide a commit message. Note that you cannot commit to a branch called `main`. 

![Connect to GitHub](/img/guides/cloud_ide_commit_to_github.png)

Your DAG will be added to the `/dags` folder in your GitHub repository.

![Dags folder on GitHub](/img/guides/cloud_ide_dags_github.png)

:::info

If you made changes to several DAGs you can select which changes to commit by checking the boxes to the left of the difference view.

:::

:::caution

If a DAG with the same file as a file name already exists (i.e. if you already had a file named `dog_smarts_pipeline` in the `/dags` folder of this repository) the Cloud IDE will overwrite the existing file. For this reason it is best practise to use a seperate branch for commits from your Cloud IDE environment than for commits from other sources to the same repository.

:::

## Step 11: Deploy your DAG to Astro 

Additionally, the Cloud IDE will create a GitHub workflow to deploy to Astro in `.github/workflows/astro_deploy.yaml`.

1. Configure [GitHub Actions](https://docs.astronomer.io/astro/ci-cd?tab=multibranch#github-actions) by setting the following as [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository):
    - DEV_ASTRONOMER_KEY_ID = <your-dev-key-id>
    - DEV_ASTRONOMER_KEY_SECRET = <your-dev-key-secret> 
    - DEV_ASTRONOMER_DEPLOYMENT_ID = <your-deployment-id>

2. Send a second commit from the Cloud IDE to trigger the configured GitHub workflow to deploy your DAG to Astro

If GitHub Actions is already configured for your chosen repository the new DAG will be deployed automatically with the first commit.

:::info

Learn more on how to set up CI/CD with GitHub Actions in the [Astro Module: CI/CD](https://academy.astronomer.io/astro-module-cicd).

:::

PLACEHOLDER - image of the DAG shown on Astro (once I get a cluster)