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
    
    # Handle allOf
    if 'allOf' in schema:
        for item in schema['allOf']:
            if '$ref' in item:
                return item['$ref'].split('/')[-1]
            elif 'type' in item:
                return convert_type(item)
        return 'Any'  # fallback if no type found
    
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
    
    # Handle allOf descriptions
    if 'allOf' in schema:
        for item in schema['allOf']:
            if 'description' in item:
                desc_parts.append(item['description'])
    
    # Add main description
    elif 'description' in schema:
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
    
    return ' | '.join(filter(None, desc_parts))


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
        description = description.replace('\n', '')
        field_args.append(f'description="{description}"')
    
    # Add default value only if explicitly specified
    if 'default' in schema:
        default_value = schema['default']
        if isinstance(default_value, str):
            default_value = f'"{default_value}"'
        field_args.append(f'default={default_value}')
    
    # Add original name if different from snake_case
    snake_case_name = to_snake_case(name)
    if snake_case_name != name:
        field_args.append(f'name="{name}"')
    else:
        field_args.append(f'name="{name}"')
    
    field_decorator = f'strawberry.field({", ".join(field_args)})' if field_args else 'strawberry.field()'
    
    return f'    {snake_case_name}: {field_type} = {field_decorator}'

def create_type(name: str, schema: Dict[str, Any], required: List[str] = None) -> str:
    """Create a Strawberry type from OpenAPI schema."""
    if required is None:
        required = []
    
    fields = []
    type_description = get_field_description(schema)
    
    # Handle simple allOf with just reference and description
    if 'allOf' in schema:
        ref_type = None
        for item in schema['allOf']:
            if '$ref' in item:
                ref_type = item['$ref'].split('/')[-1]
        
        if ref_type and len(schema['allOf']) <= 2:  # Only ref and possibly description
            return f"""
@strawberry.type(description="{type_description}")
class {name}({ref_type}):
    pass
"""
    
    if not schema.get('properties') and not schema.get('allOf'):
        # For types without properties
        return f"""
@strawberry.type(description="{type_description}")
class {name}(SiaType):
    _dummy: Optional[str] = strawberry.field(default=None)
"""
    
    # Handle properties from allOf
    if 'allOf' in schema:
        properties = {}
        for item in schema['allOf']:
            if 'properties' in item:
                properties.update(item['properties'])
            if 'required' in item:
                required.extend(item['required'])
        schema['properties'] = properties
    
    for prop_name, prop_schema in schema.get('properties', {}).items():
        fields.append(get_field_definition(prop_name, prop_schema, required))
    
    if type_description:
        type_description = type_description.replace('\n', ' ')
        type_decorator = f'@strawberry.type(description="{type_description}")'
    else:
        type_decorator = '@strawberry.type'
    
    # If no fields were added but we have a description
    if not fields:
        return f"""
{type_decorator}
class {name}(SiaType):
    _dummy: Optional[str] = strawberry.field(default=None)
"""
    
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
        
    type_def = create_type(f"{name}Input", schema, required)
    return type_def.replace('(SiaType)', '')  # Remove SiaType from input types

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

def get_dependencies(schema: Dict[str, Any]) -> set:
    """Extract all type dependencies from a schema, including nested ones."""
    deps = set()
    
    def extract_deps(s):
        if '$ref' in s:
            deps.add(s['$ref'].split('/')[-1])
        elif s.get('type') == 'array' and 'items' in s:
            if '$ref' in s['items']:
                deps.add(s['items']['$ref'].split('/')[-1])
            else:
                extract_deps(s['items'])
        
        # Extract from properties
        for prop_schema in s.get('properties', {}).values():
            if '$ref' in prop_schema:
                deps.add(prop_schema['$ref'].split('/')[-1])
            elif prop_schema.get('type') == 'array' and 'items' in prop_schema:
                if '$ref' in prop_schema['items']:
                    deps.add(prop_schema['items']['$ref'].split('/')[-1])
                else:
                    extract_deps(prop_schema['items'])
        
        # Extract from allOf
        for item in s.get('allOf', []):
            if '$ref' in item:
                deps.add(item['$ref'].split('/')[-1])
            if 'properties' in item:
                for prop_schema in item['properties'].values():
                    if '$ref' in prop_schema:
                        deps.add(prop_schema['$ref'].split('/')[-1])
                    elif prop_schema.get('type') == 'array' and 'items' in prop_schema:
                        if '$ref' in prop_schema['items']:
                            deps.add(prop_schema['items']['$ref'].split('/')[-1])
                        else:
                            extract_deps(prop_schema['items'])
    
    extract_deps(schema)
    return deps


def topological_sort(schemas: Dict[str, Dict[str, Any]]) -> List[str]:
    """Sort schemas based on dependencies using depth-first search."""
    # Build dependency graph
    graph = {name: get_dependencies(schema) for name, schema in schemas.items()}
    
    # Track visited nodes and result
    visited = set()
    temp_mark = set()  # for cycle detection
    result = []
    
    def visit(name):
        if name in temp_mark:
            # We found a cycle
            cycle_path = []
            for node, deps in graph.items():
                if name in deps:
                    cycle_path.append(f"{node} -> {name}")
            raise ValueError(f"Circular dependency detected: {', '.join(cycle_path)}")
            
        if name not in visited:
            temp_mark.add(name)
            
            # Visit all dependencies first
            for dep in sorted(graph.get(name, set())):  # Sort for deterministic ordering
                if dep in graph:  # Only visit if it's a complex type
                    visit(dep)
            
            temp_mark.remove(name)
            visited.add(name)
            result.append(name)
    
    # Visit all nodes
    for name in sorted(graph.keys()):  # Sort for deterministic ordering
        if name not in visited:
            visit(name)
    
    return result


def create_schema(openapi_spec: Dict[str, Any]) -> str:
    """Create a complete GraphQL schema from OpenAPI specification."""
    scalar_types = []
    complex_types = []
    
    # First pass: identify and create scalar types
    schemas = openapi_spec.get('components', {}).get('schemas', {})
    schema_types = {}  # Track schema types for sorting
    
    for name, schema in schemas.items():
        if not any(['allOf' in schema, 'enum' in schema, schema.get('type') == 'object']):
            description = get_field_description(schema)
            type_name = convert_type(schema)
            if description:
                description = description.replace('\n', ' ')
                scalar_types.append(f"""
@strawberry.scalar(description="{description}")
class {name}({type_name}):
    pass
""")
            else:
                scalar_types.append(f"""
@strawberry.scalar
class {name}({type_name}):
    pass
""")
        else:
            schema_types[name] = schema
    
    # Sort complex types by dependencies
    sorted_names = topological_sort(schema_types)
    
    # Create complex types in correct order
    for name in sorted_names:
        schema = schema_types[name]
        if 'enum' in schema:
            complex_types.append(create_enum_type(name, schema))
        else:
            complex_types.append(create_type(name, schema, schema.get('required', [])))
            # Also create input types if needed
            # if schema.get('type') == 'object' or ('allOf' in schema and any(s.get('type') == 'object' for s in schema.get('allOf', []))):
            #     complex_types.append(create_input_type(name, schema, schema.get('required', [])))
    
    # Rest of the function remains the same...
    base_interface = """
@strawberry.interface
class SiaType:
    "Base interface for types converted from Sia network API responses"
    pass
"""
    
    query_type = create_query_resolvers(openapi_spec['paths'])
    mutation_type = create_mutation_resolvers(openapi_spec['paths'])
    
    schema_def = """
import strawberry
import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum

""" + base_interface + '\n'.join(scalar_types + complex_types + [query_type, mutation_type]) + """

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
