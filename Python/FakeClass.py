from faker import Faker
from datetime import datetime, timedelta
import re
import random
import string

def generate_specific_symbol(length=6):
    symbols = string.digits + string.ascii_uppercase
    specific_symbol = ''.join(random.choice(symbols) for _ in range(length))
    return specific_symbol

def generate_variable_symbol(length=10):
    variable_symbol = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return variable_symbol

def generate_constant_symbol(length=3):
    chars = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
    numbers = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return chars + numbers

class FakeClass:

    def __init__(self, DELIVERY_METHODS:list, PAYMENT_METHODS:list, DATE_FORMAT:str = "%Y-%m-%d"):
        fake = Faker()
        issue_date = fake.date()
        issue_date = datetime.strptime(fake.date(), "%Y-%m-%d")
        due_date = issue_date + timedelta(days=30)
        date_of_taxation = due_date
        delivery_date = fake.date_between(issue_date, due_date)
        date_of_receipt_payment = fake.date_between(issue_date, due_date)
        
        fake_supplier_company = fake.company()
        fake_supplier_company_suffix = fake.company_suffix()
        
        pattern = re.compile(r'[^a-zA-Z0-9]')
        normalized_supplier_name =  pattern.sub('', fake_supplier_company).lower()
        supplier_country = fake.country_code()

        self.company_name_value = fake_supplier_company + ' ' + fake_supplier_company_suffix
        self.address_value = fake.address()
        self.website_value = 'www.'+ normalized_supplier_name + '.' + supplier_country.lower()
        self.email_value = normalized_supplier_name + '@' + fake.free_email_domain()
        self.phone_number_value = fake.phone_number()
        self.iban_value = fake.iban()
        self.account_number_value = fake.bban()
        self.swift_value = fake.swift()
        self.recipient_company_name_value = fake.name()
        self.recipient_address_value = fake.address()
        self.recipient_phone_number_value = fake.phone_number()
        self.issue_date_value = issue_date.strftime(DATE_FORMAT)
        self.delivery_date_value = delivery_date.strftime(DATE_FORMAT)
        self.due_date_value = due_date.strftime(DATE_FORMAT)
        self.taxation_date_value = date_of_taxation.strftime(DATE_FORMAT)
        self.payment_receipt_date_value = date_of_receipt_payment.strftime(DATE_FORMAT)
        self.delivery_address_value = fake.address()
        self.invoice_number_value = fake.ean(length=13)
        self.payment_method_value = random.choice(PAYMENT_METHODS)
        self.delivery_method_value = random.choice(DELIVERY_METHODS)

        self.recipient_email_value = fake.email()

        fake_supplier_id = fake.ean(length=13)
        self.vat_id_value = supplier_country.upper() + fake_supplier_id
        self.tax_id_value = fake_supplier_id
        self.supplier_id_value = fake.ean(length=8)
        self.specific_symbol_value = generate_specific_symbol()
        self.variable_symbol_value = generate_variable_symbol()
        self.constant_symbol_value = generate_constant_symbol()



        recipient_country = fake.country_code()
        fake_recipient_id = fake.ean(length=13)
        self.recipient_vat_id_value = recipient_country.upper() + fake_recipient_id
        self.recipient_tax_id_value = fake_recipient_id
        self.recipient_id_value = fake.ean(length=8)

        
    def get_fake_value_for_key(self, key):
        try:
            if key == "company_name_text":
                return self.company_name_value
            elif key == "invoice_company_name_text":
                return self.company_name_value
            elif key == "address_text":
                return self.address_value
            elif key == "vat_reg_no_text":
                return self.vat_id_value
            elif key == "tax_id_text":
                return self.tax_id_value
            elif key == "website_text":
                return self.website_value
            elif key == "email_text":
                return self.email_value
            elif key == "phone_number_text":
                return self.phone_number_value
            elif key == "supplier_business_id_text":
                return self.supplier_id_value
            elif key == "commercial_register_text":
                return self.commercial_register_value
            elif key == "iban_text":
                return self.iban_value
            elif key == "variable_symbol_text":
                return self.variable_symbol_value
            elif key == "constant_symbol_text":
                return self.constant_symbol_value
            elif key == "specific_symbol_text":
                return self.specific_symbol_value
            elif key == "account_number_text":
                return self.account_number_value
            elif key == "bank_name_text":
                return self.bank_name_value
            elif key == "swift_text":
                return self.swift_value
            elif key == "recipient_company_name_text":
                return self.recipient_company_name_value
            elif key == "recipient_address_text":
                return self.recipient_address_value
            elif key == "recipient_vat_id_text":
                return self.recipient_vat_id_value
            elif key == "recipient_tax_id_text":
                return self.recipient_tax_id_value
            elif key == "recipient_website_text":
                return self.recipient_website_value
            elif key == "recipient_email_text":
                return self.recipient_email_value
            elif key == "recipient_phone_number_text":
                return self.recipient_phone_number_value
            elif key == "recipient_business_id_text":
                return self.recipient_id_value
            elif key == "recipient_commercial_register_text":
                return self.recipient_commercial_register_value
            elif key == "issue_date_text":
                return self.issue_date_value
            elif key == "delivery_date_text":
                return self.delivery_date_value
            elif key == "due_date_text":
                return self.due_date_value
            elif key == "taxation_date_text":
                return self.taxation_date_value
            elif key == "payment_receipt_date_text":
                return self.payment_receipt_date_value
            elif key == "payment_method_text":
                return self.payment_method_value
            elif key == "delivery_method_text":
                return self.delivery_method_value
            elif key == "currency_text":
                return self.currency_value
            elif key == "delivery_address_text":
                return self.delivery_address_value
            elif key == "to_pay_text":
                return self.to_pay_value
            elif key == "invoice_number_text":
                return self.invoice_number_value
            elif key == "note_text":
                return self.note_value
            else:
                return None  # Return None for keys that are not handled explicitly
        except:
            return ""