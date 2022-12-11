"""
"""
from typing import List
from json import JSONDecodeError, loads

import openai
openai.api_key = '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'

def get_prompt_variations(prompt: str, count: int = 20) -> List:
    """
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Create a JSON list of {count} random objects that relate to \"{prompt}\".\nExample: [\"prompt1\", \"prompt2\", \"prompt3\"]",
        # prompt=f"Create a JSON list of {num} related prompts that describe a \"{prompt}\".\nExample: [\"prompt1\", \"prompt2\", \"prompt3\"]",
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract:
    raw_text_response = response['choices'][0]['text']
    try:
        json_data = loads(raw_text_response)
    except JSONDecodeError:
        fixed_raw_text = fix_broken_json(raw_text_response)
        json_data = loads(fixed_raw_text)
    return json_data


def fix_broken_json(broken_json_data: str) -> str:
    """GPT-3 might sometimes generate a broken JSON, this uses GPT-3 to fix it.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Fix this broken JSON:\n{broken_json_data}",
        temperature=1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']
