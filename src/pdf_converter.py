import os
import json
import requests
import tempfile
import time
import zipfile
from io import BytesIO
from PyPDF2 import PdfReader
from pathlib import Path


class PDFConverter:
    def __init__(self, config_path='config/config.json'):
        # Load API keys from configuration
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.header = {
            "app_id": config["mathpix_api_id"],
            "app_key": config["mathpix_api_key"]
        }
        self.processed_text = None

    def is_conversion_not_complete(self, pdf_id):
        request = f'https://api.mathpix.com/v3/converter/{pdf_id}'
        response = requests.get(request, headers=self.header)
        response = json.loads(response.text)
        return response.get("status") != "completed"

    def convert_pdf_to_latex(self, pdf_id):
        url = f"https://api.mathpix.com/v3/pdf/{pdf_id}.tex"
        response = requests.get(url, headers=self.header)
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open("latex.tex.zip", "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile("latex.tex.zip", "r") as zip_ref:
            zip_ref.extractall("logs/latex_text")

        with open(f"logs/latex_text/{pdf_id}/{pdf_id}.tex", "r") as file:
            data = file.read()

        os.remove("latex.tex.zip")
        for file_name in os.listdir("logs/latex_text"):
            file_path = os.path.join("logs/latex_text", file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return data

    def run_conversion(self, pdf_source, from_url=False):
        """
        Main method to handle both file and URL PDF conversion.
        Args:
            pdf_source: PDF file path or URL string.
            from_url (bool): Indicates if the source is a URL.
        """
        options = {
            "conversion_formats": {"docx": False, "tex.zip": True},
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        }

        if from_url:
            r = requests.post(
                "https://api.mathpix.com/v3/pdf",
                json={"url": pdf_source, "conversion_formats": {"docx": True, "tex.zip": True}},
                headers=self.header
            )
        else:
            with open(pdf_source, "rb") as pdf_file:
                r = requests.post(
                    "https://api.mathpix.com/v3/pdf",
                    headers=self.header,
                    data={"options_json": json.dumps(options)},
                    files={"file": pdf_file}
                )

        res = r.json()
        pdf_id = str(res['pdf_id'])

        while self.is_conversion_not_complete(pdf_id):
            time.sleep(2)

        self.processed_text = self.convert_pdf_to_latex(pdf_id)
        return self.processed_text


    def process_pdf(self, pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_file)
        
        if len(pdf_reader.pages) > 100:
            return "PDF too large to process."
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
            temp_pdf_file.write(pdf_content)
            temp_pdf_file.flush()
            return self.run_conversion(temp_pdf_file.name)

    def process_pdf_link(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pdf_file = BytesIO(response.content)
            pdf_reader = PdfReader(pdf_file)
            if len(pdf_reader.pages) > 100:
                return "PDF too large to process."
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                temp_pdf_file.write(pdf_file.getvalue())
                temp_pdf_file.flush()
                return self.run_conversion(temp_pdf_file.name)
        else:
            return f"Failed to download PDF from {url}. Status code: {response.status_code}"
