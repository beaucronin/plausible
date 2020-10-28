from __future__ import annotations
from typing import Dict, Any, Union, Optional
from .resource import PlausibleResource
import json
import boto3
from botocore.response import StreamingBody

from .exceptions import ItemNotFoundException, PlausibleException

import logging

logger = logging.getLogger(__name__)

class Function(PlausibleResource):
    def __init__(self, name: str, atts: Dict[str, Any]):
        super().__init__(f"function.{name}")
        
    @classmethod
    def create(cls, name: str, atts: Dict[str, Any], environment: str) -> Function:
        if environment == "AWS":
            return AWSLambda(name, atts)
        else:
            raise NotImplementedError(f"Environment {environment} not implemented")
        
    def invoke(self):
        raise NotImplementedError()

class AWSLambda(Function):
    def __init__(self, name, atts):
        super().__init__(name, atts)
        
    
    def invoke(self):
        pass
    
    
    
    
        