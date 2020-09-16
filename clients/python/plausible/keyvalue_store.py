from __future__ import annotations
from typing import cast, Dict, Any, Union, List, Tuple, Optional
from decimal import Decimal

from plausible.resource import PlausibleResource, QueryRequest, QueryResponse

"""
resource "plausible_keyvalue_store" "kv" {
    collection_name = "MyTable"
    
    primary_index {
        partition_key = "item_id"
        row_key = "timestamp"
    }

    secondary_index {
        name = "GSI1"
        partition_key = "item_type"
        row_key = "item_name"
    }
    
    secondary_index {
        name = "GSI2"
        partition_key = "sku"
    }
}    
"""

QueryValue = Union[str, int, float, Decimal]


class KeyValueStore(PlausibleResource):
    """
    KeyValueStore An abstract superclass of all Key-Value stores. It knows how to instantiate a correct implementing class, and how to configure its indexes from the provided Terraform state. All other functionality - queries, puts - is handled by concrete subclasses.
    """
    def __init__(self, name: str, atts: Dict[str, Any]):
        super().__init__(f"keyvalue_store.{name}")

        self.indexes = {}

        key_state = atts["primary_index"][0]
        self.indexes["primary"] = {
            "partition_key": key_state["partition_key"],
            "row_key": key_state.get("row_key", None),
        }

        for key_state in atts["secondary_index"]:
            if key_state["name"].lower() == "primary":
                raise Exception("Secondary index name can't be 'primary'")
            self.indexes[key_state["name"]] = {
                "partition_key": key_state["partition_key"],
                "row_key": key_state.get("row_key", None),
            }

    @classmethod
    def create(cls, name: str, atts: Dict[str, Any], environment: str) -> KeyValueStore:
        """
        create A factory method which creates an appropriate KevValueStore instance, given an environment string that specifies the underlying cloud.

        :param name: The name of the KV store, as specified in the Terraform config
        :type name: str
        :param atts: The raw Terraform attributes dict from which to instantiate
        :type atts: Dict[str, Any]
        :param environment: The environment for which the instance should be created
        :type environment: str
        :raises NotImplementedError: Raised if the environment specified is not implemented
        :return: A concrete instance of the KeyValueStore interface
        :rtype: KeyValueStore
        """
        if environment == "AWS":
            return AWSKeyValueStore(name, atts)
        else:
            raise NotImplementedError(f"Environment {environment} not implemented")
    
    def query(self, index_name: str="primary", limit: int=None) -> KVQueryRequest:
        return KVQueryRequest(self, index_name=index_name, limit=limit)
    
    def put(self, data) -> bool:
        #TODO implement
        raise NotImplementedError()

    def __query(self, qr: KVQueryRequest) -> KVQueryResponse:
        raise NotImplementedError()


class AWSKeyValueStore(KeyValueStore):
    def __init__(self, name, atts):
        super().__init__(name, atts)
        self.table_name = atts["collection_name"]

        import boto3

        ddb = boto3.resource("dynamodb")
        self.table = ddb.Table(self.table_name)

    def __query(
        self,
        kvqr: KVQueryRequest,
        existing_response: AWSResponse = Optional[None],
        last_key=None,
    ) -> KVQueryResponse:
        kce = None
        # TODO populate KeyConditionExpression
        params: Dict[str, Any] = {
            "KeyConditionExpression": kce,
        }
        if kvqr.index_name != "primary":
            params["IndexName"] = kvqr.index_name
        if kvqr.limit:
            params["Limit"] = kvqr.limit
        if last_key:
            params["LastEvaluatedKey"] = last_key
        raw_resp: Dict[str, Any] = self.table.query(**params)
        if existing_response:
            return existing_response.__init_page(raw_resp)
        else:
            return AWSResponse(kvqr, raw_resp)


class KVQueryRequest(QueryRequest):
    def __init__(
        self, store: KeyValueStore, index_name: str = "primary", limit: int = None
    ):
        super().__init__()
        self.store = store
        self.index_name = index_name
        self.limit = limit
        self.exprs: List[Tuple[str, str, QueryValue]] = []
    
    def execute(self) -> KVQueryResponse:
        return self.store.__query(self)

    def __add(self, op: str, left: str, right: QueryValue) -> KVQueryRequest:
        self.exprs.append((op, left, right))
        return self

    def eq(self, left: str, right: QueryValue) -> KVQueryRequest:
        return self.__add("=", left, right)

    def lt(self, left: str, right: QueryValue) -> KVQueryRequest:
        return self.__add("<", left, right)

    def gt(self, left: str, right: QueryValue) -> KVQueryRequest:
        return self.__add(">", left, right)

    def lte(self, left: str, right: QueryValue) -> KVQueryRequest:
        return self.__add("<=", left, right)

    def gte(self, left: str, right: QueryValue) -> KVQueryRequest:
        return self.__add(">=", left, right)

    def bw(self, left: str, s) -> KVQueryRequest:
        return self.__add("|>", left, s)


class KVQueryResponse(QueryResponse):
    def __init__(self, request: KVQueryRequest):
        super().__init__()
        self.request = request

    def __iter__(self):
        raise NotImplementedError()

    def __next__(self):
        raise NotImplementedError()

    def __has_next_page(self) -> bool:
        raise NotImplementedError()


class AWSResponse(KVQueryResponse):
    def __init__(self, request: KVQueryRequest, aws_resp):
        super().__init__(request)
        self.store = request.store
        self.total_index = 0
        self.__init_page(aws_resp)

    def __init_page(self, aws_resp):
        self.aws_resp = aws_resp
        self.index_in_page = 0
        self.count_in_page = aws_resp["Count"]
        assert self.count_in_page == len(aws_resp["Items"])

    def __iter__(self):
        return self

    def __next__(self) -> KVItem:
        if self.index_in_page >= self.count_in_page:
            # Try to load a new page of results
            lek = self.aws_resp.get("LastEvaluatedKey", None)
            if lek:
                # NOTE: AWSKeyValueStore.__query calls __init_page on this object
                cast(AWSKeyValueStore, self.store).__query(
                    self.request, existing_response=self, last_key=lek
                )
            else:
                raise StopIteration()
        item = self.create_item(self.aws_resp["Items"][self.index_in_page])
        self.index_in_page += 1
        self.total_index += 1
        return item

    def create_item(self, data: Dict[str, Any]) -> KVItem:
        return KVItem(data)


class KVItem(object):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
    # TODO implement
