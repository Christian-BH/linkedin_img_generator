"""
This script processes LinkedIn profiles and generates responses using OpenAI.

"""
import argparse
import logging
import os
import pickle

import tomli

from modules.config import LINKEDIN_ACCCOUNTS
from modules.use_openai import UtilizeOpenAI

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

    logging.info("Running process_profile_info.py")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    if args.instruction_path is None:
        logging.info("Using default instructions")
        # with open("modules/instructions/default_openai_settings.toml", "rb") as f:
        with open("instructions/default_openai_settings.toml", "rb") as f:
            instructions_toml = tomli.load(f)
    else:
        with open(args.instruction_path, "rb") as f:
            instructions_toml = tomli.load(f)

    if args.person_name is None:
        raise ValueError(
            "Please provide a person name to process, or set to 'ALL' to process all LinkedIn accounts from config file"
        )

    # Instructions file must have the following sections to parse into OpenAI
    must_have_keys = ["open_ai_api", "open_ai_settings", "prompts"]
    if not all([key in instructions_toml for key in must_have_keys]):
        raise ValueError(f"Instructions file must have keys: {must_have_keys}")

    # Setup & Run OpenAI
    logging.info(instructions_toml)
    openai = UtilizeOpenAI(instructions_toml=instructions_toml, api_key=api_key)

    if not os.path.exists("./outputs/responses"):
        os.makedirs("./outputs/responses")

    if args.person_name == "ALL":
        persons = LINKEDIN_ACCCOUNTS.keys()  # All persons in config
    else:
        persons = [args.person_name]  # Single person

    for person in persons:
        logging.info(f"Processing LinkedIn profile for {person}")

        # Load the profile
        with open(f"./outputs/profiles/{person}.pkl", "rb") as f:
            profile = pickle.load(f)

        logging.info(f"Profile containes the following keys: {profile.keys()}")

        # Generate a response from OpenAI
        response = openai.generate(content=profile)
        logging.info(f"Response: {response}")

        # Save the response to a text file
        with open(f"./outputs/responses/{person}.txt", "w", encoding="utf-8") as f:
            f.write(response)


if __name__ == "__main__":
    main()
