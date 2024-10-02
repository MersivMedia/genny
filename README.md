# genny

This application generates images based on text prompts using various AI models through the Replicate API and displays them in a Gradio web interface.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-image-generator.git
   cd ai-image-generator
   ```

2. Install the required dependencies:
   ```
   pip install gradio replicate requests
   ```

## Configuration

### Replicate API Token

1. Sign up for an account at [Replicate](https://replicate.com/) if you haven't already.
2. Go to your [account page](https://replicate.com/account) to find your API token.
3. Open the `image_generator.py` file and replace the placeholder API token with your actual token:

   ```python
   os.environ['REPLICATE_API_TOKEN'] = 'your_api_token_here'
   ```

## Usage

1. Run the Gradio interface:
   ```
   python gradio_interface.py
   ```

2. Open the provided local URL in your web browser.

3. Upload a `prompts.json` file containing your image generation prompts. The file should have the following format:
   ```json
   [
     {
       "shot_number": 1,
       "prompt": "Your first prompt here"
     },
     {
       "shot_number": 2,
       "prompt": "Your second prompt here"
     }
   ]
   ```

4. Select the AI model you want to use from the dropdown menu.

5. Click the "Generate Images" button to start the image generation process.

6. The generated images will be displayed in the interface as they are created.

## Available Models

- SDXL
- Flux Schnell
- Flux Dev
- D-Journey
- SDXL Lightning 4step

## Notes

- The generated images are saved in a `generated_images` folder in the project directory.
- The application displays the images progressively as they are generated for each prompt.
- If you encounter any issues or errors, check the console output for more information.

## Adding New Models

To add a new model:

1. Find the model you want to use on [Replicate](https://replicate.com/explore).
2. Copy the model's identifier.
3. Open the `gradio_interface.py` file and add the new model to the `MODELS` dictionary:

   ```python
   MODELS = {
       # ... existing models ...
       "New Model Name": "new-model-identifier-here",
   }
   ```

4. The new model will automatically appear in the dropdown menu.
