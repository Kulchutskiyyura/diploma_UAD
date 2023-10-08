import docx
from text_diff import text_differences
import myers
from PyPDF2 import PdfReader
from PIL import Image
from pytesseract import pytesseract


def get_diff(file_original, file_check):
    file_handler = FileHandler()
    text_original = file_handler.get_text_from_file(file_original)
    text_check = file_handler.get_text_from_file(file_check)

    return _get_diff(text_original, text_check)

class FileHandler:
    def __init__(self):
        self.type_handlers = self._get_type_handlers()

    def _get_type_handlers(self):
        return {
            "pdf": self._get_text_from_pdf,
            "docx": self._get_text_from_docx,
            "txt": self._get_text_from_txt,
            "png": self._get_text_from_image,
        }

    def get_text_from_file(self, file):
        file_handler = self.type_handlers.get(self._get_file_type(file.filename), None)

        if file_handler:
            result = file_handler(file=file)
            return result
        else:
            return

    def _get_file_type(self, file_name: str):
        return file_name.split(".")[1]

    def _get_text_from_pdf(self, file):
        reader = PdfReader(file)
        result = []
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            result.append(text)

        return "\n".join(result)

    def _get_text_from_docx(self, file):
        document = docx.Document(file)
        text = []
        for paragraph in document.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)

    def _get_text_from_txt(self, file):
        #print(type(file.readlines()))
        result = []
        for line in file.readlines():
            result.append(line.decode())
        return "\n".join(result)

    def _get_text_from_image(self, file):
        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Opening the image & storing it in an image object
        img = Image.open(file)

        # Providing the tesseract executable
        # location to pytesseract library
        pytesseract.tesseract_cmd = path_to_tesseract

        # Passing the image object to image_to_string() function
        # This function will extract the text from the image
        return pytesseract.image_to_string(img)


def _get_diff(original_text, check_text):
    return myers.diff(original_text, check_text)
