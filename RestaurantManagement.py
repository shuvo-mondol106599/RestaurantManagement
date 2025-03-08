Author:Shuvo Mondol
Project:Restaurant Management
import tkinter as tk
from tkinter import ttk, messagebox
import csv

class Restaurant:
    def __init__(self):
        self.menu = {}  # Dictionary to store menu items, prices, and descriptions
        self.order = {}  # Dictionary to store orders
        self.load_menu_from_csv()

    def load_menu_from_csv(self):
        try:
            with open("menu.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        item_name, price, description = row
                        self.menu[item_name] = (float(price), description)
        except FileNotFoundError:
            print("No existing menu file found. Starting with an empty menu.")

    def save_menu_to_csv(self):
        try:
            with open("menu.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                for item_name, (price, description) in self.menu.items():
                    writer.writerow([item_name, price, description])
        except Exception as e:
            print(f"Error saving menu to CSV: {e}")

    def add_item(self, item_name, price, description):
        if item_name in self.menu:
            return f"Error: Item '{item_name}' already exists in the menu!"
        self.menu[item_name] = (price, description)
        self.save_menu_to_csv()
        return f"Item '{item_name}' added successfully!"

    def remove_item(self, item_name):
        if item_name in self.menu:
            del self.menu[item_name]
            self.save_menu_to_csv()
            return f"Item '{item_name}' removed successfully!"
        return f"Error: Item '{item_name}' not found in the menu."

    def take_order(self, item_name, quantity):
        if item_name not in self.menu:
            return f"Error: '{item_name}' is not available on the menu."
        if quantity <= 0:
            return "Error: Quantity must be greater than 0."
        if item_name in self.order:
            self.order[item_name] += quantity
        else:
            self.order[item_name] = quantity
        return f"'{item_name}' x {quantity} added to the order."

    def modify_order(self, item_name, new_quantity):
        if item_name not in self.order:
            return f"Error: '{item_name}' is not in the order."
        if new_quantity <= 0:
            del self.order[item_name]
            return f"'{item_name}' removed from the order."
        self.order[item_name] = new_quantity
        return f"Quantity for '{item_name}' updated to {new_quantity}."

class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.restaurant = Restaurant()
        
        self.setup_menu_tab()
        self.setup_order_tab()

    def setup_menu_tab(self):
        frame = ttk.LabelFrame(self.root, text="Manage Menu")
        frame.pack(padx=10, pady=10, fill="both")
        
        tk.Label(frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        self.item_name_entry = tk.Entry(frame)
        self.item_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.item_price_entry = tk.Entry(frame)
        self.item_price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.item_desc_entry = tk.Entry(frame)
        self.item_desc_entry.grid(row=2, column=1, padx=5, pady=5)
        
        add_button = tk.Button(frame, text="Add Item", command=self.add_item)
        add_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.menu_display = tk.Text(frame, height=10, width=50)
        self.menu_display.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.view_menu()
    
    def add_item(self):
        item_name = self.item_name_entry.get().strip().title()
        price = self.item_price_entry.get().strip()
        description = self.item_desc_entry.get().strip()
        if not item_name or not price:
            messagebox.showerror("Error", "Please enter item name and price.")
            return
        try:
            price = float(price)
            result = self.restaurant.add_item(item_name, price, description)
            messagebox.showinfo("Success", result)
            self.view_menu()
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
    
    def view_menu(self):
        self.menu_display.delete(1.0, tk.END)
        menu_text = "\n".join([f"{item}: ${price:.2f} ({desc})" for item, (price, desc) in self.restaurant.menu.items()])
        self.menu_display.insert(tk.END, menu_text)
    
    def setup_order_tab(self):
        frame = ttk.LabelFrame(self.root, text="Take Order")
        frame.pack(padx=10, pady=10, fill="both")
        
        tk.Label(frame, text="Select Item:").grid(row=0, column=0, padx=5, pady=5)
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(frame, textvariable=self.item_var, state="readonly")
        self.item_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.item_dropdown["values"] = list(self.restaurant.menu.keys())
        
        tk.Label(frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        order_button = tk.Button(frame, text="Add to Order", command=self.take_order)
        order_button.grid(row=2, column=0, columnspan=2, pady=5)
    
    def take_order(self):
        item_name = self.item_var.get()
        quantity = self.quantity_entry.get().strip()
        if not item_name or not quantity:
            messagebox.showerror("Error", "Please select an item and enter a quantity.")
            return
        try:
            quantity = int(quantity)
            result = self.restaurant.take_order(item_name, quantity)
            messagebox.showinfo("Success", result)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantGUI(root)
    root.mainloop()
