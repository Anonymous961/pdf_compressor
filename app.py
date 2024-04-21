from flask import Flask, request as req, send_file, jsonify, after_this_request
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import subprocess
from pdf2docx import Converter
from PIL import Image


def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Compresses a PDF file using Ghostscript.

    Parameters:
        input_path (str): Path to the input PDF file.
        output_path (str): Path to save the compressed PDF file.
        quality (str): Quality level for compression.
                      Possible values: 'screen', 'ebook', 'printer', 'prepress'.
    """
    args = [
        "gs",
        "-sDEVICE=pdfwrite",
        f"-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/" + quality,
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(args)
    return "file compressed successfully"


def convertpdftodoc(pdf_file, docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file)  # all pages by default
    cv.close()
    return "file converted successfully"


def compress_image(input_path, output_path, quality=85):
    """
    Compresses an image and saves it to the output path.

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the compressed image.
        quality (int): The quality of the compressed image (0-100).
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        return "image compressed successfully"
    except Exception as e:
        print(f"Error compressing image: {e}")


app = Flask(__name__)


@app.route('/')
def hello_world():
    # print("hello")
    return {"message": "hello", "filename": "output_file_path"}


@app.route("/user/<username>", methods=['POST'])
def show_username(username):
    if req.method == "POST":
        return f'user {escape(username)}'
    else:
        return "not proper method"


# check file upload
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files["file"]
    if file.filename == '':
        return "No file selected", 400

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
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    output_file = "compressed_" + secure_filename(file.filename)
    output_file_path = os.path.join("uploads", output_file)
    file.save(input_file_path)

    quality = req.form.get('quality', 'screen')
    print("quality is ", quality)
    message = compress_pdf(input_file_path, output_file_path, quality)
    print(output_file_path)
    print(output_file)
    data = {"output_file": output_file, "message": message}
    return jsonify(data)


@app.route('/converttodoc', methods=["POST"])
def convert_to_doc():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    # print(file.filename)
    filename, _ = os.path.splitext(secure_filename(file.filename))
    output_file = "doc_" + filename + ".doc"
    output_file_path = os.path.join("uploads", output_file)
    print(output_file_path)
    file.save(input_file_path)
    message = convertpdftodoc(input_file_path, output_file_path)
    data = {"output_file": output_file, "message": message}
    return jsonify(data)


@app.route("/compressimage", methods=['POST'])
def reduceimagesize():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    input_file_path = os.path.join("uploads", secure_filename(file.filename))
    output_file = "compressed_" + secure_filename(file.filename)
    output_file_path = os.path.join("uploads", output_file)
    file.save(input_file_path)

    quality = int(req.form.get('quality', 50))
    print("quality is ", quality)
    message = compress_image(input_file_path, output_file_path, quality)
    data = {"output_file": output_file, "message": message}
    return jsonify(data)


# to get any file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        path = os.path.join("uploads", filename)

        @after_this_request
        def removefile(response):

            try:
                original_file="uploads/"+filename.split("_")[1]
                # print(original_file)
                os.remove(original_file)
                os.remove(path)
                print("after this working")
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle")
            return response

        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404


if __name__ == '__main__':
    app.run()
