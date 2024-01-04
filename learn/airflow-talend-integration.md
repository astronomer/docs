---
title: "Orchestrate Talend Jobs with Airflow"
description: "Orchestrate remote jobs in Talend with your Apache Airflow DAGs."
id: airflow-talend-integration
sidebar_label: "Talend"
sidebar_custom_props: { icon: 'img/integrations/talend.png' }
---

[Talend](https://www.talend.com/) is a popular tool for data integration and data management that can be easily used along with Airflow and Astronomer to have the best of multiple worlds for data management.

Using Airflow for orchestration allows for easily running multiple jobs with dependencies, parallelizing jobs, and monitoring run status and failures. When you combine Talend and Airflow, you can use both tools for what they're good for. If Talend works particularly well for one use case and Python for another, you can do both and still have a central platform for orchestration, monitoring, and logs with Airflow.

Additionally if you are moving to Airflow with existing Talend jobs, using the tools together eliminates the need to migrate existing jobs to Python code You can even combine both Talend jobs and other tasks in the same DAG.

This guide includes examples that highlight a few ways in which Talend and Airflow can work well together.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Talend Cloud. See [Talend Cloud Getting Started Guide](https://help.talend.com/r/en-US/Cloud/talend-cloud-getting-started/tic-architecture).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Implementation overview

There are two easy ways to execute Talend jobs with Airflow:

- Use the Talend Cloud API and execute the job using the [SimpleHttpOperator](https://registry.astronomer.io/providers/http/modules/simplehttpoperator).
- Containerize your Talend jobs and execute them using the [KubernetesPodOperator](https://registry.astronomer.io/providers/kubernetes/modules/kubernetespodoperator).

Each method has pros and cons, and the method you choose will likely depend on your Talend setup and workflow requirements.

|Method      |**Docker + KubernetesPodOperator**                                                                                                                                                                    |**API + SimpleHttpOperator**                                                                                                            |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
|Pros        | - Containerizing jobs brings the benefits of containerization including efficiency, flexibility, and scaling  Easily allows for downstream dependencies <br/> - Logs from jobs are shown in Airflow UI| - Very easy and accessible. Little setup and knowledge of other tools is required                                              |
|Cons        | - Must have Talend Studio to containerize jobs  More requirements and complexity to setup                                                                                                   | - Not well suited for triggering jobs that have downstream dependencies <br/> - Logs from Talend job are not automatically sent to Airflow |
|Requirements| - Talend Studio license Docker registry (can use Dockerhub if public is okay) <br/> - Kubernetes                                                                                                 | - Talend cloud license that allows API access                                                                                  |

<br/>

## Making requests to the Talend Cloud API in Airflow

You can run Talend jobs by calling the Talend Cloud API with Airflow's `SimpleHttpOperator`. This method is ideal if you have Talend Cloud jobs that  don't have downstream dependencies.

If you are unfamiliar with the Talend Cloud API, see the following documentation:

- [Talend Public API Docs](https://community.talend.com/s/article/Using-the-Talend-Cloud-Management-Console-Public-API-O2Ndn)
- [Talend UI Docs](https://api.us-west.cloud.talend.com/tmc/swagger/swagger-ui.html#!/)

:::info

The code in this example can be found on [the Astronomer Registry](https://legacy.registry.astronomer.io/dags/talend-api).

:::

### Getting Started with the Talend Cloud API

Using the API in Talend Cloud is straightforward. First, make sure the job you want to execute is present in the Talend Management Console as shown below. For this example, you'll execute a sample `SayHello` job.

![Say Hello Job](/img/guides/talend_api_1.png)

Next, note your job's Task ID. This will be passed to the API to trigger this specific job.

![Task ID](/img/guides/talend_api_2.png)

Finally, ensure your user has a personal access token created. This is required for authenticating to the API. To create one, under your user go to Profile Preferences, then Personal Access Tokens, and then add a token.

![Token](/img/guides/talend_api_3.png)

That's all you have to do on Talend! Now you can create an Airflow DAG to execute this job.

### Using the Talend API with Airflow

You can reach the Talend API from Airflow using the `SimpleHttpOperator`. In this example you'll use Airflow show how to execute a Talend job. However, note that there are many other actions you can perform with the Talend API as described in the documentation linked above, and all of these can be accomplished using the same method. Also note that there are other ways of making an API call in Airflow besides using the `SimpleHttpOperator`.

:::info

In Airflow 2+, provider packages are separate from the core of Airflow. If you are running Airflow 2+ on an Astro Runtime image, the [HTTP Provider](https://registry.astronomer.io/providers/http) package is already included. If you're not using Astronomer, you might need to install the package separately to use the hooks, operators, and connections described here. To learn more, read the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers/index.html).

:::

First, set up an Airflow connection to connect to the API. The connection should be an HTTP type, and should be configured like this:

![Talend Connection](/img/guides/airflow_talend_5.png)

The host name should be the Talend Cloud API URL. This can vary depending on which region your account is hosted in. The **Extras** field should contain your authorization string, with `Bearer` followed by your personal access token.

Next create and run the example DAG.

```python
import json
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('talend_api_jobs',
          schedule='@once',
          default_args=default_args
          ) as dag:

    talend1 = SimpleHttpOperator(
        task_id='talend_api',
        method='POST',
        http_conn_id='talend_api',
        endpoint='/tmc/v2.2/executions',
        data=json.dumps({"executable": "5fb2f5126a1cd451b07bee7a"}),
    )
```

This DAG has a single `SimpleHttpOperator` that sends a POST request to the Talend API to trigger a job. Ensure you enter the `http_conn_id` as the connection created above. The `endpoint` should be the Talend Cloud API executions endpoint for your region. The `data` is the body of the request and needs to contain the executable, which is the Task ID described in the previous section formatted in JSON.

Now if you run this DAG in Airflow, you should see a successful log that looks something like this:

![Success log](/img/guides/airflow_talend_6.png)

And looking at the Talend Management Console, you can see the job is running:

![Talend Running Job](/img/guides/airflow_talend_7.png)

Finally, note that because the API call simply triggers the job, the Airflow task will be marked successful as soon as a response is received from the AP. This result is not tied to when the job actually completes, so if you have downstream tasks that need the Talend job to be complete you either have to use another method like the `KubernetesPodOperator` described below or design another workflow in a way that manages this dependency.

## Executing Talend Jobs with KubernetesPodOperator

You can run Talend jobs with Airflow by containerizing them and running the containers with the `KubernetesPodOperator`. This is a good option if you are using Talend studio, or if you have tasks that are dependent on your Talend jobs completing first.

:::info

The code shown in this example is also available on [the Astronomer Registry](https://legacy.registry.astronomer.io/dags/talend-containers).

:::

### Containerizing Talend jobs

Existing Talend jobs and can be can be containerized with docker and pushed to a repository with the Talend Studio. To start go to Talend studio, find the job you would like to containerize, and select the publish feature from the right-click menu.

![Talend UI](/img/guides/talend_ui_1.png)

Once clicked a publish job pop up will come up. Select Docker image as the 'Export Type' to publish the job as a docker image.

![Talend UI 2](/img/guides/talend_ui_2.png)

Select next to set up your connection between Talend and your registry. In this example the job is being published to DockerHub and being built with a local Docker host. If you are using a remote Docker host, you will need to find the IP address Docker is running on and use TCP to connect. For example put `tcp://<docker-host-ip>` in the input box to the side of 'Remote'.

![Talend UI 3](/img/guides/talend_ui_3.png)

Then, configure the following additional parameters:

- **Image name**: The name of your repository (in this example, `talendjob`)
- **Image tag**: The image tag (in this example, `0.1.0`)
- **Registry** The location of your registry
- **Username**: Your DockerHub username
- **Password**: Your DockerHub Password

When you select **Finish**, the job will be converted into Docker image and pushed to the indicated registry. In this example the job was pushed to `https://hub.docker.com/repository/docker/user/talendjob`.

You can now run this job locally by running:

`docker run user/talendjob:0.1.0`

If you ran the command on the terminal you should see the output `hello`. Now you should be able to pull and run this image from Airflow.

### Orchestrating Containerized Talend Jobs with Airflow

Once your Talend jobs are containerized and pushed to a registry, you can create a DAG to orchestrate them.

This example DAG executes two Talend jobs, one of which is dependent on the other, and then sends an email notification if the jobs are successful:

```python
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow import configuration as conf
from airflow.operators.email import EmailOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get('kubernetes', 'NAMESPACE')

# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = '/usr/local/airflow/include/.kube/config'
    in_cluster=False
else:
    in_cluster=True
    config_file=None

# Define recipient emails for successful completion notification
email_to = ["noreply@astronomer.io"]

with DAG('talend_jobs',
          schedule='@once',
          default_args=default_args
          ) as dag:

    talend1 = KubernetesPodOperator(
                namespace=namespace,
                image="your-repo/talendjob:hello",
                name="talend-test-hello",
                task_id="hello-world",
                in_cluster=in_cluster, # if set to true, will look in the cluster, if false, looks for file
                cluster_context='docker-desktop', # is ignored when in_cluster is set to True
                config_file=config_file,
                is_delete_operator_pod=True,
                get_logs=True
            )

    talend2 = KubernetesPodOperator(
                namespace=namespace,
                image="your-repo/talendjob:random",
                name="talend-test-random",
                task_id="random",
                in_cluster=in_cluster,
                cluster_context='docker-desktop',
                config_file=config_file,
                is_delete_operator_pod=True,
                get_logs=True
            )

    send_email = EmailOperator(
                    task_id='send_email',
                    to=email_to,
                    subject='Talend Jobs Completed Successfully',
                    html_content='<p>Your containerized Talend jobs have completed successfully. <p>'
                )


    talend1 >> talend2 >> send_email
```

The first half of the code imports packages and sets the DAG up to work with Kubernetes. Each Talend job is its own task using the `KubernetesPodOperator`. In this case, the two tasks correlate to two Talend jobs, `talend1` and `talend2`.

In each task, the `image` is the name of the image of the containerized job saved to a registry as described above. Note that in this example, the image is pulled from DockerHub. By default, this is where the `KubernetesPodOperator` looks for the provided image name. If you want to pull an image from a private registry (e.g. ECR, GCR, etc.) instead, the setup looks a little different. Refer to the [Apache Airflow documentation](https://airflow.apache.org/docs/docker-stack/build.html#customizing-the-image) for details.

Since this example is very simple we don't need to provide any additional arguments to run the image. But if needed, these can all be specified in the operator's parameters.

Finally, the `send_email` task notifies you that the tasks completed successfully. Then, the final lines of code define task dependencies.

If you deploy this code to Astronomer and check out the Airflow UI, you should see a DAG that looks like this:

![Airflow Talend DAG](/img/guides/airflow_talend_1.png)

Once your Talend jobs are containerized, they can be orchestrated and given dependenies using Airflow.

## Troubleshooting common issues

### Error when building images with Docker on Mac

If you are getting an error that says `Cannot run program "docker-credential-desktop"` while building an image from a job using a local docker host on Mac, it might be due to an outdated Java plugin on Talend Studio V7.3.1  

You will need to edit your `.docker/config.json`. The file is located at `~/.docker/config.json`. Delete the line `"credsStore" : "desktop"` from you config.json :

```json
{
  "credsStore" : "desktop"
}
```

This will stop the error from happening when building images from Talend jobs with your local docker host.

### SMTP configuration

Note that if you are running the specific example DAG provided above in the `KubernetesPodOperator` section, SMTP will need to be configured on your Airflow instance in order for the `send_email` task to work. This requires an SMTP server that will allow a credentialed application to send emails. If you have that, you can connect it to Airflow using the following environment variables:

```yaml
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_USER=your-mail-id@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=yourpassword
AIRFLOW__SMTP__SMTP_MAIL_FROM=your-mail-id@gmail.com
```
