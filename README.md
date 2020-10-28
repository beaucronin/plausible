# Plausible

![Integration Tests](https://github.com/beaucronin/plausible/workflows/integration-tests/badge.svg)

- [Design Decisions](#design-decisions)
- [Resource Primitives](#resource-primitives)
  - [Function](#function)
  - [Object Store](#object-store)
  - [Key-Value Store](#key-value-store)
  - [Publisher](#publisher)
  - [Stream Processor](#stream-processor)
  - [HTTP API](#http-api)
- [Store Types](#store-types)
- [Data Transformations](#data-transformations)
- [Cross-cutting Services](#cross-cutting-services)
  - [Logging and Log Aggregation](#logging-and-log-aggregation)
  - [Monitoring](#monitoring)
  - [Permission and Authorization](#permission-and-authorization)
- [Application Structure](#application-structure)
- [Infrastructure](#infrastructure)
- [What's Missing](#whats-missing)
  - [Relational Database](#relational-database)
  - [Long-running processes](#long-running-processes)
  - [Distributed Call Tracing](#distributed-call-tracing)
  - [Other API Formats](#other-api-formats)
  - [Explicit Orchestration](#explicit-orchestration)
- [Comparisons](#comparisons)
  - [Serverless Application Model (SAM) + CloudFormation](#serverless-application-model-sam--cloudformation)
  - [Chalice](#chalice)
  - [Up](#up)
  - [Terraform](#terraform)
  - [Serverless Framework](#serverless-framework)
  - [Temporal](#temporal)
  - [Dark](#dark)
  - [Summary](#summary)

Serverless approaches are very exciting, but they have come of age in the context of public cloud platforms that must meet the needs of a very wide range of requirements and development contexts. There is no "pure play" serverless cloud that includes all of the components necessary to build applications that deliver all of the benefits of serverless methods. Instead, their position as junior members of major cloud platforms  serverless capabilities to be obscured, compromised, and under-invested - a better serverless world is possible.

Plausible is a (currently experimental) framework that is unabashedly focused on greenfield development of projects that do not necessarily fit the backend enterprise mold. Its primary goal is to improve developer productivity in writing serverless applications by at least 10x. These gains will be delivered by a combination of the following methods:

1. *Modern cloud providers have continually added new services over the years, to the point where a single developer can't be familiar with all of them and significant effort must be expended just to learn which ones are essential.* 
   * => Reduce the number of resource types to the core primitives that are most commonly used in serverless applications. 
2. *Individual cloud services must serve large developer audiences with diverse requirements, most of which are irrelevant for new serverless applications.*
   * => In the spirit of opinionated frameworks like Ruby on Rails, lean heavily on conventions and defaults to simplify development and reduce cognitive load. Be fearless about excluding features that do not pay their way in value for the complexity they bring.
3. *Because of the breadth and diversity of use cases they must support, cloud providers have no choice but to compromise developer ergonomics. A more focused framework, conversely, is able to strike a different balance.*
   * => Fetishize developer experience, including highly idiomatic client libraries for the most common languages used in serverless applications

If successful, there will be another significant driver of productivity: small teams will be able to complete applications that would previously required large or multiple teams, and projects that previously required a team can be developed by an individual. Even in high-functioning teams, coordination represents a significant tax.

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
| GraphQL API | AppSync | | |

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
A key-value store contains data items that are associated with one or more keys. Because of their simplifications relative to traditional relational databases, key-value stores can scale to almost arbitrary amounts of data.

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
├── config.yaml
├── apis/
│   └── my_api/
└── functions/
    │── foo/
    └── bar/
```

## Infrastructure

Plausible uses Terraform to describe and create cloud resources. It uses a custom Terraform provider that, under the hood, creates, updates, and deletes the needed cloud resources. From a conceptual and design perspective, this infrastructure specification is on equal footing with the function and stream processing code that comprise the remainder of a Plausible app. Much of an application's core functionality will be defined within Terraform.

## What's Missing

### Relational Database

Traditional relational databases have been slow to become available under a fully serverless access model.

### Long-running processes

AWS Lambda functions and Google Cloud Functions have strict limits on the total runtime per invocation; Azure Functions have similar limites in standard tiers, and the availability of unlimited invocation times at higher service tiers.

### Distributed Call Tracing

### Other API Formats

RPC, Websockets, GraphQL

### Explicit Orchestration

## Comparisons

### Serverless Application Model (SAM) + CloudFormation

CloudFormation and SAM are AWS-native infrastructure-as-code tools that offer little or no abstraction over the underlying AWS APIs. With some minor exceptions in SAM, individual AWS resources must be specified, connected, and managed. CloudFormation allows this to be performed declaratively rather than imperatively, but the architectural complexity remains the same as any other method of configuring AWS.

And like other AWS tools - such as the command line interface, or the various language-specific SDKs - CloudFormation must cover the entire API of every AWS service. Because these services have very different interaction models and use cases, any interface that must support all of them is going to require major compromises in ergonomics.

**Business Model**: An AWS service, free in and of itself but directly tied to the cost of the managed AWS resources.

### Chalice

[Chalice](https://aws.github.io/chalice/) was revolutionary when it first appeared in 2016, and it is still an awesome framework. It was one of the first tools that enabled dead simple integration of HTTP endpoints within an API gateway with Lambda functions. This is still its core capability, although the framework has been extended over the years to include a number of other function triggers - queue and topic messages, object store events, scheduled execution, and so on.

While Chalice can be used to create serverless function pipelines and other more complex applications, its design is geared toward serverless functions that are triggered by a single external source. Chalice does not offer any way to declaratively specify interconnections between functions, nor does it offer any way to connect functions to data stores. These application elements must described by other means, such as a linked Terraform config. But once an application reaches this level of complexity, Chalice may not be the right tool for the job.

Chalice is unusual in that it explicitly provides an abstraction layer over several kinds of AWS resources: Lambdas, SQS queues, API Gateway resources, CloudFront distributions, IAM roles, and more. It remains one of the easiest ways to create a 100% utilization, auto-scaling HTTP API.

**Business Model**: An AWS service, free in and of itself but directly tied to the cost of the managed AWS resources.

### Up

TJ Holowaychuk might have the best aesthetic sense of any developer I know, and [Up](https://apex.sh/up/) is no exception. Like Plausible, Up is unusual in that it abstracts away the provider specifics; AWS is currently (as of 10/20) the only supported backend, but TJ is very clear that Lambda and API Gateway are implementation details.

That said, Up is dedicated to a specific use case:

> Up focuses on deploying "vanilla" HTTP servers so there's nothing new to learn, just develop with your favorite existing frameworks such as Express, Koa, Django, Golang net/http or others.
>
> Up currently supports Node.js, Golang, Python, Java, Crystal, Clojure and static sites out of the box. Up is platform-agnostic, supporting AWS Lambda and API Gateway as the first targets. You can think of Up as self-hosted Heroku style user experience for a fraction of the price, with the security, isolation, flexibility, and scalability of AWS.

Given this framing, Up is more like a language- and cloud-agnostic alternative to Chalice, leveraging the power of serverless functions and API gateways to streamline the development of cost-effective and highly scalable HTTP backends.

**Business Model**: Open source, with a paid tier that provides additional cross-cutting functionality (encrypted secrets, alerting, etc.)

### Terraform

[Terraform](https://www.terraform.io/) has come to dominate the infrastructure-as-code landscape, and for good reason. Its comprehensive and well-designed declarative model vastly reduces cognitive load for developers and increases the quality and reliability of cloud architectures. In recent years, Terraform has rapidly displaced imperative tools such as Puppet, Chef, and Ansible.

Terraform's declarative approach excels in describing, deploying, and maintaining traditional cloud-native infrastructure: networks and routing, security policies, load balancers, server fleets, and so on. In this  domain, Terraform is simply the best way to interact with cloud resources. But one of Terraform's core design principles is that it provide complete and high-fidelity access to the underlying APIs. Not only must each provider be exhaustive in its coverage, but they should not provide any simplification or abstraction. Terraform resources have a 1:1 correspondence with AWS, Azure, and GCP resources; it provides stateful, declarative access to them in place of their native, command-based APIs.

Terraform's 1:1 approach is not a great fit for serverless architectures, though. It requires a lot of near-boilerplate config to connect serverless functions to one another with the appropriate event triggers, permissions, and pub/sub transports, and the semantics of the architecture quickly get lost.

(Plausible makes heavy use of Terraform in its own implementation, although it thoroughly flouts Terraform's principle of directly mirroring underlying APIs.)

**Business Model**: Open source, with a managed commercial offering that provides reliability, scale, and added functionality.

### Serverless Framework

The [Serverless Framework](https://www.serverless.com/) is a full-featured and comprehensive framework that makes it easier to design and deploy serverless applications on various cloud providers. In addition to supporting every major public cloud, it is also language-agnostic for serverless functions. Serverless Framework is highly opinionated: it supports only those cloud resources that are relevant to serverless applications. Its core purpose is to adapt the very broad capabilities of various cloud providers to address the more specific requirements of serverless applications.

The most important design difference between Plausible and Serverless is that the latter does not abstract away the specifics of the underlying cloud resources. A Serverless framework app is always written for a specific cloud (such as AWS or Azure), and the resources that the application includes are cloud-specific (such as DynamoDB, IAM roles, and so on for AWS). This is in marked contrast to Plausible (and Up), in which applications are implemented (mostly) without regard to the cloud provider on which they will be deployed.

**Business Model**: Open source, with a managed commercial offering that makes it easier for teams to develop together.

### Temporal

Like Plausible, Temporal represents a rethinking of the core abstractions for a serverless world, but with a different set of priorities: reliability and fault tolerance. Temporal uses its own runtime, rather than relying on existing cloud providers. In many ways, it represents a clean break with existing cloud infrastructure in order to deliver certain guarantees. Temporal is a fork of Cadence, an open source project originally developed at Uber.

> A large number of use cases span beyond a single request-reply, require tracking of a complex state, respond to asynchronous events, and communicate to external unreliable dependencies. The usual approach to building such applications is a hodgepodge of stateless services, databases, cron jobs, and queuing systems.
> 
> The Temporal solution is a fault-oblivious stateful programming model that hides most of the complexity behind building scalable distributed applications. In essence, Temporal provides a durable virtual memory that is not linked to a specific process, and preserves the full application state, including function stacks, with local variables across all sorts of host and software failures. This allows you to write code using the full power of a programming language while Temporal takes care of durability, availability, and scalability of the application.

**Business Model**: Open source, with a managed commercial offering.

### Dark

Dark is, in many ways, complementary to Temporal. It is represents a rethinking of serverless computing with its own set of abstractions, but it focuses on ease of development and productivity for common use cases. In targets many of the same use cases as Up, but with a much more heavyweight and proprietary approach: it has its own language with an accompanying IDE and programming model, and its own cloud infrastructure.

**Business Model**: Commercial, with a free tier.

### Summary

The various options in this space have different priorities, and as a result they differ broadly in their design choices. This tables is an imperfect attempt to summarize their similarities and differences, with an emphasis on Plausible's differentiation.

| Name | Native | Complete | Polyglot | Multi-cloud | Pithy | Abstraction |
| --- | :--: | :---: | :---: | :---: | :---: | :---: |
| SAM | Yes | Yes | Yes | No | No | No |
| Chalice | Yes | No | No | No | Yes | No |
| Up | Yes | No | Yes | No | Yes | Yes |
| Terraform | No | Yes | Yes | Yes | No | No |
| Serverless | Yes | Yes | Yes | Yes | Yes | No |
| Temporal | Yes | Yes | Yes | No | Yes | Yes |
| Dark | Yes | Yes | No | No | Yes | Yes |
| Plausible | Yes | Yes | Yes | Yes | Yes | Yes |

* **Native**: Is the framework "serverless-native"? I.e., was it created specifically to address the needs of serverless application development?
* **Complete**: Does the framework offer, or attempt to offer, capabilities that are sufficient to develop arbitrary serverless applications? (Or, conversely, is it specialized to a subclass of serverless use cases?)
* **Polyglot**: Does the framework support multiple languages for serverless functions?
* **Multi-cloud**: Does the framework support multiple cloud providers?
* **Pithy**: Does the framework place a high value on reducing boilerplate and therefore surfacing application-specific design elements?
* **Abstraction**: Does the framework abstract away the public cloud provider entirely, such that an application is developed without reference to the specific resource types of the underlying provider?