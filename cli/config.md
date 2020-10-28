
## <a name="plausible_app_config"></a>[#](#plausible_app_config) `plausible_app_config` :: Object 

The outermost element in a Plausible application specification 


    
```yaml
app_name: my_app
resources:
    - foo_resource:
        ...
    - bar_resource:
        ...
```

* **`app_name`**: The name of the application, which is used in various ways to uniquely identify the resources belonging to it
* [**`resources`**](#resources)

## <a name="resource_types"></a>[#](#resource_types) `resource_types` :: List 

The list of resources that comprise the application 

* [**`function`** =>](function.md)
* [**`http_api`** =>](http_api.md)
* [**`publisher`** =>](publisher.md)
* [**`object_store`** =>](object_store.md)
* [**`keyvalue_store`** =>](keyvalue_store.md)
* [**`stream_analytics`** =>](stream_analytics.md)


# <a name="function"></a>[#](#function) **Resource**: `function` 

The function resource, which is the programmatic building block of Plausible applications. Functions are the primary home for executable code, whereas the remaining config is provided in declarative terms. 


    
```yaml
- function:
    name: my-function
    triggers:
    - schedule:
        cron: "5 0 * * * *"
    outputs:
    my-output:
        target: "keyvalue_store.kv"
```

* **`name`**: The name of the function
* [**`triggers`** (Opt)](#triggers)
* [**`outputs`** (Opt)](#outputs)

## <a name="triggers"></a>[#](#triggers) `triggers` :: List 

The trigger or triggers that determine when this function will be invoked. 

* [**`trigger`** =>](trigger.md)

## <a name="outputs"></a>[#](#outputs) `outputs` :: Map 

The (named) outputs of the function, which will receive or be triggered by the messages that are emitted by the function. The marshaling and connectivity will all be handled by the Plausible client library and the deployment 

* **Key**: 
*String* The name of the output, as it will be referenced through the client library from within the function implementation. 

* [**`Value`**](#)

## <a name="output"></a>[#](#output) `output` :: Object 

The target resource and, optionally, any transforms or filters that are applied before it is invoked. 

* **`target`**: The name of the resource that will receive or be triggered by the messages sent over this output

* [**`transform`** =>](transform.md)
* [**`filter`** =>](filter.md)

# <a name="http_api"></a>[#](#http_api) **Resource**: `http_api` 

The resource type representing an HTTP API. It is described through a valid OpenAPI 3.0 specification 


    
```yaml
- http_api:
    name: my-api
```

* **`name`**: The name of the API.


# <a name="publisher"></a>[#](#publisher) **Resource**: `publisher` 

The publisher resource, which is a combined pub/sub topic and message queue. Like a queue store, a publisher can store messages for a period of time until they are successfully consumed by the subscribers. And like a notification topic, a publisher can deliver messages to multiple subscribers. 


    
```yaml
- publisher:
    name: my-publisher
```

* **`name`**: The name of the publisher


# <a name="object_store"></a>[#](#object_store) **Resource**: `object_store` 

The object store resource, which is capable of storing binary objects (blobs) at key addresses. These objects can correspond to many things, from text files to digital media to archived data. 


    
```yaml
- object_store:
    name: my-store
```

* **`name`**: The name of the object store`


# <a name="keyvalue_store"></a>[#](#keyvalue_store) **Resource**: `keyvalue_store` 

The key-value store resource 

* **`name`**: The name of the keyvalue store resource
* **`collection_name`**: The name of the underlying key-value collection
* [**`primary_index`**](#primary_index)
* [**`secondary_index`** (Opt)](#secondary_index)


## <a name="primary_index"></a>[#](#primary_index) `primary_index` :: Object 

The required primary index for the key-value collection, comprising a required partition key and an optional, sortable row key 

* **`partition_key`**: The key which is hashed to obtain the partition or shard under which the value will be stored
* **`row_key`** (Opt): The key which differentiates and orders the items which share a partition key value.

## <a name="secondary_indexes"></a>[#](#secondary_indexes) `secondary_indexes` :: Map 

The optional secondary indexes for the collection, of which there can be zero or more 

* **Key**: 
*String* The name of the secondary index 

* [**`Value`**](#)

## <a name="secondary_index"></a>[#](#secondary_index) `secondary_index` :: Object 

A secondary index for the key-value collection, comprising a required partition key and an optional, sortable row key 

* **`partition_key`**: The key which is hashed to obtain the partition or shard under which the value will be stored
* **`row_key`** (Opt): The key which differentiates and orders the items which share a partition key value.


# <a name="stream_analytics"></a>[#](#stream_analytics) **Resource**: `stream_analytics` 

The stream analytics resource, which processes events on a windowed basis, possibly filtering, grouping by, and aggregating 

* **`name`**: The name of the stream analytics resource
* **`source`**: The name of the resource that sends messages or events to the stream processor
* [**`window`**](#window)
* [**`statements`** (Opt)](#statements)


## <a name="window"></a>[#](#window) `window` :: Object 

The basic attributes the define the analytics window, including its type and period 

* **`type`**: The type of temporal window; must be one of `sliding` or `stagger`
* **`interval`**: Integer *or* List

*Integer* The single interval, in seconds, that defines the window period 

## <a name="interval"></a>[#](#interval) `interval` :: List 

The multiple intervals, each in seconds, that define the window periods 

Item: *Integer* An interval, in seconds, that defines a window period 



## <a name="statements"></a>[#](#statements) `statements` :: Object 

The optional statements that further qualify the windowed processing 

* **`group_by`** (Opt): String *or* List
* [**`where`** (Opt)](#where)

*String* The value, other than the window times, by which to group the outputs of the window processor 

## <a name="group_bys"></a>[#](#group_bys) `group_bys` :: List 

A collection of values by which to group the outputs of the window processor 

Item: *String* The value, other than the window times, by which to group the outputs of the window processor 


## `no title` List 

 

## `no title` Map 

 

* **Key**: 
* [**`Value`**](#)
## `no title` FixedList 

 



## `no title` Object 

* [**`api_route`**](#api_route)


## `no title` Object 

* **`http_api`**: The name of the http_api to which the triggering route belongs
* **`route`**: The URL path for which requests will be handled by the function
* **`method`**: The HTTP method that
* [**`content_type`** (Opt)](#content_type)


## `no title` Object 

* [**`schedule`**](#schedule)


## `no title` Object 

A trigger that fires on a schedule 

* **`cron`**: A standard cron config string that describes when the trigger should fire


## `no title` Object 

* [**`subscription`**](#subscription)


## `no title` Object 

A trigger that fires when an event or message is recived via a subscription to a publisher 

* **`publisher`**: The name of the publisher whose events cause the trigger to fire


## `no title` Object 

* [**`function`**](#function)


## `no title` Object 

A trigger that fires whenever a calling function returns an event or message 

* **`caller`**: The name of the function whose outputs fire the trigger

