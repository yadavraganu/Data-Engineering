```yaml
name: Set and Use Output Example
on: [push]
jobs:
  job1:
    name: Generate Output
    runs-on: ubuntu-latest
    outputs:
      customMessage: ${{ steps.setMessage.outputs.message }}
    steps:
      - name: Set a custom message
        id: setMessage
        run: echo "message=Hello from Job 1!" >> $GITHUB_OUTPUT
  job2:
    name: Use Output from Job1
    needs: job1
    runs-on: ubuntu-latest
    steps:
      - name: Print job output
        run: echo "Received message: ${{ needs.job1.outputs.customMessage }}"
      - name: Save message to file
        run: echo "${{ needs.job1.outputs.customMessage }}" > message.txt
```
