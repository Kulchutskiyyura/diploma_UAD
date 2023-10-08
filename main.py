import docx

raw_php_script = """
$node = new stdClass();
$node->type = "sensor_data"; 
$node->title = "{title}";
$node->language = LANGUAGE_NONE;
node_object_prepare($node);
$node = node_submit($node); 
node_save($node);
$node_wrapper = entity_metadata_wrapper('node', $node);
$node_wrapper->field_date->set("{date}");
$node_wrapper->field_sensor_name->set("{sensor_name}");
$node_wrapper->field_temperature->set("{temperature}");
$node_wrapper->field_humidity->set("{humidity}");
$node_wrapper->field_pressure->set("{pressure}");
$node_wrapper->save();
"""
from text_diff import text_differences
import myers
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from colorama import Fore, Back, Style

import json

import pytesseract
from PIL import Image




def main():
    lines = read_met_data()
    result_php_script = generate_php_script(lines)
    write_php_script(result_php_script)


def read_met_data():
    file = open('2022-05-01.met', 'r')
    lines = file.readlines()
    file.close()

    return lines


def generate_php_script(lines):

    result_php_script = []

    for line in lines[1:]:
        local_php_script = raw_php_script[:]
        data = line.split(';')
        data = {
            'title': f'{data[2]}_{data[0]}',
            'date': data[0],
            'sensor_name': data[2],
            'temperature': f'T1: {data[3]}, T2: {data[4]}, T3: {data[5]}',
            'humidity': data[6],
            'pressure': data[7]
        }

        #print(data)
        #print(local_php_script.format(**data))
        #print("\n\n\n")

        result_php_script.append(local_php_script.format(**data))

    return result_php_script


def write_php_script(result_php_script):
    f = open("script_php.txt", "a")
    f.write("\n\n\n".join(result_php_script))
    f.close()

text_1 = [
    'Hello',
    'World',
    'How are you ?',
]

text_2 = [
    'Hello',
    'World!',
    'How are u ?',
]

TEXT2 = """
ABSTRACT  

Some important information is the next! We will win!
 
The task of the bachelor's qualification work is to develop a web application 
"Berulia" to identify differences in electronic documents.  
In the process of performing the task, the analysis of the subject area, comparison 
with similar products to determine the needs of users, and developed a specification of 
application requirements. Based on this specification and subject area analysis, the  system 
was designed, and later the web application was developed and tested.  

Application is recommended for use by any user who works with electronic 
documents.  
The IntelliJ IDEA development environment was used to implement the web 
application, the client part was developed using the React library of the JavaScript 
programming language, and the server part was developed using the Spring Framework 
of the Java prog ramming language.  
The work contains 91 pages, 5 sections, and 6 appendices.
"""


if __name__ == "__main__":
    r = myers.diff("str", "str2")
    print(r)

    # creating a pdf reader object
    reader = PdfReader('Slipenkyi_diploma.pdf')

    result = []
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        result.append(text)

    #print( "\n".join(result))
    # printing number of pages in pdf file
    print(len(reader.pages))


    def read_docx(file_path):
        document = docx.Document(file_path)
        text = []
        for paragraph in document.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)


    print(read_docx("test_d.docx"))

    # getting a specific page from the pdf file
    page = reader.pages[1]
    print("work 1")

    # extracting text from page
    text = page.extract_text()
    print("work 2")

    r = myers.diff(TEXT2, text)
    print("work 3.1")
    for element in r:
        #print("work 3")
        if element[0] == 'i':
            print(Fore.GREEN + element[1], end="")
        elif element[0] == 'r':
            print(Fore.RED + element[1], end="")
        else:
            print(Fore.WHITE, element[1], end="")
    print(r)
    js = json.dumps(r)
    print(js)

    from PIL import Image
    from pytesseract import pytesseract

    # Defining paths to tesseract.exe
    # and the image we would be using
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = r"Image.png"

    # Opening the image & storing it in an image object
    img = Image.open(image_path)

    # Providing the tesseract executable
    # location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)

    print(text)

