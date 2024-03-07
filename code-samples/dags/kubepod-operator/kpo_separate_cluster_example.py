# import DAG object and utility packages
from airflow import DAG
from pendulum import datetime
from airflow.configuration import conf

# import the KubernetesPodOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

# import EKS related packages from the Amazon Provider
from airflow.providers.amazon.aws.hooks.eks import EksHook, NodegroupStates
from airflow.providers.amazon.aws.operators.eks import (
    EksCreateNodegroupOperator,
    EksDeleteNodegroupOperator,
)
from airflow.providers.amazon.aws.sensors.eks import EksNodegroupStateSensor


# custom class to create a node group with Nodes on EKS
class EksCreateNodegroupWithNodesOperator(EksCreateNodegroupOperator):
    def execute(self, context):
        # instantiating an EKSHook on the basis of the AWS connection (Step 5)
        eks_hook = EksHook(
            aws_conn_id=self.aws_conn_id,
            region_name=self.region,
        )

        # define the Node group to create
        eks_hook.create_nodegroup(
            clusterName=self.cluster_name,
            nodegroupName=self.nodegroup_name,
            subnets=self.nodegroup_subnets,
            nodeRole=self.nodegroup_role_arn,
            scalingConfig={"minSize": 1, "maxSize": 1, "desiredSize": 1},
            diskSize=20,
            instanceTypes=["g4dn.xlarge"],
            amiType="AL2_x86_64_GPU",  # get GPU resources
            updateConfig={"maxUnavailable": 1},
        )


# instantiate the DAG
with DAG(
    start_date=datetime(2022, 6, 1),
    catchup=False,
    schedule="@daily",
    dag_id="KPO_remote_EKS_cluster_example_dag",
) as dag:
    # task 1 creates the node group
    create_gpu_nodegroup = EksCreateNodegroupWithNodesOperator(
        task_id="create_gpu_nodegroup",
        cluster_name="<your cluster name>",
        nodegroup_name="gpu-nodes",
        nodegroup_subnets=["<your subnet>", "<your subnet>"],
        nodegroup_role_arn="<arn of your EKS role>",
        aws_conn_id="<your aws conn id>",
        region="<your region>",
    )

    # task 2 check for node group status, if it is up and running
    check_nodegroup_status = EKSNodegroupStateSensor(
        task_id="check_nodegroup_status",
        cluster_name="<your cluster name>",
        nodegroup_name="gpu-nodes",
        mode="reschedule",
        timeout=60 * 30,
        exponential_backoff=True,
        aws_conn_id="<your aws conn id>",
        region="<your region>",
    )

    # task 3 the KubernetesPodOperator running a task
    # here, cluster_context and the kubernetes_conn_id are defined at the task level.
    run_on_EKS = KubernetesPodOperator(
        task_id="run_on_EKS",
        cluster_context="<arn of your cluster>",
        namespace="airflow-kpo-default",
        name="example_pod",
        image="ubuntu",
        cmds=["bash", "-cx"],
        arguments=["echo hello"],
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=False,
        kubernetes_conn_id="k8s",
        startup_timeout_seconds=240,
    )

    # task 4 deleting the node group
    delete_gpu_nodegroup = EksDeleteNodegroupOperator(
        task_id="delete_gpu_nodegroup",
        cluster_name="<your cluster name>",
        nodegroup_name="gpu-nodes",
        aws_conn_id="<your aws conn id>",
        region="<your region>",
    )

    # task 5 checking that the node group was deleted successfully
    check_nodegroup_termination = EksNodegroupStateSensor(
        task_id="check_nodegroup_termination",
        cluster_name="<your cluster name>",
        nodegroup_name="gpu-nodes",
        aws_conn_id="<your aws conn id>",
        region="<your region>",
        mode="reschedule",
        timeout=60 * 30,
        target_state=NodegroupStates.NONEXISTENT,
    )

    # setting the dependencies
    create_gpu_nodegroup >> check_nodegroup_status >> run_on_EKS
    run_on_EKS >> delete_gpu_nodegroup >> check_nodegroup_termination
