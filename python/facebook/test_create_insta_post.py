import requests
from dotenv import dotenv_values

CONFIG = {
    **dotenv_values("./.env")
}

def create_container(url, caption=""):
    user_id = CONFIG["INSTA_USER_ID"]
    response = requests.post(
        url=f"https://graph.instagram.com/v21.0/{user_id}/media",
        params={
            "image_url": url,
            "caption": caption,
            "access_token": CONFIG["INSTA_ACCESS_TOKEN"]
        }
    )
    return response.json()

def publish_container(container_id):
    user_id = CONFIG["INSTA_USER_ID"]
    response = requests.post(
        url=f"https://graph.instagram.com/v21.0/{user_id}/media_publish",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": CONFIG["INSTA_ACCESS_TOKEN"],
            "creation_id": container_id
        }
    )
    return response.json()

def publish_image(url, caption=""):
    container = create_container(url, caption)
    try:
        container_id = container.get("id")
        return publish_container(container_id)
    except KeyError as e:
        print("Key not found in response:", e)
        print("Response:", container)
        return None

# container = create_container("https://transparentimage.s3.us-east-1.amazonaws.com/stockly_1024.png", "Stockly Logo")


