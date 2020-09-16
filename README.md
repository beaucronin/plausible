# Plausible

![Integration Tests](https://github.com/beaucronin/plausible/workflows/integration-tests/badge.svg)

Serverless approaches are very exciting, but they have come of age in the context of public cloud platforms that must meet the needs of a very wide range of requirements and development contexts. There is no "pure play" serverless cloud that includes all of the components necessary to build applications that deliver all of the benefits of serverless methods. Instead, their position as junior members of major cloud platforms  serverless capabilities to be obscured, compromised, and under-invested - a better serverless world is possible.

Plausible is a (currently experimental) framework whose primary goal is to improve by 10x developer productivity in writing serverless applications. These gains will be delivered by a combination of the following methods:

1. *Modern cloud providers have contually added new services over many years, to the point where a single developer can't be familiar with all of them and significant effort must be expended just to learn which ones are essential.* 
   * => Reduce the number of resource types to the core primitives that are most commonly used in serverless applications. 
2. *Individual cloud services must serve large developer audiences with diverse requirements, most of which are irrelevant for new serverless applications.*
   * => In the spirit of opinoinated frameworks like Ruby on Rails, lean heavily on conventions and defaults to simplify development and reduce cognitive load. Be fearless about excluding features that do not pay their way in value for the complexity they bring.
3. *Because of the breadth and diversity of use cases they must support, cloud providers have no choice but to compromise developer ergonomics. A more focused framework, conversely, is able to strike a different balance.*
   * => Fetishize developer experience, including highly idiomatic client libraries for the most common languages used in serverless applications

## Design Decisions

Use existing public cloud platforms as the host system, and implement the serverless-specific Plausible framework.

Make and exploit strong assumptions about the needs of typical serverless applications to create, connect, and configure multiple underlying cloud resources to implement a single Plausible resource.

Strive to eliminate boilerplate and near-boilerplate, and thereby maximize pithiness. Assume that developers reading the code are familiar with the framework, and elide the unnecessary bits. All code and configuration provided by the developer should carry meaning that is specific to the application in question - everything else is provided by the framework.

Be willing to carve out and impose new abstractions, even when those abstractions may be leaky across different underlying cloud providers. Part of the experimental nature of Plausible is to see if a new, reduced set of contracts would offer sufficient productivity gains to justify a ground-up serverless cloud implementation.

## Resource Primitives

Plausible includes the minimum set of primitives needed to implement the majority of serverless applications. Each plausible resource type has a close analog within each major cloud platform, although Plausible typically creates and manages multiple underlying cloud resources to implement the functionality of a single Plausible resource. For example, message queues and role-based authentication entities are automatically created to connect and secure these resources; in normal use, these elements will be automatically configured and provisioned.

| Plausible | AWS | Azure | GCP |
| --- | --- | --- | --- |
| Function | Lambda | Azure Function | Cloud Function |
| Object Store | S3 | Blob Store | Cloud Storage |
| Key-Value Store | DynamoDB | Cosmos | Firestore |
| Publisher | SNS + SQS | Event Grid | Pub/Sub |
| Stream Processor | Kinesis \[Firehose, Analytics\] | Stream Analytics | Cloud DataFlow |
| HTTP API | API Gateway | API Apps | Apigee API Management |

### Function
A function is the most general component of a Plausible application - an arbitrary program that can perform just about any input, processing, and output operations. While Plausible does not impose or enforce constraints on Functions, it does encourage certain patterns that, if followed, greatly simplify the design, analysis, and implementation of applications.

In particular, Plausible makes it very easy for functions to access and use other resources within the same Plausible application. When interacting with these sister resources, the function can use very high level operations that provide out of the box logging, data transformation, and error handling.

### Object Store
An object store provides read and write access to arbitrary unstructured data. Once an object store is configured, it can be used by other resources in various ways:

* Functions can read objects from and write them to the store
* Functions can be triggered by object store events such as object creation or deletion
* Stream Processors and Publishers can deliver messages and events to the object store

Object Stores can use arbitrary object naming and categorization schemes - each object is simply identified by its string key. Building on the conventions of services like S3, Plausible's object store offers the ability to specify and enforce the hierarchical structure of keys, so that key strings can be divided into a sequence of key components that, when concatenated, form a unique object identifier. This functionality formalizes and simplifies the most common key generation strategies that are already in use.

### Key-Value Store

### Publisher

### Stream Processor

### HTTP API

## Store Types

| Store Type | Cloud Implementations | Query Abilities | Item Properties |
| --- | --- | --- | --- |
| Key Value | DynamoDB, Cosmos Table API, Firestore | Partition + Range Keys | Semi-schematized rows |
| Object | S3, Blob Store, Cloud Storage | Exact key | Arbitrary size, unstructured blobs |
| File | EFS, Azure Files, Filestore | Exact path | Arbitrary size, hierarchically organized |
| Document | Aurora Serverless, Cosmos MongoDB API, Cloud Datastore | Complex queries on multiple document fields | JSON-style structured documents |
| Wide Column | Keyspaces, Cosmos Cassandra API, BigTable| Simple queries on composite primary key | Sparse, wide rows |

## Data Transformations

Many serverless functions are largely or entirely devoted to the transformation and dispatch of individual events or messages. Plausible allows for these common operations to be specified declaratively, which can reduce the procedural logic required in many functions and eliminate the need for other functions to be explicitly provided at all.

For example, consider a function that receives events from POST calls to an API endpoint, filters them, and then outputs them to two different destinations.

`infra/main.tf` -- 

```
resource "plausible_function" "f" {
    source = "${local.functions_home}/main/"

    api_route_trigger {
        api_id = <an api resource>
        route = "/submit"
        method = "POST"
    }

    output {
        name = "publish"
        target = plausible_publisher.my_publisher.id
    }

    output {
        name = "kv"
        target = plausible_keyvalue_store.my_kv.id
        transform = "<transform goes here>"
    }
}
```

`functions/main/function.py` --

```
def handler():
    obj = pbl.function.current_trigger.payload
    if "some_value" in obj["some_field"]:
        return obj
```

We know that `obj` conforms to the data model, and that it has been deserialized into a dict-like object.

## Cross-cutting Services

In addition to being opinionated and concise, Plausible is "batteries included". This included two main areas that are both universal and cumbersome in distributed, cloud-native applications: observability and access control. Plausible provides out-of-the-box, zero-configuration solutions for log capture and aggregation, application metrics and monitoring, and intra-application permissions.

### Logging and Log Aggregation

### Monitoring

### Permission and Authorization

## Application Structure

One of the primary ways that Plausible simplifies the developer experience and delivers improved productivity is by using strong conventions in project layout. Every Plausible app has the following folder structure:

```
root
├── project.yaml
├── apis/
│   └── my_api/
├── functions
│   │── foo/
│   └── bar/
├── infra
│   └── main.tf
└── vars.tf
```

## Infrastructure

Plausible uses Terraform to describe and create cloud resources. It uses a custom Terraform provider that, under the hood, creates, updates, and deletes the needed cloud resources. From a conceptual and design perspective, this infrastructure specification is on equal footing with the function and stream processing code that comprise the remainder of a Plausible app. Much of an application's core functionality will be defined within Terraform.

## What's Missing

### Relational Database

### Long-running processes

### Distributed Call Tracing

### Other API Formats

RPC, Websockets, GraphQL

### Explicit Orchestration

## Comparisons

### Serverless Framework

* Both aim to reduce or eliminate boilerplate
* Both are polyglot, and cross-cloud
* Plausible attempts to identify new abstractions for serverless applications that are platform-agnostic
* Plausible goes beyond functions to include other major components as first-class resource types
* Plausible places more emphasis on applications that create and maintain state - even as individual function invocations remain largely stateless
* Plausible provides more functionality in terms of the declarative specification of data transformations, including the automatic creation of functions to implement those transformations