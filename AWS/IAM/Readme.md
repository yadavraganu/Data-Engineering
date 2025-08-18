## AWS IAM Policy Type

### Core IAM Policy Types

| Policy Type              | Description                                                                                  | Use Case Example                                  |
|--------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------------|
| **Identity-based**       | Attached to IAM users, groups, or roles. Grants permissions to those identities.             | Allow a user to access S3 buckets.                |
| **Resource-based**       | Attached directly to AWS resources (e.g., S3 buckets, Lambda functions).                     | Allow cross-account access to an S3 bucket.       |
| **Managed Policies**     | Standalone policies managed by AWS or the user. Can be reused across identities.             | AWS-managed: `AmazonEC2ReadOnlyAccess`<br>Customer-managed: Custom EC2 access policy |
| **Inline Policies**      | Embedded directly into a single IAM identity. Cannot be reused.                              | One-off permissions for a specific user.          |

###  Advanced Policy Types

| Policy Type                   | Description                                                                                      | Use Case Example                                  |
|-------------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------|
| **Permissions Boundaries**    | Defines the maximum permissions an identity-based policy can grant.                             | Limit a developer role to read-only access.       |
| **Service Control Policies (SCPs)** | Used in AWS Organizations to define max permissions for accounts or OUs.                       | Prevent accounts from deleting CloudTrail logs.   |
| **Session Policies**          | Passed during role assumption to limit permissions for the session duration.                    | Temporary access with restricted actions.         |
| **Access Control Lists (ACLs)** | Legacy mechanism for controlling access to resources like S3 and Amazon VPC.                    | Grant public read access to an S3 object.         |
