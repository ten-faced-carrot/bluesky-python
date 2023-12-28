import requests


def _create_session(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD):
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
    )
    resp.raise_for_status()
    session = resp.json()
    print(session)
    return session["accessJwt"], session["did"]


def _post(session, payload):
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session.token},
        json={
            "repo": session.did,
            "collection": "app.bsky.feed.post",
            "record": payload,
        },
    )

    resp.raise_for_status()
