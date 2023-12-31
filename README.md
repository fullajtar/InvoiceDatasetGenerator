# InvoiceDatasetGenerator

## Description

Purpose of this project is to generate invoice datataset for my thesis. <br>
The dataset should contain multiple invoce templates, languages, randomized data and partially randomized layouts. <br>
Contains basic augmentation.

## Installation

Windows users enable long paths
```bash
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Install required python modules
```bash
$ pip install -r requirements.txt
```

## Usage

Invoices will be generated first, augmentation will follow <br>
Modify constants.py for desired functionality, run main.py

### Constants in constants.py

| constant | type | default | description |
| ---------|----------|----------|---------|
| CLEAR_DIRECTORIES | bool | True | removes dataset directories before generation of new dataset |
| ORIGINAL_DATASET_DIRECTORY | string | './generated/original/' | 
| ORIGINAL_IMAGES_DIRECTORY | string | './generated/original/images/' | directory where **generated** invoices will be saved |
| ORIGINAL_ANNOTATIONS_DIRECTORY | string | './generated/original/images/' | directory where **generated** annotations will be saved |
| AUGMENTED_IMAGES_DIRECTORY | string | './generated/augmented/images/' | directory where **augmented** invoices will be saved |
| AUGMENTED_ANNOTATIONS_DIRECTORY | string | './generated/augmented/annotations/' | directory where **augmented** annotations will be saved |
| HIDE_LABELS | bool/'Maybe' | maybe | hides invoice labels, 'Maybe' is randomized on per-invoice basis |
| INVOICE_LANGUAGES | [string] | ['./JSON/slovak.json', './JSON/english.json'] | language templates used for generation |
| INVOICE_TEMPLATES | [string] | ['./HTML/template.html'] | layout/style templates used for generation |
| FIELD_INCLUSION | string | './JSON/include_fields.json' | bool dictionary of fields to be present in generated invoice |
| INVOICES_TO_GENERATE | int | 2 | number of invoices **per language and template**, generated_number = INVOICES_TO_GENERATE \* len(INVOICE_LANGUAGES) \* len(INVOICE_TEMPLATES) |
| INVOICE_NAME_START_AT | int | 0 | invoices are named (f"{i}.png"), sets index of first invoice |
| HIDE_EMPTY_ROWS | bool | False | if field with emty value will be hidden |

# TODO: 
1. randomize stytling and layout
1. add more templates
1. add more languages
1. impove agumentation
1. implement batching for large datasets