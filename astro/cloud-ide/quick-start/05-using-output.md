---
sidebar_label: Using cell outputs
title: Using cell outputs
id: using-cell-outputs
---

import Image from '@site/src/components/Image';

The Cloud IDE makes it very easy to share data between cells. SQL cells return their output if the `Create Table` checkbox is selected in the bottom right corner of the cell. Python cells must explicitly return their output. To do so, simply add a `return` statement in the cell. See below for some examples.

### Python Return Examples

```python
return 'Hello, world!'
```

```python
return 42
```

```python
return [1, 2, 3]
```

```python
return {'a': 1, 'b': 2}
```

### SQL Return Examples

```sql
SELECT * FROM my_table
```

```sql
SELECT col_a, col_b FROM my_table LIMIT 10
```

```sql
SELECT a.col_a, b.col_b
FROM my_table_a a
JOIN my_table_b b
ON a.id = b.id
```

## Using output in Python

In Python cells, you can use the output of other cells by referencing the cell name. For example, if you have a cell named `my_table`, you can use the output of that cell in a Python cell by referencing it as `my_table`. This works for referencing both SQL and Python cells. For example:

```python
df = my_table # my_table is a SQL cell and gets converted to a pandas dataframe by default
df['col_a'] = df['col_a'] + 1
return df
```

## Using output in SQL

In SQL cells, you can use the output of other cells by referencing the cell name using Jinja templating (surrounding the cell name with double brackets). For example, if you have a cell named `my_table`, you can use the output of that cell in a SQL cell by referencing it as `{{my_table}}`. This works for referencing both SQL and Python cells. For example:

:::info

Python cells must return a pandas DataFrame in order to be used in SQL cells.

:::

```sql
select * from {{my_table}} -- my_table is another SQL cell
```

```sql
select * from {{my_dataframe}} -- my_dataframe is a Python cell
where col_a > 10
```

Feel free to keep adding more cells to complete your pipeline!
