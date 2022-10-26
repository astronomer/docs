---
sidebar_label: Connecting to a database
title: Connecting to a database
id: connecting-to-a-database
---

Now that you've created a Python cell, let's connect to a database and run some SQL against it using the SQL cell.

## Setting up your connection

You can create a connection to your database from two locations: either the project page, under the **Connections** tab, or the environment sidebar in the pipeline editor.

From either location, click the **Create Connection** button. You'll see a modal appear asking you to select a connection type.

![Select Connection Type](/img/cloud-ide/select-connection-type.png)

Once you select a connection type, you'll be prompted for the connection details. For example, if you select **Postgres**, you'll be prompted for the host, port, username, password, and database name.

![Configure Connection](/img/cloud-ide/configure-connection.png)

## Test your connection

Once you've filled out the connection details, you can optionally test your connection details before creating it. To do so, click the **Test Connection** button. If the connection is successful, you'll see a message letting you know. If the connection fails, you'll see an error message. Note that not all connection types can be tested. If your connection type doesn't support testing, you'll see a message letting you know.

Regardless of whether the test connection succeeds or fails, you can still create the connection.

![Test Connection Success](/img/cloud-ide/test-connection-success.png)
![Test Connection Fail](/img/cloud-ide/test-connection-fail.png)

## Writing SQL

Now that you've created a connection, you can write some SQL. To do so, click on the **Create Cell** button in the top left corner of the screen. You'll be presented with a list of cell types to choose from. Choose **SQL**.

:::tip

You can also quick add a SQL cell with a given connection by clicking on the **+** button from the connection in the environment sidebar.

![Connection Quick Add](/img/cloud-ide/connection-quick-add.png)

:::

You'll be presented with a SQL cell with a default name and some boilerplate code. You can write any SQL code in this cell. For example, you can write a simple hello world query:

```sql
select 1 as hello_world;
```

After you write your query, make sure to select a connection from the connection dropdown in the top right of the cell. You can also change the name of the cell by clicking on the cell name in the top left corner of the cell.

Once you've written your SQL and selected a connection, you can run the cell by clicking on the **Run** button in the top right corner of the cell. While it's running, you should see logs streaming in from the **Logs** tab on the bottom left of the cell. When the cell is finished executing, you should see your results in the **Output** tab on the bottom of the cell.
