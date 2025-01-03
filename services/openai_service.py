import json
import os
import pprint

from loguru import logger
from openai import OpenAI

from utils.prompt_utils import json_to_nested_string, load_prompt

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_prompt_for_playbook(scraped_data: dict, sell_description: str):
    prompt = [
        {
            "role": "system",
            "content": load_prompt(
                os.path.join(os.getcwd(), "prompts", "playbook_generation.md"),
                data={
                    "scraped_data": json_to_nested_string(scraped_data),
                    "sell_description": sell_description,
                },
            ),
        }
    ]

    logger.debug(
        f"Using the following prompt for generating the playbook: {pprint.pformat(prompt)}"
    )

    return prompt


def create_prompt_for_bot_response(
    message_history: list[dict],
    calendar_link: str,
    sell_description: str,
    playbook: dict,
    sdr_name: str,
    sdr_description: str,
    initial_contact: bool,
):
    prompt = []

    # Add system prompt
    prompt.append(
        {
            "role": "system",
            "content": load_prompt(
                os.path.join(os.getcwd(), "prompts", "message_generation.md"),
                data={
                    "sdr_name": sdr_name,
                    "sdr_description": sdr_description,
                    "playbook": playbook,
                    "sell_description": sell_description,
                    "calendar_link": calendar_link,
                    "initial_contact": initial_contact,
                },
            ),
        }
    )

    prompt.extend(message_history)

    logger.debug(
        f"Using the following prompt for generating a response: {pprint.pformat(prompt)}"
    )

    return prompt


def generate_playbook(scraped_data: dict, sell_description: str, calendar_link: str):
    """
    Generates a sales playbook using OpenAI's API.

    Args:
        scraped_data (dict): Data extracted from the LinkedIn profile.
        sell_description (str): Description of the product or service being sold.
        calendar_link (str): Link to schedule a meeting.

    Returns:
        dict: The generated playbook.
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=create_prompt_for_playbook(scraped_data, sell_description),
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    response = completion.choices[0].message.content
    playbook = json.loads(response)

    return playbook


def generate_bot_response(
    message_history: list[dict],
    sell_description: str,
    calendar_link: str,
    playbook: dict,
    sdr_name: str,
    sdr_description: str,
    initial_contact: bool = False,
):
    """
    Generates a response from the bot using OpenAI's API.

    Args:
        message_history (list): Conversation history including user and bot messages.
        sell_description (str): What the SDR is selling.
        calendar_link (str): The SDR's calendar link.
        playbook (dict): The sales playbook to guide the bot's responses.
        sdr_name (str): The SDR's name.
        sdr_description (str): The SDR's description.
        initial_contact (bool): Whether the response to generate is the bot sending a initial contact.

    Returns:
        str: The bot's response.
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=create_prompt_for_bot_response(
            message_history=message_history,
            sell_description=sell_description,
            calendar_link=calendar_link,
            playbook=playbook,
            sdr_name=sdr_name,
            sdr_description=sdr_description,
            initial_contact=initial_contact,
        ),
        max_tokens=1024,
    )

    response = completion.choices[0].message.content

    return response
