import os
import tkinter as tk
from tkinter import messagebox, ttk
from validators import *

from index_direct_file import IndexDirectFile


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lab3")

        self.create_block = tk.Frame(self.master, bg="lightgray", padx=10, pady=10)
        self.create_text = tk.Entry(self.create_block, width=15)
        self.select_block = tk.Frame(self.master, bg="lightgray", padx=10, pady=10)
        self.select_text = tk.Entry(self.select_block, width=15)
        self.generate_block = tk.Frame(self.master, bg="lightgray", padx=10, pady=10)
        self.generate_text = tk.Entry(self.generate_block, width=15)

        self.selected_db_var = tk.StringVar(value="No Database Selected")
        self.selected_text = tk.Entry(self.master, textvariable=self.selected_db_var, state='readonly', width=30)

        self.key = tk.Entry(self.master, width=15)
        self.value = tk.Entry(self.master, width=15)
        self.found_var = tk.StringVar(value="")
        self.found = tk.Entry(self.master, textvariable=self.found_var, width=15, state='readonly')
        self.comparisons_var = tk.StringVar(value="")
        self.comparisons = tk.Entry(self.master, textvariable=self.comparisons_var, width=15, state='readonly')

        self.tree = ttk.Treeview(self.master, columns=["Row"] + [f"{i + 1}" for i in range(10)], show='headings')

        self.index_direct_file = None

        self.master.protocol("WM_DELETE_WINDOW", self.save_data)
        self.master.after(5000 * 60, self.save_data_periodic)

    def create_gui(self):
        self.master.title("Lab3")

        self.create_block.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        create_label = tk.Label(self.create_block, text="Create", font=("Arial", 12))
        create_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.create_text.grid(row=0, column=1, sticky="e")
        self.create_text.insert(tk.END, "Enter DB name")
        create_button = tk.Button(self.create_block, text="Create", command=self.create_db)
        create_button.grid(row=1, column=1, sticky="e")

        self.select_block.grid(row=0, column=2, columnspan=2, padx=10, pady=10)
        select_label = tk.Label(self.select_block, text="Select", font=("Arial", 12))
        select_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.select_text.grid(row=0, column=1, sticky="e")
        self.select_text.insert(tk.END, "Enter DB name")
        select_button = tk.Button(self.select_block, text="Select", command=self.select_db)
        select_button.grid(row=1, column=1, sticky="e")

        self.generate_block.grid(row=0, column=4, columnspan=2, padx=10, pady=10)
        generate_label = tk.Label(self.generate_block, text="Generate", font=("Arial", 12))
        generate_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.generate_text.grid(row=0, column=1, sticky="e")
        self.generate_text.insert(tk.END, "Enter DB name")
        generate_button = tk.Button(self.generate_block, text="Generate", command=self.generate_db)
        generate_button.grid(row=1, column=1, sticky="e")

        selected_label = tk.Label(self.master, text="Selected Database:")
        selected_label.grid(row=1, column=2, columnspan=2, pady=(10, 0))
        self.selected_text.grid(row=2, column=2, columnspan=2, pady=(10, 0))

        key_label = tk.Label(self.master, text="Key:")
        key_label.grid(row=3, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        self.key.grid(row=3, column=1, padx=(0, 5), pady=(10, 0), sticky="e")

        value_label = tk.Label(self.master, text="Value:")
        value_label.grid(row=3, column=3, pady=(10, 0), padx=(0, 10), sticky="e")
        self.value.grid(row=3, column=4, pady=(10, 0), sticky="w")

        found_label = tk.Label(self.master, text="Found value:")
        found_label.grid(row=4, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        self.found.grid(row=4, column=1, padx=(0, 5), pady=(10, 0), sticky="e")

        comparisons_label = tk.Label(self.master, text="Comparisons num:")
        comparisons_label.grid(row=4, column=3, pady=(10, 0), padx=(0, 10), sticky="e")
        self.comparisons.grid(row=4, column=4, pady=(10, 0), sticky="w")

        button_find = tk.Button(self.master, text=" Find ", command=self.find_button)
        button_add = tk.Button(self.master, text="  Add ", command=self.add_button)
        button_modify = tk.Button(self.master, text="Modify", command=self.modify_button)
        button_remove = tk.Button(self.master, text="Remove", command=self.remove_button)

        button_find.grid(row=5, column=1, padx=10, pady=10)
        button_add.grid(row=5, column=2, padx=10, pady=10)
        button_modify.grid(row=5, column=3, padx=10, pady=10)
        button_remove.grid(row=5, column=4, padx=10, pady=10, sticky="w")

        button_update = tk.Button(self.master, text="Update", command=self.update_button)
        button_update.grid(row=6, column=2, columnspan=2, pady=10, padx=(0, 30))

        self.tree.heading("Row", text="Row")
        self.tree.column("Row", width=30)
        for i in range(10):
            col_name = f"{i + 1}"
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=30)

        y_scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        y_scrollbar.grid(row=0, column=7, sticky='ns', rowspan=7)
        self.tree.configure(yscrollcommand=y_scrollbar.set)
        self.tree.grid(row=0, column=6, rowspan=7)

    def fill_table(self):
        self.clear_table()
        num_rows = len(self.index_direct_file.lines) // self.index_direct_file.b_size
        for i in range(num_rows):
            values = [i + 1] + [index[0] for index in self.index_direct_file.lines[i * self.index_direct_file.b_size:
                                                (i + 1) * self.index_direct_file.b_size]]
            self.tree.insert("", "end", values=values)
        num_rows_overflow = len(self.index_direct_file.overflow_lines) // self.index_direct_file.b_size
        for i in range(num_rows_overflow):
            values = [f"ov{i + 1}"] + [index[0] for index in
                                       self.index_direct_file.overflow_lines[i * self.index_direct_file.b_size:
                                                                             (i + 1) * self.index_direct_file.b_size]]
            self.tree.insert("", "end", values=values)

    def clear_table(self):
        # Clear all items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

    def select_db(self):
        selected = self.select_text.get()
        if len(selected) > 15:
            messagebox.showerror("Error", "Please enter value less than 15 symbols")
            return
        index_file = selected + 'index.txt'
        main_file = selected + 'main.txt'
        overflow_file = selected + 'overflow.txt'
        self.index_direct_file = IndexDirectFile(10000, index_file, main_file, overflow_file, 0.6)
        validation = self.index_direct_file.validate()
        if not validation[0]:
            self.index_direct_file = None
            messagebox.showerror("Error", validation[1])
            return
        self.index_direct_file.upload_data()
        self.selected_db_var.set(main_file)
        self.fill_table()

    def create_db(self):
        selected = self.create_text.get()
        if len(selected) > 15:
            messagebox.showerror("Error", "Please enter value less than 15 symbols")
            return
        index_file = selected + 'index.txt'
        main_file = selected + 'main.txt'
        overflow_file = selected + 'overflow.txt'
        if os.path.exists(main_file) or os.path.exists(index_file) or os.path.exists(overflow_file):
            messagebox.showerror("Error", "Index-direct file already exists")
            return
        with open(main_file, 'w') as _:
            with open(index_file, 'w') as _:
                with open(overflow_file, 'w') as _:
                    pass
        self.index_direct_file = IndexDirectFile(10000, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.upload_data()
        self.selected_db_var.set(main_file)
        self.fill_table()
        messagebox.showinfo("Success", "Operation Successful!")

    def generate_db(self):
        selected = self.generate_text.get()
        if len(selected) > 15:
            messagebox.showerror("Error", "Please enter value less than 15 symbols")
            return
        index_file = selected + 'index.txt'
        main_file = selected + 'main.txt'
        overflow_file = selected + 'overflow.txt'
        self.index_direct_file = IndexDirectFile(10000, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.generate_file()
        self.index_direct_file.upload_data()
        self.selected_db_var.set(main_file)
        self.fill_table()
        messagebox.showinfo("Success", "Operation Successful!")

    def find_button(self):
        if self.index_direct_file is None:
            messagebox.showerror("Error", "Please select index-direct file")
            self.clear_values()
            return
        key = self.key.get()
        validation = validate_positive_integer(key, 10)
        if not validation[0]:
            self.clear_values()
            messagebox.showerror("Error", validation[1])
            return
        indexes = self.index_direct_file.search(int(key))
        if indexes is None:
            self.clear_values()
            messagebox.showerror("Error", "Index not found")
            return
        self.found_var.set(indexes[-1])
        self.comparisons_var.set(indexes[-2])

    def modify_button(self):
        self.clear_values()
        if self.index_direct_file is None:
            messagebox.showerror("Error", "Please select index-direct file")
            return
        key = self.key.get()
        validation = validate_positive_integer(key, 10)
        if not validation[0]:
            messagebox.showerror("Error", validation[1])
            return
        value = self.value.get()
        if not 1 <= len(value) <= 15:
            messagebox.showerror("Error", "Value should be between 1 and 15 symbols")
            return
        value = value.zfill(15)
        result = self.index_direct_file.modify(int(key), value)
        if result is None:
            messagebox.showerror("Error", "Index not found")
            return

    def remove_button(self):
        self.clear_values()
        if self.index_direct_file is None:
            messagebox.showerror("Error", "Please select index-direct file")
            return
        key = self.key.get()
        validation = validate_positive_integer(key, 10)
        if not validation[0]:
            messagebox.showerror("Error", validation[1])
            return
        result = self.index_direct_file.remove(int(key))
        if result is None:
            messagebox.showerror("Error", "Index not found")
            return

    def add_button(self):
        self.clear_values()
        if self.index_direct_file is None:
            messagebox.showerror("Error", "Please select index-direct file")
            return
        key = self.key.get()
        validation = validate_positive_integer(key, 10)
        if not validation[0]:
            messagebox.showerror("Error", validation[1])
            return
        value = self.value.get()
        if not 1 <= len(value) <= 15:
            messagebox.showerror("Error", "Value should be between 1 and 15 symbols")
            return
        value = value.zfill(15)
        result = self.index_direct_file.add(int(key), value)
        if result is None:
            messagebox.showerror("Error", "Index already exists")
            return

    def update_button(self):
        if self.index_direct_file is None:
            messagebox.showerror("Error", "Please select index-direct file")
            return
        self.index_direct_file.formatted_write(self.index_direct_file.index_n)
        self.index_direct_file.formatted_write(self.index_direct_file.main_n)
        self.index_direct_file.formatted_write(self.index_direct_file.overflow_n)
        self.fill_table()

    def save_data(self):
        if self.index_direct_file is None:
            self.master.destroy()
            return
        self.index_direct_file.formatted_write(self.index_direct_file.index_n)
        self.index_direct_file.formatted_write(self.index_direct_file.main_n)
        self.index_direct_file.formatted_write(self.index_direct_file.overflow_n)
        self.master.destroy()

    def save_data_periodic(self):
        if self.index_direct_file is None:
            return
        self.index_direct_file.formatted_write(self.index_direct_file.index_n)
        self.index_direct_file.formatted_write(self.index_direct_file.main_n)
        self.index_direct_file.formatted_write(self.index_direct_file.overflow_n)

    def clear_values(self):
        self.found_var.set("")
        self.comparisons_var.set("")
