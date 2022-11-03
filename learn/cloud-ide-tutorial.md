---
title: 'Write and schedule a simple ML pipeline using the Cloud IDE'
sidebar_label: 'Cloud IDE - Simple ML pipeline'
id: cloud-ide-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

Developing your pipelines has never been easier than using the Cloud IDE on Astro.

This tutorial is Astro customers who want to create their first simple ML pipeline in the Cloud IDE. To explore Cloud IDE functionality, you will create a pipeline that runs a random forest model to predict dog breed intelligence and then schedule that pipeline on an Airflow deployment on Astro.

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
- Basic SQL. See the [W3 Schools SQL tutorial](https://www.w3schools.com/sql/).
- The Cloud IDE. See [Astro Cloud IDE](https://docs.astronomer.io/astro/cloud-ide).

## Prerequisites

To complete this tutorial, you need:

- An Astro account. If you are not an Astronomer customer yet and want to learn more about Astro you can [join the weekly demo](https://www.astronomer.io/events/weekly-demo/) or [contact us directly](https://www.astronomer.io/get-started/?referral=docs-nav-button).
- An account in one of the following database services, which are currently supported in the Cloud IDE: [GCP BigQuery](https://cloud.google.com/bigquery/docs/quickstarts), [Postgres](https://www.postgresql.org/docs/current/tutorial-start.html), [Snowflake](https://docs.snowflake.com/en/user-guide-getting-started.html) or [AWS Redshift](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html). Additionally you will need your login credentials to create the connection to your database.
- A GitHub account with access to a private or public repository that contains an Airflow Project created by the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) as well as a Personal Access Token for your GitHub account. If you do not have a GitHub account, you can create one for free on the [GitHub website](https://github.com/signup). To create a personal access token, see the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Step 1: Create your Cloud IDE project

Log in to your Astro Cloud workspace and click on the **Cloud IDE** tab in the navigation bar on the left. 

1. Create a new Cloud IDE project with the **+ Project** button in the right upper corner of the screen.
2. Give your Cloud IDE project a catchy name and a description.

![Create new project](/img/guides/cloud_ide_create_project.png)

3. Click on **Create**.

## Step 2: Create a new pipeline

Click on **+ Pipeline** to create a new pipeline. 

![Create new pipeline](/img/guides/cloud_ide_new_pipeline.png)

Give your pipeline a name and description and click **Create**. The pipeline editor for the new pipeline will open automatically.

:::info

The name you give your pipeline will be the name of the DAG which the Cloud IDE will create from your input. Names of pipelines within a project must be unique and can't contain special characters.

:::

## Step 3: Configure a connection

You can add a connection to your database from within the pipeline editor. 

1. Click on the fourth icon ("Environment") of the panel on the right side of your screen to be able to add connections, variables and requirements to your Cloud IDE project. 

![Configure a connection](/img/guides/cloud_ide_environment_button.png)

2. Click on **+ Connection** to add a new connection. We use Snowflake in this tutorial, but you can also use Postgres, Bigquery, or Redshift. 

    In the UI provide your connection credentials as shown in the screenshots below.

    ![Configure a connection](/img/guides/cloud_ide_add_connection.png)

    ![Configure a connection 2](/img/guides/cloud_ide_add_connection_2.png)

3. Use the **Test Connection button** to make sure Astro is able to connect to your database. If your credentials are correct, a green banner will appear above saying "Connection successfully tested". 

4. Save the connection by clicking **Create Connection**.

:::info

You can also add connections, variables and requirements to your Cloud IDE project from the project overview.

:::

## Step 4: Add required Python packages

Navigate to the **Requirements** tab in the pipeline editor "Environment" section. Under this tab you can add any Python packages that you are planning to use in Cloud IDE Python cells within this Cloud IDE project. To create the simple ML model shown in this tutorial, you will need the `scikit-learn` package. Click on **+ Requirement** and type `scikit-learn` into the "package name" field. Select the latest version at the top of the list and click **Add**.

![Add scikit-learn](/img/guides/cloud_ide_add_requirement.png)

## Step 5: Import a dataset into your database

Now that you have your Cloud IDE project set up, you can move on to creating an ML pipeline. For this tutorial you will try to predict the intelligence of a dog breed based on their upper and lower height and weight limits. 

:::info

The dataset we use in this tutorial is a slightly changed version of [this dataset on Kaggle](https://www.kaggle.com/datasets/jasleensondhi/dog-intelligence-comparison-based-on-size). 

:::

1. Download the [ dog_intelligence.csv ] PLACEHOLDER LINK dataset.

2. Run the following SQL statement in a Snowflake worksheet to create the target table:

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

3. Run this SQL statement to create the file format `my_csv_format`:

```sql
CREATE FILE FORMAT my_csv_format
    TYPE = csv
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = true;
```

4. Use the ["Loading Using the Web Interface" wizard](https://docs.snowflake.com/en/user-guide/data-load-web-ui.html) by navigating to the `dog_intelligence` table in the **Databases** tab of the Snowflake UI and clicking on **Load Table**. Select the `dog_intelligence.csv` file you downloaded as the "Source File" and `my_csv_format` as the "File Format".

![Load csv Snowflake](/img/guides/cloud_ide_load_csv.png)

:::info

The steps above are specific to using Snowflake. If you are using a different database please refer to their documentation to upload the data from the CSV file provided into a table.

:::

## Step 6: Query your table

Navigate back to your Cloud IDE on Astro.

1. Create your first SQL cell by clicking on **Add Cell** in the topleft corner and selecting **SQL**. 

2. Rename your cell from `cell_1` to `query_table`.

3. In the right sidebar click on the top "Pipeline" icon to view your cell in the pipeline view.

![Pipeline View](/img/guides/cloud_ide_pipeline_view.png)

4. Paste the following SQL code into your cell. This query will select all records that do not contain any NULL values in any column. Make sure to update the query with your database and schema name.

```sql 
SELECT * FROM <your database>.<your_schema>.DOG_INTELLIGENCE 
WHERE CONCAT(BREED, HEIGHT_LOW_INCHES, HEIGHT_HIGHT_INCHES, WEIGHT_LOW_LBS, 
WEIGHT_HIGH_LBS, REPS_UPPER, REPS_LOWER) IS NOT NULL
```

5. Select your Snowflake connection as shown in the screenshot below.

![Select Snowflake Connection](/img/guides/cloud_ide_select_connection.png)

6. Run the cell by either clicking on the play button next to the connection field or by hitting Command + Enter.

Running the cell will create a temporary table in your database containing the output from your query.
With the **Table Expression** box activated you should now see the output containing 136 rows below the cell.

![Table output](/img/guides/cloud_ide_query_table.png)

The dataset has 7 columns containing information about the height, weight, breed, and learning speed of different dogs. The `reps_lower` and `reps_higher` columns contain the lower and upper bounds of how many repetitions of a new command each breed of dog needed to learn it. This value is used to sort the dogs into two categories which will be the target of your classification model. The predictors will be the four columns containing height and weight information.

## Step 7: Transform your table

Before you can train the model, you first need to transform the data in your table to convert the command repetitions to a binary intelligence category.

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

The output table should contain a new binary `INTELLIGENCE_CATEGORY` column which will be used as a target for your classification model. All dogs who needed 25 or fewer repetitions to learn a new command are put in the `very_smart_dog` category. All other dogs are put in the `smart_dog` category (because of course, all dogs are smart).

## Step 8: Train a model on your data

Train a random forest model to predict the dog intelligence category of a breed based on height and weight information.

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

# get feature importances
feature_importances = list(zip(X_train.columns, model.feature_importances_))

return f"baseline accuracy: {baseline_accuracy}", f"model accuracy: {score}", feature_importances 
```

You will notice again how the Cloud IDE will automatically create a dependency between the `transform_table` task and the `model_task` task. The Python code above references the `transform_table` object returned from the `tranform_table` cell directly (without Jinja syntax) on line 6. 

The Python code completes the following steps:

- Imports necessary functions and classes from the scikit-learn package.
- Calculates the baseline accuracy, which is the accuracy you would get if you always guessed the most common outcome (in our data `smart_dog`).
- Separates out predictors (height and weight information) and the target (the intelligence category).
- Splits the data into a training and testing set.
- Standardizes the predicting features.
- Trains a [RandomForestClassifier model](https://scikit-learn.org/stable/modules/ensemble.html#forest) on the training data.
- Scores the trained model on the testing data.

4. Run the cell.

The output of the cell will show you both the baseline and the model accuracy. With the model accuracy being higher than baseline we can conclude that height and weight of dogs have a correlation (but not necessarily causation!) with how many repetitions they need to learn a new command. 

![Model output](/img/guides/cloud_ide_model_output.png)

The feature importances give you an idea which of the predictor columns were most important in the model to predict the intelligence category. The `weight_low_lbs`, the lower end of the weights of the dogs examined for a breed, gave the most information to the model for our small dataset.

:::info

To learn more about random forests check out this [MLU explain article](https://mlu-explain.github.io/random-forest/).

:::

## Step 9: Pick a schedule for your pipeline

Setting a schedule for your pipeline will determine how this pipeline will be scheduled once it is deployed to Astro as a DAG. Within the Cloud IDE a pipeline will only run if you start a run manually.

1. Click on the calendar symbol ("Schedule") in the right sidebar to see possibilities to schedule your DAG. 

2. Set the "START DATE" to yesterday's date.

![Schedule DAG](/img/guides/cloud_ide_schedule_dag.png)

3. Edit the "CRON STRING" to schedule your DAG to run every weekday at 2:30am and 6:30pm.

![CRON menu](/img/guides/cloud_ide_cron_menu.png)

4. Click **Update Settings** to save your schedule.

## Step 10: View your DAG code

Pipelines in the Cloud IDE offer you the possibility of running ad-hoc analysis and easy DAG development. Once you finish a pipeline and want to run it in a local Airflow instance or on Astro you will need to export your pipeline as DAG code.

1. Click on the "Code" tab on the right sidebar. You can see your pipeline which was automatically converted to DAG code using the [Astro SDK](https://docs.astronomer.io/learn/astro-python-sdk-etl).

![View Code](/img/guides/cloud_ide_code_view.png)

2. Click **Download** in order to download the DAG file if you want to manually add it to a project.

## Step 10: Connect your GitHub to the Cloud IDE

Now that you have trained the model, you can connect GitHub to the Cloud IDE to commit your pipeline as a DAG to any Airflow project.

1. Click on the GitHub **Configure** button in the topright corner of your screen to connect your Cloud IDE Project to your GitHub account.

![Connect to GitHub](/img/guides/cloud_ide_github_conn.png)

2. Enter your personal access token and the name of an existing GitHub repository that contains an Astro project. 

3. Click update to save your connection details.

## Step 11: Commit your DAG to GitHub

Export your DAG by commiting it to your connected GitHub repository. 

Click the branch you want to commit to and provide a commit message. Note that you cannot commit to a branch called `main`. 

![Connect to GitHub](/img/guides/cloud_ide_commit_to_github.png)

Your DAG will be added to the `/dags` folder in your GitHub repository.

![Dags folder on GitHub](/img/guides/cloud_ide_dags_github.png)

:::info

If you made changes to several DAGs you can select which changes to commit by checking the boxes to the left of the difference view.

:::

:::caution

If file with the same name as your Cloud IDE pipeline already exists (i.e. if you already had a file named `dog_smarts_pipeline` in the `/dags` folder of this repository) the Cloud IDE will overwrite the existing file. For this reason it is best practise to use a seperate branch for commits from your Cloud IDE environment than for commits from other sources to the same repository.

:::

## Step 12: Deploy your DAG to Astro 

When you commit a Cloud IDE pipeline to a GitHub repository, the Cloud IDE will create a GitHub workflow of the name `astro_deploy.yaml` in case it does not exist yet.

1. Configure [GitHub Actions](https://docs.astronomer.io/astro/ci-cd?tab=multibranch#github-actions) by setting the following as [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

- DEV_ASTRONOMER_KEY_ID = `<your-dev-key-id>`
- DEV_ASTRONOMER_KEY_SECRET = `<your-dev-key-secret>`
- DEV_ASTRONOMER_DEPLOYMENT_ID = `<your-deployment-id>`

![GitHub Secrets](/img/guides/cloud_ide_github_secrets.png)

2. Add the `scikit-learn` to `requirements.txt` and commit the change. This second commit will trigger GitHub Actions again, using the GitHub secrets you configured.

If GitHub Actions is already configured for your chosen repository the new DAG will be deployed automatically with the first commit.

:::info

Learn more on how to set up CI/CD with GitHub Actions in the [Astro Module: CI/CD](https://academy.astronomer.io/astro-module-cicd).

:::caution

To be able to deploy your DAG the Runtime Image used in the Airflow project of your GitHub repo needs to be compatible with the Runtime Image used in your Astro cloud deployment. You might need to change the version number in the Dockerfile of the Airflow project in your GitHub repository.

:::

## Step 13: Run your DAG on Astro

1. Back on Astro, click on the Astronomer logo to exit the pipeline editor.

2. Open the Airflow UI of your deployment (**Deployments** -> Your deployment -> **Open Airflow**).

3. Make sure that your Airflow deployment has a connection with the same Connection ID and credentials configured as your Cloud IDE project.

4. Since temporary tables are not JSON serializeable you will need to set XCom pickling to True. To do so click on **Admin** -> **Variables** in your Airflow UI and add a new variable with the **+** button. Provide the key `AIRFLOW__CORE__ENABLE_XCOM_PICKLING` and the value `True`. Click **Save**.

![Add Variable in Airflow UI](/img/guides/cloud_ide_add_variable.png)

5. Back in the DAGs view run your DAG by clicking the play button.

![Run DAG on Astro](/img/guides/cloud_ide_dag_ran_in_UI.png)

## Conclusion

You now know how to use the Cloud IDE to write a simple ML pipeline! More specifically, you can now:

- Create a new Cloud IDE project and pipeline. 
- Use a SQL cells to query and transform tables in a database.
- Pass information between SQL and Python cells
- Run a simple RandomForestClassifier on a dataset.
- Commit your pipeline to GitHub.
- Use GitHub Actions to deploy your new DAG to Astro.

As a next step, read the [Cloud IDE documentation](https://docs.astronomer.io/astro/cloud-ide) to learn more about this next generation DAG writing environment.