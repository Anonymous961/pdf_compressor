from flask import Flask, request as req
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import subprocess


def compress_pdf(input_path, output_path, quality='screen'):
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

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user/<username>", methods=['POST'])
def show_username(username):
    if req.method == "POST":
        return f'user {escape(username)}'
    else:
        return "not proper method"


@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files["file"]
    if file.filename == '':
        return "No file selected", 400

    file.save("uploads/" + file.filename)
    return "File saved successfully!"


@app.route("/compresspdf", methods=['POST'])
def upload_file():
    if 'file' not in req.files:
        return "No files uploaded", 400
    file = req.files['file']
    if file.filename == '':
        return "No file selected", 400
    input_file_path = os.path.join("uploads",secure_filename(file.filename))
    output_file_path = os.path.join("uploads","compressed_"+secure_filename(file.filename))
    file.save(file.filename)
    message = compress_pdf(input_file_path , output_file_path)
    return message



if __name__ == '__main__':
    app.run()
