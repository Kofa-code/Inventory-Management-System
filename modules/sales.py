import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.CTkScrollableDropdown import *

class SalesManagement:
    def __init__(self, parent_frame, db, current_user, accounting_service):
        self.parent_frame = parent_frame
        self.db = db
        self.current_user = current_user
        self.accounting_service = accounting_service
        self.cart_items = []
        self.selected_stock_item = None  # Store the currently selected item
        self.sales_mode = False  # Flag to track if we're in sales search mode
        self.setup_ui()
        self.load_stock_items()
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Add items
        left_panel = ctk.CTkFrame(self.main_container, width=350, border_width=2, border_color="#68a2a6", fg_color="transparent")
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(left_panel, text="New Sale", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Customer info
        cust_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        cust_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(cust_frame, text="Customer Name:").pack(anchor="w", pady=2)
        self.customer_entry = ctk.CTkEntry(cust_frame, justify="center", fg_color="transparent")
        self.customer_entry.pack(fill="x", pady=2)
        
        ctk.CTkLabel(cust_frame, text="Payment Method:").pack(anchor="w", pady=2)
        self.payment_method = ctk.CTkComboBox(cust_frame, values=["Cash", "Credit Card", "Mobile Payment", "Debt"])
        self.payment_method.pack(fill="x", pady=2)
        self.payment_method.set("Cash")
        
        # Item selection
        item_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        item_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(item_frame, text="Select Item:").pack(anchor="w", pady=2)
        
        # Search entry for items with scrollable dropdown
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(item_frame, textvariable=self.search_var, fg_color="transparent",
                                         placeholder_text="Search or select item...", justify="center")
        self.search_entry.pack(fill="x", pady=2)
        
        # Quantity
        qty_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        qty_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(qty_frame, text="Quantity:").pack(side="left", padx=5)
        self.qty_spinbox = ctk.CTkEntry(qty_frame, width=100, justify="center", fg_color="transparent")
        self.qty_spinbox.insert(0, "1")
        self.qty_spinbox.pack(side="left", padx=(5, 30))
        
        # Add to cart button
        add_btn = ctk.CTkButton(
            qty_frame,
            text="Add to Cart",
            command=self.add_to_cart,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        add_btn.pack(side="left", pady=10)
        
        # Cart summary
        summary_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        self.total_items_label = ctk.CTkLabel(summary_frame, text="Total Items: 0", font=("Arial", 12))
        self.total_items_label.pack(pady=2)
        
        self.total_amount_label = ctk.CTkLabel(summary_frame, text="Total Amount: Ksh 0.00", font=("Arial", 14, "bold"))
        self.total_amount_label.pack(pady=2)

        # Paid amount entry
        paid_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        paid_frame.pack(pady=(20, 10))

        ctk.CTkLabel(paid_frame, text="Amount Paid:", font=("Arial", 12)).pack(side="left", padx=(10, 10), pady=2)
        
        self.paid_entry = ctk.CTkEntry(paid_frame, justify="center", fg_color="transparent")
        self.paid_entry.pack(side="left")
        self.paid_entry.insert(0, "0.00")
        
        # Update paid button
        update_paid_btn = ctk.CTkButton(
            paid_frame,
            text="Update Paid",
            command=self.update_paid_amount,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            width=100
        )
        update_paid_btn.pack(side="left", padx=(10, 0))
        
        # Process sale button
        process_btn = ctk.CTkButton(
            left_panel,
            text="Process Sale",
            command=self.process_sale,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=40,
            font=("Arial", 14, "bold")
        )
        process_btn.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Right panel - Cart items / Sales search results
        self.right_panel = ctk.CTkFrame(self.main_container)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Search Frame
        search_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        search_frame.pack(pady=(20, 20))

        # Search entry
        self.sales_search_entry = ctk.CTkEntry(
            search_frame, 
            width=250, 
            placeholder_text="Search by customer name...", 
            justify="center",
            fg_color="transparent"
        )
        self.sales_search_entry.pack(side="left", padx=(10, 10), pady=0)

        # Search button
        self.search_btn = ctk.CTkButton(
            search_frame, 
            text="🔍 Search Sales",
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.search_sales_by_customer
        )
        self.search_btn.pack(side="left", padx=0)

        # Back to cart button (hidden initially)
        self.back_to_cart_btn = ctk.CTkButton(
            search_frame,
            text="⬅ Back to Cart",
            width=120,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.show_cart_view,
            state="disabled"
        )
        self.back_to_cart_btn.pack(side="left", padx=(10, 0))

        # Cart/Sales table container
        self.table_container = ctk.CTkFrame(self.right_panel)
        self.table_container.pack(fill="both", expand=True, padx=(5, 5), pady=0)
        
        # Create Treeview style
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
        
        # Create cart tree (initially visible)
        self.create_cart_tree()
        
        # Create sales tree (initially hidden)
        self.create_sales_tree()
        
        # Initially show cart tree
        self.show_cart_view()
    
    def create_cart_tree(self):
        """Create the cart items treeview with paid and balance columns"""
        columns = ("Item", "Model", "Quantity", "Price", "Total", "Paid", "Balance")
        self.cart_tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=15)
        
        column_widths = {
            "Item": 120,
            "Model": 100,
            "Quantity": 70,
            "Price": 80,
            "Total": 80,
            "Paid": 80,
            "Balance": 80
        }
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=column_widths.get(col, 80), anchor="center")
        
        self.cart_scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=self.cart_scrollbar.set)
        
        # Bind double-click to remove item
        self.cart_tree.bind("<Double-1>", self.remove_cart_item)
    
    def create_sales_tree(self):
        """Create the sales search results treeview"""
        columns = ("Date", "Customer", "Payment", "Total", "Paid", "Balance", "Status")
        self.sales_tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=15)
        
        column_widths = {
            "Date": 80,
            "Customer": 100,
            "Payment": 100,
            "Total": 80,
            "Paid": 80,
            "Balance": 80,
            "Status": 80
        }
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        self.sales_scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=self.sales_scrollbar.set)
    
    def show_cart_view(self):
        """Show the cart tree and hide the sales tree"""
        self.sales_mode = False
        
        # Hide sales tree
        self.sales_tree.pack_forget()
        self.sales_scrollbar.pack_forget()
        
        # Show cart tree
        self.cart_tree.pack(side="left", fill="both", expand=True)
        self.cart_scrollbar.pack(side="right", fill="y")
        
        # Update buttons
        self.search_btn.configure(state="normal")
        self.back_to_cart_btn.configure(state="disabled")
        
        # Update placeholder text
        self.sales_search_entry.configure(placeholder_text="Search by customer name...")
    
    def show_sales_view(self):
        """Show the sales tree and hide the cart tree"""
        self.sales_mode = True
        
        # Hide cart tree
        self.cart_tree.pack_forget()
        self.cart_scrollbar.pack_forget()
        
        # Show sales tree
        self.sales_tree.pack(side="left", fill="both", expand=True)
        self.sales_scrollbar.pack(side="right", fill="y")
        
        # Update buttons
        self.search_btn.configure(state="normal")
        self.back_to_cart_btn.configure(state="normal")
        
        # Update placeholder text
        self.sales_search_entry.configure(placeholder_text="Search by customer name...")
    
    def load_stock_items(self):
        query = '''
            SELECT id, name, model, price, quantity 
            FROM stock 
            WHERE quantity > 0
            ORDER BY name
        '''
        items = self.db.fetch_all(query)
        
        self.stock_items = items
        
        # Create scrollable dropdown for search entry
        dropdown_values = []
        for item in items:
            display_text = f"{item[1]} ({item[2]}) - Ksh {item[3]:.2f} - Stock: {item[4]}"
            dropdown_values.append(display_text)
        
        # Create the scrollable dropdown
        self.item_dropdown = CTkScrollableDropdown(
            attach=self.search_entry,
            values=dropdown_values,
            command=self.on_item_selected,
            autocomplete=True,
            height=200,
            justify="left",
            resize=True,
            frame_border_width=1,
            frame_border_color="#555555",
            button_color="#3a3a3a",
            hover_color="#4a4a4a",
            text_color="white",
            alpha=0.98,
            double_click=True
        )
        
        # Bind Enter key to add item
        self.search_entry.bind('<Return>', lambda e: self.add_to_cart())
        
        # Bind focus event to show dropdown
        self.search_entry.bind('<FocusIn>', lambda e: self.show_dropdown())
    
    def show_dropdown(self):
        """Show the dropdown when search entry gets focus"""
        if self.item_dropdown and hasattr(self.item_dropdown, '_withdraw'):
            # If dropdown is hidden, show it
            if not self.item_dropdown.winfo_viewable():
                self.item_dropdown._iconify()
    
    def on_item_selected(self, selected_text):
        """Handle item selection from dropdown"""
        if selected_text:
            # Find the corresponding stock item
            for item in self.stock_items:
                display_text = f"{item[1]} ({item[2]}) - Ksh {item[3]:.2f} - Stock: {item[4]}"
                if display_text == selected_text:
                    self.selected_stock_item = item
                    # Auto-focus quantity field
                    self.qty_spinbox.focus()
                    self.qty_spinbox.select_range(0, 'end')
                    break
            self.search_entry.delete(0, 'end')
            self.search_entry.insert(0, selected_text.split(" - ")[0])  # Just show item name
    
    def search_sales_by_customer(self):
        """Search sales by customer name"""
        customer_name = self.sales_search_entry.get().strip()
        
        if not customer_name:
            messagebox.showwarning("Warning", "Please enter a customer name to search!")
            return
        
        try:
            # First, switch to sales view
            self.show_sales_view()
            
            # Clear existing items in sales tree
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
            
            # Query to search sales by customer name
            query = '''
                SELECT 
                    invoice_number,
                    date, 
                    customer_name,
                    payment_method,
                    total_amount,
                    paid_amount,
                    balance,
                    CASE 
                        WHEN balance = 0 THEN 'Paid'
                        WHEN balance > 0 AND paid_amount > 0 THEN 'Partial'
                        WHEN balance = total_amount THEN 'Unpaid'
                        ELSE 'Pending'
                    END as status
                FROM sales 
                WHERE customer_name LIKE ?
                ORDER BY date DESC
            '''
            
            # Use parameterized query with wildcards for partial matching
            results = self.db.fetch_all(query, (f'%{customer_name}%',))
            
            if not results:
                messagebox.showinfo("No Results", f"No sales found for customer: {customer_name}")
                return
            
            # Add results to sales tree
            for sale in results:
                self.sales_tree.insert("", "end", values=(
                    sale[1],  # Date
                    sale[2],  # Customer
                    sale[3],  # Payment Method
                    f"Ksh {sale[4]:.2f}",  # Total
                    f"Ksh {sale[5]:.2f}",  # Paid
                    f"Ksh {sale[6]:.2f}",  # Balance
                    sale[7]   # Status
                ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search sales: {str(e)}")
            # If there's an error, go back to cart view
            self.show_cart_view()
    
    def add_to_cart(self):
        try:
            # Check if we have a selected item from dropdown
            if not self.selected_stock_item and self.search_entry.get():
                # Try to find item by search text
                search_text = self.search_entry.get().lower()
                for item in self.stock_items:
                    display_text = f"{item[1]} ({item[2]}) - Ksh {item[3]:.2f} - Stock: {item[4]}"
                    if (search_text in item[1].lower() or 
                        search_text in item[2].lower() or
                        search_text in display_text.lower()):
                        self.selected_stock_item = item
                        break
            
            if not self.selected_stock_item:
                messagebox.showwarning("Warning", "Please select an item from the dropdown!")
                return
            
            # Get quantity
            quantity = int(self.qty_spinbox.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be greater than 0!")
                return
            
            # Check stock availability
            if quantity > self.selected_stock_item[4]:
                messagebox.showerror("Error", f"Insufficient stock! Available: {self.selected_stock_item[4]}")
                return
            
            # Get paid amount for this item (default 0)
            paid_amount = 0.0
            try:
                paid_amount = float(self.paid_entry.get())
                if paid_amount < 0:
                    paid_amount = 0.0
            except ValueError:
                paid_amount = 0.0
            
            # Calculate item total and balance
            item_total = quantity * self.selected_stock_item[3]
            item_balance = max(0, item_total - paid_amount)
            
            # Check if item already in cart
            for i, item in enumerate(self.cart_items):
                if item['id'] == self.selected_stock_item[0]:
                    # Update quantity and amounts
                    new_qty = item['quantity'] + quantity
                    if new_qty > self.selected_stock_item[4]:
                        messagebox.showerror("Error", f"Insufficient stock! Available: {self.selected_stock_item[4]}")
                        return
                    
                    self.cart_items[i]['quantity'] = new_qty
                    self.cart_items[i]['total'] = new_qty * self.selected_stock_item[3]
                    self.cart_items[i]['paid'] = paid_amount
                    self.cart_items[i]['balance'] = max(0, self.cart_items[i]['total'] - paid_amount)
                    self.update_cart_display()
                    
                    # Clear selection and reset
                    self.selected_stock_item = None
                    self.search_entry.delete(0, 'end')
                    self.qty_spinbox.delete(0, 'end')
                    self.qty_spinbox.insert(0, "1")
                    self.paid_entry.delete(0, 'end')
                    self.paid_entry.insert(0, "0.00")
                    return
            
            # Add new item to cart
            cart_item = {
                'id': self.selected_stock_item[0],
                'name': self.selected_stock_item[1],
                'model': self.selected_stock_item[2],
                'price': self.selected_stock_item[3],
                'quantity': quantity,
                'total': item_total,
                'paid': paid_amount,
                'balance': item_balance
            }
            self.cart_items.append(cart_item)
            
            self.update_cart_display()
            
            # Clear selection and reset
            self.selected_stock_item = None
            self.search_entry.delete(0, 'end')
            self.qty_spinbox.delete(0, 'end')
            self.qty_spinbox.insert(0, "1")
            self.paid_entry.delete(0, 'end')
            self.paid_entry.insert(0, "0.00")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Please enter valid values! Error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    def update_paid_amount(self):
        """Update paid amount for the entire sale"""
        try:
            # Get total amount
            total_amount = sum(item['total'] for item in self.cart_items)
            
            # Get paid amount from entry
            paid_amount = float(self.paid_entry.get())
            
            if paid_amount < 0:
                messagebox.showwarning("Warning", "Paid amount cannot be negative!")
                return
            
            if paid_amount > total_amount:
                messagebox.showwarning("Warning", "Paid amount cannot exceed total amount!")
                paid_amount = total_amount
                self.paid_entry.delete(0, 'end')
                self.paid_entry.insert(0, f"{paid_amount:.2f}")
            
            # Distribute paid amount proportionally among items
            if self.cart_items and total_amount > 0:
                remaining_paid = paid_amount
                for i, item in enumerate(self.cart_items):
                    # Calculate proportional paid amount for this item
                    item_paid = (item['total'] / total_amount) * paid_amount
                    self.cart_items[i]['paid'] = item_paid
                    self.cart_items[i]['balance'] = max(0, item['total'] - item_paid)
            
            self.update_cart_display()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid paid amount!")
    
    def update_cart_display(self):
        # Clear tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items to tree
        total_items = 0
        total_amount = 0.0
        total_paid = 0.0
        total_balance = 0.0
        
        for item in self.cart_items:
            total_items += item['quantity']
            total_amount += item['total']
            total_paid += item['paid']
            total_balance += item['balance']
            
            self.cart_tree.insert("", "end", values=(
                item['name'],
                item['model'],
                item['quantity'],
                f"Ksh {item['price']:.2f}",
                f"Ksh {item['total']:.2f}",
                f"Ksh {item['paid']:.2f}",
                f"Ksh {item['balance']:.2f}"
            ))
        
        # Update labels
        self.total_items_label.configure(text=f"Total Items: {total_items}")
        self.total_amount_label.configure(text=f"Total Amount: Ksh {total_amount:.2f}")
        
        # Update paid entry with total paid
        self.paid_entry.delete(0, 'end')
        self.paid_entry.insert(0, f"{total_paid:.2f}")
    
    def remove_cart_item(self, event):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            return
        
        item_index = self.cart_tree.index(selected_item[0])
        self.cart_items.pop(item_index)
        self.update_cart_display()
    
    def process_sale(self):
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        date = datetime.now().strftime('%d/%m/%Y')
        
        customer_name = self.customer_entry.get().strip()
        if not customer_name:
            customer_name = "Walk-in Customer"
        
        payment_method = self.payment_method.get()
        
        # Calculate totals
        total_amount = sum(item['total'] for item in self.cart_items)
        paid_amount = sum(item['paid'] for item in self.cart_items)
        balance = total_amount - paid_amount
        
        try:
            # Generate invoice number
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Start transaction
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Insert sale record
            cursor.execute('''
                INSERT INTO sales (invoice_number, date, customer_name, total_amount, paid_amount, 
                                 balance, payment_method, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, date, customer_name, total_amount, paid_amount, 
                  balance, payment_method, self.current_user['id']))
            
            sale_id = cursor.lastrowid
            
            # Insert sale items and update stock
            for item in self.cart_items:
                # Insert sale item
                cursor.execute('''
                    INSERT INTO sale_items (sale_id, stock_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (sale_id, item['id'], item['quantity'], item['price'], item['total']))
                
                # Update stock quantity
                cursor.execute('''
                    UPDATE stock SET quantity = quantity - ? WHERE id = ?
                ''', (item['quantity'], item['id']))
                
                # Add stock transaction
                cursor.execute('''
                    INSERT INTO stock_transactions (stock_id, transaction_type, quantity, price, reference)
                    VALUES (?, ?, ?, ?, ?)
                ''', (item['id'], 'OUT', item['quantity'], item['price'], invoice_number))
            
            # If there's a balance, create debt record
            if balance > 0:
                cursor.execute('''
                    INSERT INTO debts (customer_name, total_amount, paid_amount, balance, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (customer_name, total_amount, paid_amount, balance, 'pending'))
            
            conn.commit()
            
            # Now record the accounting transaction (after successful commit)
            sale_data = {
                'sale_id': sale_id,
                'total_amount': total_amount,
                'paid_amount': paid_amount,
                'balance': balance,
                'customer_name': customer_name,
                'invoice_number': invoice_number,
                'sale_date': datetime.now().strftime("%d/%m/%Y"),
                'created_by': self.current_user['id']
            }
            self.accounting_service.record_sale_transaction(sale_data)
            
            conn.close()
            
            messagebox.showinfo("Success", 
                               f"Sale processed successfully!\n"
                               f"Invoice: {invoice_number}\n"
                               f"Total: Ksh {total_amount:.2f}\n"
                               f"Paid: Ksh {paid_amount:.2f}\n"
                               f"Balance: Ksh {balance:.2f}")
            
            # Clear cart and form
            self.cart_items = []
            self.update_cart_display()
            self.customer_entry.delete(0, 'end')
            self.search_entry.delete(0, 'end')
            self.payment_method.set("Cash")
            self.qty_spinbox.delete(0, 'end')
            self.qty_spinbox.insert(0, "1")
            self.paid_entry.delete(0, 'end')
            self.paid_entry.insert(0, "0.00")
            self.selected_stock_item = None
            
            # Reload stock items to update availability
            self.load_stock_items()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process sale: {str(e)}")