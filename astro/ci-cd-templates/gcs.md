---
sidebar_label: GCS bucket
title: Deploy DAGs from Google Cloud Storage to Astro
id: gcs
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using Google Cloud Storage.
---

## Prerequisites

- A Google cloud storage (GCS) bucket.
- An [Astro Deployment](create-deployment.md) with [DAG-only deploys enabled](deploy-code.md#enable-dag-only-deploys-on-a-deployment).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- An [Astro project](create-first-dag.md) containing your project configurations.

## DAG-based deploy

This CI/CD template can be used to deploy DAGs from a single GCS bucket to a single Astro Deployment. When you create or modify a DAG in the GCS bucket, a Cloud function triggers and initialises an `astro` project to deploy your DAGs using Astro CLI.

:::info

To deploy any non-DAG code changes to Astro, you need to trigger a standard image-only deploy with your Astro project. When you do this, your Astro project must include the latest version of your DAGs from your GCS bucket. If your Astro project `dags` folder isn't up to date with your GCS DAGs bucket when you trigger this deploy, you will revert your DAGs back to the version hosted in your Astro project.

:::

1. Download the latest Astro CLI binary from [GitHub releases](https://github.com/astronomer/astro-cli/releases), then rename the file to, `astro_cli.tar.gz`. For example, to use Astro CLI version 1.13.0 in your template, download `astro_1.13.0_linux_amd64.tar.gz` and rename it to `astro_cli.tar.gz`.
2. In your GCS bucket, create the following new folders:

    - `dags`
    - `cli_binary`

3. Add `astro_cli.tar.gz` to `cli_binary`.
4. Create a [1st gen Cloud Function](https://cloud.google.com/functions/docs/console-quickstart-1st-gen#create_a_function) with the Python 3.9 Runtime in the same region as your storage bucket.
5. Create a [Cloud Storage trigger](https://cloud.google.com/functions/docs/calling/storage) with the following configuration: 

    - **Event provider**: Select **Cloud Storage**.
    - **Event**: Select **On finalizing/creating file in the selected bucket**.
    - **Bucket**: Select your storage bucket.

6. Choose the Runtime Service Account. Ensure that the service account has `storage.objects.list` access to the Google Cloud Storage bucket.

7. Set the following [environment variables](https://cloud.google.com/functions/docs/configuring/env-var#setting_runtime_environment_variables) for your Cloud Function:

    - `ASTRO_HOME` = `\tmp`
    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRO_DEPLOYMENT_ID`: Your Deployment ID.

    For production Deployments, ensure that you store the value for your API token in a secrets backend. See [Secret Manager overview](https://cloud.google.com/secret-manager/docs/overview).

8. Add the dependency `google-cloud-storage` to the `requirements.txt` file for your Cloud Function. See [Specifying Dependencies in Python](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python).

9. Add the following code to `main.py`:

    ```python
    import os
    import tarfile
    import subprocess
    from pathlib import Path
    from google.cloud import storage
    BUCKET = os.environ.get("BUCKET", "my-demo-bucket")
    deploymentId = os.environ.get("ASTRO_DEPLOYMENT_ID", "missing-deployment-id")

    def untar(filename: str, destination: str) -> None:
        with tarfile.open(filename) as file:
            file.extractall(destination)
    
    def run_command(cmd: str) -> None:
        p = subprocess.Popen("set -x; " + cmd, shell=True)
        p.communicate()

    def download_to_local(bucket_name: str, gcs_folder: str, local_dir: str = None) -> None:
        """Download the contents of a folder directory
        :param bucket_name: the name of the gcs bucket
        :param gcs_folder: the folder path in the gcs bucket
        :param local_dir: a relative or absolute directory path in the local file system
        """

        ## create a storage client to access GCS objects
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(bucket_name)

        ## get a list of all the files in the bucket folder
        blobs = source_bucket.list_blobs(prefix=gcs_folder)

        ## download each of the dag to local
        for blob in blobs:
            if blob.name.endswith('/'):
                continue

        target = blob.name if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(blob.name, gcs_folder))
        print(target)
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))

        blob.download_to_filename(target)
        print("downloaded file")
    
    def astro_deploy(event, context) -> None:
        """Triggered by a change to a Cloud Storage bucket.
        :param event: Event payload.
        :param context: Metadata for the event.
        """

        base_dir = '/tmp/astro'
        ## download dag files to temp local storage
        download_to_local(BUCKET, 'dags', f'{base_dir}/dags')
    
        ## download astro cli binary and move to /tmp/astro
        download_to_local(BUCKET, 'cli_binary', base_dir)

        ## deploy to astro
        os.chdir(base_dir)
        untar('./astro_cli.tar.gz', '.')
        run_command('echo y | ./astro dev init')
        run_command(f'./astro deploy {deploymentId} --dags')
    ```

10. If you haven't already, deploy your complete Astro project to your Deployment. See [Deploy code](deploy-code.md).
11. Add your DAGs to the `dags` folder in your storage bucket.
12. In the Cloud UI, select a Workspace, click **Deployments**, and then select your Deployment. Confirm that your deploy worked by checking the Deployment **DAG bundle version**. The version's name should include the time that you added the DAGs to your GCS bucket. 
