#!/usr/bin/env python3

from connexion.resolver import Resolver

import re

"""
Starts the API server
"""

class MyResolver(Resolver):
    """
    Resolves endpoint functions using REST semantics (unless overridden by specifying operationId)
    """

    def __init__(self, default_module_name, collection_endpoint_name='search'):
        """
        :param default_module_name: Default module name for operations
        :type default_module_name: str
        """
        Resolver.__init__(self)
        self.default_module_name = default_module_name
        self.collection_endpoint_name = collection_endpoint_name

    def resolve_operation_id(self, operation):
        """
        Resolves the operationId using REST semantics unless explicitly configured in the spec
        :type operation: connexion.operations.AbstractOperation
        """
        if operation.operation_id:
            return Resolver.resolve_operation_id(self, operation)

        return self.resolve_operation_id_using_rest_semantics(operation)

    def resolve_operation_id_using_rest_semantics(self, operation):
        """
        Resolves the operationId using REST semantics
        :type operation: connexion.operations.AbstractOperation
        """
        print(operation.path)
        path_match = re.search(
            r'^/?(?P<resource_name>([\w\-](?<!/))*)(?P<trailing_slash>/*)(?P<extended_path>.*)$', operation.path
        )

        def get_controller_name():
            x_router_controller = operation.router_controller

            name = self.default_module_name
            resource_name = path_match.group('resource_name')

            if x_router_controller:
                name = x_router_controller

            elif resource_name:
                resource_controller_name = resource_name.replace('-', '_')
                name += '.' + resource_controller_name

            return name

        def get_function_name():
            method = operation.method

            is_collection_endpoint = \
                method.lower() == 'get' \
                and path_match.group('resource_name') \
                and not path_match.group('extended_path')

            extended_path = path_match.group('extended_path')
            extended_path_match = re.search(
                r'^/?(\{)(?P<param_name>(\w)*)(\})(?P<trailing_slash>/*)(?P<method_name>.*)$', extended_path
            )

            method_name = ""
            if extended_path:
                method_name = extended_path_match.group("method_name")
                if method_name:
                    method_name = f"_{method_name}"

            if is_collection_endpoint:
                function_name = f"{self.collection_endpoint_name}{method_name}"
            else:
                function_name = f"{method.lower()}{method_name}"

            return function_name

        print("controller", get_controller_name())
        print("function", get_function_name())
        return '{}.{}'.format(get_controller_name(), get_function_name())


from flask import render_template
import config

connex_app = config.connex_app
connex_app.add_api("swagger.yml", arguments={'title': 'Energy Measurement API'}, pythonic_params=True, resolver=MyResolver('api.controller'))

if __name__ == "__main__":
    connex_app.run(debug=True)
