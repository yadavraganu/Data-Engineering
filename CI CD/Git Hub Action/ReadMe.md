# Building Blocks of GitHub Actions
1.  **Workflows:**
    * **Definition:** A workflow is a configurable automated process defined by a YAML file (e.g., `main.yml`) located in your repository's `.github/workflows` directory.
    * **Purpose:** It's the highest level of organization for your automation. A single repository can have multiple workflows, each designed for a different purpose (e.g., one for building, one for testing, one for deployment).
    * **Triggers:** Workflows are triggered by events, manually, or on a defined schedule (cron jobs).

2.  **Events:**
    * **Definition:** An event is a specific activity in a repository that triggers a workflow run.
    * **Examples:** Common events include:
        * `push`: When code is pushed to a repository.
        * `pull_request`: When activity occurs on a pull request (e.g., opened, synchronized, closed).
        * `schedule`: To run workflows at specific times using cron syntax.
        * `workflow_dispatch`: To manually trigger a workflow from the GitHub UI or API.
        * `issue`: When an issue is opened, labeled, etc.
    * **Filtering:** Events can often be filtered to run only on specific branches, tags, or other criteria.

3.  **Jobs:**
    * **Definition:** A job is a set of sequential steps within a workflow that executes on the same runner.
    * **Purpose:** Jobs are independent of each other by default and can run in parallel. However, you can define dependencies between jobs, causing them to run sequentially (e.g., a "test" job running only after a "build" job completes successfully).
    * **Environment:** Each job specifies the `runs-on` property to define the type of runner (operating system) it will execute on.
    * **Outputs & Artifacts:** Jobs can produce outputs that can be consumed by subsequent jobs and can upload "artifacts" (files or directories) that persist after the job completes, allowing data to be shared across jobs or downloaded for later inspection.

4.  **Steps:**
    * **Definition:** Steps are individual tasks within a job. They are executed in the order they are defined.
    * **Purpose:** Steps perform the actual work of the job. If a step fails, the job typically stops executing subsequent steps.
    * **Types of Steps:**
        * **`run` scripts:** These execute shell commands directly on the runner (e.g., `npm install`, `python test.py`).
        * **`uses` actions:** These execute pre-defined, reusable units of code called "actions".

5.  **Actions:**
    * **Definition:** An action is a reusable unit of code that performs a specific task within a workflow.
    * **Purpose:** Actions encapsulate complex but common tasks, reducing the amount of repetitive code you need to write. They can be thought of as mini-applications for GitHub Actions.
    * **Sources:**
        * **GitHub Marketplace:** A vast collection of community-contributed and GitHub-maintained actions (e.g., `actions/checkout`, `actions/setup-node`).
        * **Custom Actions:** You can create your own actions (JavaScript, Docker container, or composite actions) and use them in your workflows or share them with others.
    * **Inputs & Outputs:** Actions can take inputs to customize their behavior and produce outputs that can be used by subsequent steps or jobs.

6.  **Runners:**
    * **Definition:** A runner is a server (virtual machine or container) that executes your workflow jobs.
    * **Types:**
        * **GitHub-hosted runners:** These are virtual machines provided by GitHub with various operating systems (Ubuntu, Windows, macOS) and pre-installed software. They are managed by GitHub and offer a convenient way to get started.
        * **Self-hosted runners:** You can host your own runners on your own infrastructure (servers, VMs, containers). This provides more control over the environment, hardware, and network access, which is useful for specific requirements (e.g., private networks, custom hardware, specific software).
    * **Isolation:** Each workflow run executes in a fresh, newly provisioned environment on the runner, ensuring isolation between runs.

An **Event** occurs (e.g., a code `push`). This triggers a **Workflow** (defined in a YAML file). The workflow then executes one or more **Jobs**. Each job runs on a dedicated **Runner** and consists of a sequence of **Steps**. These steps either run shell commands (`run`) or leverage pre-built, reusable **Actions** (`uses`).

