import strawberry
from typing import Optional, List, Dict, Any, Union
import yaml
from dataclasses import dataclass
from enum import Enum
import re

import strawberry
from typing import Optional, List, Dict, Any, Union
import yaml
from dataclasses import dataclass
from enum import Enum
import re

def to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    # Handle consecutive uppercase letters (e.g., publicURL -> public_url)
    name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name).lower()
    return name

def convert_type(schema: Dict[str, Any]) -> str:
    """Convert OpenAPI schema to Python/GraphQL types."""
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'array': 'List',
        'object': 'JSON'
    }
    
    # Special handling for Currency type pattern
    if schema.get('type') == 'string' and schema.get('pattern', '').startswith('^\\d+$'):
        return 'str'
    
    # Handle $ref
    if '$ref' in schema:
        return schema['$ref'].split('/')[-1]
        
    # Handle format
    if schema.get('type') == 'string' and schema.get('format') == 'date-time':
        return 'datetime.datetime'
        
    # Handle arrays
    if schema.get('type') == 'array' and 'items' in schema:
        item_type = convert_type(schema['items'])
        return f'List[{item_type}]'
        
    return type_mapping.get(schema.get('type', 'string'), 'str')

def get_field_description(schema: Dict[str, Any]) -> str:
    """Get complete field description including constraints."""
    desc_parts = []
    
    # Add main description
    if 'description' in schema:
        desc_parts.append(schema['description'])
    
    # Add pattern if exists
    if 'pattern' in schema:
        desc_parts.append(f"Pattern: {schema['pattern']}")
    
    # Add enum values if exists
    if 'enum' in schema:
        desc_parts.append(f"Allowed values: {', '.join(map(str, schema['enum']))}")
    
    # Add type-specific constraints
    if schema.get('type') == 'string':
        if 'minLength' in schema:
            desc_parts.append(f"Min length: {schema['minLength']}")
        if 'maxLength' in schema:
            desc_parts.append(f"Max length: {schema['maxLength']}")
    elif schema.get('type') in ['integer', 'number']:
        if 'minimum' in schema:
            desc_parts.append(f"Minimum: {schema['minimum']}")
        if 'maximum' in schema:
            desc_parts.append(f"Maximum: {schema['maximum']}")
    
    # Add format if exists
    if 'format' in schema:
        desc_parts.append(f"Format: {schema['format']}")
    
    # Add example if exists
    if 'example' in schema:
        desc_parts.append(f"Example: {schema['example']}")
    
    return ' | '.join(desc_parts)

def sanitize_name(name: str) -> str:
    """Convert OpenAPI names to valid Python identifiers."""
    # Remove special characters and convert to snake case
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Ensure it doesn't start with a number
    if name[0].isdigit():
        name = 'f_' + name
    return name

def create_enum_type(name: str, schema: Dict[str, Any]) -> str:
    """Create a Strawberry enum type."""
    enum_name = name.title().replace('_', '') + 'Enum'
    enum_values = [sanitize_name(val.upper()) for val in schema['enum']]
    
    description = get_field_description(schema)
    
    return f"""
@strawberry.enum(description=\"\"\"{description}\"\"\")
class {enum_name}(Enum):
    {'''
    '''.join(f'{val} = "{val}"' for val in enum_values)}
"""


def get_field_definition(name: str, schema: Dict[str, Any], required: List[str]) -> str:
    """Create a field definition with proper type, description, and default value."""
    field_type = convert_type(schema)
    is_optional = name not in required
    
    if is_optional:
        field_type = f'Optional[{field_type}]'
    
    field_args = []
    
    # Add description
    description = get_field_description(schema)
    if description:
        field_args.append(f'description="""{description}"""')
    
    # Add default value if specified
    if 'default' in schema:
        default_value = schema['default']
        if isinstance(default_value, str):
            default_value = f'"{default_value}"'
        field_args.append(f'default={default_value}')
    elif is_optional:
        field_args.append('default=None')
    
    # Add original name if different from snake_case
    snake_case_name = to_snake_case(name)
    if snake_case_name != name:
        field_args.append(f'name="{name}"')
    
    field_decorator = f'strawberry.field({", ".join(field_args)})' if field_args else 'strawberry.field'
    
    return f'    {snake_case_name}: {field_type} = {field_decorator}'

def create_type(name: str, schema: Dict[str, Any], required: List[str] = None) -> str:
    """Create a Strawberry type from OpenAPI schema."""
    if required is None:
        required = []
    
    if not schema.get('properties'):
        return f"""
@strawberry.type
class {name}(SiaType):
    \"\"\"
    {get_field_description(schema)}
    \"\"\"
    _dummy: Optional[str] = strawberry.field(default=None)
"""
    
    fields = []
    for prop_name, prop_schema in schema.get('properties', {}).items():
        fields.append(get_field_definition(prop_name, prop_schema, required))
    
    type_description = get_field_description(schema)
    type_decorator = f'@strawberry.type(description="""{type_description}""")' if type_description else '@strawberry.type'
    
    return f"""
{type_decorator}
class {name}(SiaType):
{'''
'''.join(fields)}
"""

def create_input_type(name: str, schema: Dict[str, Any], required: List[str] = None) -> str:
    """Create a Strawberry input type from OpenAPI schema."""
    if required is None:
        required = []
        
    # Replace SiaType with SiaInput for input types
    return create_type(f"{name}Input", schema, required).replace('(SiaType)', '(SiaInput)').replace('@strawberry.type', '@strawberry.input')

