import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from tkinter.filedialog import  asksaveasfilename




os.environ["INVOICE_LANG"] = "en"

patient = Client("patientname",address="3")
kdah_name_on_bill = Provider('Kokilaben Dhirubhai Ambani Hospital',address="(A Unit of Mandke Foundation), Andheri(W)",city="Mumbai +91 22 42696969",logo_filename="imageResources/logo.png",bank_account="1")

signature = Creator('')

invoice = Invoice(patient, kdah_name_on_bill,signature,)
invoice.currency_locale = 'en_US.UTF-8'
invoice.add_item(Item(32, 600, description="Item 1"))
invoice.add_item(Item(60, 50, description="Item 2", tax=21))
invoice.add_item(Item(50, 60, description="Item 3", tax=0))
invoice.add_item(Item(5, 600, description="Item 4", tax=15))
    
files_type = [('All Files', '*.*'), 
            ('PDF Files', '*.py')]

file = asksaveasfilename(defaultextension=".pdf",filetypes=files_type,initialfile="a.pdf",title="Save File of ANE Report in PDF format")

pdf = SimpleInvoice(invoice)
    
pdf.gen(file, generate_qr_code=True)

os.startfile(file)

