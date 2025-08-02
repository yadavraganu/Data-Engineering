## Environment Variables (env)
Environment variables are used to pass non-sensitive configuration values to your workflow
### Define Globally
```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com
```
### Define Per Job or Step
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      BUILD_ENV: staging
    steps:
      - name: Print env
        run: echo "Build environment is $BUILD_ENV"
```
## Secrets (secrets)
Secrets are encrypted values stored in GitHub and used for sensitive data like tokens, passwords, and API keys.
### Define in GitHub UI
Go to Repo Settings → Secrets and Variables → Actions → New Repository Secret
### Use in Workflow
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret
        run: echo "Using secret: ${{ secrets.API_KEY }}"
```
```yaml
name: Deploy App
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production
      API_URL: https://api.example.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Use secret directly
        run: echo "Deploying with token: ${{ secrets.DEPLOY_TOKEN }}"
      - name: Run deployment script
        run: |
          echo "Environment: $NODE_ENV"
          echo "API URL: $API_URL"
          ./deploy.sh
