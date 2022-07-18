---
sidebar_label: 'Debugging'
title: 'Debug Your Astronomer Software installation'
id: debug-install
description: Common snags users run into while deploying and running Astronomer Software.
---


Use the information provided here when the Astronomer platform is not functioning as expected after you install it.

## Houston and Grafana stuck in CrashLoopBackOff

When deploying the base Astronomer platform, the Houston (API) and Grafana pods connect directly to the database. All other database connections are created from Airflow deployments created on Astronomer.

```
$ kubectl get pods -n astro-demo
NAME                                                       READY   STATUS             RESTARTS   AGE
manageable-snail-alertmanager-0                            1/1     Running            0          1h
manageable-snail-cli-install-5b96bfdc-25nzs                1/1     Running            0          1h
manageable-snail-commander-787bdfff8b-d8snw                1/1     Running            0          1h
manageable-snail-elasticsearch-client-69c74bbd5b-57nhj     1/1     Running            0          1h
manageable-snail-elasticsearch-client-69c74bbd5b-fwsng     1/1     Running            0          1h
manageable-snail-elasticsearch-data-0                      1/1     Running            0          1h
manageable-snail-elasticsearch-data-1                      1/1     Running            0          1h
manageable-snail-elasticsearch-exporter-57786f5f96-lgtjg   1/1     Running            0          1h
manageable-snail-elasticsearch-master-0                    1/1     Running            0          1h
manageable-snail-elasticsearch-master-1                    1/1     Running            0          1h
manageable-snail-elasticsearch-master-2                    1/1     Running            0          1h
manageable-snail-elasticsearch-nginx-cfb4bd77d-gzgkj       1/1     Running            0          1h
manageable-snail-fluentd-45tnm                             1/1     Running            0          1h
manageable-snail-fluentd-6gs9z                             1/1     Running            0          1h
manageable-snail-fluentd-bp4lp                             1/1     Running            0          1h
manageable-snail-fluentd-bxnk6                             1/1     Running            0          1h
manageable-snail-fluentd-f5nkj                             1/1     Running            0          1h
manageable-snail-fluentd-hmbtd                             1/1     Running            0          1h
manageable-snail-fluentd-jx4tg                             1/1     Running            0          1h
manageable-snail-fluentd-vk9rr                             1/1     Running            0          1h
manageable-snail-fluentd-zslx4                             1/1     Running            0          1h
manageable-snail-grafana-5bdd6cdf64-s77c7                  0/1     CrashLoopBackOff   20         1h
manageable-snail-houston-6fb7956994-2tngn                  0/1     CrashLoopBackOff   20         1h
manageable-snail-kibana-5c7bbb5dc6-z5jb5                   1/1     Running            0          1h
manageable-snail-kube-state-bf86885f-g46pp                 1/1     Running            0          1h
manageable-snail-kubed-5b5d65dd9d-l7nds                    1/1     Running            2          1h
manageable-snail-nginx-799d79ccf9-kfnzn                    1/1     Running            0          1h
manageable-snail-nginx-default-backend-5cc4755696-vh5zq    1/1     Running            0          1h
manageable-snail-astro-ui-7b9b9df4f9-pb99f                 1/1     Running            0          1h
manageable-snail-prometheus-0                              1/1     Running            0          1h
manageable-snail-registry-0                                1/1     Running            0          1h
```

If these pods do not come up in a healthy state, it is usually an issue with the database connection. See the following topics to confirm your connection.

#### Networking
Make sure that the Kubernetes cluster Astronomer is running on can connect to the database. Run the following comannd to start a `postgresql` pod in your cluster and then connect to it:

```sh
kubectl run psql --rm -it --restart=Never --namespace <astronomer-namespace> --image bitnami/postgresql --command -- psql $(kubectl get secret -n <astronomer-namespace> <release-name>-houston-backend --template='{{.data.connection | base64decode }}' | sed 's/?.*//g')
```

If the connection times out, there may be a networking issue.

#### Verify the Secret
Check to make sure the `astronomer-bootstrap` secret created earlier, which contains the connection string to the database, does not contain any typos:

```
$ kubectl get secrets -n astro-demo
NAME                                                   TYPE                                  DATA   AGE
astronomer-bootstrap                                   Opaque                                1      33h
astronomer-tls                                         kubernetes.io/tls                     2      44d
manageable-snail-commander-token-hxq6v                 kubernetes.io/service-account-token   3      33h
manageable-snail-fluentd-token-s8fp9                   kubernetes.io/service-account-token   3      33h
manageable-snail-grafana-backend                       Opaque                                1      33h
manageable-snail-grafana-bootstrapper-token-krlhk      kubernetes.io/service-account-token   3      33h
manageable-snail-houston-backend                       Opaque                                1      33h
manageable-snail-houston-bootstrapper-token-5z9gb      kubernetes.io/service-account-token   3      33h
manageable-snail-houston-jwt-signing-certificate       Opaque                                1      33h
manageable-snail-houston-jwt-signing-key               Opaque                                1      33h
manageable-snail-kube-state-token-b9gqf                kubernetes.io/service-account-token   3      33h
manageable-snail-kubed                                 Opaque                                1      33h
manageable-snail-kubed-apiserver-cert                  Opaque                                2      33h
manageable-snail-kubed-notifier                        Opaque                                0      33h
manageable-snail-kubed-token-dhd94                     kubernetes.io/service-account-token   3      33h
manageable-snail-nginx-token-xk5pn                     kubernetes.io/service-account-token   3      33h
manageable-snail-prometheus-token-2v59c                kubernetes.io/service-account-token   3      33h
manageable-snail-registry-auth                         kubernetes.io/dockerconfigjson        1      33h
```

To decrypt the `astronomer-bootstrap` secret:

```
$ kubectl get secret astronomer-bootstrap -o yaml
apiVersion: v1
data:
  connection: <encoded_value>
kind: Secret
metadata:
  creationTimestamp: "2019-12-27T16:57:42Z"
  name: astronomer-bootstrap
  namespace: astro-demo
  resourceVersion: "37526902"
  selfLink: /api/v1/namespaces/astro-demo/secrets/astronomer-bootstrap
  uid: ff0ed7a4-28c9-11ea-87af-4201ac100003
type: Opaque
```

Now to see the secret in plaintext:
```
echo <encoded_value> | base64 --decode
```

If there is a typo, delete the secret, recreate it with the right value, and then delete all the pods in the namespace.

```
$ kubectl delete secret astronomer-bootstrap -n astro-demo
secret/astronomer-bootstrap deleted
$ kubectl create secret generic astronomer-bootstrap --from-literal connection="<your_connection_string>" --namespace <namespace>
secret/astronomer-bootstrap created
$ kubectl delete --all pods --namespace <namespace>
```
Restarting the pods will force them to pick up the new value.

## Houston and Astronomer Software x509 Certificate Signed by Unknown Authority error

Occasionally, the shared Houston and Astronomer Software registry Pod certificates fail to synchronize and the following error message appears: 

```
Warning Failed 24m (x4 over 26m) kubelet, <node> Failed to pull image "registry.astronomer.base.domain/testing/airflow:deploy-5": rpc error: code = Unknown desc = Error response from daemon: Get https://registry.astronomer.base.domain/v2/: x509: certificate signed by unknown authority
```
To resolve this issue and clear the error message, restart the Houston pods and then the Astronomer Software registry Pod.
