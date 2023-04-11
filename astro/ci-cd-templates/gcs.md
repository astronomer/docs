---
sidebar_label: GCS bucket
title: Deploy DAGs to from Google Cloud Storage to Astro
id: gcs
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using Google Cloud Storage.
---

### Prerequisites

- A Google cloud storage (GCS) bucket.
- An [Astro Deployment](create-deployment.md) with [DAG-only deploys enabled](deploy-code.md#enable-dag-only-deploys-on-a-deployment).
- A [Deployment API key ID and secret](api-keys.md).
- An [Astro project](create-first-dag.md) containing your project configurations.

### DAG-based deploy

This CI/CD template can be used to deploy DAGs from a single GCS bucket to a single Astro Deployment. When you create or modify a DAG in the GCS bucket, a Lambda function triggers to deploy your DAGs to Astro.

:::info

To deploy any non-DAG code changes to Astro, you need to trigger a standard image-only deploy with your Astro project. When you do this, your Astro project must include the latest version of your DAGs from your GCS bucket. If your Astro project `dags` folder isn't up to date with your GCS DAGs bucket when you trigger this deploy, you will revert your DAGs back to the version hosted in your Astro project.

:::

1. Download the latest Astro CLI binary from [GitHub releases](https://github.com/astronomer/astro-cli/releases), then rename the file to, `astro_cli.tar.gz`. For example, to use Astro CLI version 1.13.0 in your template, you would download `astro_1.13.0_linux_amd64.tar.gz` and rename it to `astro_cli.tar.gz`.
2. In your GCS bucket, create the following new folders:

    - `dags`
    - `cli_binary`

3. Add `astro_cli.tar.gz` to `cli_binary`.
4. Create a [1st gen Cloud Function](https://cloud.google.com/functions/docs/console-quickstart-1st-gen#create_a_function) with the Python 3.9 Runtime in the same region as your storage bucket.
5. Create a [Cloud Storage trigger](https://cloud.google.com/functions/docs/calling/storage) with the following configuration: 

    - **Event provider**: Select **Cloud Storage**.
    - **Event**: Select **On finalizing/creating file in the selected bucket**.
    - **Bucket**: Select your storage bucket.

6. Set the following [environment variables](https://cloud.google.com/functions/docs/configuring/env-var#setting_runtime_environment_variables) for your Cloud Function:

    - `ASTRO_HOME` = `\tmp`
    - `ASTRONOMER_KEY_ID` = `<your-deployment-api-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-deployment-api-key-secret>`

7. Add the dependency `google-cloud-storage` to the `requirements.txt` file for your Cloud Function. See [Specifying Dependencies in Python](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python).

8. Add the following code to `main.py`:

  ```python
  import os
  import tarfile
  import subprocess
  from google.cloud import storage
  def untar(filename):
      # open file
      file = tarfile.open(filename)
      # extracting file
      file.extractall('/tmp/astro/')
      file.close()
  def run_command(cmd):
      print("running command: ", cmd)
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      out, err = p.communicate()
      print(out)
      print(err)
      p.kill()
  def download_to_local(bucket_name, gcs_folder, local_dir=None):
      """
      Download the contents of a folder directory
      Args:
          bucket_name: the name of the gcs bucket
          gcs_folder: the folder path in the gcs bucket
          local_dir: a relative or absolute directory path in the local file system
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
      
  def astro_deploy(event, context):
      """Triggered by a change to a Cloud Storage bucket.
      Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
      """
      ## download dag files to temp local storage
      download_to_local('my-demo-bucket', 'dags', '/tmp/astro/dags')
      
      ## download astro cli binary and move to /tmp/astro
      download_to_local('my-demo-bucket', 'cli_binary', '/tmp/astro')
      untar('/tmp/astro/astro_cli.tar.gz')
      ## deploy to astro
      os.chdir('/tmp/astro')
      run_command('echo y | ./astro dev init')
      run_command('./astro deploy --dags')
  ```

9. If you haven't already, deploy your complete Astro project to your Deployment. See [Deploy code](deploy-code.md).
10. Add your DAGs to the `dags` folder in your storage bucket.
11. In the Cloud UI, select a Workspace, click **Deployments**, and then select your Deployment. Confirm that your deploy worked by checking the Deployment **DAG bundle version**. The version's name should include the time that you added the DAGs to your GCS bucket. 
