import io
import base64
from PIL import Image

def resize_image(image, target_size=100, format="JPEG"):
    # Calculate the target size in bytes
    target_size_bytes = target_size * 1024

    # Convert the image array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Initialize the resizing factor
    factor = 0.9

    # Variable to store the encoded image
    encoded_image = None

    # Resize the image until it fits within the target size
    while True:
        with io.BytesIO() as output:
            # Save the image to the output buffer
            image_pil.save(output, format=format)
            encoded_image = output.getvalue()

        # Check if the encoded image size is within the target size
        if len(encoded_image) <= target_size_bytes:
            break

        # Reduce the size of the image by the factor
        width, height = image_pil.size
        image_pil = image_pil.resize((int(width * factor), int(height * factor)))
        factor *= 0.9

    return image_pil

def encode_image(image_pil, format="JPEG"):
    with io.BytesIO() as output:
        # Save the image to the output buffer
        image_pil.save(output, format=format)
        encoded_image = output.getvalue()

    # Encode the image as base64 and convert it to a string
    base64_encoded_image = base64.b64encode(encoded_image).decode("utf-8")
    return base64_encoded_image

def image_publisher(client, IMAGE_FEED_ID, ndarray_image, format="JPEG"):
    resized_image = resize_image(ndarray_image, format=format)
    img_str = encode_image(resized_image, format=format)

    # Publish the encoded image to the client
    client.publish(IMAGE_FEED_ID, img_str)
