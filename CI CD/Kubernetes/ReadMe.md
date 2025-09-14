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
