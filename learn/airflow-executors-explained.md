---
title: "Airflow Executors"
sidebar_label: "Executor"
description: "An introduction to the Apache Airflow Executors: Celery, Local, and Kubernetes."
id: airflow-executors-explained
---

If you're new to Apache Airflow, the world of Executors is difficult to navigate. Even if you're a veteran user overseeing 20 or more DAGs, knowing what Executor best suits your use case at any given time isn't always easy - especially as the OSS project (and its utilities) continues to grow and develop.

This guide will help you:

- Understand the core function of an executor
- Contextualize Executors with general Airflow fundamentals
- Understand the purpose of the three most popular Executors: Local, Celery, and Kubernetes

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## What is an executor?

After a DAG is defined, the following needs to happen in order for the tasks within that DAG to execute and be completed:

- The [Metadata Database](airflow-database.md) keeps a record of all tasks within a DAG and their corresponding status (`queued`, `scheduled`, `running`, `success`, `failed`, and so on) behind the scenes.

- The scheduler reads from the metadata database to check on the status of each task and decide what needs to get done and when.

- The executor works closely with the scheduler to determine what resources will actually complete those tasks (using a worker process or otherwise) as they're queued.

The difference between Executors comes down to the resources they have at hand and how they choose to utilize those resources to distribute work (or not distribute it at all).

## Related definitions

