CLEAR_DIRECTORIES = True
ORIGINAL_DATASET_DIRECTORY = "./generated/original/"
ORIGINAL_IMAGES_DIRECTORY = f"{ORIGINAL_DATASET_DIRECTORY}images/"
ORIGINAL_ANNOTATIONS_DIRECTORY = f"{ORIGINAL_DATASET_DIRECTORY}annotations/"
AUGMENTED_IMAGES_DIRECTORY = "./generated/augmented/images/"
AUGMENTED_ANNOTATIONS_DIRECTORY = "./generated/augmented/annotations/"
HIDE_LABELS = "Maybe"
INVOICE_LANGUAGES = ["./JSON/slovak.json", "./JSON/english.json"]
INVOICE_TEMPLATES = ["./HTML/template.html"]
FIELD_INCLUSION = "./JSON/include_fields.json"  # bool dictionary, true => field will be visible, false => 'display: none'
INVOICES_TO_GENERATE = 2  # per each combination of language-template
INVOICE_NAME_START_AT = 0  # name of first generated invoice
HIDE_EMPTY_ROWS = False  # empty datafields will have 'display: none
ORIGINAL_HEIGHT, ORIGINAL_WIDTH = 1153, 821
GENERATE_DATA_ANNOTATIONS = True
GENERATE_BOUNDING_BOX_ANNOTATIONS = False
