import typing as t
from collections import OrderedDict
from strictyaml import (
    YAML,
    load,
    Any,
    Map,
    MapPattern,
    Str,
    Int,
    Enum,
    Seq,
    FixedSeq,
    Optional,
    YAMLError,
)
from strictyaml.exceptions import YAMLValidationError

WHERE_OPS = ["eq", "lt", "gt", "lte", "gte", "startswith"]
WINDOW_TYPES = ["sliding", "stagger"]
HTTP_METHODS = ["get", "post", "put", "patch", "delete"]

top_schema = {
    "top": Map(
        {
            "app_name": Str(
                doc={
                    "text": "The name of the application, which is used in various ways to uniquely identify the resources belonging to it",
                    "label": "top",
                }
            ),
            "resources": Seq(
                Any(
                    doc={
                        "any_options": [
                            "function",
                            "http_api",
                            "publisher",
                            "object_store",
                            "keyvalue_store",
                            "stream_analytics",
                        ]
                    }
                ),
                doc={
                    "text": "The list of resources that comprise the application",
                    "label": "top",
                    "title": "resource_types",
                },
            ),
        },
        doc={
            "text": "The outermost element in a Plausible application specification",
            "title": "plausible_app_config",
            "example": """
```yaml
app_name: my_app
resources:
    - foo_resource:
        ...
    - bar_resource:
        ...
```
""",
        },
    )
}

