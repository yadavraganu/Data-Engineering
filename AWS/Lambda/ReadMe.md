## Layers
AWS Lambda Layers are a way to package libraries, custom runtimes, and other dependencies to be used by multiple Lambda functions. They help to manage dependencies, reduce the size of your deployment package, and promote code sharing across your functions.

### How to Set Up Layers for a Python Application

To set up a Lambda Layer for a Python application, follow these steps:

1.  **Prepare your dependencies**: Create a directory named `python` and place all your necessary libraries (e.g., via `pip install -t python <library_name>`) inside it. This specific directory structure is crucial, as AWS Lambda looks for Python modules in a folder named `python`.
2.  **Create a .zip file**: Zip the `python` directory. The structure should be `python/your_libraries`.
3.  **Upload to AWS Lambda**:
    * Navigate to the AWS Lambda console.
    * Click on **Layers** in the left navigation pane.
    * Click **Create layer**.
    * Provide a name and description for your layer.
    * Upload the .zip file you created.
    * Select the compatible runtime (e.g., Python 3.9).
4.  **Attach the layer to your function**:
    * Go to your Lambda function's configuration page.
    * In the **Designer** section, click on **Layers**.
    * Click **Add a layer**.
    * Select the layer you just created from the list and choose a version.
    * Click **Add**.

Your Lambda function can now access the libraries from the layer as if they were in the function's own deployment package.

### Where Are Layers Stored?

Lambda Layers are stored in a centralized location managed by AWS. They are not stored within your function's deployment package. Each layer is versioned, and a specific version of a layer is immutable. When you attach a layer to a function, Lambda mounts the layer's content to the `/opt` directory in the function's execution environment. This is why you need to ensure your libraries are in the `python` folder within the .zip file, as this becomes `/opt/python` in the Lambda environment.

### When to Use Layers

Use Lambda Layers in the following scenarios:

* **Sharing code between functions**: If you have multiple functions that use the same set of libraries (e.g., a database driver, an SDK, or a common utility library), a layer is an efficient way to manage and share them.
* **Reducing deployment package size**: A Lambda function's deployment package has a size limit. By moving bulky libraries to a layer, you can keep your function code small, which speeds up deployments and makes them easier to manage.
* **Managing dependencies**: Layers simplify dependency management. Instead of bundling the same large libraries with every function, you can update the library in one place (the layer) and then just update the layer version for all dependent functions.
* **Custom runtimes**: Layers can be used to package and deploy custom runtimes, allowing you to write Lambda functions in languages not natively supported by AWS.

### Benefits of Using Layers

* **Smaller deployment packages**: Leads to faster deployments and easier management of function code.
* **Reduced build time**: By separating dependencies, you only need to update and deploy the layer when dependencies change, not every single function.
* **Code sharing and reusability**: Promotes a more modular and organized architecture by centralizing common components.
* **Improved development workflow**: Teams can independently manage function code and shared libraries, leading to a more efficient development process.
* **Simplified management**: It's easier to maintain and update a single layer than to manage dependencies across dozens or hundreds of functions.

### CLI Setup
Setting up AWS Lambda layers for a Python application using the AWS CLI is a three-step process: package your dependencies, publish the layer, and then attach it to your function.

#### Step 1: Package Your Dependencies

First, you need to prepare your dependencies in the correct directory structure. For a Python layer, all your packages must be in a folder named `python`.

1.  Create the `python` directory:
    ```bash
    mkdir python
    ```
2.  Install your required libraries into this directory using `pip`:
    ```bash
    pip install <package-name> -t python/
    ```
    Repeat this for all the packages you need.
3.  Zip the `python` folder. This is the file you'll upload to AWS.
    ```bash
    zip -r my-python-layer.zip python/
    ```
    The zipped file will have a structure where the `python` directory is at the root.

#### Step 2: Publish the Layer

Once you have the `.zip` file, you can publish it as a new Lambda layer version using the `aws lambda publish-layer-version` command.

```bash
aws lambda publish-layer-version \
    --layer-name my-python-layer \
    --description "My custom Python dependencies" \
    --zip-file fileb://my-python-layer.zip \
    --compatible-runtimes python3.9 python3.10 python3.11 \
    --region us-east-1
```

  * `--layer-name`: A unique name for your layer.
  * `--description`: A brief description of what the layer contains.
  * `--zip-file fileb://...`: Specifies the path to your zipped file. The `fileb://` prefix indicates that the content is a binary file.
  * `--compatible-runtimes`: A space-separated list of Python runtimes that can use this layer.
  * `--region`: The AWS region where you want to create the layer.

