# InvoiceDatasetGenerator

## Description

Purpose of this project is to generate invoice datataset for my thesis. <br>
The dataset should contain multiple invoce templates, languages, randomized data and partially randomized layouts. <br>
Contains basic augmentation.

## TODO: Installation

```bash
# Python version: xxx
# Install required python modules
$ pip install -r requirements.txt
```

## Usage

Invoices will be generated first, augmentation will follow <br>
Modify constants.py for desired functionality, run main.py

### Constants in constants.py

| constant | type | default | description |
| ---------|----------|----------|---------|
| OUT_DIRECTORY | string | './generated_images/' | directory where **generated** invoices will be saved |
| AUGMENTED_IMAGES_DIRECTORY | string | './augmented_images' | directory where **augmented** invoices will be saved |
| INVOICE_LANGUAGES | [string] | ['./JSON/slovak.json', './JSON/english.json'] | language templates used for generation |
| INVOICE_TEMPLATES | [string] | ['./HTML/template.html'] | layout/style templates used for generation |
| FIELD_INCLUSION | string | './JSON/include_fields.json' | bool dictionary of fields to be present in generated invoice |
| INVOICES_TO_GENERATE | int | 2 | number of invoices **per language and template**, generated_number = INVOICES_TO_GENERATE \* len(INVOICE_LANGUAGES) \* len(INVOICE_TEMPLATES) |
| INVOICE_NAME_START_AT | int | 0 | invoices are named (f"{i}.png"), sets index of first invoice |
| HIDE_EMPTY_ROWS | bool | False | if field with emty value will be hidden |

# TODO: 
1. automatic annotations
1. randomize field skipping
1. randomize stytling and layout
1. add more templates
1. add more languages
1. impove agumentation
1. optimize imports
1. update requirements.txt