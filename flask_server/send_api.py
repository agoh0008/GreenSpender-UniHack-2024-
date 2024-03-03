import base64
import json
import os
from urllib.parse import urlparse
from openai import OpenAI


def analyze_image_and_update_json(image_url, api_key):
    """
    This function analyzes an image using the OpenAI API and updates a JSON file with the analysis results.
    Parameters:
    - image_url: The URL of the image to analyze.
    - api_key: The API key for the OpenAI API.
    """
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)

    # Send a request to the API to analyze the image
    response = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Return JSON document with data. Only return JSON not other text. "
                                             "Give the category (in 1 of this type: Groceries, Food, Entertainment, Shopping, Other), total cost and month (first 3 words of month. If there is no month, put it Feb" 
                                             "For example: Groceries, 29.00, Jan "},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ],
            }
        ],
        max_tokens=500,
    )

    # Extract JSON data from the response
    json_string = response.choices[0].message.content.replace("```json\n", "").replace("\n```", "")
    print(json_string)
    json_data = json.loads(json_string)

    # Define the path for the JSON file to update
    json_filename = "D:\\Projects\\Hackathon1\\flask_server\\data.json"

    # Read existing data from the file, or initialize an empty dictionary if the file does not exist or is empty
    try:
        with open(json_filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Update the dictionary with new data from the analysis
    data.update(json_data)

    # Write the updated dictionary back to the JSON file
    with open(json_filename, 'a') as file:
        if os.path.getsize(json_filename) > 0:
            file.write(',\n')
        json.dump(data, file, indent=4)

    print(f"JSON data saved to {json_filename}")


# # Example usage
# image_url = 'https://image-storage--testing.s3.ap-southeast-2.amazonaws.com/images%5CWhatsApp+Image+2024-03-02+at+15.58.11_115d3483.jpg'
# api_key = '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'
# analyze_image_and_update_json(image_url, api_key)
