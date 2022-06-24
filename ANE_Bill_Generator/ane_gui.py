from tkinter import *
from tkinter.font import BOLD
from tkinter.ttk import Treeview
from tkinter.filedialog import  asksaveasfilename
from oracle_config import *
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import subprocess



class App(Tk):
    """
    status_label(rootsource)
    menu_items(rootsource)
    frames(self,rootsource)
    home()
    search_n_view()
    cur_ane_pat()
    aboutpage()
    hide_menu_frames()
    search_n_view()
    search_current_ane_patient()
    clear()
    clear_ane()
    bill_generator()
    direct_ane_bill()
    clear_table(table)

    """
    def __init__(self):

        super(App,self).__init__()
        self.geometry("1000x600") # Dimentions
        self.title("ANE Bill Report") # Title Name
        self.iconbitmap("imageResources/logo.ico") # Logo


   
    def status_label(self,rootsource): #Stutas Bar

        self.status_bar = Label(rootsource, text='Welcome to the Application', bd=1, relief=SUNKEN, anchor=W)
        #self.status_bar.grid(pady=315,columnspan=5 ,sticky='ew')
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=2)
        


    
    def menu_items(self,rootsource): # All menu items goes here

        self.menu = Menu(rootsource)
        rootsource.config(menu=self.menu)
        #main_menu = Menu(self.menu,tearoff="off")
        self.menu.add_command(label="Home", command=self.home)
        self.menu.add_command(label="Current ANE Patients", command=self.cur_ane_pat)
        self.menu.add_command(label="About", command=self.aboutpage)


    def frames(self,rootsource): # Frames are listed here

        self.main_menu_frame = Frame(rootsource,width=1000,height=600) # Packing in home function bg="#00a8ff
        
        self.current_ane_patient_frame = Frame(rootsource,width=1000,height=600) #Packing in cur_ane_pat function

        
        self.about_frame = Frame(rootsource,width=1000,height=600) # Packing in aboutpage funciton
        

    def runbat(self):
        subprocess.call([r'imageResources\KillUnwantedServices.bat'])
   


    
    def home(self): # Fist function of the Application
        self.hide_menu_frames() 
        self.main_menu_frame.pack(fill=BOTH)
        

        self.home_label = Label(self.main_menu_frame, text="Please Enter The UHID Number", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.home_label.pack(pady=25)

        self.uhid = StringVar() # Tk inter requires this for entry widget

        max_len = 12
        
        def on_write(*args): #function to limit the UHID Charater feild to 12 
            s = self.uhid.get()

            if len(s) > max_len:
                self.uhid.set(s[:max_len])

        self.uhid.trace_variable("w", on_write)


        self.input_box = Entry(self.main_menu_frame,width = 40, textvariable = self.uhid,)
        self.uhid.set("KH1000")
        self.input_box.pack()
        self.input_box.focus_force()
        
        self.search_button_image = PhotoImage(file='imageResources/search_button.png')
        self.search_button = Button(self.main_menu_frame, image=self.search_button_image, borderwidth=0 , command=self.search_n_view)
        self.search_button.pack(pady=30)

        # self.view_button_image = PhotoImage(file='imageResources/view_button.png')
        # self.view_button = Button(self.main_menu_frame, image=self.view_button_image, borderwidth=0 , command=self.runbat)
        # self.view_button.pack(side = TOP, pady=30)

        

        # Create a Table width=400, height=200

        columns  = ["uhid","patient_name", "episode_type","episode_id","encounter_id", "item_code",

                    "item_desc","bas_rate","qty","net_charge" ]
        
        headings = ["PATIENT UHID", "PATIENT NAME", "ET", "EPI ID","ENCOUNTER ID", "ITEM CODE",
        
                    "ITEM DESC", "BASE RATE", "QTY", "NET CHARGE"]

        self.table = Treeview(self.main_menu_frame, columns=columns,show='headings')

        for items, desc in zip(columns,headings):
            self.table.column(items, anchor=CENTER)
            self.table.heading(items, text=desc)
            
 
        self.table.pack()

        self.table_scroll_bar = Scrollbar(self.main_menu_frame, orient=VERTICAL)
        self.table_scroll_bar.pack(side=RIGHT, fill=Y)

        self.table.config(yscrollcommand=self.table_scroll_bar.set)
        self.table_scroll_bar.config(command=self.table.yview)

        self.download_button_image = PhotoImage(file='imageResources/download_button.png')
        self.download_button = Button(self.main_menu_frame, image=self.download_button_image, borderwidth=0 , command=self.bill_generator)
        self.download_button.pack(side=LEFT, pady=30)

        self.clear_button_image_red = PhotoImage(file='imageResources/clear_button_red.png')
        self.clear_button_home = Button(self.main_menu_frame, image=self.clear_button_image_red,borderwidth=0 , command=self.clear)  
        self.clear_button_home.pack(side=RIGHT, pady=30)
        

      

    def cur_ane_pat(self):
        self.hide_menu_frames()
        self.current_ane_patient_frame.pack(fill=BOTH)
        
        self.cur_ane_pat_label = Label(self.current_ane_patient_frame, text="Click on Search Button to see Current A & E Patients", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.cur_ane_pat_label.pack(pady=25)

        self.search_button_image = PhotoImage(file='imageResources/search_button1.png')
        self.search_button = Button(self.current_ane_patient_frame, image=self.search_button_image, borderwidth=0 , command=self.search_current_ane_patient)
        self.search_button.pack(pady=30)

        # self.view_button_image = PhotoImage(file='view_button.png')
        # self.view_button = Button(self.main_menu_frame, image=self.view_button_image, borderwidth=0 , command="")
        # self.view_button.pack(side = TOP, pady=30)

        

        # Create a Table width=400, height=200

        columns_ane  = ["uhid","patient_name", "date_of_admit","episode_type","episode_id","encounter_id"]
        
        headings_ane = ["PATIENT UHID", "PATIENT NAME", "DATE OF ADMISSION","ET", "EPI ID","ENCOUNTER ID"]

        self.cur_ane_table = Treeview(self.current_ane_patient_frame, columns=columns_ane,show='headings')

        for items, desc in zip(columns_ane,headings_ane):
            self.cur_ane_table.column(items, anchor=CENTER)
            self.cur_ane_table.heading(items, text=desc)

        self.cur_ane_table.bind('<Double-1>', self.direct_ane_bill)
            
 
        self.cur_ane_table.pack()
    
        self.cur_ane_table_scroll_bar = Scrollbar(self.current_ane_patient_frame, orient=VERTICAL)
        self.cur_ane_table_scroll_bar.pack(side=RIGHT, fill=Y)

        self.cur_ane_table.config(yscrollcommand=self.cur_ane_table_scroll_bar.set)
        self.cur_ane_table_scroll_bar.config(command=self.cur_ane_table.yview)

        # self.download_button_image = PhotoImage(file='imageResources/download_button.png')
        # self.download_button = Button(self.main_menu_frame, image=self.download_button_image, borderwidth=0 , command="")
        # self.download_button.pack(pady=30)

        self.clear_button_image_ane = PhotoImage(file='imageResources/clear_button.png')
        self.clear_button_ane = Button(self.current_ane_patient_frame, image=self.clear_button_image_ane,borderwidth=0 , command=self.clear_ane)  
        self.clear_button_ane.pack(pady=30)



    def aboutpage(self):
        self.hide_menu_frames()
        self.about_frame.pack(fill=BOTH)

        self.about_button_image = PhotoImage(file='imageResources/about.png')
        self.about_button = Button(self.about_frame, image=self.about_button_image, borderwidth=0 , command = lambda:[self.status_bar.config(text="Designed and Developed By AHMED QURESHI :p"),self.runbat()])
        self.about_button.pack(pady=30)


        self.about_label = Label(self.about_frame, text="This Application is a property of Kokilaben Hospital.", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.about_label.pack(pady=10)

        self.about_label = Label(self.about_frame, text="Distribution of this Application outside of the hospital premises is strictly prohibited.", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.about_label.pack(pady=10)

        self.about_label = Label(self.about_frame, text="This programme was built and intended to be used by A & E Staff ONLY!!!", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.about_label.pack(pady=10)

        self.about_label = Label(self.about_frame, text="Version 1.1", fg="black", font=("Bookman Old Style", 14, BOLD))
        self.about_label.pack(pady=5)



    def search_n_view(self,uhid=None):
        
        self.clear_table(self.table) # Clear Table

        if uhid == None:
            
            self.uhid = self.input_box.get().upper() # Takes value from Input field from user
        
        else:
            
            self.uhid = uhid

        self.dbcon = Ora()
        self.status_bar.config(text=self.dbcon.status_update())

        self.items_from_server = self.dbcon.view_ane_bill(self.uhid) # return value form server

        self.item_list = [] #empty list to iterate

        for row in self.items_from_server: # itreation to convert tuple to a list 
                
                self.item_list.append(list(row))
        

        for row in self.item_list:

                
                if row[6] == None and row[7] == 200:
                      
                      row[6] = "Registration Charges"

                if row[6] == None:

                        row[6] = "Description not availabe. Description will be in the Final Bill"


                self.table.insert("","end",text="", values=row)


        #self.status_bar.config(text="You Searched Something")



    def search_current_ane_patient(self):

        self.clear_table(self.cur_ane_table)

        
        self.dbcon = Ora()
        self.status_bar.config(text=self.dbcon.status_update())

        self.cur_pat_list = self.dbcon.current_ane_patient()
        #self.cur_pat_list.config(text="You Searched Something")
        for row in self.cur_pat_list:
            self.cur_ane_table.insert("","end",text="", values=row)


    def bill_generator(self):
        
        os.environ["INVOICE_LANG"] = "en"

        self.patient = Client(self.item_list[0][1],address=self.item_list[0][0])
        self.kdah_name_on_bill = Provider('Kokilaben Dhirubhai Ambani Hospital')

        self.signature = Creator('')

        self.invoice = Invoice(self.patient, self.kdah_name_on_bill,self.signature)
        self.invoice.currency_locale = 'en_US.UTF-8'
        

        self.invoice.add_item(Item(1, 1000, description="Casualty Examination Charges",))

        
     
        for values in self.item_list:
            
          
                #self.invoice.add_item(Item(count=int(qty), price=int(base_rate), description=item_desc))
            
            self.invoice.add_item(Item(count=float(values[8]), price=float(values[7]), description=values[6]))
                
        
        self.files_type = [('All Files', '*.*'), ('PDF Files', '*.pdf')]

        self.file = asksaveasfilename(defaultextension=".pdf",filetypes=self.files_type, initialfile="ANE Bill Report.pdf",title="Save File of ANE Report in PDF format")

        bill = SimpleInvoice(self.invoice)
        
        bill.gen(self.file, generate_qr_code=FALSE)

        os.startfile(self.file)
        

    def direct_ane_bill(self,event):
        

        cur_click_item = self.cur_ane_table.focus() # will take item in focus / click from tree
        
        dict_value_from_table = self.cur_ane_table.item(cur_click_item) # gives back dictonary item
        
        self.uhid_from_ane_click = dict_value_from_table['values'] # sort it down to only uhid

        self.search_n_view(self.uhid_from_ane_click[0])

        self.bill_generator()

        
        
      



    def hide_menu_frames(self):

        for widget in self.main_menu_frame.winfo_children():
            widget.forget()

        for widget in self.current_ane_patient_frame.winfo_children():
            widget.forget()

        for widget in self.about_frame.winfo_children():
            widget.forget()
        
        self.main_menu_frame.pack_forget()
        self.current_ane_patient_frame.pack_forget()
        self.about_frame.pack_forget()

    def clear(self):
        self.hide_menu_frames()
        self.home()

    def clear_ane(self):
        self.hide_menu_frames()
        self.cur_ane_pat()
    
    def clear_table(self,table):
        
        all_tables = table.get_children()
        
        for item in all_tables:
            table.delete(item)


if __name__ == '__main__':
    root = App()
    
    root.frames(root)

    root.menu_items(root)

    root.home()

    root.status_label(root)

    root.mainloop()
