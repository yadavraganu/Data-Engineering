## **Step Functions Variable Control Table**

| Field         | Purpose | Default Behavior | Example | Result |
|---------------|---------|------------------|---------|--------|
| **InputPath** | Filters the input to the state | Entire input is passed | `"InputPath": "$.user"` | Only `user` object is passed to the state |
| **Parameters** | Constructs custom input using JSONPath | Input (after InputPath) is passed as-is | `"Parameters": { "id.$": "$.user.id" }` | Input reshaped to `{ "id": 1 }` |
| **ResultPath** | Specifies where to place the result | Result replaces input | `"ResultPath": "$.result"` | Merges result under `result` key |
| **OutputPath** | Filters output passed to next state | Entire result is passed | `"OutputPath": "$.result.status"` | Only `status` value is passed forward |
