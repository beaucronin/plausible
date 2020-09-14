from typing import Dict, Any

from .resource import PlausibleResource, QueryRequest, QueryResponse


class DocumentStore(PlausibleResource):
    def __init__(self, name: str, atts: Dict[str, Any]):
        super().__init__(f"document_store.{name}")

    def query(self, query: DocumentStoreQueryRequest) -> DocumentStoreQueryResponse:
        pass


class AWSDocumentStore(DocumentStore):
    def __init__(self):
        super().__init__()


class DocumentStoreQueryRequest(QueryRequest):
    def __init__(self):
        super().__init__()


class DocumentStoreQueryResponse(QueryResponse):
    def __init__(self):
        super().__init__()

