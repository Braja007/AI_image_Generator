from flask import Flask, request, jsonify, send_from_directory, render_template
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
import os

app = Flask(__name__, static_folder="static")

# Ensure output folder exists
os.makedirs("static", exist_ok=True)

# Load the Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "stabilityai/stable-diffusion-2-1"

# Use a faster scheduler
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)  # Faster scheduler
pipe.to(device)

@app.route("/")
def home():
    """Serve the homepage."""
    return send_from_directory("static", "index.html")

@app.route("/favicon.ico")
def favicon():
    """Fix missing favicon error."""
    return "", 204  # No content

@app.route("/generate", methods=["POST"])
def generate():
    """Handles image generation."""
    if "prompt" not in request.form:
        return jsonify({"error": "Missing prompt"}), 400

    prompt = request.form["prompt"]

    try:
        # Generate new image from prompt
        generated_image = pipe(prompt, num_inference_steps=30).images[0]  # Reduce steps for speed

        output_path = "static/output.png"
        generated_image.save(output_path)

        return jsonify({"imageUrl": output_path})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
