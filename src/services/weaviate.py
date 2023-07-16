import weaviate

from utils.common import SettingsLoader


class Weaviate:

    APP_NAME = "WEAVIATE"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )
        self.client = weaviate.Client(
            url=self.options.get("url"),
            auth_client_secret=weaviate.AuthApiKey(
                api_key=self.options.get("api_key")
            ),
        )

    def get_answers(self, embedding):
        response = (
            self.client.query
            .get("Message", ["message"])
            .with_near_vector({"vector": embedding})
            .with_limit(5)
            .do()
        )

        answers = response["data"]["Get"]["Message"]
        
        outputs = []
        for answer in answers:
            message = answer["message"]
            if len(message)>5000:
                message = message[0:5000]
            outputs.append(message)
        return outputs
