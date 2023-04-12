---
title: "Manage your ML models with Weights and Biases and Airflow"
sidebar_label: "Weights and Biases"
description: "Learn how to use Airflow and Weights and Biases to manage and visualize your ML model lifecycle."
id: airflow-weights-and-biases
---

import CodeBlock from '@theme/CodeBlock';
import weights_and_biases from '!!raw-loader!../code-samples/dags/airflow-weights-and-biases/weights_and_biases.py';

[Weights and Biases](https://wandb.ai/site) (W&B) is a machine learning platform for model management that includes features like experiment tracking, dataset versioning, and model performance evaluation and visualization. Using W&B with Airflow gives you a powerful ML orchestration stack with first-class features for building, training, and managing your models.

In this tutorial, you'll learn how to create an Airflow DAG that completes feature engineering, model training, and predictions with the Astro Python SDK and scikit-learn, and registers the model with W&B for evaluation and visualization.

:::note

This tutorial was developed in partnership with Weights and Biases. For a more complex example integration that includes dbt for data transformations, check out ADD LINK TO OTHER POSTS/TUTORIALS HERE.

:::

## Time to complete

This tutorial takes approximately one hour to complete.

## Assumed knowledge

To get the most out of this tutorial, you should be familiar with:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- The Astro Python SDK. See [Write a DAG with the Astro Python SDK](astro-python-sdk.md)
- Weights and Biases. See [What is Weights and Biases?](https://docs.wandb.ai/?_gl=1*i7pmr7*_ga*MTI3ODk4OTUzNy4xNjc5Njc2MzE5*_ga_JH1SJHJQXJ*MTY4MTI0ODQ2OS42LjEuMTY4MTI0ODUxMS4xOC4wLjA.).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A [Weights and Biases](https://wandb.ai/site) account. Personal accounts are available for free.
- A Snowflake Enterprise account. If you don't already have an account, Snowflake has a [free Snowflake trial](https://signup.snowflake.com/) for 30 days. 

## Step 1: Configure your Astro project

Use the Astro CLI to create and run an Airflow project locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-wandb-tutorial && cd astro-wandb-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    astro-sdk-python[snowflake]==1.5.3
    wandb==0.14.0
    pandas==1.5.3
    numpy==1.24.2
    scikit-learn==1.2.2
    ```

    This installs the packages needed to transform the data and complete feature engineering, model training and predictions.

## Step 2: Prepare the data

This tutorial will create a model that predicts....[ADD MORE HERE ON WHAT THE MODEL ACTUALLY DOES/WHAT THE DATA IS]

1. Create a folder called `data` in your `include` directory.
2. Download the CSV files from [this GitHub directory](https://github.com/astronomer/airflow-wandb-demo/tree/simple/include/data).
3. Save the downloaded CSV files in the `include/data` folder. You should have 8 total files.

## Step 3: Create your SQL transformation scripts

Before feature engineering and training, the data needs to be transformed. This tutorial uses the Astro Python SDK `transform_file` function to complete several transformations using SQL.

1. Create a file in your `include` directory called `customer_churn_month.sql` and copy the following code into the file.

    ```sql
    with subscription_periods as (
        select subscription_id, 
            customer_id, 
            cast(start_date as date) as start_date, 
            cast(end_date as date) as end_date, 
            monthly_amount 
            from {{subscription_periods}}
    ),
    months as (
        select cast(date_month as date) as date_month from {{util_months}}
    ),
    customers as (
        select
            customer_id,
            date_trunc('month', min(start_date)) as date_month_start,
            date_trunc('month', max(end_date)) as date_month_end
        from subscription_periods
        group by 1
    ),
    customer_months as (
        select
            customers.customer_id,
            months.date_month
        from customers
        inner join months
            on  months.date_month >= customers.date_month_start
            and months.date_month < customers.date_month_end
    ),
    joined as (
        select
            customer_months.date_month,
            customer_months.customer_id,
            coalesce(subscription_periods.monthly_amount, 0) as mrr
        from customer_months
        left join subscription_periods
            on customer_months.customer_id = subscription_periods.customer_id
            and customer_months.date_month >= subscription_periods.start_date
            and (customer_months.date_month < subscription_periods.end_date
                    or subscription_periods.end_date is null)
    ),
    customer_revenue_by_month as (
        select
            date_month,
            customer_id,
            mrr,
            mrr > 0 as is_active,
            min(case when mrr > 0 then date_month end) over (
                partition by customer_id
            ) as first_active_month,

            max(case when mrr > 0 then date_month end) over (
                partition by customer_id
            ) as last_active_month,

            case
            when min(case when mrr > 0 then date_month end) over (
                partition by customer_id
            ) = date_month then true
            else false end as is_first_month,
            case
            when max(case when mrr > 0 then date_month end) over (
                partition by customer_id
            ) = date_month then true
            else false end as is_last_month
        from joined
    ),
    joined1 as (
        select
            date_month + interval '1 month' as date_month,
            customer_id,
            0::float as mrr,
            false as is_active,
            first_active_month,
            last_active_month,
            false as is_first_month,
            false as is_last_month
        from customer_revenue_by_month
        where is_last_month
    )
    select * from joined1;
    ```

2. Create another file in your `include` directory called `customers.sql` and copy the following code into the file.

    ```sql
    with
    customers as (
        select *
        from {{customers_table}}
    ),
    orders as (
        select *
        from {{orders_table}}
    ),
    payments as (
        select *
        from {{payments_table}}
    ),
    customer_orders as (
        select
        customer_id,
        cast(min(order_date) as date) as first_order,
        cast(max(order_date) as date) as most_recent_order,
        count(order_id) as number_of_orders
        from orders
        group by customer_id
    ),
    customer_payments as (
        select
        orders.customer_id,
        sum(amount / 100) as total_amount
        from payments
        left join orders on payments.order_id = orders.order_id
        group by orders.customer_id
    ),
    final as (
        select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order,
        customer_orders.most_recent_order,
        customer_orders.number_of_orders,
        customer_payments.total_amount as customer_lifetime_value
        from customers
        left join customer_orders on customers.customer_id = customer_orders.customer_id
        left join customer_payments on customers.customer_id = customer_payments.customer_id
    )

    select
    *
    from final
    ```

## Step 4: Create a W&B API Key

## Step 5: Set up your connections

## Step 6: Create your DAG

2. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 7: Run your DAG and view results
