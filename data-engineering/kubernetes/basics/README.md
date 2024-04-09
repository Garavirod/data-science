
### Kubernetes
Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.
(Reference)[https://kubernetes.io/]
(Basics)[https://kubernetes.io/docs/tutorials/kubernetes-basics/]

### Overview app deployments
(Going back the time architecure)[https://kubernetes.io/docs/concepts/overview/]


### Create token kubernetes dashboard
```
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```
(Deploy and Access the Kubernetes Dashboard)[https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/]


### Kubernetes installation

(Kubernetes Install)[https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/]

### Run Kubernetes dashboard

```
kubectl proxy
```

### List pods

```
kubectl get pods -n airflow
```

### Get values from image to yaml file

```
helm show values apache-airflow/airflow > values.yaml
```

### Airflow installation via Helm
(airflow installation via helm)[https://airflow.apache.org/docs/helm-chart/stable/index.html]

### Helm cli installation
(Helm installation)[https://helm.sh/docs/intro/install/]