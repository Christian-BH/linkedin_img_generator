"""
Job to scrape LinkedIn profiles
"""
import argparse
import logging
import os
import pickle

from modules.config import LINKEDIN_ACCCOUNTS
from modules.linked_in_scraper import LinkedInScraper

parser = argparse.ArgumentParser()
parser.add_argument(
    "--person_name",
    dest="person_name",
    type=str,
    default=None,
    help="Name of the person, must be enclosed in quotes. Set to 'ALL' to process all people.",
)
parser.add_argument(
    "--user_email",
    dest="user_email",
    type=str,
    default=None,
    help="Email of the user to login to LinkedIn",
)


def main(args=None):
    """Main Function"""
    # Parse command-line arguments
    args = parser.parse_args(args)

    logging.basicConfig(level=logging.INFO)

    logging.info("Running extract_profile_info.py")

    name_link_url = LINKEDIN_ACCCOUNTS.get(args.person_name)

    if name_link_url is None:
        raise ValueError(
            f"Person name {args.person_name} not found in LINKEDIN_ACCCOUNTS"
        )

    password = input("Enter your LinkedIn password: ")
    logging.info(
        f"Using following API inputs: {args.user_email}, {password}, {name_link_url}"
    )
    linkedin_scraper = LinkedInScraper(
        user_email=args.user_email, user_password=password, linkedin_url=name_link_url
    )

    logging.info("Scraping LinkedIn")
    profile = linkedin_scraper.scrape()

    logging.info(f"Profile keys: {profile.keys()}")

    logging.info("Cleaning profile Information")
    # Retain relevant information
    keys_to_keep = [
        "firstName",
        "headline",
        "summary",
        "experience",
        "industryName",
        "education",
        "skills",
        "languages",
        "honors",
        "projects",
        "publications",
        "certifications",
        "volunteer",
    ]
    extracted_profile = {k: profile.get(k) for k in keys_to_keep}

    # Save the profile
    if not os.path.exists("./outputs/profiles"):
        os.makedirs("./outputs/profiles")

    with open(f"./outputs/profiles/{args.person_name}.pkl", "wb") as f:
        pickle.dump(extracted_profile, f)


if __name__ == "__main__":
    main()
