import replicate
import os
import logging
import requests
import re

# Set up Replicate API token
os.environ['REPLICATE_API_TOKEN'] = 'your_api_token_here'  # Replace with your actual API token

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize the filename
def sanitize_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    return text.strip()[:50]

def generate_images(prompt, shot_number, model):
    # Create directory to save images
    output_dir = 'generated_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.info(f"Generating image for Shot {shot_number}: {prompt}")

    try:
        output = replicate.run(
            model,
            input={
                "prompt": prompt,
                "num_outputs": 4
            }
        )

        # Sanitize the prompt text for the filename
        short_prompt = sanitize_filename(prompt)

        # Save all output images with the new naming convention
        shot_images = []
        for i, image_url in enumerate(output):
            response = requests.get(image_url)
            if response.status_code == 200:
                filename = f"{shot_number:03d}-{i}-{short_prompt}.png"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                logging.info(f"Image saved as {filepath}")
                shot_images.append(filepath)
            else:
                logging.error(f"Failed to download image {i} for Shot {shot_number}.")

        logging.info(f"All images for Shot {shot_number} generated and saved successfully.\n")
        return shot_images

    except Exception as e:
        logging.error(f"Error generating images for Shot {shot_number}: {e}\n")
        raise

if __name__ == "__main__":
    # This is just for testing
    generate_images("A beautiful sunset over the ocean", 1, "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")
