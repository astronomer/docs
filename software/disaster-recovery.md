---
sidebar_label: 'Disaster recovery'
title: 'Astronomer Software disaster recovery'
id: disaster-recovery
description: A guide to platform backups and disaster recovery for Astronomer Software.
---

All applications are vulnerable to service-interrupting events - a network outage, a team member accidentally deleting a namespace, a critical bug introduced by your latest application push or even a natural disaster. All are rare and undesirable events that modern teams running enterprise-grade software need to protect against. At Astronomer, we encourage all customers to have a robust, targeted, and well-tested DR (Disaster Recovery) plan.

The doc below will provide guidelines for how to:

*   Backup the Astronomer Platform
*   Restore the Astronomer Platform in case of an incident

At Astronomer, we strongly recommend [Velero](https://velero.io/) for both backup and restore operations. Velero is an open source tool acquired by VMWare that is built for Kubernetes backups and migrations.

### Why Velero

Unlike other tools that directly access the [Kubernetes etcd database](https://kubernetes.io/docs/concepts/overview/components/#etcd) to perform backups and restores, Velero uses the Kubernetes API to capture the state of cluster resources and to restore them when necessary. This API-driven approach has a number of key benefits:

*   Backups can capture subsets of the cluster’s resources, filtering by namespace, resource type, and/or label selector, providing a high degree of flexibility around what’s backed up and restored.
*   Users of managed Kubernetes offerings often do not have access to the underlying etcd database, so direct backups/restores of it are not possible.
*   Resources exposed through aggregated API servers can easily be backed up and restored even if they’re stored in a separate etcd database.

## Backup

To recover the Astronomer platform in the case of an incident, back up the following resources in order of priority:

- The Kubernetes cluster state and Astronomer Postgres database.
- ElasticSearch, Prometheus, and Alertmanager persistent volume claims (PVCs).

You should never back up Redis PVCs. Restoring Redis can result in conflicting Airflow and Celery task state information.

Read below for specific instructions for how to backup these components.

### Kubernetes cluster backup

With Velero, you can back up or restore all objects in your cluster, or you can filter objects by type, namespace, and/or label. There are two types of backups:

1. On-Demand
2. Scheduled

Generally speaking, the backup operation does the following:

*   Uploads a tarball of copied Kubernetes objects into cloud object storage.
*   Calls the cloud provider API to make disk snapshots of persistent volumes, if specified.

We’ll cover both on-demand and scheduled backups below. For more information, see [How Velero Works](https://velero.io/docs/main/how-velero-works/)

#### Prerequisites

The following instructions assume you have:

* Velero installed in your cluster
* The Velero CLI
* `kubectl` access to your cluster

If you do not have Velero or the Velero CLI installed, see [How Velero Works](https://velero.io/docs/main/how-velero-works/).

#### On-demand backup

If you need to create a backup on demand, run the following in the Velero CLI:

```
velero backup create <BACKUP NAME>
```

By default, the command above makes disk snapshots of any persistent volumes. You can adjust the snapshots by specifying additional flags. To see available flags, run:

```
velero backup create --help
```

Snapshots can be disabled with the option `--snapshot-volumes=false.`

#### Scheduled backup

Production environments should have scheduled backups enabled. The frequency of this backup depends on your needs and constraints.

We recommend that you start with at least daily backups and adjust the frequency from there as needed. To schedule a backup for a specific time, run:

```
velero schedule create <SCHEDULE NAME> --schedule "0 1 * * *"
```

The command above will schedule a daily backup of the entire cluster at 1am UTC. Velero uses standard Unix cron syntax to specify the schedule frequency and occurrence.

### Database backup

You can use one of the following methods to backup the Astronomer database:

- Enable automatic backups with your cloud provider (Preferred)
- Use traditional backup tools such as [pg_dump](https://www.postgresql.org/docs/12/app-pgdump.html) for Postgresql

#### Enable automatic backups with your cloud provider

The easiest and most reliable way to ensure the database is backed up  is to enable automatic backups with your cloud provider. This will create daily backups of your Astronomer Postgresql database.

Refer to the following links to Cloud Provider documentation for creating Postgres Database Backups:

*   AWS: [Database backup and restore in AWS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
*   GCP: [Create automatic backups in GCP](https://cloud.google.com/sql/docs/postgres/backup-recovery/backing-up)
*   Azure: [Azure Postgres backup and restore](https://docs.microsoft.com/en-us/azure/postgresql/concepts-backup)

Similar to Velero, one-off snapshots can also be created that will represent the database at that specific time, rather than at the normal scheduled intervals.

#### Traditional backup tool (`pg_dump`):

To run `pg_dump` successfully, someone with “read” access to the Astronomer Database will need to collect the following (stored as a Kubernetes Secret):

*   Database connection string
*   Username
*   Password

Run the following command to return the connection string with the username and password:

```
kubectl -n astronomer get secret  astronomer-houston-backend -o jsonpath='{.data.connection}' | base64 -d
```

## Restore

In the case of an incident, you’re always free to restore either:

*   A single Airflow Deployment
*   The Whole Platform (all Airflow Deployments)

The guidelines below will cover both, including specifics for restoring both deleted and non-deleted Airflow Deployments.

### Single Deployment

The steps below are valid for the Astronomer Platform on Helm3 (Astronomer v0.14+).

#### Non-deleted Airflow Deployment

To restore a previous version of a deployment that has not been deleted in the Astronomer Software UI (or CLI/API) and that has been backed up with Velero, follow the steps below.

1. Identify the Velero backup you intend to use by running:

    ```
    velero backup get
    ```

2. Identify the Kubernetes namespace in question, which corresponds to your Airflow Deployment’s “release name” and has your platform’s namespace (typically “astronomer”) prepended to the front.

    For example, the namespace for an Airflow Deployment with the release name `weightless-meteor-5042` would be `astronomer-weightless-meteor-5042`.

3. Run:

    ```
    velero restore create --from-backup <BACKUP NAME> --include-namespaces <NAMESPACE NAME>
    ```

#### Deleted Airflow Deployment

To restore a single Airflow Deployment that _was_ deleted in the Astronomer Software UI (or CLI/API), perform the previous steps to restore its Velero namespace.

Once that is complete, the Astronomer Database needs to be updated to mark that release as not deleted. Follow the steps below.

1. Grab your database connection string (stored as a Kubernetes secret)

    ```
    kubectl -n astronomer get secret  astronomer-houston-backend -o jsonpath='{.data.connection}' | base64 -D
    ```

2. To connect to the database, launch a container into your cluster with the Postgres client:

    ```
    kubectl run pgclient -ti --image=postgres --restart=Never --image-pull-policy=Always -- bash
    ```

3. Then run the following command to connect to the database:

    ```
    psql <YOUR CONNECTION STRING>
    ```

    Example:

    ```
    psql postgres://airflow:XXXXXXX@database1.cloud.com:5432/astronomer_houston
    ```

4. Update the record for the deployment you wish to restore.

    ```
    UPDATE houston$default."Deployment" SET "deletedAt" = NULL WHERE "releaseName" = '<YOUR RELEASE NAME>';
    ```

Following these steps, the restored Airflow Deployment should render in the Software UI with its corresponding Workspace. All associated pods should be running in the cluster.

### Whole platform

In case your team ever needs to migrate to new infrastructure or your existing infrastructure is no longer accessible and you need to restore the Astronomer Platform in its entirety, including all Airflow Deployments within it, follow the steps below.

1. Create a new Kubernetes cluster _without_ Astronomer installed
2. Install Velero into the new cluster, ensuring that it can reach the previous backups in their storage location (e.g. S3 storage or GCS Bucket)
3. Set the Velero backup storage location to `readonly` to prevent accidentally overwriting any backups by running:

```
    kubectl patch backupstoragelocation <STORAGE LOCATION NAME> \
    --namespace velero \
    --type merge \
    --patch '{"spec":{"accessMode":"ReadOnly"}}'
```

From here,

1. Restore database snapshots to a new Postgres database or create a new database and restore from `pg_dump` backups.
2. Perform velero full cluster restore by running:

    ```
    velero restore create --from-backup <BACKUP NAME>
    ```

3. If the database endpoint has changed (e.g. it has a new hostname), it needs to be provided to the platform.

    * **AWS** - Update the `astronomer-bootstrap` secret to have the new connection string. Then the pods in the astronomer namespace will need to be restarted to pick up this change. The `pgbouncer-config `secret in each release namespace will also need to be updated with the new endpoint in the connection string.
    * **GCP**  - The `pg-sqlproxy-gcloud-sqlproxy `deployment needs to be updated to put the new database instance name in the `instances` argument passed to the container
