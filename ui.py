import base64
import json
import os 

import cv2
import numpy as np
import requests
import streamlit as st
from PIL import Image


def str_to_image(s: str) -> np.ndarray:
    img_bytes = base64.b64decode(s)
    return cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), flags=cv2.IMREAD_COLOR)


st.title("Better Images example")
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

HOST = os.environ.get('BETTER_IMAGES_HOST', 'http://127.0.0.1:8000')
endpoints = {'enlighten': 'improve_colors',
             'remove artifacts': 'filter_artifacts'
             }
endpoint = endpoints[st.radio('operation', list(endpoints.keys()))]


def process(uploaded_file=uploaded_file, endpoint=endpoint):
    img_b64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    if st.button('Process!'):
        url = f'{HOST}/{endpoint}'
        print(f'posting to {url}')
        resp = requests.post(url,
                             data=json.dumps({'auth_key': os.environ['BETTER_IMAGES_API_KEY'], 'image': img_b64}).encode(),
                             headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
                             )
        result = resp.json()
        st.write(result['message'])
        if not result['error']:
            st.image(
                cv2.cvtColor(str_to_image(result['image']), cv2.COLOR_BGR2RGB),
                caption='Processed image.', use_column_width=True)


if uploaded_file is not None:
    process()
