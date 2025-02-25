from PIL import Image
from string import Template
from detect_delimiter import detect
import pillow_heif
import numpy as np
import cv2
import img2pdf
import io
import re
import os
import subprocess
import pandas as pd
import pdfkit
import messages as m
import chardet


IMG_EXT = {'.jpg', '.jpeg', '.jp2', '.png', '.tiff', '.bmp', '.gif', '.webp'}
IMG_EXT_IOS = {'.heif', '.heic'}
DOC_EXT = {'.doc', '.docx', '.odt'}
XLS_EXT = {'.xls', '.xlsx', '.ods'}
TXT_EXT = {'.txt', '.csv'}
DEFAULT_ENCODING = 'utf-8'


def get_pdf_path(doc_path):
    return re.sub(r'\.[^.]*$', ".pdf", doc_path, flags=re.IGNORECASE)


def get_png_path(doc_path):
    return re.sub(r'\.[^.]*$', ".png", doc_path, flags=re.IGNORECASE)


def get_html_path(doc_path):
    return re.sub(r'\.[^.]*$', ".html", doc_path, flags=re.IGNORECASE)


def get_encoding(doc_path):
    default_enc = DEFAULT_ENCODING
    with open(doc_path, 'rb') as f:
        enc = chardet.detect(f.read()).get('encoding', default_enc)
        if not enc or default_enc in enc.lower():
            return default_enc
        return enc

def get_delimiter(doc_path, enc):
    with open(doc_path, 'r', encoding=enc) as f:
        data = f.read()
        return detect(data, default=",")


def txt_to_pdf(doc_path):
    _, ext = os.path.splitext(doc_path)
    pdf_path = get_pdf_path(doc_path)
    html_path = get_html_path(doc_path)
    enc = get_encoding(doc_path)
    delimiter = get_delimiter(doc_path, enc)
    print(enc)
    if ext == ".txt":
        with open(doc_path, 'r', encoding=enc) as txt_file:
            with open(html_path, 'w', encoding=enc) as res:
                res.write(Template(m.HTML_HEAD).substitute(enc=enc))
                for line in txt_file.readlines():
                    res.write("<p>" + line + "</p>\n")
                res.write(m.HTML_TAIL)
    else:
        CSV = pd.read_csv(doc_path, encoding=enc, delimiter=delimiter)
        CSV = CSV.replace(np.nan, '', regex=True)
        html = CSV.to_html()
        with open(html_path, "w", encoding=enc) as file:
            file.writelines(f'<meta charset="{enc}">\n')
            file.write(html)

    pdfkit.from_file(html_path, pdf_path)
    return pdf_path


def img_to_pdf(doc_path: str):
    # получаем путь pdf
    pdf_path = get_pdf_path(doc_path)

    # используем конвертер img2pdf
    try:
        pdf_bytes = img2pdf.convert(doc_path)
    except img2pdf.AlphaChannelError as alphaError:
        rgbBytes = _rgba_to(doc_path)
        pdf_bytes = img2pdf.convert(rgbBytes)

    # создаем pdf файл
    with open(pdf_path, "wb") as file:
        # пишем куски pdf файла
        file.write(pdf_bytes)
    
    return pdf_path


def _rgba_to(image: bytes or str, to='RGB', intermediate='PNG') -> bytes:
    # Image is a filepath
    if isinstance(image, str):
        img = Image.open(image)
        converted: Image = img.convert(to)

    # Image is a bytestream
    elif isinstance(image, bytes):
        buffered = io.BytesIO(image)
        img = Image.open(buffered)
        converted: Image = img.convert(to)
    else:
        raise Exception(f"rgba downsampling only supported for images of type str (ie. filepath) or bytes - got {type(image)}")
    buf = io.BytesIO()
    converted.save(buf, format=intermediate)
    byte_im = buf.getvalue()
    return byte_im


def ios_img_to_pdf(doc_path: str):
    heif_file = pillow_heif.open_heif(doc_path, convert_hdr_to_8bit=False)
    heif_file.convert_to("BGRA;16" if heif_file.has_alpha else "BGR;16")
    np_array = np.asarray(heif_file)
    png_path = get_png_path(doc_path)
    _, width, _ = np_array.shape
    fine_width_size = 1200
    img = np_array
    if width > fine_width_size:
        scale = fine_width_size / width
        img = cv2.resize(np_array, (0, 0), fx=scale, fy=scale) 
    cv2.imwrite(png_path, img)
    output_src = img_to_pdf(png_path)
    return output_src


def excel_to_pdf(doc_path, path):
    subprocess.call(['soffice',
                 '--headless',
                 '--nologo',
                 '--nofirststartwizard',
                 '--norestore',
                 doc_path,
                 'macro:///Standard.Module1.FitToPage'])    
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])    
    return get_pdf_path(doc_path)


def word_to_pdf(doc_path, path):
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])    
    return get_pdf_path(doc_path)
