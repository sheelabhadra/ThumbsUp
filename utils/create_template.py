# import pandas as pd
# import requests

# from io import BytesIO
# from jinja2 import Template
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration

# # Load the processor and model
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
# model = BlipForConditionalGeneration.from_pretrained(
#     "Salesforce/blip-image-captioning-large"
# )


# # Function to get description of an image
# def get_image_description(image_url):
#     try:
#         # response = requests.get(image_url)
#         # image = Image.open(BytesIO(response.content))
#         image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
#         text = "a photography of"
#         inputs = processor(image, text, return_tensors="pt")
#         outputs = model.generate(**inputs)
#         description = processor.decode(outputs[0], skip_special_tokens=True)
#         print(image_url, description)
#         return description
#     except Exception as e:
#         return str(e)


# df_1 = pd.read_csv("../data/youtube_channel_data_1.csv")
# df_1 = df_1[["Title", "Thumbnail"]]

# df_2 = pd.read_csv("../data/youtube_channel_data_2.csv")
# df_2 = df_2[["Title", "Thumbnail"]]

# df = pd.concat([df_1, df_2], ignore_index=True, sort=False)

# # Apply the function to the DataFrame
# df["Description"] = df["Thumbnail"].apply(get_image_description)

# # Convert DataFrame to list of dictionaries
# data = df[["Title", "Description"]].to_dict(orient="records")

# # Define the template
# template_str = """
# [
# {% for item in items %}
# {
#     "prompt": "{{ item.Title }}",
#     "response": "{{ item.Description }}"
# }
# {% if not loop.last %},{% endif %}
# {% endfor %}
# ]
# """
# template = Template(template_str)

# # Render the template with data
# rendered = template.render(items=data)

# # Save to a file
# with open("../data/dataset_blip_large.json", "w") as f:
#     f.write(rendered)

import re
import pandas as pd
import requests

from io import BytesIO
from jinja2 import Template
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def de_emojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# Function to get description of an image
def get_image_description(title, image_url):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
        text = f"Photo title: {title}, a photography of "
        inputs = processor(image, text, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=300)
        description = processor.decode(outputs[0], skip_special_tokens=True)
        print(image_url, description)
        return description
    except Exception as e:
        return str(e)


# Load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

df_1 = pd.read_csv("../data/youtube_channel_data_1.csv")
df_1 = df_1[["Title", "Thumbnail"]]

df_2 = pd.read_csv("../data/youtube_channel_data_2.csv")
df_2 = df_2[["Title", "Thumbnail"]]

df = pd.concat([df_1, df_2], ignore_index=True, sort=False)

# Apply the function to the DataFrame
df["Title"]= df["Title"].apply(lambda s:s.replace('"', "`")).apply(de_emojify)
# df["Title"] = df["Title"].replace({'"': '<br>'}, regex=True).apply(de_emojify)
df["Description"] = df.apply(lambda x: get_image_description(x.Title, x.Thumbnail), axis=1)

# Convert DataFrame to list of dictionaries
data = df[["Title", "Description"]].to_dict(orient="records")

# Define the template
template_str = """
[
{% for item in items %}
{
    "prompt": "{{ item.Title }}",
    "response": "{{ item.Description }}"
}
{% if not loop.last %},{% endif %}
{% endfor %}
]
"""
template = Template(template_str)

# Render the template with data
rendered = template.render(items=data)

# Save to a file
with open("../data/dataset_blip_large_clean.json", "w") as f:
    f.write(rendered)
