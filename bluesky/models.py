from .api import _create_session, _post
from datetime import datetime, timezone
from enum import Enum
from .utils import *
from mimetypes import guess_type
from pyenvs import load_dotenv
import os


class BlueskyBasicClient:
    def __init__(self, accessToken, did):
        self.token = accessToken
        self.did = did

    @classmethod
    def from_login_data(cls, username, password):
        return cls(*_create_session(username, password))

    @classmethod
    def from_login_env(
        cls, Username_Key="BSKY_APP_HANDLE", Password_Key="BSKY_APP_PASSWORD"
    ):
        """
        Essentially the same as ~.from_login_data(), except that the credentials are being
        pulled from `os.environ`
        """
        load_dotenv()
        return cls.from_login_data(os.environ[Username_Key], os.environ[Password_Key])

    def say(self, message, languages=["en-US"], files: list["File"] = None):
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        post = {"$type": "app.bsky.feed.post", "text": message, "createdAt": now}
        post["langs"] = languages
        post["facets"] = parse_facets(post["text"])
        if files:
            images = []
            for file in files:
                fileBlob = file.upload_blob(self)
                images.append({"alt": file.alt, "image": fileBlob})
            post["embed"] = {"$type": "app.bsky.embed.images", "images": images}

        _post(self, post)


class File:
    def __init__(self, path, alt=""):
        self.path = path
        self.mimetype = guess_type(path)
        self.alt = alt
        self.data = open(path, "rb").read()

    def upload_blob(self, session):
        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
            headers={
                "Content-Type": self.mimetype,
                "Authorization": "Bearer " + session.token,
            },
            data=self.data,
        )
        resp.raise_for_status()
        return resp.json()["blob"]
