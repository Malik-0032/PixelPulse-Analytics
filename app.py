# app.py
from flask import Flask, request, send_file, Blueprint
from flask_cors import CORS
from datetime import datetime
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
LOG_FILE = 'spy_pixel_logs.txt'

def log_pixel_access(campaign_id, user_agent, ip_address, timestamp):
    """Log pixel access details to file"""
    try:
        log_entry = f"[{timestamp}] Campaign: {campaign_id} | IP: {ip_address} | UA: {user_agent}\n"
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error logging pixel access: {e}")

def get_pixel_image():
    """Generate a 1x1 transparent PNG pixel"""
    try:
        img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io
    except Exception as e:
        print(f"Error generating pixel image: {e}")
        return None

@app.route('/')
def home():
    return 'PixelPulse Analytics API is running!'

@app.route('/pixel/<campaign_id>.png')
def serve_pixel(campaign_id):
    try:
        # Get user information
        user_agent = request.headers.get('User-Agent', 'Unknown')
        ip_address = request.remote_addr
        timestamp = datetime.now().isoformat()
        
        # Log the access
        log_pixel_access(campaign_id, user_agent, ip_address, timestamp)
        
        # Generate and serve the pixel
        pixel_image = get_pixel_image()
        if pixel_image:
            return send_file(pixel_image, mimetype='image/png')
        else:
            return 'Error generating pixel', 500
            
    except Exception as e:
        print(f"Error serving pixel: {e}")
        return 'Internal Server Error', 500

@app.route('/logs')
def view_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = f.readlines()
            return {'logs': logs}
        return {'logs': []}
    except Exception as e:
        print(f"Error reading logs: {e}")
        return {'error': 'Error reading logs'}, 500

if __name__ == '__main__':
    app.run(debug=True)