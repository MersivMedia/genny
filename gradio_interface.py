import gradio as gr
import json
import os
import base64
from image_generator import generate_images

# List of available models
MODELS = {
    "SDXL": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    "Flux Schnell": "black-forest-labs/flux-schnell",
    "Flux Dev": "black-forest-labs/flux-dev",
    "D-Journey": "lorenzomarines/d-journey",
    "SDXL Lightning 4step": "bytedance/sdxl-lightning-4step"
}

def process_upload(file):
    if file is None:
        return None
    file_path = file.name
    return file_path

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_and_display(file_path, model_name):
    if not file_path or not os.path.exists(file_path):
        yield "Error: Please upload a valid prompts.json file first.", None
        return

    try:
        with open(file_path, 'r') as file:
            prompts = json.load(file)
    except json.JSONDecodeError:
        yield "Error: The uploaded file is not a valid JSON file.", None
        return
    except Exception as e:
        yield f"Error reading the file: {str(e)}", None
        return

    model = MODELS[model_name]
    html_output = f"<h2>Using model: {model_name}</h2>"

    for item in prompts:
        prompt = item['prompt']
        shot_number = item['shot_number']
        
        html_output += f"<h3>Shot {shot_number}: {prompt}</h3><p>Generating images...</p>"
        yield html_output, None
        
        try:
            shot_images = generate_images(prompt, shot_number, model)
            
            html_output = html_output.replace("<p>Generating images...</p>", "")
            html_output += "<div style='display: flex; flex-wrap: wrap; justify-content: space-around;'>"
            for image_path in shot_images:
                base64_image = image_to_base64(image_path)
                html_output += f"<img src='data:image/png;base64,{base64_image}' style='max-width: 45%; margin-bottom: 20px;'>"
            html_output += "</div><hr>"
            
            yield html_output, None
        except Exception as e:
            html_output = html_output.replace("<p>Generating images...</p>", "")
            html_output += f"<p>Error generating images: {str(e)}</p><hr>"
            yield html_output, None

    html_output += "<h3>All images generated!</h3>"
    yield html_output, None

with gr.Blocks() as demo:
    gr.Markdown("# AI Image Generator")
    
    with gr.Row():
        upload_button = gr.File(label="Upload prompts.json")
        file_output = gr.Textbox(label="Uploaded File")
    
    model_dropdown = gr.Dropdown(choices=list(MODELS.keys()), label="Select Model", value="SDXL")
    
    generate_button = gr.Button("Generate Images")
    
    gallery = gr.HTML()
    image_output = gr.Image(visible=False)
    
    upload_button.upload(process_upload, upload_button, file_output)
    generate_button.click(generate_and_display, inputs=[file_output, model_dropdown], outputs=[gallery, image_output])

demo.launch()
