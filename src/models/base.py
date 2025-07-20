from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import ClassVar

class BaseInputModel(BaseModel, ABC):
    """
    Base model for all input models.
    """
    id: str
    
    @abstractmethod
    def to_dynamo_item(self):
        """
        Convert the model to dynamo item.
        """
        pass

class BaseDynamoModel(BaseModel, ABC):
    """
    Base model for all DynamoDB models.
    """
    id: str
    table: ClassVar = None
    
    @abstractmethod
    def to_payload(self) -> dict:
        """
        Convert the model to payload.
        """
        pass
    
    @classmethod
    def put_item(cls, item: dict):
        cls.table.put_item(Item=item)

    @classmethod
    def query_item(cls, key_condition_expression: str, index_name: str=None, limit: int=10, last_evaluated_key=None, ascending: bool=True): 
        if index_name and last_evaluated_key:
            response = cls.table.query(
                IndexName=index_name,
                KeyConditionExpression=key_condition_expression,
                Limit=limit,
                LastEvaluatedKey=last_evaluated_key,
                ScanIndexForward=ascending
            )
        elif index_name and not last_evaluated_key:
            response = cls.table.query(
                IndexName=index_name,
                KeyConditionExpression=key_condition_expression,
                Limit=limit,
                ScanIndexForward=ascending
            )
        elif not index_name and last_evaluated_key:
            response = cls.table.query(
                KeyConditionExpression=key_condition_expression,
                Limit=limit,
                LastEvaluatedKey=last_evaluated_key,
                ScanIndexForward=ascending
            )
        else:
            response = cls.table.query(
                KeyConditionExpression=key_condition_expression,
                Limit=limit,
                ScanIndexForward=ascending
            )
        return response
    
    @classmethod
    def delete_item(cls, key: str, sort_key: str):
        cls.table.delete_item(Key={'PK': key, 'SK': sort_key})

    @classmethod
    def update_item(cls, key: str, sort_key: str, update_expression: str, expression_attribute_values: dict):
        cls.table.update_item(
            Key={'PK': key, 'SK': sort_key},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )