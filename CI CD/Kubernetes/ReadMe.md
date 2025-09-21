# Kubernetes Namespaces

Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single cluster, allowing teams and projects to share the same physical cluster without interfering with each other.

### Key Benefits

- **Name Isolation**  
  Resource names need only be unique within a namespace, so the same Deployment or Service name can exist in different namespaces without conflict.  

- **Access Control**  
  Apply Role-Based Access Control (RBAC) policies per namespace to restrict who can view or modify resources.  

- **Resource Quotas**  
  Enforce CPU, memory, and object-count limits on each namespace to prevent any single team from exhausting cluster resources.  

- **Environment Separation**  
  Logical separation of environments (e.g., `dev`, `staging`, `prod`) without provisioning multiple clusters.

### Default Namespaces

Kubernetes starts with four namespaces by default:

| Namespace       | Purpose                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------|
| `default`       | The default target for resource creation when no namespace is specified.                     |
| `kube-system`   | Holds Kubernetes system components (API server, scheduler, controller manager, etc.).        |
| `kube-public`   | Readable by all users (including unauthenticated clients); used for cluster-wide info.       |
| `kube-node-lease` | Manages node heartbeat leases to help the control plane detect node failures.             |

### When to Use Namespaces

- Multiple teams share the same cluster.  
- You need clear separation between environments (e.g., development vs. production).  
- You want to apply different security or resource policies per team or project.  

Avoid namespaces when you require hard isolation (use separate clusters) or when your cluster is small and managed by a single team.

### Basic Commands

- List all namespaces:  
  ```bash
  kubectl get namespaces
  ```
- Create a new namespace:  
  ```bash
  kubectl create namespace my-team
  ```
- Run a pod in a specific namespace:  
  ```bash
  kubectl run nginx --image=nginx --namespace=my-team
  ```
- Switch your default namespace for kubectl:  
  ```bash
  kubectl config set-context --current --namespace=my-team
  ```

# Pods in Kubernetes

Pods are the smallest deployable units in Kubernetes, serving as the fundamental building blocks for containerized applications.

### What Is a Pod?

A Pod is a group of one or more containers that share storage, networking, and specifications for how to run those containers. It acts as a logical host, co-locating tightly coupled application components within the same scheduling and isolation context.

### Pod Structure and Features

- Shared Network Namespace: All containers in a Pod share the same IP address and port space, allowing them to communicate via localhost.  
- Shared Storage Volumes: Volumes defined in the Pod spec are accessible to every container in the Pod.  
- Specification for Containers: The Pod manifest describes each container’s image, resource requirements, ports, and environment variables.  
- Init and Ephemeral Containers: Init containers run to completion before app containers start, and ephemeral containers can be injected for debugging purposes.

### Common Use Cases

- Single-Container Pods  
  Use the “one-container-per-Pod” pattern when your application runs in a single process. Here, a Pod is essentially a lightweight wrapper around that container for easier orchestration and scaling.  

- Multi-Container Pods  
  Employ when multiple processes need to work closely together and share resources. Typical scenarios include sidecar patterns (e.g., logging or proxy containers) and ambassador or adapter containers for data transformation.

### Pod Lifecycle

1. Scheduling: The control plane assigns a Pod to a node based on resource requirements and affinity rules.  
2. Init Containers: Run sequentially to set up prerequisites (e.g., pulling secrets, setting up volumes).  
3. Application Containers: Start concurrently once init containers complete.  
4. Termination: When containers finish or fail, the Pod’s status updates; controllers can recreate Pods to maintain desired state.  
5. Deletion: Pods are removed when their managing controller is scaled down or explicitly deleted.

### Types of Pods

1. Single-Container Pods  
   - Basic building block for stateless apps.  
2. Multi-Container Pods  
   - Sidecar pattern for helpers (logging, metrics).  
3. Static Pods  
   - Managed directly by a node’s kubelet without the API server; used for bootstrapping critical services.  
4. DaemonSet Pods  
   - Ensure one copy runs on every node, ideal for monitoring agents or log collectors.

### Working with Pods

Pods are rarely created directly in production. Instead, you define higher-level workload resources—such as Deployments, StatefulSets, or Jobs—that manage Pod creation, scaling, and updates. For ad hoc testing, you can apply a manifest like:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

Run `kubectl apply -f simple-pod.yaml` to create this Pod directly on the cluster.

# ReplicaSet

A **ReplicaSet** in Kubernetes (often abbreviated as **RS**) is a controller that ensures a specified number of identical Pods are running at any given time. Think of it as Kubernetes’ way of saying, “I want _n_ copies of this Pod, no matter what.”

### What Does a ReplicaSet Do?
- **Maintains Availability**: If a Pod crashes or is deleted, the ReplicaSet automatically creates a new one to maintain the desired count.
- **Scales Easily**: You can increase or decrease the number of replicas dynamically.
- **Matches Pods by Labels**: It uses a selector to find and manage Pods with specific labels.

### Anatomy of a ReplicaSet
A ReplicaSet is defined using a YAML or JSON manifest. It includes:
- `replicas`: Number of Pods to maintain.
- `selector`: Criteria to identify which Pods it should manage.
- `template`: Blueprint for creating new Pods.

Here’s a simple example:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: myapp:1.0
```
You rarely use ReplicaSets directly. Instead, you use **Deployments**, which manage ReplicaSets behind the scenes and add features like rolling updates and rollbacks.
