# The Basics

These are the basic operations to get up and running with the client.

## `reflect.Client`

### `reflect.Client(api_token)`

Instantiate a new version of the Reflect API client.

#### Parameters

* **api_token** - The API token to connect to Reflect with.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
```

## `generateToken(secretKey, params)`

Use the `generateToken` function to create a signed authentication token to use
when authenticating with Reflect.

#### Parameters

* **secretKey** - The secret key for the project you want to embed.
* **params** - An array of parameter objects.

#### Example

```python
import reflect

REFLECT_PROJECT_SECRET_KEY = "abc123-my-secret-key-xyz987"

params = [
  {
    "field": "My Field",
    "op": "=",
    "value": "abc123"
  }
]

signedToken = reflect.generateToken(REFLECT_PROJECT_SECRET_KEY, params)
```
