# Bluesky-Python
Just a very lightweight wrapper around the Bluesky API


### Installation
`pip install -U bluesky-python`

### Example

```py
from bluesky import BlueskyBasicClient

client = BlueskyBasicClient.from_login_data("example.bsky.social", "1234567890")

client.say("Hello World!")
```