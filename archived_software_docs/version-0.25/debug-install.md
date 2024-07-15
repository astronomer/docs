---
sidebar_label: 'Debugging'
title: 'Debug Your Astronomer Software Installation'
id: debug-install
---


Use the information provided here when the Astronomer platform is not functioning as expected after you install it.

## Houston and Grafana stuck in CrashLoopBackOff

When deploying the base Astronomer platform, the Houston (API) and Grafana pods connect directly to the database. All other database connections are created from Apache Airflow® deployments created on Astronomer.

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
Make sure that the Kubernetes cluster Astronomer is running on can connect to the database. One way to check this is to jump into an Astronomer pod and try connecting directly to the database:

```
kubectl exec -it manageable-snail-houston-6fb7956994-2tngn /bin/sh -n astro-demo
```

Once inside the pod, add the `postgresql` package:

```
/houston # apk add postgresql
fetch https://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
(1/12) Installing ncurses-terminfo-base (6.1_p20190518-r0)
(2/12) Installing ncurses-terminfo (6.1_p20190518-r0)
(3/12) Installing ncurses-libs (6.1_p20190518-r0)
(4/12) Installing libedit (20190324.3.1-r0)
(5/12) Installing db (5.3.28-r1)
(6/12) Installing libsasl (2.1.27-r4)
(7/12) Installing libldap (2.4.48-r0)
(8/12) Installing libpq (11.6-r0)
(9/12) Installing postgresql-client (11.6-r0)
(10/12) Installing tzdata (2019c-r0)
(11/12) Installing libxml2 (2.9.9-r2)
(12/12) Installing postgresql (11.6-r0)
Executing busybox-1.30.1-r2.trigger
OK: 89 MiB in 35 packages
```

Now try connecting with `psql`:

```
/houston # psql -U <username> -h <host> -p <port>
Password for user <username>:

```
If the connection times out here, there may be a networking issue.

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

If there is indeed a typo, delete the secret, recreate it with the right value, and then delete all the pods in the namespace.

```
$ kubectl delete secret astronomer-bootstrap -n astro-demo
secret/astronomer-bootstrap deleted
$ kubectl create secret generic astronomer-bootstrap --from-literal connection="<your_connection_string>" --namespace <namespace>
secret/astronomer-bootstrap created
$ kubectl delete --all pods --namespace <namespace>
```

Restarting the pods will force them to pick up the new value.