resource_schemas = {
    "function": Map(
        {
            "function": Map(
                {
                    "name": Str(doc={"text": "The name of the function"}),
                    Optional("triggers"): Seq(
                        Any(doc={"any_options": ["trigger"]}),
                        doc={
                            "title": "triggers",
                            "text": "The trigger or triggers that determine when this function will be invoked.",
                        },
                    ),
                    Optional("outputs"): MapPattern(
                        Str(
                            doc={
                                "text": "The name of the output, as it will be referenced through the client library from within the function implementation."
                            }
                        ),
                        Map(
                            {
                                "target": Str(
                                    doc={
                                        "text": "The name of the resource that will receive or be triggered by the messages sent over this output"
                                    }
                                ),
                                Optional("transform"): Any(
                                    doc={"any_options": ["transform"]}
                                ),
                                Optional("filter"): Any(
                                    doc={"any_options": ["filter"]}
                                ),
                            },
                            doc={
                                "title": "output",
                                "text": "The target resource and, optionally, any transforms or filters that are applied before it is invoked."
                            },
                        ),
                        doc={
                            "title": "outputs",
                            "text": "The (named) outputs of the function, which will receive or be triggered by the messages that are emitted by the function. The marshaling and connectivity will all be handled by the Plausible client library and the deployment",
                        },
                    ),
                },
                doc={
                    "title": "function",
                    "text": "The function resource, which is the programmatic building block of Plausible applications. Functions are the primary home for executable code, whereas the remaining config is provided in declarative terms.",
                    "break": True,
                    "label": "resource",
                    "example": """
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
""",
                },
            )
        },
        doc={"skip": True},
    ),
    "http_api": Map(
        {
            "http_api": Map(
                {
                    "name": Str(doc={"text": "The name of the API."}),
                    Optional("openapi_spec"): Any(),
                },
                doc={
                    "title": "http_api",
                    "text": "The resource type representing an HTTP API. It is described through a valid OpenAPI 3.0 specification",
                    "break": True,
                    "label": "resource",
                    "example": """
```yaml
- http_api:
    name: my-api
```
""",
                },
            )
        },
        doc={"skip": True},
    ),
    "publisher": Map(
        {
            "publisher": Map(
                {"name": Str(doc={"text": "The name of the publisher"})},
                doc={
                    "title": "publisher",
                    "text": "The publisher resource, which is a combined pub/sub topic and message queue. Like a queue store, a publisher can store messages for a period of time until they are successfully consumed by the subscribers. And like a notification topic, a publisher can deliver messages to multiple subscribers.",
                    "break": True,
                    "label": "resource",
                },
            )
        },
        doc={"skip": True},
    ),
    "object_store": Map(
        {
            "object_store": Map(
                {"name": Str(doc={"text": "The name of the object store`"})},
                doc={
                    "title": "object_store",
                    "text": "The object store resource, which is capable of storing binary objects (blobs) at key addresses. These objects can correspond to many things, from text files to digital media to archived data.",
                    "break": True,
                    "label": "resource",
                },
            )
        },
        doc={"skip": True},
    ),
    "keyvalue_store": Map(
        {
            "keyvalue_store": Map(
                {
                    "name": Str(
                        doc={"text": "The name of the keyvalue store resource"}
                    ),
                    "collection_name": Str(
                        doc={"text": "The name of the underlying key-value collection"}
                    ),
                    "primary_index": Map(
                        {
                            "partition_key": Str(
                                doc={
                                    "text": "The key which is hashed to obtain the partition or shard under which the value will be stored"
                                }
                            ),
                            Optional("row_key"): Str(
                                doc={
                                    "text": "The key which differentiates and orders the items which share a partition key value."
                                }
                            ),
                        },
                        doc={
                            "title": "primary_index",
                            "text": "The required primary index for the key-value collection, comprising a required partition key and an optional, sortable row key",
                        },
                    ),
                    Optional("secondary_index"): MapPattern(
                        Str(doc={"text": "The name of the secondary index"}),
                        Map(
                            {
                                "partition_key": Str(
                                    doc={
                                        "text": "The key which is hashed to obtain the partition or shard under which the value will be stored"
                                    }
                                ),
                                Optional("row_key"): Str(
                                    doc={
                                        "text": "The key which differentiates and orders the items which share a partition key value."
                                    }
                                ),
                            },
                            doc={
                                "title": "secondary_index",
                                "text": "A secondary index for the key-value collection, comprising a required partition key and an optional, sortable row key",
                            },
                        ),
                        doc={
                            "title": "secondary_indexes",
                            "text": "The optional secondary indexes for the collection, of which there can be zero or more",
                        },
                    ),
                },
                doc={
                    "title": "keyvalue_store",
                    "text": "The key-value store resource",
                    "break": True,
                    "label": "resource",
                },
            ),
        },
        doc={"skip": True},
    ),
    "stream_analytics": Map(
        {
            "stream_analytics": Map(
                {
                    "name": Str(
                        doc={"text": "The name of the stream analytics resource"}
                    ),
                    "source": Str(
                        doc={
                            "title": "source",
                            "text": "The name of the resource that sends messages or events to the stream processor"
                        }
                    ),
                    "window": Map(
                        {
                            "type": Enum(
                                WINDOW_TYPES,
                                doc={
                                    "title": "type",
                                    "text": "The type of temporal window; must be one of `sliding` or `stagger`"
                                },
                            ),
                            "interval": Int(
                                doc={
                                    "title": "interval",
                                    "text": "The single interval, in seconds, that defines the window period"
                                }
                            )
                            | Seq(
                                Int(
                                    doc={
                                        "title": "interval",
                                        "text": "An interval, in seconds, that defines a window period"
                                    }
                                ),
                                doc={
                                    "title": "interval",
                                    "text": "The multiple intervals, each in seconds, that define the window periods"
                                }
                            ),
                        },
                        doc={
                            "title": "window",
                            "text": "The basic attributes the define the analytics window, including its type and period"
                        },
                    ),
                    Optional("statements"): Map(
                        {
                            Optional("group_by"): Str(
                                doc={
                                    "title": "group_by",
                                    "text": "The value, other than the window times, by which to group the outputs of the window processor"
                                }
                            )
                            | Seq(
                                Str(
                                    doc={
                                        "title": "group_by",
                                        "text": "The value, other than the window times, by which to group the outputs of the window processor"
                                    }
                                ),
                                doc={
                                    "title": "group_bys",
                                    "text": "A collection of values by which to group the outputs of the window processor"
                                },
                            ),
                            Optional("where"): Seq(
                                MapPattern(
                                    Enum(WHERE_OPS), FixedSeq([Str(), Str(), Str()])
                                )
                            ),
                        },
                        doc={
                            "title": "statements",
                            "text": "The optional statements that further qualify the windowed processing"
                        },
                    ),
                },
                doc={
                    "title": "stream_analytics",
                    "text": "The stream analytics resource, which processes events on a windowed basis, possibly filtering, grouping by, and aggregating",
                    "break": True,
                    "label": "resource",
                },
            )
        },
        doc={"skip": True},
    ),
}

