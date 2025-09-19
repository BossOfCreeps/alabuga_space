from io import BytesIO

from PIL import Image
from pyzbar.pyzbar import decode


def decode_qr_from_image(image_data: bytes) -> str:
    image = Image.open(BytesIO(image_data))
    if image.mode != "RGB":
        image = image.convert("RGB")

    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
