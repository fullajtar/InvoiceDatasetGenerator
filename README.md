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

Install requirements
```bash
# Python version: 3.11.6
# Install required python modules
$ pip install -r requirements.txt

# installed modules + their dependencies:
    # absl-py==2.0.0
    # astunparse==1.6.3
    # attrs==23.1.0
    # beautifulsoup4==4.12.2
    # cachetools==5.3.2
    # certifi==2023.11.17
    # cffi==1.16.0
    # charset-normalizer==3.3.2
    # Faker==20.1.0
    # flatbuffers==23.5.26
    # gast==0.4.0
    # google-auth==2.23.4
    # google-auth-oauthlib==1.0.0
    # google-pasta==0.2.0
    # grpcio==1.59.3
    # h11==0.14.0
    # h5py==3.10.0
    # idna==3.6
    # keras==2.13.1
    # libclang==16.0.6
    # Markdown==3.5.1
    # MarkupSafe==2.1.3
    # numpy==1.24.3
    # oauthlib==3.2.2
    # opt-einsum==3.3.0
    # outcome==1.3.0.post0
    # packaging==23.2
    # Pillow==10.1.0
    # protobuf==4.25.1
    # pyasn1==0.5.1
    # pyasn1-modules==0.3.0
    # pycparser==2.21
    # PySocks==1.7.1
    # python-dateutil==2.8.2
    # requests==2.31.0
    # requests-oauthlib==1.3.1
    # rsa==4.9
    # selenium==4.15.2
    # six==1.16.0
    # sniffio==1.3.0
    # sortedcontainers==2.4.0
    # soupsieve==2.5
    # tensorboard==2.13.0
    # tensorboard-data-server==0.7.2
    # tensorflow==2.13.1
    # tensorflow-estimator==2.13.0
    # tensorflow-intel==2.13.1
    # tensorflow-io-gcs-filesystem==0.31.0
    # termcolor==2.3.0
    # trio==0.23.1
    # trio-websocket==0.11.1
    # typing_extensions==4.5.0
    # urllib3==2.1.0
    # Werkzeug==3.0.1
    # wrapt==1.16.0
    # wsproto==1.2.0
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