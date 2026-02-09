import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class StockManagement:
    def __init__(self, parent_frame, db, accounting_service):
        self.parent_frame = parent_frame
        self.db = db
        self.accounting_service = accounting_service
        self.setup_ui()
        self.load_stock()
        self.load_transactions()
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add Stock Section
        add_frame = ctk.CTkFrame(self.main_container, border_width=2, border_color="#68a2a6", fg_color="transparent")
        add_frame.pack(fill="both", padx=5, pady=5)
        
        ctk.CTkLabel(add_frame, text="Add New Stock", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Form fields
        form_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        form_frame.pack(padx=10, pady=10)
        
        # Row 1
        row1 = ctk.CTkFrame(form_frame)
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Item Name:", width=100).pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(row1, width=200, justify="center", fg_color="transparent")
        self.name_entry.pack(side="left", padx=(5, 80))
        
        ctk.CTkLabel(row1, text="Model:", width=100).pack(side="left", padx=5)
        self.model_entry = ctk.CTkEntry(row1, width=200, justify="center", fg_color="transparent")
        self.model_entry.pack(side="left", padx=5)
        
        # Row 2
        row2 = ctk.CTkFrame(form_frame)
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="Quantity:", width=100).pack(side="left", padx=5)
        self.quantity_entry = ctk.CTkEntry(row2, width=200, justify="center", fg_color="transparent")
        self.quantity_entry.pack(side="left", padx=(5, 80))
        self.quantity_entry.insert(0, "0") 
        
        ctk.CTkLabel(row2, text="Item Price (Ksh):", width=100).pack(side="left", padx=5)
        self.price_entry = ctk.CTkEntry(row2, width=200, justify="center", fg_color="transparent")
        self.price_entry.pack(side="left", padx=5)
        self.price_entry.insert(0, "0.00")
        
        # Row 3
        row3 = ctk.CTkFrame(form_frame)
        row3.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row3, text="Total Cost (Ksh):", width=100).pack(side="left", padx=5)
        self.cost_entry = ctk.CTkEntry(row3, width=200, state="readonly", justify="center", fg_color="transparent")
        self.cost_entry.pack(side="left", padx=(5, 80))

        # Function to calculate total cost
        def calculate_total():
            try:
                quantity = self.quantity_entry.get().strip()
                price = self.price_entry.get().strip()
                
                # Handle empty values
                if not quantity:
                    quantity = "0"
                if not price:
                    price = "0"
                    
                total_items = int(quantity)
                item_price = float(price)
                total_amount = total_items * item_price
                
                # Update the cost entry
                self.cost_entry.configure(state="normal")
                self.cost_entry.delete(0, "end")
                self.cost_entry.insert(0, f"{total_amount:.2f}")
                self.cost_entry.configure(state="readonly")
            except ValueError:
                # Handle invalid input
                self.cost_entry.configure(state="normal")
                self.cost_entry.delete(0, "end")
                self.cost_entry.insert(0, "0.00")
                self.cost_entry.configure(state="readonly")

        # Set up trace to update total when quantity or price changes
        self.quantity_entry.bind("<KeyRelease>", lambda e: calculate_total())
        self.price_entry.bind("<KeyRelease>", lambda e: calculate_total())

        # Calculate initial total
        calculate_total()
        
        ctk.CTkLabel(row3, text="Min Stock Level:", width=100).pack(side="left", padx=5)
        self.min_stock_entry = ctk.CTkEntry(row3, width=200, justify="center", fg_color="transparent")
        self.min_stock_entry.insert(0, "5")
        self.min_stock_entry.pack(side="left", padx=5)
        
        # Row 4
        row4 = ctk.CTkFrame(form_frame)
        row4.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row4, text="Description:", width=100).pack(side="left", padx=5)
        self.desc_entry = ctk.CTkEntry(row4, width=200, fg_color="transparent")
        self.desc_entry.pack(side="left", padx=(5, 80))

        ctk.CTkLabel(row4, text="Date:", width=100).pack(side="left", padx=5)
        self.date_entry = ctk.CTkEntry(row4, width=200, justify="center", fg_color="transparent")
        date = datetime.now().strftime("%d/%m/%Y")
        self.date_entry.insert(0, date)
        self.date_entry.pack(side="left", padx=5)
        
        # Add button
        add_btn = ctk.CTkButton(
            form_frame, 
            text="Add Stock", 
            command=self.add_stock,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_btn.pack(pady=(10, 0))

        # Bind Enter key
        form_frame.bind('<Return>', lambda e: self.add_stock())
        
        # Separator
        ctk.CTkFrame(self.main_container, height=2, fg_color="gray").pack(fill="x", pady=10)
        
        # Stock Overview Frame
        overview_frame = ctk.CTkFrame(self.main_container)
        overview_frame.pack(fill="x", padx=5, pady=5)

        # Search Frame
        search_frame = ctk.CTkFrame(overview_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=5)

        # Search type combobox
        ctk.CTkLabel(search_frame, text="Search by:", width=80).pack(side="left", padx=0)
        self.search_type = ctk.CTkComboBox(
            search_frame, 
            width=120,
            values=["All", "Item Name", "Model", "Date", "Low Stock", "Out of Stock"],
            state="readonly"
        )
        self.search_type.set("All")
        self.search_type.pack(side="left", padx=5)

        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            width=250, 
            placeholder_text="Enter search term...", 
            justify="center"
        )
        self.search_entry.pack(side="left", padx=5, pady=0)
        self.search_entry.bind("<Return>", lambda e: self.search_stock())

        # Search button
        search_btn = ctk.CTkButton(
            search_frame, 
            text="🔍 Search", 
            command=self.search_stock,
            width=100,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=5)

        # Clear search button
        clear_btn = ctk.CTkButton(
            search_frame, 
            text="Clear", 
            command=self.clear_search,
            width=80,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        clear_btn.pack(side="left", padx=5)

        # Export button
        export_btn = ctk.CTkButton(
            search_frame, 
            text="📄 Export", 
            command=self.export_stock,
            width=80,
            fg_color="#9b59b6",
            hover_color="#7c309b"
        )
        export_btn.pack(side="right", padx=5)
        
        # Stock table frame
        table_frame = ctk.CTkFrame(overview_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create Treeview with customtkinter style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       font=('Arial', 10),
                       rowheight=35)
        style.configure("Treeview.Heading", 
                       background="#1D5568", 
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#22559b')])
        
        # Define columns
        columns = ("ID", "Name", "Model", "Quantity", "Price (Ksh)", "Cost (Ksh)", "Min Level", "Value (Ksh)", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define headings and column widths
        col_widths = {
            "ID": 50,
            "Name": 150,
            "Model": 120,
            "Quantity": 80,
            "Price (Ksh)": 100,
            "Cost (Ksh)": 100,
            "Min Level": 80,
            "Value (Ksh)": 100,
            "Status": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for editing
        self.tree.bind("<Double-1>", self.edit_stock_item)
        
        # Separator
        ctk.CTkFrame(self.main_container, height=2, fg_color="gray").pack(fill="x", pady=10)
        
        # Transactions Frame
        trans_frame = ctk.CTkFrame(self.main_container)
        trans_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(trans_frame, text="Stock Transactions", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Transactions table
        trans_table_frame = ctk.CTkFrame(trans_frame)
        trans_table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        trans_columns = ("ID", "Stock", "Type", "Qty", "Price", "Reference", "Date")
        self.trans_tree = ttk.Treeview(trans_table_frame, columns=trans_columns, show="headings", height=8)
        
        for col in trans_columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=100, anchor="center")
        
        self.trans_tree.column("Stock", width=150)
        self.trans_tree.column("Reference", width=150)
        
        trans_scrollbar = ttk.Scrollbar(trans_table_frame, orient="vertical", command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=trans_scrollbar.set)
        
        self.trans_tree.pack(side="left", fill="both", expand=True)
        trans_scrollbar.pack(side="right", fill="y")
    
    def add_stock(self):
        try:
            name = self.name_entry.get().strip()
            model = self.model_entry.get().strip()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get() or 0)
            cost_price = float(self.cost_entry.get() or 0)
            min_stock = int(self.min_stock_entry.get() or 5)
            description = self.desc_entry.get().strip()
            date = self.date_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Item name is required!")
                return
            
            # Check if item already exists
            existing = self.db.fetch_one(
                "SELECT id, quantity FROM stock WHERE name = ? AND model = ?",
                (name, model)
            )
            
            if existing:
                # Update existing stock
                new_qty = existing[1] + quantity
                self.db.execute_query(
                    "UPDATE stock SET quantity = ?, price = ?, cost_price = ?, updated_at = ? WHERE id = ?",
                    (new_qty, price, cost_price, datetime.now(), existing[0])
                )
                stock_id = existing[0]
            else:
                # Insert new stock
                stock_id = self.db.execute_query(
                    '''INSERT INTO stock (name, model, description, quantity, price, cost_price, min_stock_level, date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, model, description, quantity, price, cost_price, min_stock, date)
                )
            
            # Add transaction record
            transaction_ref = f"STOCK-IN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.db.execute_query(
                '''INSERT INTO stock_transactions (stock_id, transaction_type, quantity, price, reference)
                   VALUES (?, ?, ?, ?, ?)''',
                (stock_id, 'IN', quantity, price, transaction_ref)
            )
            
            # Record stock purchase as accounting transaction (Cost of Goods Sold)
            if cost_price > 0:
                purchase_data = {
                    'stock_id': stock_id,
                    'item_name': name,
                    'model': model,
                    'quantity': quantity,
                    'unit_cost': cost_price / quantity if quantity > 0 else cost_price,
                    'total_cost': cost_price,
                    'reference': transaction_ref,
                    'date': date,
                    'created_by': 1  # Default to admin, you might want to pass actual user
                }
                self.accounting_service.record_stock_purchase_transaction(purchase_data)
            
            messagebox.showinfo("Success", "Stock added successfully!")
            self.clear_form()
            self.load_stock()
            self.load_transactions()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for quantity and price!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add stock: {str(e)}")
    
    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.model_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.quantity_entry.insert(0, "0")
        self.price_entry.delete(0, 'end')
        self.price_entry.insert(0, "0.00")
        self.min_stock_entry.delete(0, 'end')
        self.min_stock_entry.insert(0, "5")
        self.desc_entry.delete(0, 'end')
        self.cost_entry.configure(state="normal")
        self.cost_entry.delete(0, "end")
        self.cost_entry.insert(0, "0.00")
        self.cost_entry.configure(state="readonly")
    
    def load_stock(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch stock from database
        query = '''
            SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                   (quantity * price) as value,
                   CASE 
                       WHEN quantity = 0 THEN 'Out of Stock'
                       WHEN quantity <= min_stock_level THEN 'Low Stock'
                       ELSE 'In Stock'
                   END as status
            FROM stock
            ORDER BY name
        '''
        stock_items = self.db.fetch_all(query)
        
        # Add items to treeview with status-based coloring
        for item in stock_items:
            item_id = item[0]
            values = list(item)
            
            # Format currency values
            values[4] = f"{values[4]:,.2f}"  # Price
            values[5] = f"{values[5]:,.2f}"  # Cost
            values[7] = f"{values[7]:,.2f}"  # Value
            
            self.tree.insert("", "end", iid=item_id, values=values)
            
            # Color code based on status
            if values[8] == "Out of Stock":
                self.tree.item(item_id, tags=("out_of_stock",))
            elif values[8] == "Low Stock":
                self.tree.item(item_id, tags=("low_stock",))
            else:
                self.tree.item(item_id, tags=("in_stock",))
        
        # Configure tag colors
        self.tree.tag_configure("out_of_stock", background="#e74c3c", foreground="white")
        self.tree.tag_configure("low_stock", background="#f39c12", foreground="white")
        self.tree.tag_configure("in_stock", background="#2a2d2e", foreground="white")
    
    def search_stock(self):
        search_type = self.search_type.get()
        search_term = self.search_entry.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Build query based on search type
        if search_type == "All":
            if search_term:
                query = '''
                    SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                           (quantity * price) as value,
                           CASE 
                               WHEN quantity = 0 THEN 'Out of Stock'
                               WHEN quantity <= min_stock_level THEN 'Low Stock'
                               ELSE 'In Stock'
                           END as status
                    FROM stock
                    WHERE name LIKE ? OR model LIKE ? OR date LIKE ?
                    ORDER BY name
                '''
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            else:
                # Show all items
                query = '''
                    SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                           (quantity * price) as value,
                           CASE 
                               WHEN quantity = 0 THEN 'Out of Stock'
                               WHEN quantity <= min_stock_level THEN 'Low Stock'
                               ELSE 'In Stock'
                           END as status
                    FROM stock
                    ORDER BY name
                '''
                params = ()
        
        elif search_type == "Item Name":
            query = '''
                SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value,
                       CASE 
                           WHEN quantity = 0 THEN 'Out of Stock'
                           WHEN quantity <= min_stock_level THEN 'Low Stock'
                           ELSE 'In Stock'
                       END as status
                FROM stock
                WHERE name LIKE ?
                ORDER BY name
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Model":
            query = '''
                SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value,
                       CASE 
                           WHEN quantity = 0 THEN 'Out of Stock'
                           WHEN quantity <= min_stock_level THEN 'Low Stock'
                           ELSE 'In Stock'
                       END as status
                FROM stock
                WHERE model LIKE ?
                ORDER BY name
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Date":
            query = '''
                SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value,
                       CASE 
                           WHEN quantity = 0 THEN 'Out of Stock'
                           WHEN quantity <= min_stock_level THEN 'Low Stock'
                           ELSE 'In Stock'
                       END as status
                FROM stock
                WHERE date LIKE ?
                ORDER BY name
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Low Stock":
            query = '''
                SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value,
                       'Low Stock' as status
                FROM stock
                WHERE quantity <= min_stock_level AND quantity > 0
                ORDER BY quantity ASC
            '''
            params = ()
        
        elif search_type == "Out of Stock":
            query = '''
                SELECT id, name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value,
                       'Out of Stock' as status
                FROM stock
                WHERE quantity = 0
                ORDER BY name
            '''
            params = ()
        
        try:
            # Execute query
            if params:
                stock_items = self.db.fetch_all(query, params)
            else:
                stock_items = self.db.fetch_all(query)
            
            # Display results
            if not stock_items:
                messagebox.showinfo("No Results", "No items found matching your search criteria.")
                return
            
            # Add items to treeview
            for item in stock_items:
                item_id = item[0]
                values = list(item)
                
                # Format currency values
                values[4] = f"{values[4]:,.2f}"  # Price
                values[5] = f"{values[5]:,.2f}"  # Cost
                values[7] = f"{values[7]:,.2f}"  # Value
                
                self.tree.insert("", "end", iid=item_id, values=values)
                
                # Color code based on status
                if values[8] == "Out of Stock":
                    self.tree.item(item_id, tags=("out_of_stock",))
                elif values[8] == "Low Stock":
                    self.tree.item(item_id, tags=("low_stock",))
                else:
                    self.tree.item(item_id, tags=("in_stock",))
            
            # Show result count
            result_count = len(stock_items)
            if search_term or search_type not in ["All", "Low Stock", "Out of Stock"]:
                search_info = f" ({result_count} items found)"
                if search_term:
                    search_info = f" for '{search_term}'{search_info}"
                messagebox.showinfo("Search Results", f"Search completed{search_info}")
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search stock: {str(e)}")
    
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.search_type.set("All")
        self.load_stock()
    
    def edit_stock_item(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_id = selected_item[0]
        values = self.tree.item(item_id, 'values')
        
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.parent_frame)
        dialog.title("Edit Stock Item")
        dialog.geometry("500x400")
        dialog.transient(self.parent_frame)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content frame
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"Edit Stock Item (ID: {values[0]})", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Form fields
        form_frame = ctk.CTkFrame(content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Item Name
        name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(name_frame, text="Item Name:").pack(side="left", padx=(20, 10), pady=0)
        name_entry = ctk.CTkEntry(name_frame, width=300, justify="center", fg_color="transparent")
        name_entry.pack(side="right", padx=(0, 20), pady=0)
        name_entry.insert(0, values[1])
        
        # Model
        model_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        model_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(model_frame, text="Model:").pack(side="left", padx=(20, 10), pady=0)
        model_entry = ctk.CTkEntry(model_frame, width=300, justify="center", fg_color="transparent")
        model_entry.pack(side="right", padx=(0, 20), pady=0)
        model_entry.insert(0, values[2])
        
        # Quantity
        qty_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        qty_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(qty_frame, text="Quantity:").pack(side="left", padx=(20, 10), pady=0)
        qty_entry = ctk.CTkEntry(qty_frame, width=300, justify="center", fg_color="transparent")
        qty_entry.pack(side="right", padx=(0, 20), pady=0)
        qty_entry.insert(0, values[3])
        
        # Price
        price_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        price_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(price_frame, text="Price (Ksh):").pack(side="left", padx=(20, 10), pady=0)
        price_entry = ctk.CTkEntry(price_frame, width=300, justify="center", fg_color="transparent")
        price_entry.pack(side="right", padx=(0, 20), pady=0)
        price_entry.insert(0, values[4].replace(',', ''))
        
        # Min Stock Level
        min_stock_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        min_stock_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(min_stock_frame, text="Min Stock Level:").pack(side="left", padx=(20, 10), pady=0)
        min_stock_entry = ctk.CTkEntry(min_stock_frame, width=300, justify="center", fg_color="transparent")
        min_stock_entry.pack(side="right", padx=(0, 20), pady=0)
        min_stock_entry.insert(0, values[6])
        
        def save_changes():
            try:
                # Get updated values
                name = name_entry.get().strip()
                model = model_entry.get().strip()
                quantity = int(qty_entry.get())
                price = float(price_entry.get().replace(',', ''))
                min_stock = int(min_stock_entry.get())
                
                # Update database
                self.db.execute_query(
                    '''UPDATE stock 
                       SET name = ?, model = ?, quantity = ?, price = ?, min_stock_level = ?, updated_at = ?
                       WHERE id = ?''',
                    (name, model, quantity, price, min_stock, datetime.now(), item_id)
                )
                
                messagebox.showinfo("Success", "Stock item updated successfully!")
                dialog.destroy()
                self.load_stock()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update item: {str(e)}")
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Save Changes",
            command=save_changes,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(side="left", padx=10)
    
    def export_stock(self):
        try:
            # Get all stock items
            query = '''
                SELECT name, model, quantity, price, cost_price, min_stock_level,
                       (quantity * price) as value, date,
                       CASE 
                           WHEN quantity = 0 THEN 'Out of Stock'
                           WHEN quantity <= min_stock_level THEN 'Low Stock'
                           ELSE 'In Stock'
                       END as status
                FROM stock
                ORDER BY name
            '''
            stock_items = self.db.fetch_all(query)
            
            if not stock_items:
                messagebox.showwarning("No Data", "No stock items to export!")
                return
            
            # Create CSV content
            import csv
            from datetime import datetime
            
            filename = f"stock_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Item Name', 'Model', 'Quantity', 'Price (Ksh)', 'Cost (Ksh)', 
                                'Min Stock Level', 'Value (Ksh)', 'Date', 'Status'])
                
                # Write data
                for item in stock_items:
                    writer.writerow(item)
            
            messagebox.showinfo("Export Successful", f"Stock data exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export stock: {str(e)}")
    
    def load_transactions(self):
        # Clear existing items
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        
        # Fetch transactions
        query = '''
            SELECT st.id, s.name, st.transaction_type, st.quantity, 
                   st.price, st.reference, 
                   strftime('%Y-%m-%d %H:%M', st.created_at) as date
            FROM stock_transactions st
            JOIN stock s ON st.stock_id = s.id
            ORDER BY st.created_at DESC
            LIMIT 50
        '''
        transactions = self.db.fetch_all(query)
        
        for trans in transactions:
            self.trans_tree.insert("", "end", values=trans)