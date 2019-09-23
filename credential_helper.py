import configparser
import json
import requests


class CredentialHelper:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_access_token(self):
        if "credentials" not in self.config:
            raise "config file does not include credentials"

        if "client_id" not in self.config["credentials"] or "client_secret" not in self.config["credentials"]:
            raise "credentials section does not contain client_id or client_secret"

        client_id = self.config["credentials"]["client_id"]
        client_secret = self.config["credentials"]["client_secret"]

        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        res = requests.post(
            "https://api.oregonstate.edu/oauth2/token", params)
        res.raise_for_status()

        data = json.loads(res.text)

        return data["access_token"]
