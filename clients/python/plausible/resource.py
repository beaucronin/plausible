from __future__ import annotations
from typing import Dict, Any, Type, Optional

import logging

logger = logging.getLogger(__name__)

class PlausibleResource(object):
    def __init__(self, fullname):
        super().__init__()
        self.fullname = fullname
    
    @classmethod
    def create_from_tfstate(cls, state, environment) -> Optional[PlausibleResource]:
        resource_type = state["type"]
        resource_name = state["name"]
        resource_atts = state["instances"][0]["attributes"]
        
        from plausible import ObjectStore, KeyValueStore

        resource_map = {
            "plausible_object_store": ObjectStore,
            "plausible_keyvalue_store": KeyValueStore,
        }
        ResourceClass: Optional[Type[PlausibleResource]] = resource_map.get(resource_type, None)
        if ResourceClass:
            resource = ResourceClass.create(resource_name, resource_atts, environment)
            return resource
        else:
            logger.error(f"No resource found of type {resource_type}")
            return None
            
    @classmethod
    def create(cls, name: str, atts: Dict[str, Any], environment: str):
        raise NotImplementedError()


def loader_factory(resource_type):
    loaders = {
        "plausible_object_store": ObjectStore,
        "plausible_http_api": HttpApi,
        "plausible_function": Function,
    }
    loader = loaders.get(resource_type, None)
    if not loader:
        raise Exception(f"Loader not found for {resource_type}")
    return loader


class QueryRequest(object):
    def __init__(self):
        super().__init__()

class QueryResponse(object):
    def __init__(self):
        super().__init__()