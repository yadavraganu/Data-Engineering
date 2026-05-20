## EC2 Tenancy Overview
Amazon EC2 offers three primary tenancy options that determine how your virtual machines are distributed across physical hardware: Shared (Default) Tenancy, Dedicated Instances, and Dedicated Hosts.
Choosing the right option depends on your specific compliance, licensing, and budget requirements.
| Tenancy Option | Hardware Isolation | License Visibility (Cores/Sockets) | Key Use Case | Cost |
|---|---|---|---|---|
| Shared (Default) | Multi-tenant | No | Standard cloud workloads | Lowest (Pay for usage) |
| Dedicated Instances | Single-tenant (Account level) | No | Corporate compliance & isolation | Higher (Instance fee + regional fee) |
| Dedicated Hosts | Single-tenant (Physical server level) | Yes | Bring Your Own License (BYOL) | Highest (Pay for the whole host) |
### Shared Tenancy (Default)
This is the default setting for almost all Amazon EC2 instances.
* **How it works:** Your instances run on physical hardware that is shared with other AWS accounts.
* **Isolation:** Complete programmatic and security isolation is managed by the AWS hypervisor.
* **Best for:** Cost-optimized applications, development environments, and standard production workloads.
### Dedicated Instances
This option isolates your hardware at the AWS account level.

* **How it works:** Instances run on hardware dedicated to your specific AWS account. Other instances on that same physical machine will only belong to you.
* **Caveat:** You do not have visibility or control over instance placement on the hardware. If you stop and restart the instance, it may move to a different dedicated server.
* **Best for:** Satisfying strict corporate compliance or regulatory frameworks requiring physical tenant isolation.
### Dedicated Hosts
This option provides a physical server fully dedicated to your use with advanced visibility.

* **How it works:** You lease the entire physical server. You gain full visibility into the physical sockets and cores.
* **Placement control**: You can map instances directly to specific hosts using a Host ID, ensuring they stay on the exact same hardware even after restarts.
* **Best for:** Bring Your Own License (BYOL) software models—like Microsoft Windows Server or SQL Server—that require licensing tied to physical hardware sockets or cores.
### Important Considerations

* **VPC Tenancy:** When creating an Amazon VPC, you can set its default tenancy. A "Dedicated" VPC forces all instances launched within it to use Dedicated tenancy unless specified otherwise.
* **Tenancy Switching:** You can switch an instance's tenancy between Dedicated and Dedicated Host while it is stopped. However, you cannot convert an existing instance from Dedicated/Host back to a Shared default tenancy.
