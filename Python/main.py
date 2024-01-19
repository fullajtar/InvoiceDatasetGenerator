import csv
import json
import time
import os
import random

from bs4 import BeautifulSoup
from FakeClass import FakeClass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from constants import * 
from augment import augment
from dir_functions import init_annotations_dirs, init_dir, remove_dir

def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--host-resolver-rules=MAP * 127.0.0.1")
    chrome_options.add_argument("--disable-extensions")  # Disable browser extensions
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    chrome_options.add_argument("--disable-infobars")  # Disable the infobar for Chrome being controlled by automated software

    driver = webdriver.Chrome(options=chrome_options)
    width_mm, height_mm, dpi = 215, 302, 97
    width_px, height_px = int((width_mm / 25.4) * dpi), int((height_mm / 25.4) * dpi)
    driver.set_window_size(width_px, height_px)
    return driver

def export_html_as_jpg(filename, output_dir, driver, input_abs_path_to_html):
    driver.get(input_abs_path_to_html)
    os.makedirs(output_dir, exist_ok=True)
    driver.save_screenshot(f"{output_dir}{filename}.png")

def read_language_pack(language):
    with open(language, 'r', encoding='utf-8') as file:
        loaded_dict = json.load(file)
        delivery_methods = loaded_dict.pop('delivery_methods')
        payment_methods = loaded_dict.pop('payment_methods')
        return loaded_dict, delivery_methods, payment_methods

def translate_template(soup, loaded_dict):
    # translate titles
    for id, value in loaded_dict.items():
        paragraph = soup.find(id=id)
        if paragraph:
            paragraph.string = value
    return soup

# replace "maybe" values with random true/false
def randomize_include_fields(path_to_json):
    with open(FIELD_INCLUSION, 'r', encoding='utf-8') as file:
        fields_dict = json.load(file)
        for element_id, include_field in fields_dict.items():
            if type(include_field) != bool and include_field.lower() == "maybe":
                fields_dict[element_id] = random.choice([True, False])
                # print(include_field)
    return fields_dict

def generate_html_item_list(soup:BeautifulSoup, invoice:FakeClass):
    tbody_element = soup.find(id='invoice-items-tbody')
    if tbody_element:
        i = 1
        for item in invoice.item_list:
            tr_element = soup.new_tag('tr')
            td_element = soup.new_tag('td')
            td_element.string = str(i)
            tr_element.append(td_element)

            for attr_name, attr_value in vars(item).items():
                td_element = soup.new_tag('td')
                td_element.string = str(attr_value)
                tr_element.append(td_element)
            tbody_element.append(tr_element)
            i += 1
        return soup

