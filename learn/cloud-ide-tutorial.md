---
title: 'ML pipelines with the Astro Cloud IDE'
sidebar_label: 'ML with the Astro Cloud IDE'
id: cloud-ide-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

Developing data pipelines has never been easier than when using the Astro Cloud IDE.

The Astro Cloud IDE automatically generates DAGs based on configurations you set in its visual interface. Using the Astro Cloud IDE, you can create a complete data pipeline of Python and SQL tasks without setting dependencies or connections in code. 

This tutorial is for Astro customers who want to create their first simple ML pipeline in the Astro Cloud IDE. To explore Astro Cloud IDE functionality, you will create a pipeline that runs a random forest model to predict dog breed intelligence, then schedule and deploy the pipeline on Airflow.

After you complete this tutorial, you'll be able to:

- Create an Astro Cloud IDE project with a pipeline.
- Configure connections and requirements in the Astro Cloud IDE.
- Run a query on a table in a database from the Astro Cloud IDE.
- Transform a table in a database from the Astro Cloud IDE.
- Train a simple ML model in the Astro Cloud IDE.
- Export a DAG from the Astro Cloud IDE to GitHub.
- Configure GitHub Secrets to deploy your DAG to Astro.

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).
- Basic SQL. See the [W3 Schools SQL tutorial](https://www.w3schools.com/sql/).
- The Astro Cloud IDE. See [Astro Cloud IDE](https://docs.astronomer.io/astro/cloud-ide).

## Prerequisites

- An account in one of the following database services, which are currently supported in the Astro Cloud IDE: [GCP BigQuery](https://cloud.google.com/bigquery/docs/quickstarts), [Postgres](https://www.postgresql.org/docs/current/tutorial-start.html), [Snowflake](https://docs.snowflake.com/en/user-guide-getting-started.html) or [AWS Redshift](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html). Additionally you will need your login credentials to create the connection to your database.
- A GitHub account with access to a private or public repository that contains an Airflow Project created by the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) 
- A Personal Access Token for your GitHub account. To create a personal access token, see the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Step 0: Create an Astro account

If you do not already have an Astro account, [sign up for a free trial](https://www.astronomer.io/try-astro/) and follow the onboarding flow to create your first Organization, Workspace and Deployment.

## Step 1: Create your Astro Cloud IDE project

1. In the Cloud UI, select a Workspace, and click **Cloud IDE** in the left menu.

    ![Cloud IDE](/img/tutorials/cloud-ide-tutorial_cloud_ide_button.png)

2. Click **+ Project** and give your Astro Cloud IDE project a name and a description.

    ![Create new project](/img/guides/cloud_ide_create_project.png)

3. Click **Create**.

## Step 2: Create a new pipeline

1. Click on **+ Pipeline** to create a new pipeline. 

    ![Create new pipeline](/img/guides/cloud_ide_new_pipeline.png)

2. Give your pipeline a name and description and click **Create**. The pipeline editor for the new pipeline will open automatically.

The name you give your pipeline will be the name of the DAG which the Astro Cloud IDE will create from your input. Names of pipelines must be unique within a project and can't contain special characters.

## Step 3: Configure a connection

To run your ML model on data, you need to connect to your database. Thankfully, the Astro Cloud IDE handles connection configuration for you!

1. Click **Environment** to add connections, variables, and dependencies to your Astro Cloud IDE project. 

    ![Configure a connection](/img/guides/cloud_ide_environment_button.png)

2. Click **+ Connection** to add a new connection. This tutorial uses Snowflake as an example, but you can also use Postgres, Bigquery, or Redshift. 

    Provide your connection credentials as shown in the following screenshots:

    ![Configure a connection](/img/guides/cloud_ide_add_connection.png)

    ![Configure a connection 2](/img/guides/cloud_ide_add_connection_2.png)

3. Click **Test Connection** to confirm that Astro can connect to your database. If your credentials are correct, a green banner will appear above saying "Connection successfully tested". 

4. Click **Create Connection** to save your changes.

## Step 4: Add required Python packages

In the same section where you configured your database connection, open the **Requirements** tab. Here you can add any Python packages that you need for your project. To create the simple ML model, you need to add the `scikit-learn` package. 

1. Click **+ Requirements**
2. In the "Package name" field, type `scikit-learn`. The Astro Cloud IDE produces a list of packages to choose from.
3. Select the latest version at the top of the list and click **Add**.

    ![Add scikit-learn](/img/guides/cloud_ide_add_requirement.png)

## Step 5: Import a dataset into your database

Now that you've set up the environment for your pipelines, you can create pipelines - starting with your source data! For this tutorial you will try to predict the intelligence of a dog breed based on their upper and lower limits for weight and height. 

:::info

The dataset used in this tutorial is a slightly modified version of [this dataset on Kaggle](https://www.kaggle.com/datasets/jasleensondhi/dog-intelligence-comparison-based-on-size). 

:::

1. Download the [dog_intelligence.csv](https://github.com/astronomer/learn-tutorials-data/blob/main/dog_intelligence.csv) dataset.

2. Run the following SQL statement in a Snowflake worksheet to create the target table:

    ```sql 
    CREATE TABLE dog_intelligence (
        BREED varchar(50),
        HEIGHT_LOW_INCHES INT,
        HEIGHT_HIGH_INCHES INT,
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

4. In the Snowflake UI, go to the `dog_intelligence` table in **Databases** and click on **Load Table**.
5. Use the ["Loading Using the Web Interface" wizard](https://docs.snowflake.com/en/user-guide/data-load-web-ui.html). Select the `dog_intelligence.csv` file you downloaded as the **Source File** and `my_csv_format` as the **File Format**.

    ![Load csv Snowflake](/img/guides/cloud_ide_load_csv.png)

6. Verify that the data has been loaded into your Snowflake database by running the following query in a worksheet:

    ```sql
    SELECT * FROM <your database>.<your_schema>.dog_intelligence
    ```

The steps above are specific to using Snowflake. If you are using a different database, please refer to their documentation and upload the data from the provided CSV file into a table.

## Step 6: Query your table

Navigate back to your Astro Cloud IDE on Astro.

1. Create your first SQL cell by clicking **Add Cell** and selecting **SQL**. A cell is equivalent to an Airflow task. However, you don't have to know how to write an Airflow task to write a cell!

2. Rename your cell from `cell_1` to `query_table`.

3. Click **Pipeline** to view your cell as a data pipeline.

    ![Pipeline View](/img/guides/cloud_ide_pipeline_view.png)

4. Paste the following SQL code into your cell. This query selects all records that do not contain any `NULL` values in any column. Make sure to update the query with your database and schema name.

    ```sql 
    SELECT * FROM <your database>.<your_schema>.DOG_INTELLIGENCE 
    WHERE CONCAT(BREED, HEIGHT_LOW_INCHES, HEIGHT_HIGH_INCHES, WEIGHT_LOW_LBS, 
    WEIGHT_HIGH_LBS, REPS_UPPER, REPS_LOWER) IS NOT NULL
    ```

5. Add your Snowflake connection to the cell as shown in the following screenshot:

    ![Select Snowflake Connection](/img/guides/cloud_ide_select_connection.png)

6. Make sure that the **Table Expression** checkbox is checked to create a temporary in your database and view the output below your SQL cell upon running it.

7. Run the cell by clicking the play button next to the connection.

8. Below the cell, click **RESULTS** to see the output containing 136 rows.

    ![Table output](/img/guides/cloud_ide_query_table.png)

The dataset has 7 columns containing information about the height, weight, breed, and learning speed of different dogs. The `reps_lower` and `reps_higher` columns contain the lower and upper bounds of how many repetitions of a new command each breed of dog needed to learn it. This value is used to sort the dogs into two categories which will be the target of your classification model. The predictors will be the four columns containing height and weight information.

## Step 7: Transform your table

Before you can train the model, you first need to transform the data in your table to convert the command repetitions to a binary intelligence category.

1. Create a second SQL cell.

2. Rename the cell from `cell_1` to `transform_table`.

3. Select the same connection as in your `query_table` cell. 

4. Copy the following SQL statement into the cell:

    ```sql 
    SELECT HEIGHT_LOW_INCHES, HEIGHT_HIGH_INCHES, WEIGHT_LOW_LBS, WEIGHT_HIGH_LBS,
        CASE WHEN reps_upper <= 25 THEN 'very_smart_dog'
        ELSE 'smart_dog'
        END AS INTELLIGENCE_CATEGORY
    FROM {{query_table}}
    ```

    Notice that after you create this cell, the Astro Cloud IDE automatically creates a dependency between `query_table` and `transform_table` in the pipeline view. This happens because the SQL statement in `transform_table` references the temporary table created by the `query_table` task using the Jinja syntax `{{query_table}}`.

    ![Table output](/img/guides/cloud_ide_cell_dependency.png)

5. Run the cell.

The output table should contain a new binary `INTELLIGENCE_CATEGORY` column which will be used as a target for your classification model. All dogs who needed 25 or fewer repetitions to learn a new command are put in the `very_smart_dog` category. All other dogs are put in the `smart_dog` category (because, of course, all dogs are smart).

## Step 8: Train a model on your data

Train a random forest model to predict the dog intelligence category of a breed based on height and weight information.

1. Create a new Python cell by clicking **Add Cell** and selecting **Python**. 

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

    return f"""
    baseline accuracy: {baseline_accuracy},\n
    model accuracy: {score},\n
    feature importances: {feature_importances}
    """ 
    ```

    You will notice again how the Astro Cloud IDE will automatically create a dependency between the `transform_table` task and the `model_task` task. The Python code above references the `transform_table` object returned from the `transform_table` cell directly (without Jinja syntax) on line 6. 

    The Python code completes the following steps:

    - Import necessary functions and classes from the `scikit-learn` package.
    - Calculate the baseline accuracy, which is the accuracy you would get if you always guessed the most common outcome (in our data `smart_dog`).
    - Separate out predictors (height and weight information) and the target (the intelligence category).
    - Split the data into a training and testing set.
    - Standardize the predicting features.
    - Train a [RandomForestClassifier model](https://scikit-learn.org/stable/modules/ensemble.html#forest) on the training data.
    - Score the trained model on the testing data.

4. Run the cell.

The output of the cell shows you both the baseline and the model accuracy. With the model accuracy being higher than baseline, you can conclude that height and weight of dogs have a correlation (but not necessarily causation!) with how many repetitions they need to learn a new command. 

![Model output](/img/guides/cloud_ide_model_output.png)

The feature importances give you an idea which of the predictor columns were most important in the model to predict the intelligence category. The `weight_low_lbs`, the lower end of the weights of the dogs examined for a breed, gave the most information to the model for our small dataset.

To learn more about random forests check out this [MLU explain article](https://mlu-explain.github.io/random-forest/).

## Step 9: Pick a schedule for your pipeline

Setting a schedule for your pipeline will determine how this pipeline will be scheduled once it is deployed to Astro as a DAG. Within the Astro Cloud IDE a pipeline will only run if you start a run manually.

1. Click **Schedule** to see your DAG's current schedule. 

2. Set **START DATE** to yesterday's date.

    ![Schedule DAG](/img/guides/cloud_ide_schedule_dag.png)

3. Edit **CRON STRING** to schedule your DAG to run every weekday at 2:30 AM and 6:30 PM.

    ![CRON menu](/img/guides/cloud_ide_cron_menu.png)

4. Click **Update Settings** to save your schedule.

## Step 10: View your DAG code (Optional)

Through this tutorial, the Astro Cloud IDE was building a DAG based on the configurations you set in the Cloud UI. Export your pipeline as DAG code to see the results of your work.

1. Click **Code**. You can see that your pipeline was automatically converted to DAG code using the [Astro SDK](https://docs.astronomer.io/learn/astro-python-sdk-etl).

    ![View Code](/img/guides/cloud_ide_code_view.png)

2. Click **Download** to download the DAG file.

## Step 11: Connect your GitHub to the Astro Cloud IDE

Now that you have trained the model, you can connect GitHub to the Astro Cloud IDE to commit your pipeline as a DAG to any Airflow project.

1. Click **Configure** to connect your Astro Cloud IDE Project to your GitHub account.

    ![Connect to GitHub](/img/guides/cloud_ide_github_conn.png)

2. Enter your personal access token and the name of an existing GitHub repository that contains an Astro project. 

3. Click **Update** to save your connection details.

## Step 12: Commit your DAG to GitHub

Export your pipeline by committing it to your connected GitHub repository. 

1. Click the branch you want to commit to (in the screenshot below the `cloud-ide-branch`) and provide a commit message. Note that you cannot commit to a branch called `main`. 

    ![Connect to GitHub](/img/guides/cloud_ide_commit_to_github.png)

  :::caution

  If a file with the same name as your Astro Cloud IDE pipeline already exists in your GitHub repository, the Astro Cloud IDE will overwrite the existing file. For this reason, Astronomer recommends using a separate branch for commits from your Astro Cloud IDE environment than for commits from other sources to the same repository.

  :::

2. Scroll through the list of changes and make sure that only changes are checked that you want to commit. The Astro Cloud IDE will offer to commit versions of Astro project configuration files, as well as a GitHub workflow. Note that all pipeline changes in a given Astro Cloud IDE project will be listed to be selected for the commit, not only the changes to the pipeline you are currently editing.

    Your DAG will be added to the `/dags` folder in your GitHub repository.

    ![Dags folder on GitHub](/img/guides/cloud_ide_dags_github.png)

3. Create a pull request in GitHub from your dedicated Astro Cloud IDE branch to your development branch and merge the changes you want to add to your Astro Cloud environment.

## Step 13: Deploy your DAG to Astro 

When you first commit an Astro Cloud IDE pipeline to a GitHub repository, the Astro Cloud IDE will create a GitHub workflow named `astro_deploy.yaml`. This action can be modified to fit your CI/CD workflow, or used out of the box after you configure a few environment variables. 

1. Set the following [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in your repository:

    - DEV_ASTRONOMER_KEY_ID = `<your-dev-key-id>`
    - DEV_ASTRONOMER_KEY_SECRET = `<your-dev-key-secret>`
    - DEV_ASTRONOMER_DEPLOYMENT_ID = `<your-deployment-id>`

    ![GitHub Secrets](/img/guides/cloud_ide_github_secrets.png)

    Depending on the version of the Astro CLI you are using you might need to adjust the GitHub workflow using the [configuration detailed in the Astro documentation](https://docs.astronomer.io/astro/ci-cd?tab=multibranch#github-actions).

2. Add the `scikit-learn` package to `requirements.txt` and commit the change. This second commit will trigger GitHub Actions again, using the GitHub secrets you configured. If your `requirements.txt` file already contains the `scikit-learn` package, make a different commit.

If GitHub Actions is already configured for your chosen branch and repository the new DAG will be deployed automatically with the first commit.

Learn more on how to set up CI/CD with GitHub Actions in the [Astro Module: CI/CD](https://academy.astronomer.io/astro-module-cicd).

## Step 14: Run your DAG on Astro

1. In the Cloud UI, open your Deployment. 

2. Click **Open Airflow**

3. In the Airflow UI, configure a connection with the same values as your connection in the Astro Cloud IDE. See [Manage connections in Apache Airflow](connections.md).

4. Since temporary tables are not JSON serializable, you need to enable XCom pickling which is on by default in the Astro Cloud IDE. Go to the Astro Cloud UI and click on your deployment. Select **Variables** and click on **Edit Variables** to add a new variable with a key of `AIRFLOW__CORE__ENABLE_XCOM_PICKLING` and a value of `True`. Click **Save Variables**.

    ![Add Variable in Airflow UI](/img/guides/cloud_ide_add_variable.png)

5. Go to **DAGs** and run your DAG by clicking the play button.

    ![Run DAG on Astro](/img/guides/cloud_ide_dag_ran_in_UI.png)

## Conclusion

You now know how to use the Astro Cloud IDE to write a simple ML pipeline! More specifically, you can now:

- Create a new Astro Cloud IDE project and pipeline. 
- Use a SQL cell to query and transform tables in a database.
- Pass information between SQL and Python cells.
- Run a simple `RandomForestClassifier` on a dataset.
- Commit your pipeline to GitHub.
- Use GitHub Actions to deploy your new DAG to Astro.

See the [Astro Cloud IDE documentation](https://docs.astronomer.io/astro/cloud-ide) to learn more about this next-generation DAG writing environment.
