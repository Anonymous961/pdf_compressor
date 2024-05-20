import os
from pdf2docx import Converter
import subprocess
from PIL import Image

def upload_dir_check():
    upload_dir = "uploads"

    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)


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
        return "error compressing image"