def generate_html_invoice(delivery_methods, payment_methods, fields_dict, soup): 
    # init fake invoice class
    faked = FakeClass(delivery_methods, payment_methods)

    hide_labels = HIDE_LABELS
    if type(hide_labels) != bool and hide_labels.lower() == "maybe":
        hide_labels = random.choice([True, False])

    if hide_labels:
        style = soup.find('style')
        style.string = style.string + '''       .label{
            visibility: hidden;
            display: none;
        }'''

    # insert faked fields to HTML code
    for element_id, include_field in fields_dict.items():
        paragraph = soup.find(id=element_id)
        if paragraph:
            if include_field:
                fake = str(faked.get_fake_value_for_key(element_id))
                paragraph.string = fake
                if (HIDE_EMPTY_ROWS and hide_labels) and fake == '':
                    paragraph.parent['style'] = 'display: none;'
                    fields_dict[element_id] = False
                elif fake == '':
                    fields_dict[element_id] = False
            else:
                paragraph.parent['style'] = 'display: none;' 
                fields_dict[element_id] = False
    soup = generate_html_item_list(soup, faked)

    # temporarily save HTML file, later used for image export
    with open('./HTML/output.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    return fields_dict, faked

def read_html_template(filename):
    with open(filename, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        return BeautifulSoup(html_content, 'html.parser')

def generate_bounding_box_annotations(fields_dict, template, driver, invoice_index, annotations_path): 
    # insert faked fields to HTML code
    for element_id, include_field in fields_dict.items():
        soup = read_html_template(template)
        body = soup.find('body')
        body['style'] = 'visibility: hidden; color: rgba(0,0,0,0);'
        style = soup.find('style')
        style.string = style.string + '''       a{
            visibility: hidden;
        }'''
        paragraph = soup.find(id=element_id)
        if paragraph:
            if include_field:
                paragraph['style'] = 'border: 1px solid #333; visibility: visible;'
                # temporarily save HTML file, later used for image export
            annotation_path = f"{annotations_path}{element_id}.html"
            with open(annotation_path, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            annotation_absolute_path = os.path.join(os.path.sep, ROOT_DIR, '..' , 'HTML', 'annotations', f"{element_id}.html")
            export_html_as_jpg( f"{element_id}/{invoice_index}" , ORIGINAL_ANNOTATIONS_DIRECTORY, driver, annotation_absolute_path)
    return None

def init_data_annotations_csv():
    with open(FIELD_INCLUSION, 'r', encoding='utf-8') as file:
        fields_dict = json.load(file)
        headers = ['filename']
        for field_id, field_inclusion in fields_dict.items():
            if field_inclusion != False:
                headers.append(field_id)

    csv_output_path = os.path.join(ORIGINAL_ANNOTATIONS_DIRECTORY, 'data_annotations.csv')
    with open(csv_output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
    
    return fields_dict

def prepare_directories():
    if CLEAR_DIRECTORIES:
        remove_dir(ORIGINAL_IMAGES_DIRECTORY)
        remove_dir(ANNOTATIONS_PATH)
        remove_dir(ORIGINAL_ANNOTATIONS_DIRECTORY)
        
    init_dir(ORIGINAL_IMAGES_DIRECTORY)
    init_dir(ANNOTATIONS_PATH)
    init_dir(ORIGINAL_ANNOTATIONS_DIRECTORY)

    init_annotations_dirs(ORIGINAL_ANNOTATIONS_DIRECTORY)

ANNOTATIONS_PATH = './HTML/annotations/'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



def generate_data_annotations(fields_dict, faked, invoice_index):
    row = [f"{invoice_index}.png"]
    for field_id, field_inclusion in fields_dict.items():
        if field_inclusion != False:
            row.append(faked.get_fake_value_for_key(field_id))
            
    csv_output_path = os.path.join(ORIGINAL_ANNOTATIONS_DIRECTORY, 'data_annotations.csv')
    with open(csv_output_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def main():
    t_start = time.time()
    driver = init_webdriver()
    invoice_index = INVOICE_NAME_START_AT
    html_output_path = os.path.join(os.path.sep, ROOT_DIR, '..' , 'HTML', 'output.html')

    prepare_directories()
    if GENERATE_DATA_ANNOTATIONS:
        FIELD_INCLUSION_DICT = init_data_annotations_csv()
        
    for template in INVOICE_TEMPLATES:
        soup_template = read_html_template(template)

        for language in INVOICE_LANGUAGES:
            loaded_dict, delivery_methods, payment_methods = read_language_pack(language)
            soup_template_translated = translate_template(soup_template, loaded_dict)

            for i in tqdm(range(INVOICES_TO_GENERATE), desc=f'template: {template}; language: {language}', colour='Green'):
                soup = soup_template_translated
                soup = read_html_template(template)
                soup = translate_template(soup, loaded_dict)
                # generate these dict fields to final invoice
                fields_dict = randomize_include_fields(FIELD_INCLUSION)
                fields_dict, faked = generate_html_invoice(delivery_methods, payment_methods, fields_dict, soup)
                export_html_as_jpg(invoice_index, ORIGINAL_IMAGES_DIRECTORY, driver, html_output_path)
                if GENERATE_BOUNDING_BOX_ANNOTATIONS:
                    generate_bounding_box_annotations(fields_dict, './HTML/output.html', driver, invoice_index, ANNOTATIONS_PATH)
                if GENERATE_DATA_ANNOTATIONS:
                    generate_data_annotations(FIELD_INCLUSION_DICT, faked, invoice_index)
                invoice_index += 1

    # Close the browser
    driver.quit()
    t = time.time() - t_start
    print(str(invoice_index - INVOICE_NAME_START_AT)+" invoices generated in -->  ", f"{t:.3f}", 'seconds')

    t_start = time.time()
    augment()
    t = time.time() - t_start
    print(str(invoice_index - INVOICE_NAME_START_AT)+" invoices augmented in -->  ", f"{t:.3f}", 'seconds', end="  ")

main()