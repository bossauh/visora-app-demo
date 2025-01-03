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
