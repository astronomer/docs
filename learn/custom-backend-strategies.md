---
title: 'Strategies for custom XCom backends in Airflow'
sidebar_label: 'Custom XCom backends'
id: custom-backend-strategies
description: 'Use this guide to learn about different ways you can set up custom XCom backends.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow [XComs](airflow-passing-data-between-tasks.md) allow you to pass data between tasks. By default, Airflow uses the [metadata database](airflow-database.md) to store XComs, which works well for local development but has limited performance. If you configure a custom XCom backend, you can define where and how Airflow stores XComs, as well as customize serialization and deserialization methods.

In this guide you'll learn:

- When you should use a custom XCom backend.
- How to set up a custom XCom backend using the Object Storage Custom XCom Backend.
- How to use a custom XCom backend class with custom serialization and deserialization methods.
- How to override the `.clear()` method to delete XComs from a custom XCom backend when clearing tasks.

:::warning

While a custom XCom backend allows you to store virtually unlimited amounts of data as XComs, you will need to scale other Airflow components to pass large amounts of data between tasks. For help running Airflow at scale, [reach out to Astronomer](https://www.astronomer.io/try-astro/?referral=docs-content-link&utm_medium=docs&utm_content=learn-xcom-backend-tutorial&utm_source=body).

:::

## Assumed Knowledge

To get the most benefits from this guide, you need an understanding of:

- XCom basics. See [Pass data between tasks](airflow-passing-data-between-tasks.md).
- Basic knowledge of a cloud-based object storage service like [AWS S3](https://aws.amazon.com/s3/), [GCP Cloud Storage](https://cloud.google.com/storage) or [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/).

## Why use a custom XCom backend?

Common reasons to use a custom XCom backend include:

- You need more storage space for XComs than the Airflow metadata database can offer.
- You're running a production environment where you require custom retention, deletion, and backup policies for XComs.
- You want to access XComs without accessing the metadata database.
- You want to restrict types of allowed XCom values.
- You want to save XComs in multiple locations simultaneously.

You can also use custom XCom backends to define custom serialization and deserialization methods for XComs if you need to add a serialization method to a class, or if registering a custom serializer is not feasible. See [Custom serialization and deserialization](#custom-serialization-and-deserialization) for more information.

## How to set up a custom XCom backend

There are two main ways to set up a custom XCom backend:

- **Object Storage Custom XCom Backend**: Use this method to create a custom XCom backend when you want to store XComs in a cloud-based object storage service like AWS S3, GCP Cloud Storage, or Azure Blob Storage. This option is recommended when you need to store XComs in a single remote location and the Object Storage Custom XCom Backend threshold and compression options meet your requirements.
- **Custom XCom backend class**: Use this method when you want to further customize how XComs are stored, for example to simultaneously store XComs in two different locations.

Additionally, some provider packages offer custom XCom backends that you can use out of the box. For example, the [Snowpark provider](airflow-snowpark.md) contains a custom XCom backend for Snowflake.

### Use the Object Storage XCom Backend

Airflow 2.9+ added the possibility to create a custom XCom backend using object storage. The Object Storage XCom Backend is part of the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) provider and can be defined using the following environment variables:

- `AIRFLOW__CORE__XCOM_BACKEND`: The XCom backend to use. Set this to `airflow.providers.common.io.xcom.backend.XComObjectStoreBackend` to use the Object Storage Custom XCom Backend.
- `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH`: The path to the object storage where XComs are stored. The path should be in the format `<your-scheme>://<your-connection-id@<your-bucket>/xcom`. For example, `s3://my-s3-connection@my-bucket/xcom`. The most common schemes are `s3`, `gs`, and `abfs` for Amazon S3, Google Cloud Storage, and Azure Blob Storage, respectively.
- `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_THRESHOLD`: The threshold in bytes for XComs to be stored in the object storage. All objects smaller or equal to this threshold are stored in the metadata database. All objects larger than this threshold are stored in the object storage. The default value is `-1`, meaning all XComs are stored in the metadata database.
- `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_COMPRESSION`: Optional. The compression algorithm to use when storing XComs in the object storage, for example `zip`. The default value is `None`.

For a step-by-step tutorial on how to set up a custom XCom backend using the Object Storage Custom XCom Backend for Amazon S3, Google Cloud Storage and Azure Blob Storage, see the [Set up a custom XCom backend using object storage](custom-xcom-backends-tutorial.md).

:::caution

Object storage is currently experimental and might be subject to breaking changes in future releases. For more information see [AIP-58](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=263430565).

:::

### Use a custom XCom backend class

To create a custom XCom backend, you need to define an XCom backend class which inherits from the `BaseXCom` class.

The code below shows an example `MyCustomXComBackend` class that only allows JSON-serializeable XComs and stores them in both, Amazon S3 and Google Cloud Storage using a custom `serialize_value()` method. The `deserialize_value()` method retrieves the XComs from the Amazon S3 bucket and returns the value.

The Airflow metadata database stores a reference string to the XCom, which is displayed in the XCom tab of the Airflow UI. The reference string is prefixed with `s3_and_gs://` to indicate that the XCom is stored in both Amazon S3 and Google Cloud Storage. You can add any serialization and deserialization logic to the `serialize_value()` and `deserialize_value()` methods that you need, see [Custom serialization and deserialization](#custom-serialization-and-deserialization) for more information.

<details>
<summary>Click to view the full custom XCom backend class example code</summary>
<div>

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import json
import uuid
import os

class MyCustomXComBackend(BaseXCom):
    # the prefix is optional and used to make it easier to recognize
    # which reference strings in the Airflow metadata database
    # refer to an XCom that has been stored in remote storage
    PREFIX = "s3_and_gs://"
    S3_BUCKET_NAME = "s3-xcom-backend-example"
    GS_BUCKET_NAME = "gcs-xcom-backend-example"

    @staticmethod
    def serialize_value(
        value,
        key=None,
        task_id=None,
        dag_id=None,
        run_id=None,
        map_index=None,
        **kwargs,
    ):

        # make sure the value is JSON-serializable
        try:
            serialized_value = json.dumps(value)
        except TypeError as e:
            raise ValueError(f"XCom value is not JSON-serializable!: {e}")

        # instantiate a context with the value as a temporary JSON file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_file.write(serialized_value)
            tmp_file.flush()
            tmp_file_name = tmp_file.name

            # the connection to AWS is created by using the S3 hook
            hook = S3Hook(aws_conn_id="my_aws_conn_id")
            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename = "data_" + str(uuid.uuid4()) + ".json"
            # define the full S3 key where the file should be stored
            key = f"{dag_id}/{run_id}/{task_id}/{map_index}/{key}_{filename}"

            # load the local JSON file into the S3 bucket
            hook.load_file(
                filename=tmp_file_name,
                key=key,
                bucket_name=MyCustomXComBackend.S3_BUCKET_NAME,
                replace=True,
            )

            # the connection to GCS is created by using the GCS hook
            hook = GCSHook(gcp_conn_id="my_gcs_conn_id")

            if hook.exists(MyCustomXComBackend.GS_BUCKET_NAME, key):
                print(
                    f"File {key} already exists in the bucket {MyCustomXComBackend.GS_BUCKET_NAME}."
                )
            else:
                # load the local JSON file into the GCS bucket
                hook.upload(
                    filename=tmp_file_name,
                    object_name=key,
                    bucket_name=MyCustomXComBackend.GS_BUCKET_NAME,
                )

        # define the string that will be saved to the Airflow metadata
        # database to refer to this XCom
        reference_string = MyCustomXComBackend.PREFIX + key

        # use JSON serialization to write the reference string to the
        # Airflow metadata database (like a regular XCom)
        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        import logging

        reference_string = BaseXCom.deserialize_value(result=result)y
        hook = S3Hook(aws_conn_id="my_aws_conn")
        key = reference_string.replace(MyCustomXComBackend.PREFIX, "")

        # Use a temporary directory to download the file
        with tempfile.TemporaryDirectory() as tmp_dir:
            local_file_path = hook.download_file(
                key=key,
                bucket_name=MyCustomXComBackend.S3_BUCKET_NAME,
                local_path=tmp_dir,
            )

            # ensure the file is not empty and log its size
            file_size = os.path.getsize(local_file_path)
            logging.info(f"Downloaded file size: {file_size} bytes.")
            if file_size == 0:
                raise ValueError(
                    f"The downloaded file is empty. Check the content of the S3 object at {key}."
                )

            with open(local_file_path, "r") as file:
                try:
                    output = json.load(file)
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON from the file: {e}")
                    raise

        return output
```

</div>
</details>

To use a custom XCom backend class, you need to save it in a Python file in the `include` directory of your Airflow project. Then, set the `AIRFLOW__CORE__XCOM_BACKEND` environment variable in your Airflow instance to the path of the custom XCom backend class. If you run Airflow locally with the Astro CLI, you can set the environment variable in the `.env` file of your Astro project. On Astro, you can [set the environment variable in the Astro UI](https://docs.astronomer.io/astro/environment-variables).

```text
AIRFLOW__CORE__XCOM_BACKEND=include.<your-file-name>.MyCustomXComBackend
```

If you want to further customize the functionality for your custom XCom backend, you can override additional methods of the [XCom module](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/xcom/index.html) ([source code](https://github.com/apache/airflow/blob/main/airflow/models/xcom.py)). 

A common use case for this is removing stored XComs upon clearing and rerunning a task in both the Airflow metadata database and the custom XCom backend. To do so, the `.clear()` method needs to be overridden to include the removal of the referenced XCom in the custom XCom backend. The code below shows an example of a `.clear()` method that includes the deletion of an XCom stored in a custom S3 backend, using the AWS version of the `MyCustomXComBackend` XCom backend from [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization) of the tutorial.

<details>
<summary>Click to view an example override of the .clear() method</summary>
<div>

This clear method override can be added to the `MyCustomXComBackend` class shown previously to delete the XCom from the S3 bucket when the XCom is cleared from the Airflow metadata database. The deletion does not affect the XCom stored in Google Cloud Storage.

```python
from airflow.utils.session import NEW_SESSION, provide_session

@classmethod
@provide_session
def clear(
    cls,
    execution_date=None,
    dag_id=None,
    task_id=None,
    session=NEW_SESSION,
    *,
    run_id=None,
    map_index=None,
) -> None:

    from airflow.models import DagRun
    from airflow.utils.helpers import exactly_one
    import warnings
    from airflow.exceptions import RemovedInAirflow3Warning

    if dag_id is None:
        raise TypeError("clear() missing required argument: dag_id")
    if task_id is None:
        raise TypeError("clear() missing required argument: task_id")

    if not exactly_one(execution_date is not None, run_id is not None):
        raise ValueError(
            f"Exactly one of run_id or execution_date must be passed. "
            f"Passed execution_date={execution_date}, run_id={run_id}"
        )

    if execution_date is not None:
        message = "Passing 'execution_date' to 'XCom.clear()' is deprecated. Use 'run_id' instead."
        warnings.warn(message, RemovedInAirflow3Warning, stacklevel=3)
        run_id = (
            session.query(DagRun.run_id)
            .filter(
                DagRun.dag_id == dag_id, DagRun.execution_date == execution_date
            )
            .scalar()
        )

    #### Customization start

    # get the reference string from the Airflow metadata database
    query = session.query(cls).filter_by(
        dag_id=dag_id, task_id=task_id, run_id=run_id
    )

    print(query.all())

    if map_index is not None:
        query = query.filter_by(map_index=map_index)

    # iterate through xcoms of this task and delete them from S3
    xcom_entries = query.all()
    for xcom_entry in xcom_entries:
        reference_string = xcom_entry.value
        if reference_string:
            print(reference_string)
            key = reference_string.replace(MyCustomXComBackend.PREFIX, "")
            hook = S3Hook(aws_conn_id="my_aws_conn")
            hook.delete_objects(
                bucket=MyCustomXComBackend.S3_BUCKET_NAME, keys=[key]
            )

    # delete the XCom containing the reference string from metadata database
    query.delete()
```

</div>
</details>

## Custom serialization and deserialization

By default, Airflow includes [serialization](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/serializers.html) methods for common object types like [JSON](https://www.json.org/json-en.html), [pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and [NumPy](https://numpy.org/). You can see all supported types in the [Airflow source code](https://github.com/apache/airflow/tree/main/airflow/serialization/serializers).

If you need to pass data objects through XCom that are not supported, you have several options:

- Enable [pickling](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#enable-xcom-pickling). This method is easy to implement for local testing, but not suitable for production due to [security issues](https://docs.python.org/3/library/pickle.html). 
- Register a custom serializer, see [Serialization](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/serializers.html).
- Add a `serialize()` and `deserialize()` method to the class of the object you want to pass through XCom, see [Serialization](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/serializers.html).
- Use a custom XCom backend to define custom serialization and deserialization methods, see [Use a custom XCom backend class](#use-a-custom-xcom-backend-class).
