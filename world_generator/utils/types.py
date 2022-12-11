"""Types to help in the code
"""

from typing import TypedDict, Any

from PIL import Image

class WorldFrame(TypedDict):
    path: str
    image: Any
