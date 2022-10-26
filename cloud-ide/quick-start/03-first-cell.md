---
sidebar_label: Your first cell
title: Your first cell
id: first-cell
---

You're now ready to write your first cell. In this section, you'll write a simple _hello world_ cell. To begin, click on the **Create Cell** button in the top left corner of the screen. You'll be presented with a list of cell types to choose from.

![Create Cell](/img/cloud-ide/create-cell.png)

Select **Python**. You should see a Python cell that's been created for you with a default name and some boilerplate code.

![Python Cell](/img/cloud-ide/empty-python-cell.png)

You can write any Python code in this cell. For example, you can write a function that returns a simple string:

```python
return "Hello, world!"
```

Changes to the cell are autosaved. You can edit the name by clicking on the cell name in the top left corner of the cell.

To run this cell, click on the **Run** button in the top right corner of the cell. While it's running, you should see logs streaming in from the **Logs** tab on the bottom left of the cell.

![Python Cell Logs](/img/cloud-ide/python-cell-logs.png)

Once the cell is finished running, you should see the output in the **Output** tab on the bottom of the cell. You should see the string that you returned.

![Python Cell Output](/img/cloud-ide/python-hello-world.png)

Next, let's set up a connection to your database and run some SQL against it.
