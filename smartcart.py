import tkinter as tk
from tkinter import messagebox
import keyboard

class KioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")

        # Products with their barcodes, names, prices, and weights
        self.products = {
            '8901057510028': {'name': 'KANGARO PINS', 'price': 10.0,'weight':30.0},
            '8901012116869': {'name': 'BODY WASH', 'price': 450.0,'weight':200.0},
            '600310067696': {'name': 'BODY LOTION', 'price': 190.0,'weight':500.0},
            # Add more products as needed
        }

        self.cart = {}
        self.barcode = ''

        # Setup GUI
        self.setup_gui()

        # Attach the barcode scan listener
        keyboard.on_press(self.on_barcode_scan)

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.root.geometry("480x320")
        self.frame.pack(pady=20)

        self.product_listbox = tk.Listbox(self.frame, width=70)
        self.product_listbox.pack()

        self.total_label = tk.Label(self.frame,fg='green',borderwidth=1, text="Total: 0.00 Rs/-", font=("Arial", 14))
        self.total_label.pack(pady=10)

        self.remove_button = tk.Button(self.frame, text="Remove Selected", fg='red', borderwidth=1,  command=self.remove_selected)
        self.remove_button.pack(pady=5)

        self.clear_button = tk.Button(self.frame, text="Clear All",fg='blue', borderwidth=1, command=self.clear_all)
        self.clear_button.pack(pady=5)

    def on_barcode_scan(self, event):
        if event.name == 'enter':
            self.process_barcode(self.barcode)
            self.barcode = ''
        else:
            self.barcode += event.name

    def process_barcode(self, barcode):
        if barcode in self.products:
            product = self.products[barcode]
            if barcode in self.cart:
                self.cart[barcode]['quantity'] += 1
            else:
                self.cart[barcode] = {
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': 1,
                    'weight': product['weight']
                }
            self.update_listbox()
            self.update_total()
        else:
            messagebox.showerror("Error", "Product not found!")

    def update_listbox(self):
        self.product_listbox.delete(0, tk.END)
        for barcode, details in self.cart.items():
            self.product_listbox.insert(tk.END, f"{details['name']} - Rs {details['price']} x {details['quantity']} (Weight: {details['weight']} gms)")

    def update_total(self):
        total = sum(details['price'] * details['quantity'] for details in self.cart.values())
        self.total_label.config(text=f"Total: {total:.2f} Rs/-")

    def remove_selected(self):
        selected = self.product_listbox.curselection()
        if selected:
            item_text = self.product_listbox.get(selected[0])
            product_name = item_text.split(' - ')[0]
            barcode_to_remove = None
            for barcode, details in self.cart.items():
                if details['name'] == product_name:
                    barcode_to_remove = barcode
                    break
            if barcode_to_remove:
                del self.cart[barcode_to_remove]
                self.update_listbox()
                self.update_total()

    def clear_all(self):
        self.cart.clear()
        self.update_listbox()
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()
