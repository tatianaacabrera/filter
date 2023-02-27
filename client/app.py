import pandas as pd
import os

import datetime as dt

import tkinter as tk

from tkinter import Scrollbar, ttk, filedialog, messagebox

# Pandas
PATH = os.path.expanduser('~/Documents/')
TYPE = '.csv'

# Tkinter
X = 10
Y = 10

def menu_bar(root):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    main_menu = tk.Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label='main', menu=main_menu)

    main_menu.add_command(label='Handle')
    main_menu.add_command(label='Exit', command=root.destroy)

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        
        self.main_window()

    def main_window(self):
        self.label_open = tk.Label(self, text='Open file')
        self.label_open.grid(row=0, column=0, padx=X, pady=Y)

        self.btn_open = tk.Button(self, text='Open', command=self.open_file)
        self.btn_open.grid(row=0, column=1, padx=X, pady=Y)

    def open_file(self):
        self.path = filedialog.askopenfilename(
            initialdir = '/',
            title = 'Seleccione el archivo',
            filetypes = (('CSV Files','*.csv'),)
            )
        if self.path != '':
            try: 
                self.df = pd.read_csv(
                    self.path, delimiter=',' or ';', 
                    encoding='utf-8', 
                    encoding_errors='ignore', on_bad_lines='skip'
                    )
                self.fields_window()
            except Exception as e:
                messagebox.showinfo(
                    message=e,
                    title='Cannot open file'
                    )


    def fields_window(self):
        self.fields_dialog = tk.Toplevel()
        self.fields_dialog.title('Fields')

        options = self.df.columns.values

        self.listbox = tk.Listbox(self.fields_dialog, selectmode=tk.MULTIPLE)
        self.listbox.insert(0, *options)
        self.listbox.pack(side= tk.LEFT, fill= tk.BOTH)
        
        scrollbar = ttk.Scrollbar(self.fields_dialog, orient= 'vertical')
        scrollbar.pack(side= tk.LEFT, fill= tk.BOTH)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        done_btn = ttk.Button(self.fields_dialog, text='Done', command=self.selected)
        done_btn.pack(side=tk.BOTTOM, padx=X, pady=Y)
        skip_btn = ttk.Button(self.fields_dialog, text='Skip', command=self.fields_dialog.destroy)
        skip_btn.pack(side=tk.BOTTOM, padx=X, pady=Y)

    def selected(self):
        self.fields_dialog.withdraw()

        # TODO: Permitir prioridad de campos, preseleccionar ID

        index = self.listbox.curselection()
        self.filters = [self.listbox.get(i) for i in index]

        msg = ', '.join(self.filters)

        confirm = messagebox.askquestion(
            title='Selected filters',
            message=msg
        )

        if confirm == 'yes' and len(self.filters) > 0:
            self.handle_window()
        else:
            self.listbox.selection_clear(0, tk.END)
            messagebox.showinfo(
                    message=f'You should choose almost one parameter.',
                    title='Error'
                )
            self.fields_dialog.deiconify()
        
    def handle_window(self):
        self.fields_dialog.destroy()

        self.final = self.df.groupby(self.filters).size().to_frame('Total')
    
        self.handle_dialog = tk.Toplevel()
        self.handle_dialog.title('Handle file')


        self.handle_table()

        ok_btn = ttk.Button(self.handle_dialog, text='confirm', command=self.create_file)
        ok_btn.pack(side='bottom', padx=X, pady=Y)

    def handle_table(self):
        self.table = tk.Text(self.handle_dialog)
        self.table.insert(tk.INSERT, self.final.to_string())
        self.table.pack()

    def create_file(self):
        self.handle_dialog.destroy()

        final_name = 'grouped_' + dt.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        self.final.to_csv(PATH + final_name + TYPE)
        