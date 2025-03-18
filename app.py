from flask import Flask, render_template_string
import subprocess
import os
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the server monitoring app. Visit /htop for system information."

@app.route('/htop')
def htop():
    # Set specific name and username as requested
    full_name = "Sireesha Kudupuri"
    username = "SireeshaK"
    
    # Get server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Get top output
    try:
        top_output = subprocess.check_output(['top', '-b', '-n', '1'], text=True)
    except subprocess.CalledProcessError:
        top_output = "Error: Unable to retrieve top output"
    
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Server Monitoring</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }
            h1 {
                color: #333;
            }
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .info {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h1>System Information</h1>
        <div class="info">
            <p><strong>Name:</strong> {{ full_name }}</p>
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Server Time (IST):</strong> {{ server_time }}</p>
        </div>
        <h2>Top Output:</h2>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """
    
    return render_template_string(html_template, 
                                  full_name=full_name,
                                  username=username,
                                  server_time=server_time,
                                  top_output=top_output)

if __name__ == '__main__':
    # Run the app on port 5000 with public visibility (0.0.0.0)
    app.run(host='0.0.0.0', port=5000, debug=False)