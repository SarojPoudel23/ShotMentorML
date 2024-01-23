from PIL import Image
import numpy as np
import pandas as pd

# Load the image
image_path = 'saroj.jpg'  # Replace with the actual path to your image
image = Image.open(image_path)

# Convert the image to a numpy array
image_array = np.array(image)
# image_array = np.expand_dims(image_array, axis=0)

resized_image = image.resize((28, 28))# Replace with your actual image array

resized_image_array = np.array(resized_image)
# Flatten the pixels
flattened_pixels = resized_image_array.flatten()

print(flattened_pixels.shape)