When you're learning about task execution, you'll want to be familiar with these [somewhat confusing](https://issues.apache.org/jira/browse/AIRFLOW-57) terms, all of which are called "environment variables." The terms themselves have changed a bit over Airflow versions, but this list is compatible with 1.10+.

- Environment variables: A set of configurable values that allow you to dynamically fine tune your Airflow deployment. They're defined in your `airflow.cfg` (or directly through the Astro Cloud UI) and include everything from [email alerts](https://docs.astronomer.io/software/airflow-alerts) to DAG concurrency (see the following).

- Parallelism: Determines how many task instances can be _actively_ running in parallel across DAGs given the resources available at any given time at the deployment level. Think of this as "maximum active tasks anywhere." `ENV AIRFLOW__CORE__PARALLELISM=18`

- `dag_concurrency`: Determines how many task instances your scheduler is able to schedule at once _per DAG_. Think of this as "maximum tasks that can be scheduled at once, per DAG." You might see: `ENV AIRFLOW__CORE__DAG_CONCURRENCY=16`

- `worker_concurrency`: Determines how many tasks each worker can run at any given time. The CeleryExecutor for example, will [by default](https://github.com/apache/airflow/blob/main/airflow/config_templates/default_airflow.cfg#L723) run a max of 16 tasks concurrently. Think of it as "How many tasks each of my workers can take on at any given time." This number will naturally be limited by `dag_concurrency`. If you have 1 worker and want it to match your deployment's capacity, worker\_concurrency = parallelism. `ENV AIRFLOW__CELERY__WORKER_CONCURRENCY=9`

:::tip

Parallelism and concurrency are somewhat co-dependent. You're encouraged to keep them in line with one another.

:::

- Pool: Configurable in the Airflow UI and are used to limit the _parallelism_ on any particular set of tasks. You could use it to give some tasks priority over others, or to put a cap on execution for things like hitting a third party API that has rate limits on it, for example.

- `parsing_processes`: Determines how many linear scheduling processes the scheduler can handle in parallel at any given time. The default value is 2, but adjusting this number gives you some control over CPU usage - the higher the value, the more resources you'll need.

:::info

In Airflow 1.10.13 and prior versions, this setting is called max_threads.

:::

:::tip

Rather than trying to find one set of configurations that work for _all_ jobs, Astronomer recommends grouping jobs by their type as much as you can.

:::

## Local executor

Running Apache Airflow on a Local executor exemplifies single-node architecture.

The Local executor completes tasks in parallel that run on a single machine (think: your laptop, an EC2 instance, etc.) - the same machine that houses the Scheduler and all code necessary to execute. A single LocalWorker picks up and runs jobs as they’re scheduled and is fully responsible for all task execution.

In practice, this means that you don't need resources outside of that machine to run a DAG or a set of DAGs (even heavy workloads). For example, you might hear: "Our organization is running the Local executor for development on a t3.xlarge AWS EC2 instance."

### Pros

- It's straightforward and easy to set up.
- It's cheap and resource light.
- It still offers parallelism.

### Cons

- It's less scalable.
- It's dependent on a single point of failure.

### When you should use it

The Local executor is ideal for testing.

The obvious risk is that if something happens to your machine, your tasks will see a standstill until that machine is back up.

Heavy Airflow users whose DAGs run in production will find themselves migrating from Local executor to Celery executor after some time, but you'll find plenty of use cases out there written by folks that run quite a bit on Local executor before making the switch. How much that executor can handle fully depends on your machine's resources and configuration. Until all resources on the server are used, the Local executor actually scales up quite well.

## Celery executor

At its core, the Celery executor is built for horizontal scaling.

[Celery](https://docs.celeryproject.org/en/stable/) itself is a way of running python processes in a distributed fashion. To optimize for flexibility and availability, the Celery executor works with a "pool" of independent workers and uses messages to delegate tasks. On Celery, your deployment's scheduler adds a message to the queue and the Celery broker delivers it to a Celery worker (perhaps one of many) to execute.

If a worker node is ever down or goes offline, the Celery executor quickly adapts and is able to assign that allocated task or tasks to another worker.

If you're running native Airflow, adopting a Celery executor means you'll have to set up an underlying database to support it (RabbitMQ/Redis).

:::info

When running Celery on top of a managed Kubernetes service, if a node that contains a Celery worker goes down, Kubernetes will reschedule the work. When the pod comes back up, it'll reconnect to [Redis](https://redis.io/) and continue processing tasks.

:::

### Worker termination grace period

An Airflow deployment on Astronomer Software running with Celery workers has a setting called **Worker Termination Grace Period** that helps minimize task disruption upon deployment by continuing to run tasks for a number of minutes after you push up a deploy.

Conversely, when using the Local executor, tasks start immediately upon deployment regardless of whether or not tasks were mid-execution, which could be disruptive.

### Pros

- High availability
- Built for horizontal scaling
- Worker Termination Grace Period

### Cons

- It's pricier
- It takes some work to set up
- Worker maintenance

### When you should use it

Astronomer recommends using the Celery executor for running DAGs in production, especially if you're running anything that's time sensitive.

## Kubernetes executor

The Kubernetes executor leverages the power of [Kubernetes](https://kubernetes.io/) for resource optimization.

The Kubernetes executor relies on a fixed single Pod that dynamically delegates work and resources. For each and every task that needs to run, the executor talks to the Kubernetes API to dynamically launch Pods which terminate when that task is completed.

This means a few things:

- In times of high traffic, you can scale up.
- In times of low traffic, you can scale to zero.
- For each individual task, you can configure the following:
    - Memory allocation
    - Service accounts
    - Airflow image

#### Scale to near-zero

With the Local and Celery executors, a deployment whose DAGs run once a day will operate with a fixed set of resources for the full 24 hours - only 1 hour of which actually puts those resources to use. That's 23 hours of resources you're paying for but don't deliver.

With the Kubernetes executor, your webserver and scheduler costs remain fixed, but the dynamic scaling of the actual Pods allow you to shed the fixed cost of having a Celery worker up for 24 hours a day.

### Less work for your scheduler

On the Local and Celery executors, the scheduler is charged with constantly having to check the status of each task at all times from the Postgres backend - "Is it running? Queued? Failed?"

With the Kubernetes executor, the workers (Pods) talk directly to the _same_ Postgres backend as the scheduler and can take on the labor of task monitoring. In this architecture, a task failure is handled by its individual Pod. The scheduler is only responsible for keeping an eye on the Pods themselves and taking action if one or more of them fail.

Using the Kubernetes "Watcher" API, the scheduler reads event logs for anything with a failed label tied to that Airflow instance. If a Pod fails, the scheduler alerts Postgres and bubbles that failure up to the user to trigger whatever alerting solution is set up on your deployment.

### Pros

- Cost and resource efficient
- Fault tolerant
- Task-level configurations
- No interruption to running tasks if a deploy is pushed

### Cons

- Kubernetes familiarity as a potential barrier to entry
- An overhead of a few extra seconds per task for a pod to spin up

### When you should use it

The Kubernetes executor offers extraordinary capabilities. If you're familiar with Kubernetes and want to give it a shot, Astronomer recommends doing so to be at the forefront of the modern Apache Airflow configuration.

:::tip

If you have a high quantity of tasks that are intended to finish executing particularly quickly, note the extra handful of seconds it takes for each individual Pod to spin up might slow those tasks down.

:::

## Honorable mention

**Sequential executor:** The Sequential executor runs a _single_ task instance at a time in a linear fashion with no parallelism functionality (A → B → C). It does identify a single point of failure, making it helpful for debugging. Otherwise, the Sequential executor is not recommended for any use cases that require more than a single task execution at a time.
