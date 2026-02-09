import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class AccountingManagement:
    def __init__(self, parent_frame, db, current_user, accounting_service):
        self.parent_frame = parent_frame
        self.db = db
        self.current_user = current_user
        self.accounting_service = accounting_service
        self.setup_ui()
        self.load_transactions()
        self.update_summary()
        self.update_charts()
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Summary frame
        summary_frame = ctk.CTkFrame(self.main_container)
        summary_frame.pack(fill="x", padx=5, pady=5)
        
        # Summary labels
        self.income_label = ctk.CTkLabel(
            summary_frame, 
            height=50,
            text="Total Income: Ksh 0.00",
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            corner_radius=5,
            text_color="white"
        )
        self.income_label.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        self.expense_label = ctk.CTkLabel(
            summary_frame,
            height=50,
            text="Total Expenses: Ksh 0.00",
            font=("Arial", 14, "bold"),
            fg_color="#e74c3c",
            corner_radius=5,
            text_color="white"
        )
        self.expense_label.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        self.balance_label = ctk.CTkLabel(
            summary_frame,
            height=50,
            text="Net Balance: Ksh 0.00",
            font=("Arial", 14, "bold"),
            fg_color="#3498db",
            corner_radius=5,
            text_color="white"
        )
        self.balance_label.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        self.cash_flow_label = ctk.CTkLabel(
            summary_frame,
            height=50,
            text="Cash Flow: Ksh 0.00",
            font=("Arial", 14, "bold"),
            fg_color="#9b59b6",
            corner_radius=5,
            text_color="white"
        )
        self.cash_flow_label.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Tabs for different views
        self.tabview = ctk.CTkTabview(self.main_container, border_width=2, border_color="#68a2a6")
        self.tabview.pack(fill="both", expand=True, padx=5, pady=10)
        
        # Create tabs
        self.tabview.add("Add Transaction")
        self.tabview.add("Transactions")
        self.tabview.add("Reports")
        self.tabview.add("Auto Transactions")
        
        # Tab 1: Add Transaction
        self.setup_add_transaction_tab()
        
        # Tab 2: Transactions List
        self.setup_transactions_tab()
        
        # Tab 3: Reports
        self.setup_reports_tab()
        
        # Tab 4: Auto Transactions
        self.setup_auto_transactions_tab()
    
    def setup_add_transaction_tab(self):
        tab = self.tabview.tab("Add Transaction")
        
        add_frame = ctk.CTkFrame(tab)
        add_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(add_frame, text="Add Manual Transaction", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Form
        form_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        form_frame.pack(padx=20, pady=10)
        
        # Row 1
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Transaction Type:", width=150).pack(side="left", padx=5)
        self.type_combo = ctk.CTkComboBox(row1, values=["Income", "Expense"], width=200)
        self.type_combo.pack(side="left", padx=5)
        self.type_combo.set("Income")
        self.type_combo.configure(command=self.on_type_change)
        
        ctk.CTkLabel(row1, text="Category:", width=80).pack(side="left", padx=5)
        self.category_combo = ctk.CTkComboBox(row1, width=200)
        self.category_combo.pack(side="left", padx=5)
        self.update_categories()
        
        # Row 2
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="Amount (Ksh):", width=150).pack(side="left", padx=5)
        self.amount_entry = ctk.CTkEntry(row2, width=200, justify="center")
        self.amount_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Date:", width=80).pack(side="left", padx=5)
        self.date_entry = ctk.CTkEntry(row2, width=200, justify="center", placeholder_text="DD/MM/YYYY")
        self.date_entry.pack(side="left", padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Row 3
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row3, text="Description:", width=150).pack(side="left", padx=5)
        self.desc_entry = ctk.CTkEntry(row3, width=200)
        self.desc_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row3, text="Reference No:", width=80).pack(side="left", padx=5)
        self.ref_entry = ctk.CTkEntry(row3, width=200, justify="center")
        self.ref_entry.pack(side="left", padx=5)
        self.ref_entry.insert(0, f"MAN-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=40)
        
        add_btn = ctk.CTkButton(
            btn_frame,
            text="Add Transaction",
            command=self.add_transaction,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150
        )
        add_btn.pack(side="left", padx=20)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear Form",
            command=self.clear_form,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            width=150
        )
        clear_btn.pack(side="left", padx=20)
    
    def setup_transactions_tab(self):
        tab = self.tabview.tab("Transactions")
        
        # Filter frame
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(filter_frame, text="Filter by:",).pack(side="left", padx=(0, 10))
        
        self.filter_type = ctk.CTkComboBox(
            filter_frame, 
            values=["All", "Income", "Expense", "Sales", "Debt Payments", "Bad Debts"],
            width=150,
            state="readonly"
        )
        self.filter_type.set("All")
        self.filter_type.pack(side="left", padx=5)
        
        date = datetime.now().strftime("%d/%m/%Y")

        ctk.CTkLabel(filter_frame, text="Date Range:", width=80).pack(side="left", padx=5)
        self.start_date_entry = ctk.CTkEntry(filter_frame, width=120, placeholder_text=date)
        self.start_date_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="to", width=20).pack(side="left")
        self.end_date_entry = ctk.CTkEntry(filter_frame, width=120, placeholder_text=date)
        self.end_date_entry.pack(side="left", padx=5)
        
        filter_btn = ctk.CTkButton(
            filter_frame,
            text="Apply Filter",
            command=self.filter_transactions,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=100
        )
        filter_btn.pack(side="left", padx=10)
        
        reset_btn = ctk.CTkButton(
            filter_frame,
            text="Reset",
            command=self.reset_filter,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            width=80
        )
        reset_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            filter_frame,
            text="Export",
            command=self.export_transactions,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            width=80
        )
        export_btn.pack(side="right", padx=0)
        
        # Table frame
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
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
        
        columns = ("ID", "Date", "Type", "Category", "Amount", "Description", "Reference", "Auto")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        col_widths = {
            "ID": 50,
            "Date": 100,
            "Type": 80,
            "Category": 120,
            "Amount": 100,
            "Description": 200,
            "Reference": 150,
            "Auto": 80
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for editing
        self.tree.bind("<Double-1>", self.edit_transaction)
    
    def setup_reports_tab(self):
        tab = self.tabview.tab("Reports")
        
        # Report options frame
        options_frame = ctk.CTkFrame(tab, fg_color="transparent")
        options_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(options_frame, text="Report Type:").pack(side="left", padx=(0, 10))
        
        self.report_type = ctk.CTkComboBox(
            options_frame,
            values=["Income Statement", "Expense Report", "Category Summary", "Monthly Summary"],
            width=200,
            state="readonly"
        )
        self.report_type.set("Income Statement")
        self.report_type.pack(side="left", padx=5)
        
        ctk.CTkLabel(options_frame, text="Month:", width=60).pack(side="left", padx=5)
        
        self.report_month = ctk.CTkComboBox(
            options_frame,
            values=["All Months"] + [f"{i:02d}/{datetime.now().year}" for i in range(1, 13)],
            width=120,
            state="readonly"
        )
        self.report_month.set("All Months")
        self.report_month.pack(side="left", padx=5)
        
        generate_btn = ctk.CTkButton(
            options_frame,
            text="Generate Report",
            command=self.generate_report,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=120
        )
        generate_btn.pack(side="left", padx=20)
        
        # Report display frame
        report_frame = ctk.CTkFrame(tab)
        report_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create Treeview for report
        self.report_tree = ttk.Treeview(report_frame, show="headings", height=15)
        
        report_scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=report_scrollbar.set)
        
        self.report_tree.pack(side="left", fill="both", expand=True)
        report_scrollbar.pack(side="right", fill="y")
    
    def setup_auto_transactions_tab(self):
        tab = self.tabview.tab("Auto Transactions")
        
        info_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=20, pady=0)
        
        ctk.CTkLabel(
            info_frame,
            text="Automatic Transaction Recording",
            font=("Arial", 18, "bold"),
            text_color="#3498db"
        ).pack(pady=10)
        
        # Info box
        info_text = """This system automatically records the following transactions:

1. SALES TRANSACTIONS (Income):
   • When a sale is processed, it's automatically recorded as income
   • Category: "Sales Revenue"
   • Amount: Total sale amount

2. DEBT PAYMENTS (Income):
   • When a customer pays a debt, it's recorded as income
   • Category: "Debt Collections"
   • Amount: Payment amount

3. BAD DEBTS (Expense):
   • When you mark a debt as "bad debt" (uncollectible)
   • Category: "Bad Debt Expense"
   • Amount: Uncollectible amount

4. DEBT CREATION:
   • When a sale is made on credit (debt)
   • No immediate transaction recorded
   • Becomes income when paid, expense if bad debt

All automatic transactions are marked with "Auto" flag in the transactions list.
You can also add manual transactions in the "Add Transaction" tab."""
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 12),
            justify="left",
            wraplength=600
        )
        info_label.pack(pady=20, fill="both", expand=True)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 10))
        
        auto_stats = self.get_auto_transaction_stats()
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Auto Income: Ksh {auto_stats['auto_income']:,.2f}",
            font=("Arial", 14),
            fg_color="#2ecc71",
            corner_radius=8,
            text_color="white"
        ).pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Auto Expenses: Ksh {auto_stats['auto_expense']:,.2f}",
            font=("Arial", 14),
            fg_color="#e74c3c",
            corner_radius=8,
            text_color="white"
        ).pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Total Auto: {auto_stats['total_auto']} transactions",
            font=("Arial", 14),
            fg_color="#3498db",
            corner_radius=8,
            text_color="white"
        ).pack(side="left", padx=10, pady=10, fill="x", expand=True)
    
    def on_type_change(self, choice):
        self.update_categories()
    
    def update_categories(self):
        trans_type = self.type_combo.get().lower()
        
        if trans_type == "income":
            categories = [
                "Sales Revenue",
                "Debt Collections",
                "Other Income",
                "Service Income",
                "Rental Income",
                "Interest Income"
            ]
        else:  # expense
            categories = [
                "Cost of Goods Sold",
                "Bad Debt Expense",
                "Rent Expense",
                "Utilities",
                "Salaries",
                "Marketing",
                "Repairs",
                "Other Expenses"
            ]
        
        self.category_combo.configure(values=categories)
        if categories:
            self.category_combo.set(categories[0])
    
    def add_transaction(self):
        try:
            trans_type = self.type_combo.get().lower()
            category = self.category_combo.get().strip()
            amount = float(self.amount_entry.get().replace(',', ''))
            trans_date = self.date_entry.get().strip()
            description = self.desc_entry.get().strip()
            reference = self.ref_entry.get().strip()
            
            if not category:
                messagebox.showerror("Error", "Category is required!")
                return
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0!")
                return
            
            # Validate date format (DD/MM/YYYY)
            try:
                day, month, year = map(int, trans_date.split('/'))
                datetime(year, month, day)
            except:
                messagebox.showerror("Error", "Invalid date format! Use DD/MM/YYYY")
                return
            
            # Insert transaction (manual)
            self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (trans_type, category, amount, description, reference, 
                  trans_date, self.current_user['id'], 0))
            
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.clear_form()
            self.load_transactions()
            self.update_summary()
            self.update_charts()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {str(e)}")
    
    # ===== AUTOMATIC TRANSACTION METHODS =====
    
    def record_sale_transaction(self, sale_data):
        """Automatically record a sale as income"""
        try:
            self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_sale_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('income', 'Sales Revenue', sale_data['total_amount'], 
                  f"Sale to {sale_data['customer_name']}", sale_data['invoice_number'],
                  sale_data['sale_date'], sale_data['created_by'], 1, sale_data['sale_id']))
            
            # Update summary
            self.update_summary()
            return True
        except Exception as e:
            print(f"Error recording sale transaction: {e}")
            return False
    
    def record_debt_payment_transaction(self, payment_data):
        """Automatically record a debt payment as income"""
        try:
            self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_debt_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('income', 'Debt Collections', payment_data['amount'], 
                  f"Payment from {payment_data['customer_name']}", f"PAY-{payment_data['payment_id']}",
                  payment_data['payment_date'], payment_data['created_by'], 1, payment_data['debt_id']))
            
            # Update summary
            self.update_summary()
            return True
        except Exception as e:
            print(f"Error recording debt payment transaction: {e}")
            return False
    
    def record_bad_debt_transaction(self, debt_data):
        """Record bad debt as expense when a debt is written off"""
        try:
            self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_debt_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('expense', 'Bad Debt Expense', debt_data['balance'], 
                  f"Bad debt write-off for {debt_data['customer_name']}", f"BAD-{debt_data['debt_id']}",
                  datetime.now().strftime("%d/%m/%Y"), debt_data['created_by'], 1, debt_data['debt_id']))
            
            # Update summary
            self.update_summary()
            return True
        except Exception as e:
            print(f"Error recording bad debt transaction: {e}")
            return False
    
    def record_purchase_transaction(self, purchase_data):
        """Record stock purchase as expense (Cost of Goods Sold)"""
        try:
            self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_stock_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('expense', 'Cost of Goods Sold', purchase_data['total_cost'], 
                  f"Stock purchase: {purchase_data['item_name']}", purchase_data['reference'],
                  purchase_data['date'], purchase_data['created_by'], 1, purchase_data['stock_id']))
            
            # Update summary
            self.update_summary()
            return True
        except Exception as e:
            print(f"Error recording purchase transaction: {e}")
            return False
    
    # ===== TRANSACTION MANAGEMENT METHODS =====
    
    def clear_form(self):
        self.amount_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.desc_entry.delete(0, 'end')
        self.ref_entry.delete(0, 'end')
        self.ref_entry.insert(0, f"MAN-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    def load_transactions(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch all transactions
        query = '''
            SELECT id, 
                   transaction_date as date,
                   transaction_type,
                   category,
                   amount,
                   description,
                   reference,
                   CASE WHEN is_auto = 1 THEN 'Yes' ELSE 'No' END as is_auto
            FROM accounting_transactions
            ORDER BY transaction_date DESC, id DESC
            LIMIT 200
        '''
        transactions = self.db.fetch_all(query)
        
        for trans in transactions:
            self.tree.insert("", "end", values=trans)
    
    def filter_transactions(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filter_type = self.filter_type.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        # Build query based on filters
        query_parts = []
        params = []
        
        if filter_type != "All":
            if filter_type == "Sales":
                query_parts.append("category = ?")
                params.append("Sales Revenue")
            elif filter_type == "Debt Payments":
                query_parts.append("category = ?")
                params.append("Debt Collections")
            elif filter_type == "Bad Debts":
                query_parts.append("category = ?")
                params.append("Bad Debt Expense")
            else:
                query_parts.append("transaction_type = ?")
                params.append(filter_type.lower())
        
        if start_date:
            try:
                # Convert DD/MM/YYYY to YYYY-MM-DD for SQLite
                day, month, year = map(int, start_date.split('/'))
                sql_date = f"{year:04d}-{month:02d}-{day:02d}"
                query_parts.append("DATE(transaction_date) >= DATE(?)")
                params.append(sql_date)
            except:
                messagebox.showerror("Error", "Invalid start date format! Use DD/MM/YYYY")
                return
        
        if end_date:
            try:
                # Convert DD/MM/YYYY to YYYY-MM-DD for SQLite
                day, month, year = map(int, end_date.split('/'))
                sql_date = f"{year:04d}-{month:02d}-{day:02d}"
                query_parts.append("DATE(transaction_date) <= DATE(?)")
                params.append(sql_date)
            except:
                messagebox.showerror("Error", "Invalid end date format! Use DD/MM/YYYY")
                return
        
        # Build final query
        query = '''
            SELECT id, transaction_date, transaction_type, category, amount, 
                   description, reference,
                   CASE WHEN is_auto = 1 THEN 'Yes' ELSE 'No' END as is_auto
            FROM accounting_transactions
        '''
        
        if query_parts:
            query += " WHERE " + " AND ".join(query_parts)
        
        query += " ORDER BY transaction_date DESC, id DESC"
        
        try:
            transactions = self.db.fetch_all(query, params)
            
            for trans in transactions:
                self.tree.insert("", "end", values=trans)
            
            messagebox.showinfo("Filter Applied", f"Found {len(transactions)} transactions")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter transactions: {str(e)}")
    
    def reset_filter(self):
        self.filter_type.set("All")
        self.start_date_entry.delete(0, 'end')
        self.end_date_entry.delete(0, 'end')
        self.load_transactions()
    
    def edit_transaction(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_values = self.tree.item(selected_item[0], 'values')
        
        # Check if it's an auto transaction
        if item_values[7] == "Yes":
            messagebox.showwarning("Warning", "Auto transactions cannot be edited manually!")
            return
        
        # Create edit dialog
        self.show_edit_dialog(item_values)
    
    def show_edit_dialog(self, values):
        dialog = ctk.CTkToplevel(self.parent_frame)
        dialog.title("Edit Transaction")
        dialog.geometry("500x500")
        dialog.transient(self.parent_frame)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content frame (similar to stock edit)
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=f"Edit Transaction (ID: {values[0]})", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Form fields (aligned like stock edit)
        form_frame = ctk.CTkFrame(content, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Transaction Type
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(type_frame, text="Transaction Type:").pack(side="left", padx=(20, 10), pady=0)
        type_combo = ctk.CTkComboBox(type_frame, values=["Income", "Expense"], width=300)
        type_combo.pack(side="right", padx=(0, 20), pady=0)
        type_combo.set(values[2].title())
        
        # Category
        category_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        category_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(category_frame, text="Category:").pack(side="left", padx=(20, 10), pady=0)
        category_entry = ctk.CTkEntry(category_frame, width=300, justify="center", fg_color="transparent")
        category_entry.pack(side="right", padx=(0, 20), pady=0)
        category_entry.insert(0, values[3])
        
        # Amount
        amount_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        amount_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(amount_frame, text="Amount (Ksh):").pack(side="left", padx=(20, 10), pady=0)
        amount_entry = ctk.CTkEntry(amount_frame, width=300, justify="center", fg_color="transparent")
        amount_entry.pack(side="right", padx=(0, 20), pady=0)
        amount_entry.insert(0, values[4])
        
        # Date
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(date_frame, text="Date (DD/MM/YYYY):").pack(side="left", padx=(20, 10), pady=0)
        date_entry = ctk.CTkEntry(date_frame, width=300, justify="center", fg_color="transparent")
        date_entry.pack(side="right", padx=(0, 20), pady=0)
        date_entry.insert(0, values[1])
        
        # Description
        desc_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        desc_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(desc_frame, text="Description:").pack(side="left", padx=(20, 10), pady=0)
        desc_entry = ctk.CTkEntry(desc_frame, width=300, fg_color="transparent")
        desc_entry.pack(side="right", padx=(0, 20), pady=0)
        desc_entry.insert(0, values[5])
        
        # Reference
        ref_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        ref_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(ref_frame, text="Reference:").pack(side="left", padx=(20, 10), pady=0)
        ref_entry = ctk.CTkEntry(ref_frame, width=300, justify="center", fg_color="transparent")
        ref_entry.pack(side="right", padx=(0, 20), pady=0)
        ref_entry.insert(0, values[6])
        
        def save_changes():
            try:
                trans_id = values[0]
                trans_type = type_combo.get().lower()
                category = category_entry.get().strip()
                amount = float(amount_entry.get().replace(',', ''))
                trans_date = date_entry.get().strip()
                description = desc_entry.get().strip()
                reference = ref_entry.get().strip()
                
                # Validate
                if not category:
                    messagebox.showerror("Error", "Category is required!")
                    return
                
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
                
                # Update database
                self.db.execute_query('''
                    UPDATE accounting_transactions 
                    SET transaction_type = ?, category = ?, amount = ?, 
                        description = ?, reference = ?, transaction_date = ?
                    WHERE id = ?
                ''', (trans_type, category, amount, description, reference, trans_date, trans_id))
                
                messagebox.showinfo("Success", "Transaction updated successfully!")
                dialog.destroy()
                self.load_transactions()
                self.update_summary()
                self.update_charts()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update transaction: {str(e)}")
        
        def delete_transaction():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
                try:
                    self.db.execute_query("DELETE FROM accounting_transactions WHERE id = ?", (values[0],))
                    messagebox.showinfo("Success", "Transaction deleted successfully!")
                    dialog.destroy()
                    self.load_transactions()
                    self.update_summary()
                    self.update_charts()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Save Changes",
            command=save_changes,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Delete",
            command=delete_transaction,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(side="left", padx=5)
    
    def export_transactions(self):
        try:
            import csv
            from datetime import datetime
            
            # Get all visible transactions
            transactions = []
            for item in self.tree.get_children():
                transactions.append(self.tree.item(item, 'values'))
            
            if not transactions:
                messagebox.showwarning("No Data", "No transactions to export!")
                return
            
            filename = f"accounting_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['ID', 'Date', 'Type', 'Category', 'Amount', 
                                'Description', 'Reference', 'Auto'])
                
                # Write data
                for trans in transactions:
                    writer.writerow(trans)
            
            messagebox.showinfo("Export Successful", f"Transactions exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export transactions: {str(e)}")
    
    def generate_report(self):
        report_type = self.report_type.get()
        month_filter = self.report_month.get()
        
        # Clear existing items
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Clear existing columns
        for col in self.report_tree["columns"]:
            self.report_tree.heading(col, text="")
            self.report_tree.column(col, width=0)
        
        if report_type == "Income Statement":
            self.generate_income_statement(month_filter)
        elif report_type == "Expense Report":
            self.generate_expense_report(month_filter)
        elif report_type == "Category Summary":
            self.generate_category_summary(month_filter)
        elif report_type == "Monthly Summary":
            self.generate_monthly_summary()
    
    def generate_income_statement(self, month_filter):
        columns = ("Category", "Amount (Ksh)")
        self.report_tree["columns"] = columns
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=200, anchor="center")
        
        # Get income data
        query_income = '''
            SELECT category, SUM(amount) as total
            FROM accounting_transactions
            WHERE transaction_type = 'income'
        '''
        params = []
        
        if month_filter != "All Months":
            month, year = month_filter.split('/')
            query_income += " AND strftime('%m', transaction_date) = ? AND strftime('%Y', transaction_date) = ?"
            params.extend([month, year])
        
        query_income += " GROUP BY category ORDER BY total DESC"
        
        income_data = self.db.fetch_all(query_income, params)
        
        total_income = 0
        for category, amount in income_data:
            self.report_tree.insert("", "end", values=(category, f"{amount:,.2f}"))
            total_income += amount
        
        # Separator
        self.report_tree.insert("", "end", values=("", ""))
        self.report_tree.insert("", "end", values=("Total Income", f"{total_income:,.2f}"))
        
        # Get expense data
        query_expense = '''
            SELECT category, SUM(amount) as total
            FROM accounting_transactions
            WHERE transaction_type = 'expense'
        '''
        params = []
        
        if month_filter != "All Months":
            month, year = month_filter.split('/')
            query_expense += " AND strftime('%m', transaction_date) = ? AND strftime('%Y', transaction_date) = ?"
            params.extend([month, year])
        
        query_expense += " GROUP BY category ORDER BY total DESC"
        
        expense_data = self.db.fetch_all(query_expense, params)
        
        total_expense = 0
        self.report_tree.insert("", "end", values=("", ""))
        self.report_tree.insert("", "end", values=("EXPENSES", ""))
        
        for category, amount in expense_data:
            self.report_tree.insert("", "end", values=(category, f"{amount:,.2f}"))
            total_expense += amount
        
        # Separator
        self.report_tree.insert("", "end", values=("", ""))
        self.report_tree.insert("", "end", values=("Total Expenses", f"{total_expense:,.2f}"))
        
        # Net Profit/Loss
        net_income = total_income - total_expense
        self.report_tree.insert("", "end", values=("", ""))
        self.report_tree.insert("", "end", values=(
            "NET PROFIT/LOSS", 
            f"{net_income:,.2f}",
            "green" if net_income >= 0 else "red"
        ))
    
    def generate_expense_report(self, month_filter):
        columns = ("Category", "Amount (Ksh)", "Percentage")
        self.report_tree["columns"] = columns
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150, anchor="center")
        
        query = '''
            SELECT category, SUM(amount) as total
            FROM accounting_transactions
            WHERE transaction_type = 'expense'
        '''
        params = []
        
        if month_filter != "All Months":
            month, year = month_filter.split('/')
            query += " AND strftime('%m', transaction_date) = ? AND strftime('%Y', transaction_date) = ?"
            params.extend([month, year])
        
        query += " GROUP BY category ORDER BY total DESC"
        
        expense_data = self.db.fetch_all(query, params)
        
        total_expense = sum(amount for _, amount in expense_data)
        
        for category, amount in expense_data:
            if total_expense > 0:
                percentage = (amount / total_expense) * 100
                percentage_str = f"{percentage:.1f}%"
            else:
                percentage_str = "0.0%"
            
            self.report_tree.insert("", "end", values=(
                category, 
                f"{amount:,.2f}",
                percentage_str
            ))
        
        # Total row
        self.report_tree.insert("", "end", values=("", "", ""))
        self.report_tree.insert("", "end", values=(
            "TOTAL EXPENSES",
            f"{total_expense:,.2f}",
            "100%"
        ))
    
    def generate_category_summary(self, month_filter):
        columns = ("Type", "Category", "Amount (Ksh)", "Count")
        self.report_tree["columns"] = columns
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, anchor="center")
        
        query = '''
            SELECT transaction_type, category, 
                   SUM(amount) as total_amount,
                   COUNT(*) as transaction_count
            FROM accounting_transactions
        '''
        params = []
        
        if month_filter != "All Months":
            month, year = month_filter.split('/')
            query += " WHERE strftime('%m', transaction_date) = ? AND strftime('%Y', transaction_date) = ?"
            params.extend([month, year])
        
        query += " GROUP BY transaction_type, category ORDER BY transaction_type, total_amount DESC"
        
        category_data = self.db.fetch_all(query, params)
        
        for trans_type, category, amount, count in category_data:
            self.report_tree.insert("", "end", values=(
                trans_type.title(),
                category,
                f"{amount:,.2f}",
                count
            ))
    
    def generate_monthly_summary(self):
        columns = ("Month", "Income", "Expenses", "Net", "Cash Flow")
        self.report_tree["columns"] = columns
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, anchor="center")
        
        query = '''
            SELECT strftime('%m/%Y', transaction_date) as month,
                   SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
            FROM accounting_transactions
            GROUP BY strftime('%Y-%m', transaction_date)
            ORDER BY strftime('%Y-%m', transaction_date) DESC
        '''
        
        monthly_data = self.db.fetch_all(query)
        
        for month, income, expense in monthly_data:
            net = income - expense
            cash_flow = income - expense  # Simplified cash flow
            
            self.report_tree.insert("", "end", values=(
                month,
                f"{income:,.2f}",
                f"{expense:,.2f}",
                f"{net:,.2f}",
                f"{cash_flow:,.2f}"
            ))
    
    def update_summary(self):
        # Calculate total income
        income_query = '''
            SELECT SUM(amount) 
            FROM accounting_transactions 
            WHERE transaction_type = 'income'
        '''
        total_income = self.db.fetch_one(income_query)[0] or 0.0
        
        # Calculate total expenses
        expense_query = '''
            SELECT SUM(amount) 
            FROM accounting_transactions 
            WHERE transaction_type = 'expense'
        '''
        total_expenses = self.db.fetch_one(expense_query)[0] or 0.0
        
        # Calculate net balance
        net_balance = total_income - total_expenses
        
        # Calculate cash flow (income - expenses for current month)
        cash_flow_query = '''
            SELECT 
                SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) -
                SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as cash_flow
            FROM accounting_transactions
            WHERE strftime('%m/%Y', transaction_date) = strftime('%m/%Y', 'now')
        '''
        cash_flow_result = self.db.fetch_one(cash_flow_query)
        cash_flow = cash_flow_result[0] or 0.0 if cash_flow_result else 0.0
        
        # Update labels
        self.income_label.configure(text=f"Total Income:\nKsh {total_income:,.2f}")
        self.expense_label.configure(text=f"Total Expenses:\nKsh {total_expenses:,.2f}")
        self.balance_label.configure(text=f"Net Balance:\nKsh {net_balance:,.2f}")
        self.cash_flow_label.configure(text=f"Monthly Cash Flow:\nKsh {cash_flow:,.2f}")
    
    def update_charts(self):
        # This method would update charts if you add charting functionality
        # For now, it's a placeholder
        pass
    
    def get_auto_transaction_stats(self):
        """Get statistics about automatic transactions"""
        stats = {
            'auto_income': 0.0,
            'auto_expense': 0.0,
            'total_auto': 0
        }
        
        try:
            # Auto income (Sales + Debt Collections)
            income_query = '''
                SELECT SUM(amount), COUNT(*)
                FROM accounting_transactions
                WHERE transaction_type = 'income' 
                AND is_auto = 1
                AND category IN ('Sales Revenue', 'Debt Collections')
            '''
            income_result = self.db.fetch_one(income_query)
            if income_result:
                stats['auto_income'] = income_result[0] or 0.0
                stats['total_auto'] += income_result[1] or 0
            
            # Auto expense (Cost of Goods Sold + Bad Debt Expense)
            expense_query = '''
                SELECT SUM(amount), COUNT(*)
                FROM accounting_transactions
                WHERE transaction_type = 'expense' 
                AND is_auto = 1
                AND category IN ('Cost of Goods Sold', 'Bad Debt Expense')
            '''
            expense_result = self.db.fetch_one(expense_query)
            if expense_result:
                stats['auto_expense'] = expense_result[0] or 0.0
                stats['total_auto'] += expense_result[1] or 0
        
        except Exception as e:
            print(f"Error getting auto transaction stats: {str(e)}")
        
        return stats
        