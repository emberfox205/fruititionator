import io
import base64
from PIL import Image

def resize_image(image, target_size=100):
    target_size_bytes = target_size * 1024
    image_pil = Image.fromarray(image)
    factor = 0.9
    encoded_image = None

    while True:
        with io.BytesIO() as output:
            image_pil.save(output, format="JPEG")
            encoded_image = output.getvalue()

        if len(encoded_image) <= target_size_bytes:
            break

        width, height = image_pil.size
        image_pil = image_pil.resize((int(width * factor), int(height * factor)))
        factor *= 0.9

    return image_pil

def encode_image(image_pil):
    with io.BytesIO() as output:
        image_pil.save(output, format="JPEG")
        encoded_image = output.getvalue()

    base64_encoded_image = base64.b64encode(encoded_image).decode("utf-8")
    return base64_encoded_image

def image_publisher(client, IMAGE_FEED_ID, ndarray_image):
    resized_image = resize_image(ndarray_image)
    img_str = encode_image(resized_image)
    client.publish(IMAGE_FEED_ID, img_str)