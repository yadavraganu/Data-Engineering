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

# What Are Artifacts?
**Artifacts** in GitHub Actions are files or data generated during a workflow that you want to **persist**, **share between jobs**, or **download** after the workflow completes. Common use cases include:
- Test results
- Build outputs (e.g., binaries, logs)
- Coverage reports
- Deployment packages
## Uploading Artifacts
Use the official action: `actions/upload-artifact`
### Example:
```yaml
- name: Upload test results
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: results/
```
### Parameters:
- `name`: A name for the artifact (used for reference and download).
- `path`: Path to the file(s) or directory to upload.
You can upload multiple artifacts by repeating the step with different names and paths.
## Downloading Artifacts
Use: `actions/download-artifact`
### Example:
```yaml
- name: Download test results
  uses: actions/download-artifact@v4
  with:
    name: test-results
    path: ./downloaded-results
```
### Parameters:
- `name`: Name of the artifact to download.
- `path`: Destination directory for the downloaded files.

## Sharing Artifacts Between Jobs
To share data between jobs:
1. Upload the artifact in one job.
2. Use `needs:` to ensure the dependent job runs after.
3. Download the artifact in the dependent job.

### Example:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build output" > output.txt
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: output.txt

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: ./build
      - run: cat ./build/output.txt
```
## Artifact Retention & Limits
- **Default retention**: 90 days
- **Max size per artifact**: 5 GB
- **Max total size per workflow run**: 20 GB
- You can configure retention:

```yaml
with:
  retention-days: 30
```
## Best Practices

- Use clear, descriptive names for artifacts.
- Clean up unnecessary files before uploading.
- Use artifacts to decouple jobs and improve modularity.
- Avoid uploading sensitive data unless encrypted.