trigger_schemas = {
    "api_route": Map(
        {
            "api_route": Map(
                {
                    "http_api": Str(
                        doc={
                            "text": "The name of the http_api to which the triggering route belongs"
                        }
                    ),
                    "route": Str(
                        doc={
                            "text": "The URL path for which requests will be handled by the function"
                        }
                    ),
                    "method": Enum(HTTP_METHODS, doc={"text": "The HTTP method that"}),
                    Optional("content_type", default="application/json",): Str(),
                }
            )
        }
    ),
    "schedule": Map(
        {
            "schedule": Map(
                {
                    "cron": Str(
                        doc={
                            "text": "A standard cron config string that describes when the trigger should fire"
                        }
                    )
                },
                doc={"text": "A trigger that fires on a schedule"},
            )
        },
    ),
    "subscription": Map(
        {
            "subscription": Map(
                {
                    "publisher": Str(
                        doc={
                            "text": "The name of the publisher whose events cause the trigger to fire"
                        }
                    )
                },
                doc={
                    "text": "A trigger that fires when an event or message is recived via a subscription to a publisher"
                },
            )
        },
    ),
    "function": Map(
        {
            "function": Map(
                {
                    "caller": Str(
                        doc={
                            "text": "The name of the function whose outputs fire the trigger"
                        }
                    )
                },
                doc={
                    "text": "A trigger that fires whenever a calling function returns an event or message"
                },
            )
        },
    ),
}


def single_item(d):
    assert len(list(d.keys())) == 1
    k = list(d.keys())[0]
    return k, d[k]


def ensure_value(d, k, v=None):
    if k not in d:
        d[k] = v
    return d


