from typing import Type, Any
from dotted_dict import DottedDict as ddict
import http
import json
import os
import sys

# ObjectStore: Type[Any] = Type[Any]
# KeyValueStore: Type[Any] = Type[Any]
# print(dir(ObjectStore))
from .object_store import ObjectStore
from .keyvalue_store import KeyValueStore
from .function import Function
from .exceptions import PlausibleException, ItemNotFoundException

# from .document_store import DocumentStore
from .resource import PlausibleResource

import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
environment = "AWS"

def exception_handler(exception_type, exception, traceback):
    logger.error(f"{exception_type.__name__}:{exception}")
    # logger.error(traceback)

sys.excepthook = exception_handler

class Resources(object):
    def __init__(self, app_home):
        super().__init__()
        self.resources: Dict[str, Dict[str, List[PlausibleResource]]] = {}
        self.__load_state(app_home)

    def __load_state(self, app_home):
        logger.info(f"Using app_home {app_home}")
        tf_state = os.path.join(app_home, "infra", "terraform.tfstate")
        if not os.path.exists(tf_state):
            logger.error(f"No terraform state found at {tf_state}")

        with open(tf_state, "r") as fd:
            state = json.loads(fd.read())

        for resource_description in state["resources"]:
            rsc = PlausibleResource.create_from_tfstate(resource_description, "AWS")
            self.__add(rsc)
            logger.info(f"loaded resource {rsc.fullname}")

    def __add(self, rsc: PlausibleResource):
        resource_type, resource_name = rsc.fullname.split(".")

        if not resource_type in self.resources:
            self.resources[resource_type] = ddict()
        self.resources[resource_type][resource_name] = rsc

    def __str__(self):
        return (
            "[\n" + "\n  ".join([r.fullname for _, r in self.resources.items()]) + "\n]"
        )

    # @property
    # def resources(self):
    #     return self.__resources

    def __getattr__(self, name):
        return self.resources.get(name, None)

def get_current_function(resources: Resources):
    pass

resource = Resources(os.getenv("PBL_APP_HOME", "."))
function = get_current_function(resource)
