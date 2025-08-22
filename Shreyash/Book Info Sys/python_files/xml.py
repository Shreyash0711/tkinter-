from python_files.widget_files.ButtonClass import MyButton
from tkinter import ttk, messagebox, filedialog
from python_files.widget_files.logger import Log
import tkinter as tk
import xml.etree.ElementTree as ET
import json
import os
import tempfile
import openpyxl

class Xml_tab(ttk.Frame):
    def __init__(self, parent, logger: Log):
        super().__init__(parent)
        self.logger = logger
        self.logger.info_logger("XML tab initialized")

        # Buttons export and download
        MyButton(self, text="⬇️ Display DB", command=self.display_db).grid(row=0, column=0, padx=5, pady=5)

        self.download_btn = MyButton(self, text="💾 Download XML", command=self.download_XML)
        self.download_btn.grid(row=0, column=1, padx=5)
        self.download_btn.config(state="disabled")  # disabled initially

        MyButton(self, text="📂 Open XML File", command=self.open_XML_file).grid(row=5, column=0, padx=5)

        # Display exported XML
        self.result_box = tk.Text(self, width=45, height=6, state="disabled", wrap="none")
        self.result_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        #scrollbars
        y_scroll = ttk.Scrollbar(self, orient='vertical', command=self.result_box.yview)
        y_scroll.grid(row=1, column=3, sticky='ns')
        self.result_box['yscrollcommand'] = y_scroll.set

        x_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.result_box.xview)
        x_scroll.grid(row=2, column=0, columnspan=3, sticky='ew')
        self.result_box['xscrollcommand'] = x_scroll.set



    def display_db(self):
        filename = os.path.join("data", "db.json")
        if not os.path.exists(filename):
            messagebox.showerror("Error", "db.json not found.")
            return

        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "JSON file is invalid")
                return

        if not data:
            messagebox.showinfo("Info", "No data in JSON file")
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Books"

      
        headers = ["id", "name", "author", "price", "year"]
        ws.append([h.capitalize() for h in headers])

        for item in data:
            ws.append([
                item.get("id", ""),
                item.get("name", ""),
                item.get("author", ""),  
                item.get("price", ""),
                item.get("year", "")
            ])

        # Save to temp file
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, "books_exported.xlsx")
        wb.save(filename)
        self.excel_file = filename

        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)
        for row in ws.iter_rows(values_only=True):
            self.result_box.insert(tk.END, "\t".join(map(str, row)) + "\n")
        self.result_box.config(state="disabled")

        self.download_btn.config(state="normal")

        self.logger.info_logger(f"JSON data exported to {filename}")
        messagebox.showinfo("Success", f"Exported to temporary file")



    def build_element(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                element = ET.SubElement(parent, key)
                self.build_element(element, value)
        elif isinstance(data, list):
            for item in data:
                element = ET.SubElement(parent, "item")
                self.build_element(element, item)
        else:
            parent.text = str(data)


    def create_xml_with_indentation(self, root_tag, data):
        root = ET.Element(root_tag)
        self.build_element(root, data)
        
        
        ET.indent(root, space="  ", level=0) 
        
        return ET.ElementTree(root)
    
    
    def download_XML(self):
        # Load JSON data
        filename = os.path.join("data", "db.json")
        if not os.path.exists(filename):
            messagebox.showerror("Error", "db.json not found.")
            return

        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "JSON file is invalid")
                return

        if not data:
            messagebox.showinfo("Info", "No data in JSON file")
            return

        # Create the root element
        root = ET.Element("BOOK_DETAILS")

        for book in data:
            book_id = str(book.get("id", ""))
            book_element = ET.SubElement(root, "BOOK_COMPONENT_ATTRIBUTE", ID=book_id)

            for key in ["id", "name", "author", "price", "year"]:
                value = book.get(key, "")
                sub_elem = ET.SubElement(book_element, key.upper())
                sub_elem.text = str(value)

        ET.indent(root, space="  ", level=0)
        tree = ET.ElementTree(root)

        # ask to save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")],
            title="Save XML File As",
            initialdir=os.getcwd()
        )

        if not save_path:
            return

        try:
            tree.write(save_path, encoding="utf-8", xml_declaration=True)
            self.logger.info_logger(f"Exported JSON to XML: {save_path}")
            messagebox.showinfo("Success", f"XML file saved to:\n{save_path}")

        except Exception as e:
            self.logger.error_logger(f"Failed to write XML file: {e}")
            messagebox.showerror("Error", f"Failed to save XML file:\n{e}")


    def open_XML_file(self):
        xml_path = filedialog.askopenfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")],
            title="Open XML File",
            initialdir=os.getcwd()
        )

        if not xml_path:
            return

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            rows = []
            headers = set()

            # Extract all BOOK_COMPONENT_ATTRIBUTE elements
            for book_elem in root.findall("BOOK_COMPONENT_ATTRIBUTE"):
                row = {}
                for child in book_elem:
                    
                    row[child.tag.upper()] = child.text
                    headers.add(child.tag.upper())
                rows.append(row)

            if not rows:
                messagebox.showinfo("Info", "File column issue")
                return

            headers = list(headers)
            
        
            # Display in result_box
            self.result_box.config(state="normal")
            self.result_box.delete(1.0, tk.END)

            self.result_box.insert(tk.END, "\t".join(headers) + "\n")
            for row in rows:
                self.result_box.insert(tk.END, "\t".join(row.get(h, "") for h in headers) + "\n")

            self.result_box.config(state="disabled")

            self.logger.info_logger(f"Opened XML file and displayed as table: {xml_path}")

        except Exception as e:
            self.logger.error_logger(f"Failed to open XML file: {e}")
            messagebox.showerror("Error", f"Failed to open XML file:\n{e}")