class TerraformConfig(object):
    def __init__(self, provider_version, provider_source="beaucronin/plausible"):
        super().__init__()
        self.app_name: str
        self.tf: t.Dict[str, t.Any]
        self.provider_version: str = provider_version
        self.provider_source: str = provider_source

    def compile(self, file) -> OrderedDict:
        """
        compile Uses strictyaml schemas to parse a yaml config file and return a conforming object. This makes use of strictyaml's revalidate function to process nested objects that can conform to one of several schemas, which are defined separately and referenced via a string key.

        :param file: A file-like object corresponding to the yaml source
        :type file: file-like
        :raises Exception: [description]
        :raises Exception: [description]
        :raises e: [description]
        :return: An OrderedDict whose structure conforms to the composite schema
        :rtype: OrderedDict
        """
        try:
            with open(file) as fd:
                content = fd.read()
                toplevel_obj = load(content, top_schema["top"])

                self.app_name = toplevel_obj["app_name"].data
                for resource in toplevel_obj["resources"]:
                    for k in resource.keys():
                        if k in resource_schemas:
                            resource.revalidate(resource_schemas[k])
                            if k == "function":
                                for trigger in resource["function"].get("triggers", []):
                                    for j in trigger.keys():
                                        if j in trigger_schemas:
                                            trigger.revalidate(trigger_schemas[j])
                                        else:
                                            raise Exception(
                                                f"Trigger type {j} not valid"
                                            )
                        else:
                            raise Exception(f"Resource type {k} not valid")
                return toplevel_obj.data
        except FileNotFoundError as e:
            raise e
        except YAMLValidationError as e:
            raise e
        except Exception as e:
            raise e

    def template(self) -> t.Dict[str, t.Any]:
        """
        template Generate and return the starting point for the JSON-formatted terraform config that is returned by the `generate` method.

        :return: A JSON serializable Dict with high-level structures populated or stubbed
        :rtype: t.Dict[str, t.Any]
        """
        return {
            "terraform": {
                "required_providers": {
                    "plausible": {
                        "source": self.provider_source,
                        "version": self.provider_version,
                    }
                }
            },
            "provider": {"plausible": [{"app_name": self.app_name}]},
            "variable": {
                "app_home": {"default": ".."},
                "app_name": {"default": self.app_name},
            },
            "locals": {"functions_home": "${var.app_home}/functions"},
            "resource": {},
        }

    def generate(self, parsed_obj) -> t.Dict[str, t.Any]:
        """
        generate Create a JSON-formatted Terraform config from a parsed Plausible config file, as return by the compile method.

        :param parsed_obj: The deserialized and parsed Plausible config
        :type parsed_obj: 
        :return: [description]
        :rtype: [type]
        """
        self.tf = self.template()
        for resource in parsed_obj["resources"]:
            assert len(list(resource.keys())) == 1
            resource_type = list(resource.keys())[0]
            resource_config = resource[resource_type]
            if resource_type == "function":
                self.generate_function(resource_config)
            elif resource_type == "publisher":
                self.generate_publisher(resource_config)
            elif resource_type == "http_api":
                self.generate_http_api(resource_config)
            elif resource_type == "keyvalue_store":
                self.generate_keyvalue_store(resource_config)
            elif resource_type == "object_store":
                self.generate_object_store(resource_config)
        return self.tf

    def generate_function(self, function_config):
        name = function_config["name"]
        tf = {
            "source": "${local.functions_home}/retrieve-stations/",
        }

        if "triggers" in function_config:
            for trigger in function_config["triggers"]:
                trigger_type, trigger_spec = single_item(trigger)
                tf_trigger_type = f"{trigger_type}_trigger"
                ensure_value(tf, tf_trigger_type, [])
                tf[tf_trigger_type].append(trigger_spec)

        if "outputs" in function_config:
            ensure_value(tf, "output", [])
            for output_name, output_spec in function_config["outputs"]:
                tf["output"].append(output_spec)

        ensure_value(self.tf["resource"], "plausible_function", {})
        self.tf["resource"]["plausible_function"][name] = tf

    def generate_publisher(self, publisher_config):
        name = publisher_config["name"]
        tf = {}

        ensure_value(self.tf["resource"], "plausible_publisher", {})
        self.tf["resource"]["plausible_publisher"][name] = tf

    def generate_http_api(self, http_api_config):
        name = http_api_config["name"]
        tf = {}

        ensure_value(self.tf["resource"], "plausible_http_api", {})
        self.tf["resource"]["plausible_http_api"][name] = tf

    def generate_object_store(self, object_store_config):
        name = object_store_config["name"]
        tf = {}
        ensure_value(self.tf["resource"], "plausible_object_store", {})
        self.tf["resource"]["plausible_object_store"][name] = tf

    def generate_keyvalue_store(self, keyvalue_store_config):
        def index_spec(index_desc):
            ix = {"partition_key": index_desc["partition_key"]}
            if "row_key" in index_desc:
                ix["row_key"] = index_desc["row_key"]
            return ix

        name = keyvalue_store_config["name"]
        tf = {"collection_name": keyvalue_store_config["collection_name"]}
        tf["primary_key"] = index_spec(keyvalue_store_config["primary_index"])
        if "secondary_index" in keyvalue_store_config:
            tf["secondary_index"] = {}
            for si_name, si_def in keyvalue_store_config["secondary_index"].items():
                tf["secondary_index"][si_name] = index_spec(si_def)

        ensure_value(self.tf["resource"], "plausible_keyvalue_store", {})
        self.tf["resource"]["plausible_keyvalue_store"][name] = tf

    def docs(self):
        import json

        schemas = [top_schema, resource_schemas, trigger_schemas]
        return [{k: v.doc for k, v in s.items()} for s in schemas]
