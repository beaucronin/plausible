# Plausible Python Library

The Plausible Python library makes it easy to connect to and use cloud resources from within serverless code such as AWS Lambda functions. Plausible automatically loads and configures these resources.

- [Simple Example](#simple-example)
- [Application File Structure](#application-file-structure)
- [Usage Reference](#usage-reference)
  - [Accessing resources from a function](#accessing-resources-from-a-function)
  - [Function invocations](#function-invocations)
  - [Object stores](#object-stores)
  - [Key-Value stores](#key-value-stores)

## Simple Example

Within a serverless function, you can easily reference and use the resources that you have defined in your Plausible application.

```python
import plausible as pbl

def handler():
    obj_store = pbl.resource.object_store.my_store
    osk = ObjectStoreKey("2020/10/10/foo.txt")
    obj_store.put(osk, "some text")

    return {
        "msg": "some message"
    }
```

## Application File Structure

The Python-language framework library requires that Plausible applications be laid out in the [standard manner](README.md). Within that overall structure, Plausible functions that are written in Python should be organized as follows:

```
<app name>
└── functions
    ├── <python function 1>
    │   ├── function.py
    │   └── [requirements.txt]
    └── <python function 2>
        ├── function.py
        └── [requirements.txt]
```

## Usage Reference

### Accessing resources from a function

The Plausible client library is designed for extreme clarity and ease of use. All functionality can be accessed via a singleton object:

```python
import plausible as pbl

def handler():
    my_resource = pbl.resource.RESOURCE_TYPE.RESOURCE_NAME
```

In a properly-configured Plausible function, this singleton will grant access to all of the resources controlled by the Plausible application. Specific examples of how to access these resources will be shown below.

### Function invocations

Each time a Plausible function is invoked, the framework will populate its root object with the content and context of the triggering event, as well as the defined outputs.

```python
trigger = pbl.function.current_trigger

```

### Object stores

Object stores contain unstructured, binary values that are associated with a string key. The primary operations are to `get` and `put` the values of these objects, as well as to `delete` them.

```python
store = pbl.resource.object_store.my_store

key = "foo/bar.txt"
input_val = "Here is some data - it's a string, but it can be anything"
store.put(key, val)

output_val = store.get_string(key)

assert input_val == output_val
```

Objects can be read in several ways - as binary (`get_binary`), strings (`get_string`), or objects (`get_object`). Likewise, the `put` object will accept most types, including objects, strings, bytes, and any corresponding IO stream.

### Key-Value stores

```python
store = pbl.resource.keyvalue_store.kv_store


```