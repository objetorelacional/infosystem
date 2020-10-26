from copy import copy
from typing import Tuple, List

InputResource = Tuple[str, List[str]]
RouteResource = Tuple[str, str]


class InputResourceUtils:

    @classmethod
    def parse_resources(cls, resources: List[InputResource]) \
            -> List[RouteResource]:
        output_resources = []
        for (endpoint, methods) in resources:
            for method in methods:
                output_resources.append((endpoint, method))
        return cls.remove_duplicates(output_resources)

    @classmethod
    def remove_duplicates(cls, resources: List[RouteResource]) \
            -> List[RouteResource]:
        return list(set([resource for resource in resources]))

    @classmethod
    def diff_resources(cls, first: List[RouteResource],
                       *args: List[RouteResource]):
        temp = set(copy(first))
        for arg in args:
            temp -= set(arg)
        return list(temp)

    @classmethod
    def join_resources(cls, first: List[RouteResource],
                       *args: List[RouteResource]):
        temp = copy(first)
        for arg in args:
            temp += arg
        return cls.remove_duplicates(temp)
