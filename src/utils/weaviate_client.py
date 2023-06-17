import weaviate

client = weaviate.Client(
  url="https://colombia-dev-f309rzd4.weaviate.network",  # URL of your Weaviate instance
  auth_client_secret=weaviate.AuthApiKey(api_key="tG6R2oBEzFrTAz6Hqd5EsAqmut6lTPiWbBIT"), # (Optional) If the Weaviate instance requires authenticationxw
)

def get_answers(ebd):
    response = (
        client.query
        .get("Message", ["message"])
        .with_near_vector({"vector":ebd})
        .with_limit(5)
        .do()
    )

    answers = response["data"]["Get"]["Message"]

    outputs = []
    for i, answer in enumerate(answers):
        message = answer["message"]
        if len(message)>5000:
            message = message[0:5000]
        outputs.append(message)
    return outputs
