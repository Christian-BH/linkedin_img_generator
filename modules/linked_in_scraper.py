from typing import Dict

from linkedin_api import Linkedin


class LinkedInScraper:
    def __init__(self, user_email: str, user_password: str, linkedin_url: str):
        self.email = user_email
        # self.password = input()
        self.password = user_password
        self.linkedin_url = linkedin_url
        # Initialize LinkedIn API
        self.linkedin_api = Linkedin(self.email, self.password)

    def scrape(self):
        """Returns main profile information"""
        profile = self.linkedin_api.get_profile(self.linkedin_url)
        return profile

    def extract_connections(self, profile: Dict = None):
        """Extracts connections from the profile"""
        if profile is None:
            profile = self.scrape()
        urn_id = profile.get("urn_id")
        connections = self.linkedin_api.get_connections(
            urn_id
        )  # This requires a different id input than other methods
        return connections

    def extract_long_skill_list(self):
        """Extracts a long list of skills"""
        skills = self.linkedin_api.get_skills(self.linkedin_url)
        return skills
