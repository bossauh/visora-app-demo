from jinja2 import Template


def load_prompt(path: str, data: dict) -> str:
    """
    Loads a prompt from a file and renders it using Jinja2 with the provided data.

    Args:
        path (str): The file path to the prompt template (e.g., 'prompts/playbook_generation.md').
        data (dict): A dictionary containing the data to be used in the template.

    Returns:
        str: The rendered prompt string.
    """
    with open(path, "r", encoding="utf-8") as file:
        template_str = file.read()

    template = Template(template_str)
    prompt = template.render(**data)
    return prompt


def json_to_nested_string(data, indent=0):
    """
    Converts a JSON object into a nested string format with keys and values.
    Skips keys with None, empty strings, or empty lists but includes valid False or 0 values.

    Args:
        data (dict or list): The JSON object to convert.
        indent (int): Current indentation level for nested structures.

    Returns:
        str: A formatted string representation of the JSON object.
    """
    result = []
    prefix = " " * indent  # Indentation for nested levels

    # Handle dictionary objects
    if isinstance(data, dict):
        for key, value in data.items():
            # Skip keys with None, empty strings, or empty lists
            if value is None or value == "" or value == []:
                continue

            if isinstance(value, dict):  # Nested dictionary
                result.append(f"{prefix}- {key}:")
                result.append(json_to_nested_string(value, indent=indent + 2))
            elif isinstance(value, list):  # List of items
                result.append(f"{prefix}- {key}:")
                for item in value:
                    if isinstance(item, (dict, list)):  # Nested structure in list
                        result.append(json_to_nested_string(item, indent=indent + 2))
                    else:  # Simple list item
                        result.append(f"{prefix}  - {item}")
            else:  # Simple key-value pair
                result.append(f"{prefix}- {key}: {value}")

    # Handle list objects
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):  # Nested structure in list
                result.append(json_to_nested_string(item, indent=indent + 2))
            else:  # Simple list item
                result.append(f"{prefix}- {item}")

    return "\n".join(result)
