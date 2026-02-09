import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class DebtsManagement:
    def __init__(self, parent_frame, db, accounting_service):
        self.parent_frame = parent_frame
        self.db = db
        self.accounting_service = accounting_service
        self.setup_ui()
        self.load_debts()
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top frame - Add new debt
        top_frame = ctk.CTkFrame(self.main_container, border_width=2, border_color="#68a2a6", fg_color="transparent")
        top_frame.pack(fill="both", padx=5, pady=(5, 0))
        
        ctk.CTkLabel(top_frame, text="Add New Debt", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Form
        form_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        form_frame.pack(padx=10, pady=10)
        
        # Row 1
        row1 = ctk.CTkFrame(form_frame)
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Customer Name:", width=120).pack(side="left", padx=5)
        self.cust_name_entry = ctk.CTkEntry(row1, width=250, justify="center", fg_color="transparent")
        self.cust_name_entry.pack(side="left", padx=5)
        
        self.phone_entry = ctk.CTkEntry(row1, width=200, justify="center", fg_color="transparent")
        self.phone_entry.pack(side="right", padx=5)
        ctk.CTkLabel(row1, text="Phone:", width=80).pack(side="right", padx=5)
        
        # Row 2
        row2 = ctk.CTkFrame(form_frame)
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="Amount ($):", width=120).pack(side="left", padx=5)
        self.amount_entry = ctk.CTkEntry(row2, width=250, justify="center", fg_color="transparent")
        self.amount_entry.pack(side="left", padx=5)
        
        date = datetime.now().strftime("%d/%m/%Y")
        self.due_date_entry = ctk.CTkEntry(row2, width=200, justify="center", fg_color="transparent")
        self.due_date_entry.insert(0, date)
        self.due_date_entry.pack(side="right", padx=5)
        ctk.CTkLabel(row2, text="Due Date:", width=80).pack(side="right", padx=5)
        
        # Row 3
        row3 = ctk.CTkFrame(form_frame)
        row3.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row3, text="Notes:", width=120).pack(side="left", padx=5)
        self.notes_entry = ctk.CTkEntry(row3, width=550, fg_color="transparent")
        self.notes_entry.pack(side="left", padx=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(pady=(20, 0))
        
        add_btn = ctk.CTkButton(
            btn_frame,
            text="Add Debt",
            command=self.add_debt,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        add_btn.pack(side="left", padx=10)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear",
            command=self.clear_form,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        clear_btn.pack(side="left", padx=10)
        
        # Separator
        ctk.CTkFrame(self.main_container, height=2, fg_color="gray").pack(fill="x", pady=20)
        
        # Debts list frame
        list_frame = ctk.CTkFrame(self.main_container)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Search Frame
        search_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=(0, 10), pady=5)

        # Search type combobox
        ctk.CTkLabel(search_frame, text="Search by:", width=80).pack(side="left", padx=0)
        self.search_type = ctk.CTkComboBox(
            search_frame, 
            width=120,
            values=["All", "Customer Name", "Phone", "Due Date", "Status", "Amount"],
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
        self.search_entry.bind("<Return>", lambda e: self.search_debts())

        # Search button
        search_btn = ctk.CTkButton(
            search_frame, 
            text="🔍 Search", 
            command=self.search_debts,
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
            command=self.export_debts,
            width=80,
            fg_color="#9b59b6",
            hover_color="#7c309b"
        )
        export_btn.pack(side="right", padx=0)
        
        # Table frame
        table_frame = ctk.CTkFrame(list_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create Treeview
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
        
        columns = ("ID", "Customer", "Phone", "Total", "Paid", "Balance", "Due Date", "Status", "Action")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        
        self.tree.column("Customer", width=150)
        self.tree.column("Phone", width=120)
        self.tree.column("Action", width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for payment
        self.tree.bind("<Double-1>", self.show_payment_dialog)
    
    def add_debt(self):
        try:
            customer = self.cust_name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            amount = float(self.amount_entry.get())
            due_date = self.due_date_entry.get().strip()
            notes = self.notes_entry.get().strip()
            
            if not customer:
                messagebox.showerror("Error", "Customer name is required!")
                return
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0!")
                return
            
            # Insert debt
            self.db.execute_query('''
                INSERT INTO debts (customer_name, phone, total_amount, balance, due_date, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer, phone, amount, amount, due_date, notes))
            
            messagebox.showinfo("Success", "Debt added successfully!")
            self.clear_form()
            self.load_debts()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add debt: {str(e)}")
    
    def clear_form(self):
        self.cust_name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.due_date_entry.delete(0, 'end')
        self.notes_entry.delete(0, 'end')
    
    def load_debts(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch debts
        query = '''
            SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                   due_date, status
            FROM debts
            ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
        '''
        debts = self.db.fetch_all(query)
        
        for debt in debts:
            debt_id = debt[0]
            # Convert debt tuple to list and add action column
            values = list(debt)
            values.append("Receive Payment")
            
            self.tree.insert("", "end", iid=debt_id, values=values)
            
            # Color code based on status
            status = debt[7] if len(debt) > 7 else ''
            if status == 'paid':
                self.tree.item(debt_id, tags=("paid",))
            elif status == 'partial':
                self.tree.item(debt_id, tags=("partial",))
            else:
                self.tree.item(debt_id, tags=("pending",))
        
        # Configure tag colors
        self.tree.tag_configure("paid", background="#2ecc71", foreground="white")
        self.tree.tag_configure("partial", background="#f39c12", foreground="white")
        self.tree.tag_configure("pending", background="#e74c3c", foreground="white")
    
    def search_debts(self):
        search_type = self.search_type.get()
        search_term = self.search_entry.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Build query based on search type
        if search_type == "All":
            if search_term:
                query = '''
                    SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                           due_date, status
                    FROM debts
                    WHERE customer_name LIKE ? OR phone LIKE ? OR due_date LIKE ? OR status LIKE ?
                    ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
                '''
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            else:
                # Show all debts
                query = '''
                    SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                           due_date, status
                    FROM debts
                    ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
                '''
                params = ()
        
        elif search_type == "Customer Name":
            query = '''
                SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                       due_date, status
                FROM debts
                WHERE customer_name LIKE ?
                ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Phone":
            query = '''
                SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                       due_date, status
                FROM debts
                WHERE phone LIKE ?
                ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Due Date":
            query = '''
                SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                       due_date, status
                FROM debts
                WHERE due_date LIKE ?
                ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
            '''
            params = (f"%{search_term}%",)
        
        elif search_type == "Status":
            # Map search term to status
            status_map = {
                'paid': 'paid',
                'pending': 'pending',
                'partial': 'partial',
                'unpaid': 'pending',
                'completed': 'paid',
                'partially': 'partial'
            }
            
            status_term = search_term.lower()
            if status_term in status_map:
                status = status_map[status_term]
            else:
                status = search_term  # Use as-is
            
            query = '''
                SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                       due_date, status
                FROM debts
                WHERE status = ?
                ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
            '''
            params = (status,)
        
        elif search_type == "Amount":
            try:
                # Try to parse amount
                amount = float(search_term)
                query = '''
                    SELECT id, customer_name, phone, total_amount, paid_amount, balance,
                           due_date, status
                    FROM debts
                    WHERE total_amount >= ? OR balance >= ?
                    ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
                '''
                params = (amount, amount)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for amount search!")
                self.load_debts()  # Reload all debts
                return
        
        try:
            # Execute query
            if params:
                debts = self.db.fetch_all(query, params)
            else:
                debts = self.db.fetch_all(query)
            
            # Display results
            if not debts:
                messagebox.showinfo("No Results", "No debts found matching your search criteria.")
                return
            
            # Add debts to treeview
            for debt in debts:
                debt_id = debt[0]
                # Convert debt tuple to list and add action column
                values = list(debt)
                values.append("Receive Payment")
                
                self.tree.insert("", "end", iid=debt_id, values=values)
                
                # Color code based on status
                status = debt[7] if len(debt) > 7 else ''
                if status == 'paid':
                    self.tree.item(debt_id, tags=("paid",))
                elif status == 'partial':
                    self.tree.item(debt_id, tags=("partial",))
                else:
                    self.tree.item(debt_id, tags=("pending",))
            
            # Show result count
            result_count = len(debts)
            if search_term or search_type != "All":
                search_info = f" ({result_count} debts found)"
                if search_term:
                    search_info = f" for '{search_term}'{search_info}"
                messagebox.showinfo("Search Results", f"Search completed{search_info}")
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search debts: {str(e)}")
            # Don't call load_debts() here as it might cause recursion issues
            # Just show error and leave tree empty
    
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.search_type.set("All")
        self.load_debts()
    
    def export_debts(self):
        try:
            # Get all debts
            query = '''
                SELECT customer_name, phone, total_amount, paid_amount, balance,
                       due_date, status, created_at
                FROM debts
                ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date
            '''
            debts = self.db.fetch_all(query)
            
            if not debts:
                messagebox.showwarning("No Data", "No debts to export!")
                return
            
            # Create CSV content
            import csv
            from datetime import datetime
            
            filename = f"debts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Customer Name', 'Phone', 'Total Amount ($)', 'Paid Amount ($)', 
                                'Balance ($)', 'Due Date', 'Status', 'Created Date'])
                
                # Write data
                for debt in debts:
                    writer.writerow(debt)
            
            messagebox.showinfo("Export Successful", f"Debts data exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export debts: {str(e)}")
    
    def show_payment_dialog(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_values = self.tree.item(selected_item[0], 'values')
        debt_id = item_values[0]
        customer = item_values[1]
        balance = float(item_values[5])
        
        if balance <= 0:
            messagebox.showinfo("Info", "This debt is already paid!")
            return
        
        # Create payment dialog
        dialog = ctk.CTkToplevel(self.parent_frame)
        dialog.title("Receive Payment")
        dialog.geometry("400x350")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"Customer: {customer}", font=("Arial", 14, "bold"), text_color="#3498db").pack(pady=5)
        ctk.CTkLabel(content, text=f"Outstanding Balance: Ksh {balance:,.2f}", text_color="#E4960F").pack(pady=(0, 10))
        
        payment_frame = ctk.CTkFrame(content, fg_color="transparent")
        payment_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(payment_frame, text="Payment Amount (Ksh):").pack(side="left", padx=20, pady=0)
        amount_entry = ctk.CTkEntry(payment_frame, justify="center")
        amount_entry.pack(side="right", padx=(10, 20), pady=0)
        amount_entry.insert(0, str(balance))
        
        method_frame = ctk.CTkFrame(content, fg_color="transparent")
        method_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(method_frame, text="Payment Method:").pack(side="left", padx=20, pady=0)
        payment_method = ctk.CTkComboBox(method_frame, values=["Cash", "Bank Transfer", "Mobile Payment", "Cheque"])
        payment_method.pack(side="right", padx=(10, 20), pady=0)
        payment_method.set("Cash")
        
        notes_frame = ctk.CTkFrame(content, fg_color="transparent")
        notes_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(notes_frame, text="Notes:").pack(side="left", padx=20, pady=0)
        notes_entry = ctk.CTkEntry(notes_frame, width=400)
        notes_entry.pack(side="left", padx=(10, 20), pady=0)
        
        def process_payment():
            try:
                payment_amount = float(amount_entry.get())
                if payment_amount <= 0:
                    messagebox.showerror("Error", "Payment amount must be greater than 0!")
                    return
                
                if payment_amount > balance:
                    messagebox.showerror("Error", "Payment amount cannot exceed balance!")
                    return
                
                # Update debt
                new_balance = balance - payment_amount
                new_paid = float(item_values[4]) + payment_amount
                new_status = 'paid' if new_balance <= 0 else 'partial'
                
                self.db.execute_query('''
                    UPDATE debts 
                    SET paid_amount = ?, balance = ?, status = ?, updated_at = ?
                    WHERE id = ?
                ''', (new_paid, new_balance, new_status, datetime.now().strftime("%d/%m/%Y"), debt_id))
                
                # Add payment record
                payment_id = self.db.execute_query('''
                    INSERT INTO debt_payments (debt_id, amount, payment_method, notes, payment_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (debt_id, payment_amount, payment_method.get(), notes_entry.get(), datetime.now().strftime("%d/%m/%Y")))
                
                # Record debt payment as accounting transaction
                payment_data = {
                    'debt_id': debt_id,
                    'payment_id': payment_id,
                    'amount': payment_amount,
                    'customer_name': customer,
                    'payment_date': datetime.now().strftime("%d/%m/%Y"),
                    'created_by': 1,  # Default to admin, you might want to pass actual user
                    'payment_method': payment_method.get()
                }
                self.accounting_service.record_debt_payment_transaction(payment_data)
                
                messagebox.showinfo("Success", "Payment recorded successfully!")
                dialog.destroy()
                self.load_debts()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process payment: {str(e)}")
        
        ctk.CTkButton(
            content,
            text="Record Payment",
            command=process_payment,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=40)