This command will output a JSON object containing details about the new layer version, including its **LayerVersionArn**. You'll need this ARN to attach the layer to a function.

## Lambda with VPC

By default, AWS Lambda functions run in a VPC managed by AWS, not your own. You need to configure a function to run inside your own Virtual Private Cloud (VPC) to access resources that are not publicly available, like an Amazon Relational Database Service (RDS) database or an Amazon ElastiCache cluster.

### VPC Configuration Steps

1.  **Create an IAM Role with VPC Permissions**: Your function's execution role must have permissions to manage network interfaces. The managed policy `AWSLambdaVPCAccessExecutionRole` grants the necessary permissions: `ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`, and `ec2:DeleteNetworkInterface`.
2.  **Attach the Function to a VPC**: You configure the Lambda function by specifying a VPC, two or more subnets across different Availability Zones for high availability, and one or more security groups. When the function is invoked, Lambda creates an Elastic Network Interface (**ENI**) in one of your chosen subnets, which allows the function to communicate with other resources inside that VPC. 

### Important Considerations

* **No Internet Access by Default**: When a Lambda function is connected to your VPC, it loses its default internet access. If the function needs to connect to the public internet (e.g., to fetch data from a public API), you must configure a **NAT Gateway** in a public subnet and set up routing from the private subnet where the function's ENI resides.
* **Security Groups**: The security groups you assign control the inbound and outbound traffic for the function. You must configure them to allow communication with the specific resources it needs to access within the VPC.
* **Performance**: Attaching a Lambda function to a VPC can increase cold start times because of the time it takes for AWS to create and attach the ENI.
* **IP Address Exhaustion**: Each ENI consumes an IP address from the subnet. If your function scales up rapidly and the subnets are too small, you could run out of available IP addresses, which would prevent your function from scaling further.
* **Hyperplane ENIs**: To improve performance and reusability, AWS uses a technology called Hyperplane to manage ENIs more efficiently. This allows multiple function invocations to share ENIs.

## Throttling
When AWS Lambda receives more concurrent or rapid-fire invocation requests than your account or function-level limits allow, it rejects the excess requests with a 429 TooManyRequestsException. This rejection behavior is called throttling.  

### What Is Throttling?

Throttling is AWS Lambda’s built-in mechanism to protect its infrastructure and ensure fair resource usage across all customers. When your function’s invocation rate or concurrent executions exceed specified quotas, Lambda starts returning 429 errors instead of processing new invocations.  

### When Does Throttling Happen?

- Account concurrency limit is exceeded (default 1,000 concurrent executions per region).  
- Reserved concurrency for a specific function is reached if you’ve set a cap.  
- Burst concurrency limit is hit during a sudden spike; Lambda can only launch a finite number of new execution environments in a short period.  
- Downstream API calls inside your function are themselves throttled, causing your function to fail or retry.  

### Why Does Throttling Happen?

- Shared infrastructure must be protected from “noisy neighbor” effects.  
- Prevents runaway costs and resource exhaustion at hyper scale.  
- Encourages predictable performance by enforcing throughput boundaries.  
- Ensures long-running or heavily loaded functions can’t starve others of capacity.  

### How to Mitigate Throttling

1. Monitor and Analyze  
   - Use CloudWatch metrics: ConcurrentExecutions, Throttles, and IteratorAge (for stream-based triggers).  
   - Set alarms to detect rising throttle rates early.  

2. Reserve or Provision Concurrency  
   - Reserved Concurrency guarantees minimum capacity or caps max concurrency for critical functions.  
   - Provisioned Concurrency warms execution environments ahead of time for consistent performance and higher burst headroom.  

3. Implement Retry and Backoff Logic  
   - For synchronous calls: catch 429 errors and retry with exponential backoff and jitter.  
   - For asynchronous or event-source mappings: tune the retry policy, maximum retry attempts, and dead-letter queue.  

4. Smooth Invocation Patterns  
   - Buffer spikes using SQS or Kinesis between your clients and Lambda.  
   - Use Step Functions to orchestrate high-volume workflows with built-in error handling.  

5. Optimize Function Runtime  
   - Reduce execution time by right-sizing memory. Shorter functions free up concurrency faster.  
   - Break monolithic flows into smaller, independent Lambdas to spread the load.  
