import http
import json
import os
import sys

from .object_store import ObjectStore
from .resource import PlausibleResource

import logging

logger = logging.getLogger(__name__)
environment = "AWS"


class Resources(object):
    def __init__(self, app_home):
        super().__init__()
        self.__load_state(app_home)
        self.resources = {}

    def __load_state(self, app_home):
        logger.info(app_home)
        tf_state = os.path.join(app_home, "infra", "terraform.tfstate")
        if not os.path.exists(tf_state):
            logger.error(f"No terraform state found at {tf_state}")

        with open(tf_state, "r") as fd:
            state = json.loads(fd.read())

        for resource_description in state["resources"]:
            self.__add(PlausibleResource.create_from_tfstate(resource_description))

    def __add(self, resource: PlausibleResource):
        self.resources[resource.fullname] = resource

    def __getattr__(self, name):
        return self.resources.get(name, None)


resource = Resources(os.getenv("PBL_APP_HOME", ".."))