def resolve_response_type(operation: Dict[str, Any]) -> str:
    """Resolve the response type from an operation."""
    if 'responses' in operation and '200' in operation['responses']:
        response = operation['responses']['200']
        if 'content' in response and 'application/json' in response['content']:
            schema = response['content']['application/json']['schema']
            if '$ref' in schema:
                return schema['$ref'].split('/')[-1]
            elif schema.get('type') == 'array' and 'items' in schema:
                item_type = convert_type(schema['items'])
                return f'List[{item_type}]'
            else:
                return convert_type(schema)
    return 'Any'

def create_query_resolvers(paths: Dict[str, Any]) -> str:
    """Create query resolvers from GET endpoints."""
    queries = []
    
    for path, methods in paths.items():
        if 'get' in methods:
            operation = methods['get']
            query_name = sanitize_name(operation.get('operationId', f'get_{path.replace("/", "_")}'))
            response_type = resolve_response_type(operation)
            
            parameters = []
            if 'parameters' in operation:
                for param in operation['parameters']:
                    param_name = sanitize_name(param['name'])
                    param_type = convert_type(param['schema'])
                    
                    # Handle default values and required flag
                    if not param.get('required', False):
                        param_type = f'Optional[{param_type}]'
                        if 'default' in param['schema']:
                            default_value = param['schema']['default']
                            if isinstance(default_value, str):
                                default_value = f'"{default_value}"'
                            parameters.append(f'{param_name}: {param_type} = {default_value}')
                        else:
                            parameters.append(f'{param_name}: {param_type} = None')
                    else:
                        parameters.append(f'{param_name}: {param_type}')
            
            query_description = operation.get('description', '').strip()
            if operation.get('summary'):
                query_description = f"{operation['summary']}\n\n{query_description}"
            
            queries.append(f"""
    @strawberry.field(description=\"\"\"{query_description}\"\"\")
    async def {query_name}(self, {', '.join(parameters)}) -> {response_type}:
        # Implementation would go here
        raise NotImplementedError()
""")
    
    return """
@strawberry.type
class Query:
""" + ''.join(queries)

def resolve_request_type(operation: Dict[str, Any]) -> str:
    """Resolve the request type from an operation."""
    if 'requestBody' in operation:
        request_body = operation['requestBody']
        if 'content' in request_body and 'application/json' in request_body['content']:
            schema = request_body['content']['application/json']['schema']
            if '$ref' in schema:
                return f"{schema['$ref'].split('/')[-1]}Input"
            else:
                return convert_type(schema)
    return 'Any'

def create_mutation_resolvers(paths: Dict[str, Any]) -> str:
    """Create mutation resolvers from POST/PUT/DELETE endpoints."""
    mutations = []
    
    for path, methods in paths.items():
        for method in ['post', 'put', 'delete']:
            if method in methods:
                operation = methods[method]
                mutation_name = sanitize_name(operation.get('operationId', f'{method}_{path.replace("/", "_")}'))
                
                input_type = resolve_request_type(operation)
                response_type = resolve_response_type(operation)
                
                mutation_description = operation.get('description', '').strip()
                if operation.get('summary'):
                    mutation_description = f"{operation['summary']}\n\n{mutation_description}"
                
                mutations.append(f"""
    @strawberry.mutation(description=\"\"\"{mutation_description}\"\"\")
    async def {mutation_name}(self, input: {input_type}) -> {response_type}:
        # Implementation would go here
        raise NotImplementedError()
""")
    
    return """
@strawberry.type
class Mutation:
""" + ''.join(mutations)

def create_schema(openapi_spec: Dict[str, Any]) -> str:
    """Create a complete GraphQL schema from OpenAPI specification."""
    types = []
    
    # First, create the SiaType interface
    types.append("""
@strawberry.interface
class SiaType:
    \"\"\"Base interface for types converted from Sia network API responses\"\"\"
    pass

@strawberry.interface
class SiaInput:
    \"\"\"Base interface for input types converted from Sia network API requests\"\"\"
    pass
""")

    
    # Create types from components/schemas
    if 'components' in openapi_spec and 'schemas' in openapi_spec['components']:
        for name, schema in openapi_spec['components']['schemas'].items():
            if schema.get('type') == 'object' or ('allOf' in schema and any(s.get('type') == 'object' for s in schema['allOf'])):
                types.append(create_type(name, schema, schema.get('required', [])))
                # Create input types for mutations
                types.append(create_input_type(name, schema, schema.get('required', [])))
            elif 'enum' in schema:
                types.append(create_enum_type(name, schema))
    
    # Create Query and Mutation types
    types.append(create_query_resolvers(openapi_spec['paths']))
    types.append(create_mutation_resolvers(openapi_spec['paths']))
    
    # Create the schema
    schema_def = """
import strawberry
import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum

""" + '\n'.join(types) + """

schema = strawberry.Schema(query=Query, mutation=Mutation)
"""
    
    return schema_def

def main():
    # Load OpenAPI spec from file
    with open('openapi.yml', 'r') as f:
        openapi_spec = yaml.safe_load(f)
    
    # Generate schema
    schema = create_schema(openapi_spec)
    
    # Write to file
    with open('schema.py', 'w') as f:
        f.write(schema)

if __name__ == "__main__":
    main()
