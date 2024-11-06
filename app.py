import gradio as gr
import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/sd-community/sdxl-flash"
headers = {"Authorization": "Bearer <Your api key>"}  # Replace with actual token

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an error for non-200 responses
        if 'image' in response.headers.get('Content-Type', ''):
            return response.content
        else:
            print("Response is not an image:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error with API request:", e)
        return None

def text_to_image(prompt):
    image_byte = query({"inputs": prompt})
    if image_byte:
        image = Image.open(io.BytesIO(image_byte))
        return image
    else:
        return "Error generating image"

demo = gr.Interface(
    fn=text_to_image,
    inputs="text",
    outputs="image"
)

demo.launch(share=True)
