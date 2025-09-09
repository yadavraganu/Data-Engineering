### **Detailed Workspace Admin Settings**

1. **SQL Warehouse Admin Settings**  
   Configure default settings for SQL warehouses, including compute sizes, scaling policies, and access modes. Helps standardize SQL workloads across the workspace.

2. **Enable Fleet Instance Types**  
   Allows use of AWS fleet instance types, which combine spot and on-demand instances for cost optimization and better availability.

3. **Data Access Configurations**  
   Set up secure access to cloud storage (like S3) using credential passthrough, Unity Catalog, or instance profiles. Ensures data governance and access control.

4. **Manage Databricks Previews**  
   Enable or disable experimental features that are in preview. Useful for testing new capabilities before they become generally available.

5. **Workspace Appearance Settings**  
   Customize the look and feel of the workspace:
   - **Plotly Toolbar**: Show/hide advanced chart controls.
   - **Color Palette**: Define custom dashboard colors.
   - **Language Support**: Enable multi-byte search (e.g., Chinese, Japanese).
   - **Date/Time Format**: Set default formats for visualizations.[2](https://docs.databricks.com/aws/en/admin/workspace-settings/appearance)

6. **Workspace Email Settings**  
   Configure email notifications for alerts, job failures, and workspace events.

7. **Default Access Mode for Jobs Compute**  
   Set whether job clusters default to shared or single-user mode, impacting data isolation and security.

8. **Manage Notification Destinations**  
   Define where system alerts are sent—email, webhook, or other endpoints.

9. **Auto-enable Deletion Vectors**  
   Automatically enables deletion vectors for Delta Lake tables, allowing efficient row-level deletes without rewriting entire files.

10. **Enable the Web Terminal**  
   Allows users to access a web-based terminal for debugging cluster nodes directly.

11. **Purge Workspace Storage**  
   Clean up unused files from DBFS and workspace storage to manage costs and maintain hygiene.

12. **Configure Notebook Result Storage Location**  
   Set a custom location (e.g., S3 bucket) for storing notebook outputs, useful for compliance and cost control.

13. **Manage Third-party Analytics Tools**  
   Control integrations with BI tools like Tableau, Power BI, and Looker.

14. **Manage Access to Notebook Features**  
   Enable or restrict features like real-time collaboration, commenting, and experimental UI elements.

15. **Disable the Upload Data UI**  
   Prevent users from uploading data via the UI to enforce controlled ingestion workflows.

16. **Manage the DBFS File Browser**  
   Enable or disable the DBFS browser to restrict file system access.

17. **Enforce User Isolation Cluster Types**  
   Require clusters to be single-user for better data isolation and security.

18. **Manage SSD Storage**  
   Configure SSD usage for high-performance workloads, especially for caching and temporary storage.

19. **Workspace Access for Databricks Personnel**  
   Temporarily allow Databricks support staff to access your workspace for troubleshooting. Access is:
   - Time-limited (up to 48 hours)
   - Audited
   - Approved only for relevant personnel

20. **Enforce AWS Instance Metadata Service v2**  
   Improve security by enforcing IMDSv2 for accessing AWS instance metadata, reducing exposure to SSRF attacks.

21. **Manage Instance Profiles**  
   Add or remove IAM instance profiles to control access to AWS resources from Databricks clusters.

22. **Restrict Workspace Admins**  
   Limit who can be assigned as workspace admins to enforce governance and reduce risk.
