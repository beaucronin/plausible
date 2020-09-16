from __future__ import annotations
from typing import Dict, Any, Union, Optional
from .resource import PlausibleResource
import json
import boto3
from botocore.response import StreamingBody

from .exceptions import ItemNotFoundException, PlausibleException

import logging

logger = logging.getLogger(__name__)


class ObjectStoreKey(object):
    SEP = "/"

    def __init__(self, *args, **kwargs):
        self.components = []
        self.__append(*args, **kwargs)

    def append(self, *args, **kwargs) -> ObjectStoreKey:
        self.__append(*args, **kwargs)
        return self

    def __append(self, *args, **kwargs):
        key_component: str
        component_value: str
        if len(args) == 1:
            # Only the value is provided, so we assume a terminal
            component_value = args[0]
        elif len(args) == 2:
            key_component = args[0]
            component_value = args[1]

    def __str__(self):
        return SEP.join([v for _, v in components])


Key = Union[ObjectStoreKey, str]

GZIP = "gzip"
ZIP = "zip"
BZ2 = "bz2"


class ObjectStore(PlausibleResource):
    def __init__(self, name: str, atts: Dict[str, Any]):
        """
        __init__ Create a new ObjectStore from a resource description. 
        This constructor should not be called directly; instead, use the 
        ObjectStore.create() method

        :param resource_desc: The resource description, as contained in the Terraform state.
        :type resource_desc: Dict[str, Any]
        """
        super().__init__(f"object_store.{name}")
        self.store_name = atts["store_name"]
        self.key_structure = atts["key_structure"]

    @classmethod
    def create(cls, name: str, atts: Dict[str, Any], environment: str) -> ObjectStore:
        """
        create A factory for creating an environment-appropriate ObjectStore instance.

        :param environment: The environment for which the ObjectStore should be created
        :type environment: str
        :param resource_description: The resource description, as contained in the Terraform state
        :type resource_description: Dict[str, Any]
        :raises NotImplementedError: If the environment is not recognized or supported
        :return: The ObjectStore
        :rtype: ObjectStore
        """
        if environment == "AWS":
            return AWSObjectStore(name, atts)
        else:
            raise NotImplementedError(f"Environment {environment} not implemented")

    def key_matches_structure(self, key: ObjectStoreKey) -> bool:
        """
        key_matches_structure Determines whether the given key conforms to the key structure specified for the store.

        :param key: The key object to be checked
        :type key: ObjectStoreKey
        :return: True if the key conforms, false otherwise
        :rtype: bool
        """
        return True

    def get_bytes(self, key: Key, compression=None) -> bytes:
        raise NotImplementedError()

    def get_string(self, key: Key, compression=None, encoding="utf-8") -> str:
        raise NotImplementedError()

    def get_object(
        self, key: Key, compression=None, fmt: str = None
    ) -> Optional[object]:
        raise NotImplementedError()

    def put(self, key: Key, data: Any) -> bool:
        raise NotImplementedError()

    def delete(self, key: Key) -> bool:
        raise NotImplementedError()

    def _stringify_key(self, key: Key) -> str:
        if isinstance(key, ObjectStoreKey):
            if not self.key_matches_structure(key):
                raise Exception(f"Key {key} does not match structure")
            return str(key)
        elif isinstance(key, str):
            return key

    @staticmethod
    def maybe_uncompress(b, compression):
        if compression == GZIP:
            pass
        elif compression == ZIP:
            pass
        elif compression == BZ2:
            pass
        elif not compression:
            return b
        else:
            raise Exception(f"Compression scheme {compression} not supported")


class AWSObjectStore(ObjectStore):
    def __init__(self, name, atts):
        super().__init__(name, atts)

        s3 = boto3.resource("s3")
        self.bucket = s3.Bucket(self.store_name)

    @classmethod
    def maybe_raise(cls, resp):
        status_code = resp["ResponseMetadata"]["HTTPStatusCode"]
        logger.info(status_code)
        if status_code == 200:
            return
        else:
            return

    def wrap_exception(self, e, **kwargs):
        if repr(e).startswith("NoSuchKey"):
            raise ItemNotFoundException(f"Item {kwargs['key']} was not found in {self.bucket.name}") from e
        else:
            raise PlausibleException("Unrecognized AWS exception") from e

    def get_bytes(self, key: Key, compression=None) -> bytes:
        key_str = self._stringify_key(key)
        resp = self.__get(key_str)
        # self.maybe_raise(resp)
        body: StreamingBody = ObjectStore.maybe_uncompress(resp["Body"], compression)
        return body.read()

    def get_string(self, key: Key, compression=None, encoding="utf-8") -> str:
        b: bytes = self.get_bytes(key)
        s = b.decode(encoding)
        return s

    def get_object(
        self, key: Key, compression=None, fmt: str = None
    ) -> Optional[object]:
        if not fmt:
            fmt = "json"
        fmt = fmt.lower()
        if fmt == "json":
            obj = json.loads(self.get_string(key, compression))
            return obj
        elif fmt == "jsonl":
            raise NotImplementedError()
        elif fmt == "csv":
            raise NotImplementedError()
        else:
            raise Exception(f"File format {fmt} not supported")

    def __get(self, key: str):
        obj = self.bucket.Object(key)
        try:
            resp = obj.get()
            return resp
        except Exception as e:
            self.wrap_exception(e, key=key)

    def put(self, key: Key, data: Any) -> bool:
        obj = self.bucket.Object(self._stringify_key(key))
        if isinstance(data, str):
            res = obj.put(Body=data)
            return True
        else:
            return False

    def delete(self, key: Key) -> bool:
        obj = self.bucket.Object(self._stringify_key(key))
        res = obj.delete()
        return True

    def __put(self, key, data):
        pass
