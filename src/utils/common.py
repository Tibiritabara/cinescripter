import utils.settings as settings


class SettingsLoader():

    @staticmethod
    def load(app_name: str, options: dict) -> dict:
        app_settings = getattr(settings, app_name)
        options = app_settings | options
        return options
