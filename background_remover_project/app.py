from flask import Flask, render_template, request, jsonify
from rembg import remove
from PIL import Image
import os
import io
import base64

app = Flask(__name__)

# Ensure uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    try:
        # Check for file extensions (only allow images)
        if file.filename.split('.')[-1].lower() not in ['png', 'jpg', 'jpeg', 'gif']:
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
        
        # Get the original filename
        original_filename = file.filename

        # Process the image
        img = Image.open(file.stream)
        
        # Optimize image for processing
        img = img.convert("RGBA")
        img.thumbnail((800, 800))  # Resize image to limit processing time
        
        output = remove(img)
        
        # Save the processed image to a BytesIO buffer
        buffer = io.BytesIO()
        output.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Convert image to base64 for easier frontend display
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        img_data_url = f"data:image/png;base64,{img_base64}"
        
        # Return the original filename along with the processed image URL
        return jsonify({
            'processed_image': img_data_url,
            'original_filename': original_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
