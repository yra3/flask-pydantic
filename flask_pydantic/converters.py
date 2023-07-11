import collections
from typing import Dict, List, Type, Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from werkzeug.datastructures import ImmutableMultiDict


def convert_query_params(
    query_params: ImmutableMultiDict, model: Type[BaseModel]
) -> dict:
    """
    group query parameters into lists if model defines them

    :param query_params: flasks request.args
    :param model: query parameter's model
    :return: resulting parameters
    """
    
    def is_complex(annotation) -> bool:
        if annotation is None:
            return False
        
        if get_origin(annotation) is list or get_origin(annotation) is List:
            return True
        
        if get_args(annotation) is not None:
            return any(is_complex(arg) for arg in get_args(annotation))
        
        return isinstance([], annotation)
        
    
    return {
        **query_params.to_dict(),
        **{
            key: value
            for key, value in query_params.to_dict(flat=False).items()
            if key in model.__fields__
            and is_complex(model.__fields__[key].annotation)
        },
    }
