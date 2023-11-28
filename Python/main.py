import json
import time
import os

from bs4 import BeautifulSoup
from FakeClass import FakeClass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constants import *
from augment import augment

def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=chrome_options)
    width_mm, height_mm, dpi = 215, 302, 97
    width_px, height_px = int((width_mm / 25.4) * dpi), int((height_mm / 25.4) * dpi)
    driver.set_window_size(width_px, height_px)
    return driver

def export_html_as_jpg(filename, dir, driver, html_output_path):
    driver.get(html_output_path)
    os.makedirs(dir, exist_ok=True)
    driver.save_screenshot(f"{dir}{filename}.png")

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

def generate_html_invoice(delivery_methods, payment_methods, fields_dict, soup): 
    # init fake invoice class
    faked = FakeClass(delivery_methods, payment_methods)

    # insert faked fields to HTML code
    for element_id, include_field in fields_dict.items():
        paragraph = soup.find(id=element_id)
        if paragraph:
            if include_field:
                fake = faked.get_fake_value_for_key(element_id)
                paragraph.string = fake
                if HIDE_EMPTY_ROWS and fake == "":
                    paragraph.parent['style'] = 'display: none;'
            else:
                paragraph.parent['style'] = 'display: none;' 

    # temporarily save HTML file, later used for image export
    with open('./HTML/output.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    return soup

def read_html_template(filename):
    with open(filename, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        return BeautifulSoup(html_content, 'html.parser')

def main():
    t_start = time.time()
    driver = init_webdriver()
    invoice_index = INVOICE_NAME_START_AT
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    html_output_path = os.path.join(os.path.sep, ROOT_DIR, '..' , 'HTML', 'output.html')
    os.makedirs(OUT_DIRECTORY, exist_ok=True)
    for template in INVOICE_TEMPLATES:
        for language in INVOICE_LANGUAGES:

            soup = read_html_template(template)
            loaded_dict, delivery_methods, payment_methods = read_language_pack(language)
            soup = translate_template(soup, loaded_dict)

            # generate these dict fields to final invoice
            with open(FIELD_INCLUSION, 'r', encoding='utf-8') as file:
                fields_dict = json.load(file)   

            for i in range(INVOICES_TO_GENERATE):
                generate_html_invoice(delivery_methods, payment_methods, fields_dict, soup)
                export_html_as_jpg(invoice_index, OUT_DIRECTORY, driver, html_output_path)
                invoice_index += 1

    # Close the browser
    driver.quit()
    t = time.time() - t_start
    print(str(invoice_index - INVOICE_NAME_START_AT)+" invoices generated in -->  ", f"{t:.3f}", 'seconds')

    t_start = time.time()
    augment()
    t = time.time() - t_start
    print(str(invoice_index - INVOICE_NAME_START_AT)+" invoices augmented in -->  ", f"{t:.3f}", 'seconds', end="  ")

def debug_output_html():
    invoice_index = INVOICE_NAME_START_AT
    for template in INVOICE_TEMPLATES:
        for language in INVOICE_LANGUAGES:

            soup = read_html_template(template)
            loaded_dict, delivery_methods, payment_methods = read_language_pack(language)
            soup = translate_template(soup, loaded_dict)

            # generate these dict fields to final invoice
            with open(FIELD_INCLUSION, 'r', encoding='utf-8') as file:
                fields_dict = json.load(file)   

            for i in range(INVOICES_TO_GENERATE):
                generate_html_invoice(delivery_methods, payment_methods, fields_dict, soup)
                # export_html_as_jpg(invoice_index, OUT_DIRECTORY, driver)
                invoice_index += 1

main()