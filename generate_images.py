"""
Image Generation Job
"""
import argparse
import logging
import os

import requests
import tomli

from modules.config import LINKEDIN_ACCCOUNTS
from modules.image_generator import ImageGenerator

parser = argparse.ArgumentParser()
parser.add_argument(
    "--person_name",
    dest="person_name",
    type=str,
    default=None,
    help="Name of the person, must be enclosed in quotes. Set to 'ALL' to process all people.",
)
parser.add_argument(
    "--instruction_path",
    dest="instruction_path",
    type=str,
    default=None,
    help="Path to the toml formatted instructions file. Defaults to None, which will load the default instructions.",
)


def main(args=None):
    """Main Function"""
    # Parse command-line arguments
    args = parser.parse_args(args)

    logging.basicConfig(level=logging.INFO)

    logging.info("Running generage_images.py")

    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Load the instructions file
    if args.instruction_path is None:
        logging.info("Using default instructions")
        with open("modules/instructions/default_image_gen_settings.toml", "rb") as f:
            instructions_toml = tomli.load(f)
    else:
        with open(args.instruction_path, "rb") as f:
            instructions_toml = tomli.load(f)

    # Instructions file must have the following sections to parse into OpenAI
    must_have_keys = ["img_gen_api", "img_gen_settings", "prompts"]
    if not all([key in instructions_toml for key in must_have_keys]):
        raise ValueError(f"Instructions file must have keys: {must_have_keys}")

    # Process the LinkedIn profiles and generate images
    if args.person_name == "ALL":
        persons = LINKEDIN_ACCCOUNTS.keys()  # All persons in config
    else:
        persons = [args.person_name]  # Single person

    for person in persons:
        logging.info(f"Processing LinkedIn profile for {person}")

        # Load the profile
        with open(f"./outputs/responses/{args.person_name}.txt", "r") as f:
            profile = f.read()

        # Setup & Run OpenAI
        logging.info(instructions_toml)
        openai = ImageGenerator(instructions_toml=instructions_toml, api_key=api_key)

        response = openai.generate(content=profile)
        logging.info(f"Response: {response}")

        # Save the image from the URL response
        if not os.path.exists("./outputs/images"):
            os.makedirs("./outputs/images")

        with open(f"./outputs/images/{args.person_name}.png", "wb") as f:
            f.write(requests.get(response).content)


if __name__ == "__main__":
    main()
