import requests
from dotenv import dotenv_values

CONFIG = {**dotenv_values("./.env")}


class InstagramService:
    def _create_container(self, url: str, caption: str = ""):
        user_id = CONFIG["INSTA_USER_ID"]
        response = requests.post(
            url=f"https://graph.instagram.com/v21.0/{user_id}/media",
            params={
                "image_url": url,
                "caption": caption,
                "access_token": CONFIG["INSTA_ACCESS_TOKEN"],
            },
        )
        return response.json()

    def _publish_container(self, container_id: str):
        user_id = CONFIG["INSTA_USER_ID"]
        response = requests.post(
            url=f"https://graph.instagram.com/v21.0/{user_id}/media_publish",
            headers={"Content-Type": "application/json"},
            params={
                "access_token": CONFIG["INSTA_ACCESS_TOKEN"],
                "creation_id": container_id,
            },
        )
        return response.json()

    def publish_image(self, url: str, caption: str = "") -> dict | None:
        """
        Publishes an image to instagram as a post.

        Parameters
        ----------
        url : str
            the url of the publicly hosted image
        caption : str, optional
            caption, by default ""

        Returns
        -------
        dict | None
            the success response, or None
        """
        container = self._create_container(url, caption)
        try:
            container_id = container.get("id")
            return self._publish_container(container_id)
        except KeyError as e:
            print("Key not found in response:", e)
            print("Response:", container)
            return None


instagram_service = InstagramService()
container = instagram_service.publish_image(
    "http://127.0.0.1:8000/instagram_image?url=https%3A%2F%2Fstockly-bendover.s3.us-east-1.amazonaws.com%2F4f7455028d904ee2bd1c86965b1922ad"
)
print(container)
