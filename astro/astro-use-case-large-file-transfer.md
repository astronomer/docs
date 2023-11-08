---
title: 'Move large files between object storages leveraging horizontal scaling'
navTitle: 'Parallelized large file transfer'
id: astro-use-case-large-file-transfer
description: Parallelized large file transfer.
---

Moving large files is a common ETL/ELT operation that necessitates a parallelized approach and appropriate scaling of your Astro deployment. This use case shows a custom templated task group that moves any number of large files from one S3 bucket to another and can be adjusted to work with other object storage providers. Additionally relevant scaling parameters are discussed.

![Screenshot of the Airflow UI Graph view of a DAG with 8 tasks, 7 of which are contained in the `load_big_files` task group.](/img/examples/astro-use-case-large-file-transfer_task_group_dag.png)

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).

## Clone the project

Clone the example project from the [Astronomer GitHub](https://github.com/astronomer/astro-use-case-large-file-transfer). To keep your credentials secure when you deploy this project to your own git repository, make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory. 

The example uses Amazon S3 as the object storage provider but can be adjusted to work with other providers.

## Deploy the project

To deploy the example project to Astro, follow these steps:

1. Make sure you have a [Deployment](create-deployment.md) set up using the same Airflow version that you specified in the `Dockerfile` of the Astro project. 

2. In the Astro UI, navigate to the **Details** tab of your Astro Deployment and configure a [worker queue](https://docs.astronomer.io/astro/configure-worker-queues) to handle the transfer of file chunks. Astronomer recommends to scale both, vertically by choosing a larger **Worker Type** and horizontally by increasing the **Concurrency** value to get optimized performance.

    ![Screenshot of the Astro UI showing how to add a worker queue. First click on the Details tab, then on the Edit option for the Execution parameters. The screenshot also shows two worker queues existing, `default` and a worker queue called `large` with an A60 worker type, concurrency of 180 and max # of workers 30.](/img/examples/astro-use-case-large-file-transfer_add_worker_queue.png)

3. Click on the **Environment** tab to add your object storage connections. This example project uses one AWS connection called `aws_default`. Select the **Generic** connection, then provide the **Type** `aws` as well as your own **Login** and **Password**. You can leave all other fields empty. 

    ![Screenshot of the Astro UI showing how to add a connection.](/img/examples/astro-use-case-large-file-transfer_connection.png)

4. Click on the **Variables** tab to add environment variables. Since this example will create many mapped task instances to run in parallel we need to increase the following Airflow configurations:

    ```text
    AIRFLOW__CORE__MAX_MAP_LENGTH=10240
    AIRFLOW__SCHEDULER__MAX_TIS_PER_QUERY=128
    AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG=128
    ```

    ![Screenshot of the Astro UI showing 3 Variables that have been set.](/img/examples/astro-use-case-large-file-transfer_env_vars.png)

5. In the `load_files_in_chunks.py` file, adjust the following variables to your own connection ids, buckets and keys:

    ```python
    SRC_CONN_ID_A = "aws_default"
    SRC_BUCKET_A = "bigfileloadtesta"
    SRC_KEY_A = "my_folder/my_big_file_A.mov"
    DEST_CONN_ID_A = "aws_default"
    DEST_BUCKET_A = "bigfileloadtestb"
    DEST_KEY_A = "my_folder_2/test_A.mov"

    SRC_CONN_ID_B = "aws_default"
    SRC_BUCKET_B = "bigfileloadtesta"
    SRC_KEY_B = "my_folder/my_big_file_B.mov"
    DEST_CONN_ID_B = "aws_default"
    DEST_BUCKET_B = "bigfileloadtestb"
    DEST_KEY_B = "my_folder_2/test_B.mov"
    ```

    :::tip

    This example use case moves two big files, but it can be adjusted to move any number of files that are specified in the list of dictionaries returned by the `get_file_config_dicts` task with the following parameters:

    ```python
    {
        "src_conn_id": SRC_CONN_ID_A,
        "src_bucket": SRC_BUCKET_A,
        "src_key": SRC_KEY_A,
        "dest_conn_id": DEST_CONN_ID_A,
        "dest_bucket": DEST_BUCKET_A,
        "dest_key": DEST_KEY_A,
    }
    ```

    In a production environment you can programmatically fetch the list of files to be moved from a database or other source.

    :::

5. In the root of the folder you cloned the project to, run:

    ```sh
    astro login
    ```

    And authenticate your device to your Astro account.

6. Deploy the project to your Astro Deployment.

    ```sh
    astro deploy
    ```

7. In the Airflow UI run the `load_files_in_chunks` DAG by clicking on the play button.

:::tip

This use case shows how to move large files from one S3 bucket to another. To adjust the code for other object storage solutions you will need to change the hook and methods used in the following functions:

- `get_file_size_func`: retrieves the size of the file to be moved in bytes.
- `initialize_multipart_upload_func`: initializes a multipart upload.
- `move_chunk_func`: moves a file chunk from the source to the destination.
- `complete_multipart_upload_func`: completes a multipart upload.

:::

## Run the project locally

To run the example project locally, first make sure [Docker](https://docs.docker.com/) is running. Then, open your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 6 Docker containers on your machine to run it:

- The Airflow webserver, which runs the Airflow UI and can be accessed at `https://localhost:8080/`.
- The Airflow scheduler, which is responsible for monitoring and triggering tasks.
- The Airflow triggerer, which is an Airflow component used to run [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators).
- The Airflow metadata database, which is a Postgres database that runs on port `5432`.

To run the project, provide your own mapping of source and destination connections, buckets and keys in the `load_files_in_chunks.py` file.

## Project contents

### Data source

To run this use case you can use any files you have stored in your object storage solution.

### Project overview

This use case contains three DAGs showing variations of the same file moving pattern.

The [`load_files_in_chunks` DAG](https://github.com/astronomer/astro-use-case-large-file-transfer/blob/main/dags/load_files_in_chunks.py) uses a custom templated task group to move large files from one S3 bucket to another. The task group is defined in the `load_in_chunks_tg.py` file in the include folder.

![Screenshot of the Airflow UI Graph view of the load_files_in_chunks DAG with 8 tasks, 7 of which are contained in the `load_big_files` task group.](/img/examples/astro-use-case-large-file-transfer_task_group_dag.png)

The [`s3_load_big_file_singular_poc` DAG](https://github.com/astronomer/astro-use-case-large-file-transfer/blob/main/dags/standalone_dags/s3_load_big_file_singular_poc.py) shows a simplified version of the above pipeline that moves one file from one S3 bucket to another with all code being contained in one DAG file.

![Screenshot of the Airflow UI Graph view of the s3_load_big_file_singular_poc DAG with 5 tasks.](/img/examples/astro-use-case-large-file-transfer_s3_load_big_file_singular_poc.png)

The [`s3_load_multiple_files_poc` DAG](https://github.com/astronomer/astro-use-case-large-file-transfer/blob/main/dags/standalone_dags/s3_load_multiple_files_poc.py) shows a simplified version of the above pipeline that moves several files from one S3 bucket to another with all code being contained in one DAG file.

![Screenshot of the Airflow UI Graph view of the s3_load_multiple_files_poc DAG with 7 tasks.](/img/examples/astro-use-case-large-file-transfer_s3_load_multiple_files_poc.png)

This use case describes the `load_files_in_chunks` DAG in detail. The other two DAGs are simplified versions of the same pattern.

### Project code

This use case shows how [dynamic task mapping](https://docs.astronomer.io/learn/dynamic-tasks) can be used to leverage horizontal scaling on Astro when moving large files between object storages. Additionally it shows how a common pattern can be abstracted in a custom templated task group in order to standardize and reuse it across DAGs.

#### load_files_in_chunks DAG

At the start of the `load_files_in_chunks` DAG you can set your own connection ids, buckets and keys to be used in the `get_file_config_dicts` task. This task returns a list of dictionaries, each containing the source and destination connection ids, buckets and keys for one file to be moved. More files can easily be added and the list can be programmatically generated from a database or other source.

```python
SRC_CONN_ID_A = "aws_default"
SRC_BUCKET_A = "bigfileloadtesta"
SRC_KEY_A = "my_folder/my_big_file_A.mov"
DEST_CONN_ID_A = "aws_default"
DEST_BUCKET_A = "bigfileloadtestb"
DEST_KEY_A = "my_folder_2/test_A.mov"

SRC_CONN_ID_B = "aws_default"
SRC_BUCKET_B = "bigfileloadtesta"
SRC_KEY_B = "my_folder/my_big_file_B.mov"
DEST_CONN_ID_B = "aws_default"
DEST_BUCKET_B = "bigfileloadtestb"
DEST_KEY_B = "my_folder_2/test_B.mov"

# ...

@task
def get_file_config_dicts() -> list:
    """Retrieves file config dicts.
    You can use any upstream task to retrieve the information about
    your file mappings in this format"""

    file_config_dicts = [
        {
            "src_conn_id": SRC_CONN_ID_A,
            "src_bucket": SRC_BUCKET_A,
            "src_key": SRC_KEY_A,
            "dest_conn_id": DEST_CONN_ID_A,
            "dest_bucket": DEST_BUCKET_A,
            "dest_key": DEST_KEY_A,
        },
        {
            "src_conn_id": SRC_CONN_ID_B,
            "src_bucket": SRC_BUCKET_B,
            "src_key": SRC_KEY_B,
            "dest_conn_id": DEST_CONN_ID_B,
            "dest_bucket": DEST_BUCKET_B,
            "dest_key": DEST_KEY_B,
        },
    ]

    return file_config_dicts
```

Next, a few key parameters are specified. 

- `CHUNK_SIZE` determines the size of the chunks the file is split into. The default value of 5MB is a good starting point, but you can adjust it to your needs.
- `LARGE_QUEUE` is the name of the worker queue that will handle the resource intensive moving of the file chunks. This queue needs to be configured in the Astro UI as described in the [Deploy the project](#deploy-the-project) section.
- `DELETE_SOURCE_FILE` determines whether the source files are deleted after the transfer is complete.

At the top of the DAG file, four functions are defined. These functions are passed to the `load_big_files` task group and can be adjusted to interact with other object storage solutions than S3 by replacing the hook and methods used. 

The `get_file_size_func` function takes the source connection id, bucket and key as arguments and returns the size of the file in bytes.

```python
def get_file_size_func(src_conn_id: str, src_bucket_name: str, src_key: str) -> int:
    """Get the size of the remote file in bytes."""
    s3_client = S3Hook(aws_conn_id=src_conn_id).get_conn()

    metadata = s3_client.head_object(Bucket=src_bucket_name, Key=src_key)
    file_size = metadata["ContentLength"]

    return file_size
```

The `initialize_multipart_upload_func` function takes the destination connection id, bucket and key as arguments and returns the upload id of the initialized multipart upload.

```python
def initialize_multipart_upload_func(
    dest_conn_id: str, dest_bucket_name: str, dest_key: str
) -> str:
    """Initialize a multipart upload and retrieve the idea."""

    s3_client = S3Hook(aws_conn_id=dest_conn_id).get_conn()

    multipart_upload = s3_client.create_multipart_upload(
        Bucket=dest_bucket_name, Key=dest_key
    )
    upload_id = multipart_upload["UploadId"]

    return upload_id
```

The `move_chunk_func` function is the heart of this pipeline, it takes the information about the source and destination of a file chunk as well as the upload id of the multipart upload as arguments and moves the file chunk from the source to the destination. The function returns a dictionary containing part and chunk information alongside destination parameters. This information is used downstream to complete the multipart upload.

```python
def move_chunk_func(
    src_conn_id: str,
    src_bucket: str,
    src_key: str,
    dest_conn_id: str,
    dest_bucket: str,
    dest_key: str,
    chunk_size: int,
    chunk_index: int,
    upload_id: str,
    file_size: int,
) -> dict:
    """Move a chunk of bytes from one bucket to another."""

    # connect to the source
    s3_client = S3Hook(aws_conn_id=src_conn_id).get_conn()

    range_start = chunk_index * chunk_size
    range_end = min(range_start + chunk_size - 1, file_size - 1)
    byte_range = f"bytes={range_start}-{range_end}"

    # get the chunk from the source
    obj = s3_client.get_object(Bucket=src_bucket, Key=src_key, Range=byte_range)
    bytes_chunk = obj["Body"].read()
    part_number = chunk_index + 1

    # connect to the destination
    s3_client = S3Hook(aws_conn_id=dest_conn_id).get_conn()

    # upload the chunk to the destination
    response = s3_client.upload_part(
        Body=bytes_chunk,
        Bucket=dest_bucket,
        Key=dest_key,
        UploadId=upload_id,
        PartNumber=part_number,
    )

    return {
        "ETag": response["ETag"],
        "PartNumber": part_number,
        "upload_id": upload_id,
        "dest_key": dest_key,
        "dest_bucket": dest_bucket,
        "dest_conn_id": dest_conn_id,
    }
```

The `complete_multipart_upload_func` function takes the upload id of the multipart upload as well as the parts information returned by the `move_chunk` task as arguments and completes the multipart upload.

```python
def complete_multipart_upload_func(
    dest_conn_id: str,
    dest_bucket: str,
    dest_key: str,
    upload_id: str,
    parts: list,
):
    """Complete a multipart upload."""
    s3_client = S3Hook(aws_conn_id=dest_conn_id).get_conn()

    s3_client.complete_multipart_upload(
        Bucket=dest_bucket,
        Key=dest_key,
        UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
```

The task group is instantiated in the task context with the four function described above, as well as the `file_config_dicts`, `chunk_size` and `queue_for_moving_tasks` as parameters. Note that the file config dict needs to follow the format shown in the `get_file_config_dicts` task above.

```python
tg1 = LoadBigFileTaskGroup(
    group_id="load_big_files",
    file_config_dicts=file_config_dicts,
    chunk_size=CHUNK_SIZE,
    get_file_size_func=get_file_size_func,
    initialize_multipart_upload_func=initialize_multipart_upload_func,
    move_chunk_func=move_chunk_func,
    complete_multipart_upload_func=complete_multipart_upload_func,
    queue_for_moving_task=LARGE_QUEUE,
)
```

The task group template is located in the `load_in_chunks_tg.py` file in the include folder. It uses the parameters passed to generated the file movement pattern.

![`load_big_files` task group in the Airflow UI graph view](/img/examples/astro-use-case-large-file-transfer_task_group.png)

The custom task group inherits from the `TaskGroup` class and takes the parameters described above as well as a `group_id` and `tooltip` argument.  

```python
class LoadBigFileTaskGroup(TaskGroup):
    # ...

    def __init__(
        self,
        group_id,
        file_config_dicts: list,
        chunk_size: int,
        get_file_size_func: Any,
        initialize_multipart_upload_func: Any,
        move_chunk_func: Any,
        complete_multipart_upload_func: Any,
        queue_for_moving_task: str = None,
        tooltip="Loads big files in chunks!",
        **kwargs
    ):
        super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)
```

The seven tasks are defined in the same way as regular tasks in a DAG with the only difference being that they have the `task_group` parameter set to the task group class instance using `self`.

```python
@task(task_group=self)
```

The first task of the task group is the `get_file_size` task, which uses the `get_file_size_func` function to retrieve the size of each file that is to be moved. The task is [dynamically mapped](https://docs.astronomer.io/learn/dynamic-tasks) over the list of file config dicts to create one task instance for each file. The `file_config_dict` returned by the `get_file_size` task contains all of the original parameters for a file, with the `file_size` having been added file.

```python
@task(task_group=self)
def get_filesize(file_config_dict: dict, get_file_size_func: Any):
    file_size = get_file_size_func(
        src_conn_id=file_config_dict["src_conn_id"],
        src_bucket_name=file_config_dict["src_bucket"],
        src_key=file_config_dict["src_key"],
    )
    file_config_dict["file_size"] = file_size

    return file_config_dict

file_config_dicts = get_filesize.partial(
    get_file_size_func=get_file_size_func
).expand(file_config_dict=file_config_dicts)
```

Next, the number of chunks per file is computed in the `get_chunk_info` task using the `chunk_size` specified in the DAG file and the file size of each file. Again, the new information `num_chunks` is added to the dictionary for each file and returned as a list of dictionaries.

```python
@task(task_group=self)
def get_num_chunks(chunk_size: int, file_config_dicts: list) -> list:
    files_info = []
    for file_config in file_config_dicts:
        file_size = file_config["file_size"]
        num_chunks = file_size // chunk_size
        if file_size % chunk_size:
            num_chunks += 1

        file_config["num_chunks"] = num_chunks

        files_info.append(file_config)

    return files_info

files_info = get_num_chunks(
    chunk_size=chunk_size, file_config_dicts=file_config_dicts
)
```

Before the file chunks can be moved, the multipart upload needs to be initiated at the destination location. This happens in the `initialize_multipart_upload` task, which uses the `initialize_multipart_upload_func` and adds the upload id to the chunk information dictionary for each file. This task is dynamically mapped over the list of file information dictionaries.

```python
@task(task_group=self)
def initialize_multipart_upload(
    file_info: dict,
) -> dict:
    upload_id = initialize_multipart_upload_func(
        dest_conn_id=file_info["dest_conn_id"],
        dest_bucket_name=file_info["dest_bucket"],
        dest_key=file_info["dest_key"],
    )

    file_info["upload_id"] = upload_id

    return file_info

init_chunks_info = initialize_multipart_upload.expand(file_info=files_info)
```

In order to be able to create a dynamically mapped task instance per chunk of each file, we will need an iterable with one element for each file chunk. The `create_chunks_list` task takes in the information returned from the `initialize_multipart_upload` task and creates a list of dictionaries with one dictionary for each file chunk. For example if there is one file to move with 2 chunks the task returns a list of 2 dictionaries, each containing the information about one file chunk with the corresponding chunk index: 

`{'src_conn_id': '...', 'src_bucket': '...', 'src_key': '...', 'dest_conn_id': '...', 'dest_bucket': '...', 'dest_key': '...', 'file_size': ..., 'num_chunks': 2, 'upload_id': '...', 'chunk_index': 0}`.

```python
@task(task_group=self)
def create_chunk_list(
    chunks_info: list,
) -> list:
    chunk_list = []

    for chunk_info in chunks_info:
        num_chunks = chunk_info["num_chunks"]

        for chunk_index in range(num_chunks):
            chunk_info_copy = chunk_info.copy()
            chunk_info_copy["chunk_index"] = chunk_index
            chunk_list.append(chunk_info_copy)

    return chunk_list

chunk_list = create_chunk_list(chunks_info=init_chunks_info)
```

The chunks are moved from the source to the destination location by the `move_chunk` task using the `move_chunk_func`. The task is dynamically mapped over the list of chunk information dictionaries (`chunk_list`). The `chunk_info` returned by the `move_chunk` task contains all of the original parameters for a file, with the parts information having been added. This task uses the [worker queue](https://docs.astronomer.io/astro/configure-worker-queues) specified in the DAG file as `LARGE_QUEUE`.

```python
@task(task_group=self, queue=queue_for_moving_task)
def move_chunk(chunk_info: dict, chunk_size: int, move_chunk_func: Any) -> dict:
    chunk_info = move_chunk_func(
        src_conn_id=chunk_info["src_conn_id"],
        src_bucket=chunk_info["src_bucket"],
        src_key=chunk_info["src_key"],
        dest_conn_id=chunk_info["dest_conn_id"],
        dest_bucket=chunk_info["dest_bucket"],
        dest_key=chunk_info["dest_key"],
        chunk_size=chunk_size,
        chunk_index=chunk_info["chunk_index"],
        file_size=chunk_info["file_size"],
        upload_id=chunk_info["upload_id"],
    )

    return chunk_info

parts_info = move_chunk.partial(
    chunk_size=chunk_size, move_chunk_func=move_chunk_func
).expand(
    chunk_info=chunk_list,
)
```

To be able to return from a one element per chunk to one element per file in the iterable to be mapped over the `group_parts_info` task collects the `ETag` and `PartNumber` information for each file and returns a list of dictionaries with one dictionary per file.

```python
@task(task_group=self)
def group_parts_info(parts_info):
    from itertools import groupby
    from operator import itemgetter

    sorted_parts_list = sorted(
        parts_info, key=itemgetter("dest_key", "PartNumber")
    )
    grouped_parts = [
        {
            "dest_conn_id": dest_conn_id,
            "dest_bucket": dest_bucket,
            "dest_key": dest_key,
            "upload_id": upload_id,
            "parts": [
                {
                    "ETag": part["ETag"].strip('"'),
                    "PartNumber": part["PartNumber"],
                }
                for part in parts
            ],
        }
        for (dest_key, upload_id, dest_conn_id, dest_bucket), parts in groupby(
            sorted_parts_list,
            key=lambda x: (
                x["dest_key"],
                x["upload_id"],
                x["dest_conn_id"],
                x["dest_bucket"],
            ),
        )
    ]

    return grouped_parts

grouped_parts_list = group_parts_info(parts_info)
```

The final task in the `LoadBigFileTaskGroup` task group template is the `complete_multipart_upload` task, which uses the `complete_multipart_upload_func` to complete the multipart upload. The task is dynamically mapped over the list of grouped parts information dictionaries (`grouped_parts_list`) to create one mapped task instance per file that was moved.

```python
@task(task_group=self)
def complete_multipart_upload(
    grouped_parts: dict,
    complete_multipart_upload_func: Any,
):
    dest_conn_id = grouped_parts["dest_conn_id"]
    dest_bucket = grouped_parts["dest_bucket"]
    dest_key = grouped_parts["dest_key"]
    upload_id = grouped_parts["upload_id"]
    parts = grouped_parts["parts"]

    complete_multipart_upload_func(
        dest_conn_id=dest_conn_id,
        dest_bucket=dest_bucket,
        dest_key=dest_key,
        upload_id=upload_id,
        parts=parts,
    )

complete_multipart_upload.partial(
    complete_multipart_upload_func=complete_multipart_upload_func
).expand(grouped_parts=grouped_parts_list)
```

Lastly, if you toggled `DELETE_SOURCE_FILE` to `True` in the DAG file, the `delete_source_file` task deletes the source file after the transfer is complete using the [S3DeleteObjectsOperator](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest/modules/S3DeleteObjectsOperator). The task is dynamically mapped over the list of file information dictionaries (`files_info`). Note that the format of the dictionaries in this list is modified using the [.map](https://docs.astronomer.io/learn/dynamic-tasks#transform-outputs-with-map) method.

```python
if DELETE_SOURCE_FILE:
    delete_source_file = S3DeleteObjectsOperator.partial(
        task_id="delete_source_file",
    ).expand_kwargs(
        file_config_dicts.map(
            lambda x: {
                "aws_conn_id": x["src_conn_id"],
                "bucket": x["src_bucket"],
                "prefix": x["src_key"],
            }
        )
    )

    chain(tg1, delete_source_file)
```

Congratulations! You used a templated task group to move any number of files of any sizes between object storages leveraging horizontal scaling on Astro!

## See also

- Documentation: [Configure worker queues](https://docs.astronomer.io/astro/configure-worker-queues).
- Guide: [Airflow task groups](https://docs.astronomer.io/learn/task-groups).
- Guide: [Create dynamic Airflow tasks](https://docs.astronomer.io/learn/dynamic-tasks).
- Guide: [Scaling Airflow to optimize performance](https://docs.astronomer.io/learn/airflow-scaling-workers).