from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from utils import process_audio, generate_patterns
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'backend/static/audio'
IMAGE_FOLDER = 'backend/static/images'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER


# 检查文件格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 上传音频并生成图案
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 处理音频，生成图案
        audio_path = filepath
        pattern_urls = generate_patterns(audio_path)

        return jsonify({"status": "success", "patterns": pattern_urls})
    return jsonify({"error": "Invalid file format"})


# 提供图案文件的访问
@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