# GitHub Actions Artifacts Guide
**Artifacts** are the files generated during a workflow run (e.g., binaries, test reports) that allow you to **persist data** after a run finishes or **bridge the gap** between isolated jobs.
## 1. Uploading Artifacts
Use `actions/upload-artifact@v4` to move data from the runner to GitHub’s cloud storage.
### Implementation
```yaml
- name: Upload Build Output
  uses: actions/upload-artifact@v4
  with:
    name: release-assets  # Unique reference name
    path: dist/           # Directory or specific file
    retention-days: 30    # Optional: How long to keep it (Default 90)
```
## 2. Downloading Artifacts
Use `actions/download-artifact@v4` to retrieve files in a later job or for manual inspection after the workflow completes.
### Implementation
```yaml
- name: Download Assets
  uses: actions/download-artifact@v4
  with:
    name: release-assets
    path: ./target-dir    # Local path to place files
```
## 3. Deleting Artifacts
Use `actions/delete-artifact@v5` to manually remove artifacts. This is perfect for cleaning up temporary "bridge" files to save storage space and keep your UI clean.
### Implementation
```yaml
- name: Remove Temporary Logs
  uses: actions/delete-artifact@v5
  with:
    name: temp-build-logs
```
## 4. Sharing Between Jobs (The Workflow)
Since jobs run on **isolated runners**, they do not share a filesystem. You must upload in Job A and download in Job B.
### Example: Build, Test, and Cleanup
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "v1.0.0-build" > build_id.txt
      - uses: actions/upload-artifact@v4
        with:
          name: bridge-data
          path: build_id.txt

  test:
    needs: build # Ensures jobs run in sequence
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: bridge-data
      - run: cat build_id.txt
      
  cleanup:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/delete-artifact@v5
        with:
          name: bridge-data
```
## Limits & Best Practices
### Storage & Retention
| Feature | Limit / Default |
| :--- | :--- |
| **Default Retention** | 90 Days |
| **Max File Size** | 5 GB per artifact |
| **Total Run Limit** | 20 GB per workflow |
| **Performance** | v4 is up to 10x faster than v3 |
### Pro-Tips
* **Security:** Never upload `.env` files, SSH keys, or secrets. Artifacts are accessible to anyone with "Read" access to the repository.
* **Wildcards:** You can use patterns like `path: dist/**/*.js` to upload specific file types.
* **Storage Management:** If an artifact is only needed for the workflow duration, use `retention-days: 1` or the `delete-artifact` action in your final job.
* **Zip Efficiency:** For directories with thousands of small files, zip them manually before uploading to significantly increase upload speeds.

# Job/Step Outputs
Outputs are essentially the return values of your GitHub Actions. They allow you to capture data generated in one step or job and pass it along to subsequent steps or jobs in your workflow. 
If you have stumbled upon older tutorials referencing `::set-output`, just know that it is heavily deprecated. Today, we use the `$GITHUB_OUTPUT` environment file. Let's break down how this works!
## 1. Step Outputs (Sharing Data Within the Same Job)
To pass information between steps in the **same job**, you save a key-value pair to the `$GITHUB_OUTPUT` file.
### How to set it:
Give your step a unique `id` and append your custom variable to `$GITHUB_OUTPUT`.
```yaml
- name: Generate a value
  id: generator # Highly important! You need an ID to reference this step later.
  run: |
    echo "MY_VALUE=awesome-sauce" >> "$GITHUB_OUTPUT"
```
### How to use it:
Access it in a later step within the same job using the `steps` context: `${{ steps.<step_id>.outputs.<key_name> }}`.
```yaml
- name: Consume the value
  run: |
    echo "The value generated was ${{ steps.generator.outputs.MY_VALUE }}"
```
## 2. Job Outputs (Sharing Data Between Different Jobs)
By default, jobs run in entirely separate isolated environments on different runners. This means steps in `job2` cannot natively see what happened in `job1`. To solve this, you can expose that data as a **job output**.
To pass information between jobs, you must follow this sequence:
1. Set the output at the **step** level in the first job.
2. Map that step output to a **job** level output.
3. Use the `needs` context in the second job to pull it down.
### Example Workflow:
```yaml
name: Job Outputs Demo
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    # 2. Map the step output to the job output
    outputs:
      artifact_id: ${{ steps.create_build.outputs.build_id }}
    steps:
      - name: Create Build
        id: create_build
        # 1. Set the output at the step level
        run: echo "build_id=45678" >> "$GITHUB_OUTPUT"
  deploy:
    runs-on: ubuntu-latest
    needs: build # Required to wait for the first job and inherit its outputs
    steps:
      - name: Deploy Build
        # 3. Pull the output using the needs context
        run: |
          echo "Deploying artifact with ID: ${{ needs.build.outputs.artifact_id }}"
```
## 3. Handling Multi-line Outputs
If you've ever tried to shove multi-line text (like the contents of a file or a JSON payload) into `$GITHUB_OUTPUT` using standard `echo`, you probably received an error or truncated data. 
To resolve this, you must use a unique delimiter (like `EOF`).
### Example:
```yaml
- name: Generate Multi-line Output
  id: multiline_step
  run: |
    {
      echo "MY_TEXT<<EOF"
      echo "Line 1 of the output"
      echo "Line 2 of the output"
      echo "EOF"
    } >> "$GITHUB_OUTPUT"

- name: Read Multi-line Output
  run: |
    echo "${{ steps.multiline_step.outputs.MY_TEXT }}"
```
Make sure your delimiter text (like `EOF`) doesn't accidentally appear inside the body of the text you are outputting, or the parsing will break!
