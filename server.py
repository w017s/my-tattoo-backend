import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from utils import generate_all_styles

app = Flask(__name__)

UPLOAD_FOLDER = 'audio'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'm4a', 'wav', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({"message": "Server is running"})

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": filename})
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "Missing filename"}), 400
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(audio_path):
        return jsonify({"error": "File not found"}), 404
    output_paths = generate_all_styles(audio_path, filename)
    urls = [f"/output/{os.path.basename(p)}" for p in output_paths]
    return jsonify({"message": "Images generated", "images": urls})

@app.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # render 会自动设置 PORT
    app.run(host='0.0.0.0', port=port)
