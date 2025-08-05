## What Are Artifacts?

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
