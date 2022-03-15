import configparser


class UserConfigs:
    def __init__(self) -> None:
        parser = configparser.ConfigParser()
        parser.read("config.ini")

        self.client_id = parser["reddit"]["client_id"]
        self.client_secret = parser["reddit"]["client_secret"]
        self.user_agent = parser["reddit"]["user_agent"]
