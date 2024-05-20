from flask import Flask, request as req, send_file, jsonify, after_this_request, Response
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
from utils.s3_helpers import upload_file_to_s3, delete_all_objects, get_files_from_s3
from uuid import uuid4
from utils.helpers import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return {"message": "hello", "filename": "output_file_path"}


@app.route("/user/<username>", methods=['POST'])
def show_username(username):
    if req.method == "POST":
        return f'user {escape(username)}'
    else:
        return "not proper method"

@app.route("/get/files")
def get_files():
    files, error = get_files_from_s3()
    if files:
        return jsonify(files)
    else:
        return jsonify({"error": error})

# check file upload
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files["file"]
    if file.filename == '':
        return "No file selected", 400
    upload_dir_check()
    file.save("uploads/" + file.filename)
    return "File saved successfully!"


# to compress file
@app.route("/compresspdf", methods=['POST'])
def upload_file():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    upload_dir_check()
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    output_file = "compressed_" + secure_filename(file.filename)
    output_file_path = os.path.join("uploads", output_file)
    file.save(input_file_path)

    quality = req.form.get('quality', 'screen')
    print("quality is ", quality)
    message = compress_pdf(input_file_path, output_file_path, quality)
    filename=upload_file_to_s3(output_file_path)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(input_file_path)
            os.remove(output_file_path)
        except Exception as e:
            app.logger.error(e)
        return response
    data = {"output_file": output_file, "message": message,"uploaded_file":filename}
    return jsonify(data)


@app.route('/converttodoc', methods=["POST"])
def convert_to_doc():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    upload_dir_check()
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    filename, _ = os.path.splitext(secure_filename(file.filename))
    output_file = "doc_" + filename + ".doc"
    output_file_path = os.path.join("uploads", output_file)
    file.save(input_file_path)
    message = convertpdftodoc(input_file_path, output_file_path)

    s3_filename=upload_file_to_s3(output_file_path)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(input_file_path)
            os.remove(output_file_path)
        except Exception as e:
            app.logger.error(e)
        return response

    data = {"output_file": output_file, "message": message, "uplaoded_file":s3_filename}
    return jsonify(data)


@app.route("/compressimage", methods=['POST'])
def reduce_image_size():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    upload_dir_check()
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    output_file = "compressed_" + secure_filename(file.filename)
    output_file_path = os.path.join("uploads", output_file)
    file.save(input_file_path)

    # quality = int(req.form.get('quality', 50))
    quality = req.form.get('quality', 85)
    try:
        quality = int(quality)
        if (quality > 100 or quality < 0):
            return ValueError("Quality out of range");
    except ValueError:
        return "Invalid value. Please provide integer value between 0 and 100", 400
    print("quality is ", quality)
    message = compress_image(input_file_path, output_file_path, quality)
    image_filename=upload_file_to_s3(output_file_path)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(input_file_path)
            os.remove(output_file_path)
        except Exception as e:
            print("Files not deleted")
        return response
    data = {"output_file": output_file, "message": message, "uploaded_file":image_filename}
    return jsonify(data)


if __name__ == '__main__':


    app.run()
