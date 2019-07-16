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
            extended_path = path_match.group('extended_path')
            print("name", name)
            print("resource_name", resource_name)
            print("extended_path", extended_path)

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

            return self.collection_endpoint_name if is_collection_endpoint else method.lower()

        print(get_controller_name())
        print(get_function_name())
        return '{}.{}'.format(get_controller_name(), get_function_name())


from flask import render_template
import config

connex_app = config.connex_app
connex_app.add_api("swagger.yml", arguments={'title': 'Energy Measurement API'}, pythonic_params=True, resolver=MyResolver('api'))

if __name__ == "__main__":
    connex_app.run(debug=True)
