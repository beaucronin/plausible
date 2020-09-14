# Plausible Python Library

The Plausible Python library makes it easy to connect to and use cloud resources from within serverless code such as AWS Lambda functions. Plausible automatically loads and configures these resources.

## Simple Example

Within a serverless function, you can easily reference and use the resources that you have defined in your Plausible application.

```python
import plausible as pbl

function handler():
    obj_store = pbl.resource.object_store.my_store
    osk = ObjectStoreKey("2020/10/10/foo.txt")
    obj_store.put(osk, "some text")

    return {
        "msg": "some message"
    }
```