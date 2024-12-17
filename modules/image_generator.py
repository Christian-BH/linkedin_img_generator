import logging
from typing import Dict

from openai import AzureOpenAI


class ImageGenerator:
    """
    Class for generating images of people based on the provided person profile and instructions.

    Args:
        instructions_toml (Dict): (Nested) Dictionary of instructions for the OpenAI API. Must have keys:
            img_gen_api, img_gen_settings, prompts. Each key contains a dictionary of settings for the
            corresponding part of the OpenAI API.
        api_key (str): API key for the OpenAI API.
    """

    def __init__(self, instructions_toml: Dict, api_key: str):
        self.api_key = api_key
        # Extract the necessary information from the instructions file and save as class variables for easy reference
        self.endpoint = instructions_toml.get("img_gen_api")
        self.img_gen_settings = instructions_toml.get("img_gen_settings")
        self.instructions = instructions_toml.get("prompts")

    def _init_openai(self):
        """Initialize OpenAI client"""
        client = AzureOpenAI(
            api_key=self.api_key, **self.endpoint  # Dictionary of endpoint settings
        )
        return client

    def _assemble_prompt(self, content: str):
        """
        Assembles the prompt for the OpenAI API

        Args:
            content (str): The person profile to generate an image for

        Returns:
            prompt (str): Prompt of the image generation model

        """

        for key in ["instructions"]:  # Must have keys
            if self.instructions.get(key) is None:
                self.instructions[key] = ""
                logging.warning(
                    f"{key} in instructions returns None, replacing with empty string"
                )

        prompt = f"{self.instructions.get('instructions')}\n>>>>>{content}<<<<<"
        return prompt

    def generate(self, content: str):
        """
        Generate an image from OpenAI

        Args:
            content (str): The person profile to generate an image for

        Returns:
            response (str): URL to the generated image
        """
        client = self._init_openai()

        prompt = self._assemble_prompt(content=content)

        response = client.images.generate(
            model=self.img_gen_settings.get("model"),
            prompt=prompt,
            n=self.img_gen_settings.get("n"),  # Number of images to generate
            size=self.img_gen_settings.get("size"),  # Square images works best
        )

        return response.data[0].url
