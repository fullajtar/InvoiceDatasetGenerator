OUT_DIRECTORY = './generated_images/'
AUGMENTED_IMAGES_DIRECTORY = './augmented_images'
INVOICE_LANGUAGES = ['./JSON/slovak.json', './JSON/english.json']
INVOICE_TEMPLATES = ['./HTML/template.html']
FIELD_INCLUSION = './JSON/include_fields.json' #bool dictionary, true => field will be visible, false => 'display: none'
INVOICES_TO_GENERATE = 2 #per each combination of language-template
INVOICE_NAME_START_AT = 0 #name of first generated invoice
HIDE_EMPTY_ROWS = False #empty datafields will have 'display: none'