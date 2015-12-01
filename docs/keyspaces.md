# Keyspace Operations

The following methods are provided for updating data within a keyspace.

## `reflect.Keyspace`

### `append(key, records)`

Appends a record or multiple records to a tablet. If the tablet doesn't exist
it will be created. records can be either a single object or an array of
objects. A single object represents a single row.

For more info, see the [Uploading Data Reflect API reference](https://reflect.io/docs/api-reference/uploading-data.html).

#### Parameters

* **key** - The key for the tablet you're appending to.
* **records** - The records to append to the tablet.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
keyspace = client.keyspace('my-keyspace-slug')
keyspace.append("my-key", { "column1": "Hello", "column2": "World" })
```

### `replace(key, records)`

Replaces the existing records in a tablet with a new set of records.  The
`records` parameter can be either a single object or an array of objects. A
single object represents a single row.

For more info, see the [Uploading Data Reflect API reference](https://reflect.io/docs/api-reference/uploading-data.html).

#### Parameters

* **key** - The key for the tablet you're appending to.
* **records** - The records to append to the tablet.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
keyspace = client.keyspace('my-keyspace-slug')
keyspace.replace("my-key", { "column1": "Hello", "column2": "World" })
```

### `patch(key, records, criteria)`

Patches the existing records in a tablet with the set of supplied records. The
`criteria` parameter indicates which records to match existing records on.  In
the Reflect API, if no existing records match the supplied records then those
records are dropped.

For more info, see the [Uploading Data Reflect API reference](https://reflect.io/docs/api-reference/uploading-data.html).

#### Parameters

* **key** - The key for the tablet you're appending to.
* **records** - The records to append to the tablet.
* **criteria** - An array of field names within a record to match.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
keyspace = client.keyspace('my-keyspace-slug')
keyspace.patch("my-key", { "column1": "Hello", "column2": "World" }, ['column1'])
```

### `upsert(key, records, criteria)`

Patch the existing records in a tablet with a new set of records and
insert any that aren't matched. The criteria parameter indicates which
records to match existing records on.

For more info, see the [Uploading Data Reflect API reference](https://reflect.io/docs/api-reference/uploading-data.html).

#### Parameters

* **key** - The key for the tablet you're appending to.
* **records** - The records to append to the tablet.
* **criteria** - An array of field names within a record to match.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
keyspace = client.keyspace('my-keyspace-slug')
recs = [
  { "column1": "Hello", "column2": "World" },
  { "column1": "Again", "column2": "I say HELLO" }
]

keyspace.upsert("my-key", recs, ["column1"])
```

### `delete(key)`

Delete a tablet within a keyspace. If the specified tablet exists, this is a
no-op but won't be reported as such to the client.

For more info, see the [Uploading Data Reflect API reference](https://reflect.io/docs/api-reference/uploading-data.html).

#### Parameters

* **key** - The key for the tablet you're appending to.

#### Example

```python
import reflect

client = reflect.Client("<API Token>")
keyspace = client.keyspace('my-keyspace-slug')
keyspace.delete("my-key")
```
