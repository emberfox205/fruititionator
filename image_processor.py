import io, base64
from PIL import Image

def image_editor(ndarray_image): 
    image = Image.fromarray(ndarray_image)
    resized_image = image.resize((224, 224))
    return resized_image
    
def image_encoder(resized_image):
    # create a memory buffer -> save the PIL obj to it -> turn obj into bytes -> to string
    buffered = io.BytesIO()
    resized_image.save(buffered, format="JPEG", quality=75, optimize=True)
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

def image_publisher(client, IMAGE_FEED_ID, ndarray_image):
    resized_image = image_editor(ndarray_image)
    img_str = image_encoder(resized_image)
    client.publish(IMAGE_FEED_ID, img_str)