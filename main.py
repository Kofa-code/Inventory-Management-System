# [file name]: main.py

import customtkinter as ctk
from datetime import datetime
from database import Database
from tkinter import messagebox
from modules.stock import StockManagement
from modules.sales import SalesManagement
from modules.debts import DebtsManagement
from modules.accounting import AccountingManagement
from modules.accounting_service import AccountingService
from modules.user_management import UserManagement
from modules.trial_manager import TrialManager  

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class InventoryApp:
    def __init__(self):
        self.db = Database()
        self.accounting_service = AccountingService(self.db)
        self.current_user = None
        self.current_page = None
        self.forgot_password_mode = False
        
        # Initialize trial manager
        self.trial_manager = TrialManager()
        
        # Check trial status before showing login
        if not self.check_trial_status():
            return  # App is blocked
        
        self.setup_login_window()
    
    def check_trial_status(self):
        """Check trial status before allowing app to run"""
        status = self.trial_manager.check_trial_status()
        
        if status == "show_notification":
            # We'll show notification after login
            pass
        elif status is False:  # Trial expired
            self.trial_manager.show_block_screen(None)
            return False
        
        return True
    
    def setup_login_window(self):
        self.login_window = ctk.CTk()
        self.login_window.title("ABSAM SPARES - TRIAL VERSION")
        self.login_window.geometry("1250x600")     
        
        # Center window
        self.center_window(self.login_window, 1250, 600)
        
        # Add trial info label to login screen
        trial_info = self.trial_manager.get_trial_info()
        trial_status_text = f"Trial Version | {trial_info['remaining_time']}"
        
        trial_label = ctk.CTkLabel(
            self.login_window,
            text=trial_status_text,
            font=("Arial", 12, "bold"),
            text_color="#f39c12"
        )
        trial_label.place(relx=0.5, rely=0.90, anchor="center")
        
        # Store reference for updating
        self.trial_label = trial_label
        
        # Start trial monitor timer (check every 30 seconds)
        self.start_trial_monitor()
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.login_window, 
            text="ABSAM SPARES\nInventory Management System",
            font=("Arial", 24, "bold"),
            text_color="#3498db"
        )
        self.title_label.pack(anchor="n", pady=40)

        # Main container for login/forgot password
        self.main_container = ctk.CTkFrame(self.login_window, fg_color="transparent")
        self.main_container.pack(pady=(0, 40), padx=40, expand=True)
        
        # Setup login frame by default
        self.setup_login_frame()

        # Bind Enter key
        self.login_window.bind('<Return>', lambda e: self.handle_enter_key())
        
        self.login_window.mainloop()
    
    def setup_login_frame(self):
        """Setup the login frame"""
        self.forgot_password_mode = False
        
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Login frame
        self.login_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.login_frame.pack(expand=True, fill="both")
        
        # Login label
        ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 24, "bold")).pack(pady=20)
        
        # Username       
        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="Username", font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.username_entry.pack(padx=40, pady=20)
        
        # Password
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="Password", show="*", font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.password_entry.pack(padx=40, pady=10)

        # Login button
        login_btn = ctk.CTkButton(
            self.login_frame,
            text="Login",
            command=self.login,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9"
        )
        login_btn.pack(pady=20)
        
        # Forgot password button
        forgot_btn = ctk.CTkButton(
            self.login_frame,
            text="Forgot password?",
            command=self.show_forgot_password,
            fg_color="transparent",
            hover_color="#2980b9"
        )
        forgot_btn.pack(pady=20)

        # About button
        self.about_btn = ctk.CTkButton(
            self.login_window,
            text="About App",
            command=self.show_about,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#68a2a6",
            hover_color="#68a2a6"
        )
        self.about_btn.pack(anchor="sw", padx=40, pady=(0, 40))

    def show_about(self):
        # Store the current packing info before destroying the login frame
        login_frame_pack_info = {}
        for widget in self.main_container.winfo_children():
            login_frame_pack_info[widget] = widget.pack_info()
        
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Hide the About App button
        self.about_btn.pack_forget()

        def back_to_main():
            # Clear the about frame
            for widget in self.main_container.winfo_children():
                widget.destroy()
            
            # Hide the Back to Login button
            back_btn.pack_forget()
            
            # Show the About App button again with original position
            self.about_btn.pack(anchor="sw", padx=40, pady=(0, 40))
            
            # Recreate the login frame
            self.setup_login_frame()

        # Create Back to Login button
        back_btn = ctk.CTkButton(
            self.login_window,
            text="Back to Login",
            command=back_to_main,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#68a2a6",
            hover_color="#68a2a6"
        )
        back_btn.pack(anchor="sw", padx=40, pady=(0, 40))
        
        # Forgot password frame
        about_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=15, width=500, height=300)
        about_frame.pack(expand=True, fill="both")

        about_text = """Motorbike Parts Inventory Management System
Version 1.0 (Trial Version)

A comprehensive inventory management system for 
motorbike spare parts dealerships.

Trial Version Features:
- Full functionality for 1 hour
- Automatic notifications every 15 minutes
- All modules available for testing

To purchase full version, contact:
Developer: David kofa
Email: davidkofa07@gmail.com
Phone: 0708010165

Created with Python, CustomTkinter, and SQLite
© 2024 All Rights Reserved"""

        info_label = ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=("Arial", 14),
            justify="left",
            wraplength=600
        )
        info_label.pack(padx=40, pady=40, fill="both", expand=True)
    
    def show_forgot_password(self):
        """Show the forgot password form"""
        self.forgot_password_mode = True
        
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Forgot password frame
        forgot_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        forgot_frame.pack(expand=True, fill="both")
        
        # Title
        ctk.CTkLabel(forgot_frame, text="Reset Password", font=("Arial", 24, "bold")).pack(pady=20)
        
        # Username
        username_frame = ctk.CTkFrame(forgot_frame, fg_color="transparent")
        username_frame.pack(pady=(20, 5))
        
        username_label = ctk.CTkLabel(username_frame, text="Username:", font=("Arial", 14))
        username_label.pack(side="left", padx=(20, 10), pady=(5, 5))
        
        self.forgot_username_entry = ctk.CTkEntry(username_frame, width=200, font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.forgot_username_entry.pack(side="right", padx=(20, 0), pady=5)
        
        # New Password
        new_pass_frame = ctk.CTkFrame(forgot_frame, fg_color="transparent")
        new_pass_frame.pack(pady=(10, 5))
        
        new_pass_label = ctk.CTkLabel(new_pass_frame, text="New Password:", font=("Arial", 14))
        new_pass_label.pack(side="left", padx=(20, 10), pady=(5, 5))
        
        self.new_password_entry = ctk.CTkEntry(new_pass_frame, width=200, show="*", font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.new_password_entry.pack(side="right", padx=(20, 0), pady=5)
        
        # Confirm Password
        confirm_pass_frame = ctk.CTkFrame(forgot_frame, fg_color="transparent")
        confirm_pass_frame.pack(pady=(10, 5))
        
        confirm_pass_label = ctk.CTkLabel(confirm_pass_frame, text="Confirm Password:", font=("Arial", 14))
        confirm_pass_label.pack(side="left", padx=(20, 10), pady=(5, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(confirm_pass_frame, width=200, show="*", font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.confirm_password_entry.pack(side="right", padx=(0, 20), pady=5)
        
        # Admin Password Verification
        admin_pass_frame = ctk.CTkFrame(forgot_frame, fg_color="transparent")
        admin_pass_frame.pack(pady=(20, 5))
        
        admin_pass_label = ctk.CTkLabel(admin_pass_frame, text="Admin Password:", font=("Arial", 14))
        admin_pass_label.pack(side="left", padx=(20, 10), pady=(5, 5))
        
        self.admin_password_entry = ctk.CTkEntry(admin_pass_frame, width=200, show="*", font=("Arial", 14, "bold"), justify="center", fg_color="transparent")
        self.admin_password_entry.pack(side="right", padx=(0, 20), pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(forgot_frame, fg_color="transparent")
        buttons_frame.pack(pady=30)
        
        # Submit button
        submit_btn = ctk.CTkButton(
            buttons_frame,
            text="Reset Password",
            command=self.reset_password,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150
        )
        submit_btn.pack(side="left", padx=10)
        
        # Back to login button
        back_btn = ctk.CTkButton(
            buttons_frame,
            text="Back to Login",
            command=self.setup_login_frame,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            width=150
        )
        back_btn.pack(side="left", padx=10)
    
    def handle_enter_key(self):
        """Handle Enter key press based on current mode"""
        if self.forgot_password_mode:
            self.reset_password()
        else:
            self.login()
    
    def reset_password(self):
        """Reset user password after admin verification"""
        username = self.forgot_username_entry.get().strip()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        admin_password = self.admin_password_entry.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Please enter username!")
            return
        
        if not new_password:
            messagebox.showerror("Error", "Please enter new password!")
            return
        
        if not confirm_password:
            messagebox.showerror("Error", "Please confirm password!")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            self.new_password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.new_password_entry.focus()
            return
        
        if not admin_password:
            messagebox.showerror("Error", "Please enter admin password!")
            return
        
        try:
            # Verify admin password
            admin = self.db.fetch_one(
                "SELECT id FROM users WHERE username = 'admin' AND password = ?",
                (admin_password,)
            )
            
            if not admin:
                messagebox.showerror("Error", "Invalid admin password!")
                self.admin_password_entry.delete(0, 'end')
                self.admin_password_entry.focus()
                return
            
            # Check if user exists
            user = self.db.fetch_one(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            )
            
            if not user:
                messagebox.showerror("Error", f"User '{username}' not found!")
                self.forgot_username_entry.delete(0, 'end')
                self.forgot_username_entry.focus()
                return
            
            # Update password
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_password, username)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Password for '{username}' has been reset successfully!")
            
            # Clear all fields
            self.forgot_username_entry.delete(0, 'end')
            self.new_password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.admin_password_entry.delete(0, 'end')
            
            # Return to login
            self.setup_login_frame()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset password: {str(e)}")
    
    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        # Check credentials
        user = self.db.fetch_one(
            "SELECT id, username, full_name, role FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'role': user[3]
            }
            self.login_window.destroy()
            self.setup_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    
    def start_trial_monitor(self):
        """Start periodic trial monitoring"""
        if hasattr(self, 'trial_label'):
            trial_info = self.trial_manager.get_trial_info()
            trial_status_text = f"Trial Version | {trial_info['remaining_time']}"
            self.trial_label.configure(text=trial_status_text)
        
        # Check trial status
        if hasattr(self, 'login_window') and self.login_window.winfo_exists():
            status = self.trial_manager.check_trial_status()
            
            if status == "show_notification":
                self.trial_manager.show_notification(self.login_window)
            elif status is False:  # Trial expired
                if self.trial_manager.show_block_screen(self.login_window):
                    # App is blocked, stop monitoring
                    return
        
        # Schedule next check in 30 seconds
        if hasattr(self, 'login_window') and self.login_window.winfo_exists():
            self.login_window.after(30000, self.start_trial_monitor)  # Check every 30 seconds
    
    def setup_main_window(self):
        self.main_window = ctk.CTk()
        self.main_window.title("ABSAM SPARES - TRIAL VERSION")
        self.main_window.geometry("1250x600")
        
        # Start trial monitor for main window
        self.start_main_trial_monitor()
        
        # Configure grid
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_window, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # User info
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(pady=20, padx=10, fill="x")
        
        ctk.CTkLabel(
            user_frame, 
            text=f"Welcome,\n{self.current_user['full_name']}",
            font=("Arial", 16, "bold"),
            anchor="w"
        ).pack(fill="x", padx=50, pady=10)
        
        ctk.CTkLabel(
            user_frame,
            text=f"Role: {self.current_user['role'].title()}",
            font=("Arial", 12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", padx=50, pady=10)
        
        # Separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray").pack(fill="x", pady=20, padx=10)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)
        
        button_config = {
            "height": 40,
            "font": ("Arial", 14),
            "corner_radius": 5,
            "anchor": "w"
        }
        
        self.dashboard_btn = ctk.CTkButton(
            nav_frame,
            text="📊 Dashboard",
            command=lambda: self.show_page("dashboard"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.dashboard_btn.pack(pady=5, fill="x")
        
        self.stock_btn = ctk.CTkButton(
            nav_frame,
            text="📦 Stock Management",
            command=lambda: self.show_page("stock"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.stock_btn.pack(pady=5, fill="x")
        
        self.sales_btn = ctk.CTkButton(
            nav_frame,
            text="💰 Sales",
            command=lambda: self.show_page("sales"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.sales_btn.pack(pady=5, fill="x")
        
        self.debts_btn = ctk.CTkButton(
            nav_frame,
            text="💳 Debts",
            command=lambda: self.show_page("debts"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.debts_btn.pack(pady=5, fill="x")
        
        self.accounting_btn = ctk.CTkButton(
            nav_frame,
            text="📊 Accounting",
            command=lambda: self.show_page("accounting"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.accounting_btn.pack(pady=5, fill="x")

        self.manager_btn = ctk.CTkButton(
            nav_frame,
            text="👥 Manage Users",
            command=lambda: self.show_page("manage_users"),
            fg_color="transparent",
            border_width=2,
            border_color="#2980b9",
            hover_color="#2980b9",
            **button_config
        )
        self.manager_btn.pack(pady=5, fill="x")
        
        # Separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray").pack(fill="x", pady=20, padx=10)
        
        # Logout button
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.logout,
            height=40,
            font=("Arial", 14),
            fg_color="transparent",
            border_width=2,
            border_color="#e74c3c",
            hover_color="#e74c3c",
            corner_radius=5
        )
        logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")
        
        # Main content area
        self.main_content = ctk.CTkFrame(self.main_window)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Show dashboard by default
        self.show_page("dashboard")
        
        self.main_window.mainloop()
    
    def start_main_trial_monitor(self):
        """Start periodic trial monitoring for main window"""
        if hasattr(self, 'main_trial_label'):
            trial_info = self.trial_manager.get_trial_info()
            trial_status_text = f"Trial Version | {trial_info['remaining_time']}"
            self.main_trial_label.configure(text=trial_status_text)
        
        # Check trial status
        if hasattr(self, 'main_window') and self.main_window.winfo_exists():
            status = self.trial_manager.check_trial_status()
            
            if status == "show_notification":
                self.trial_manager.show_notification(self.main_window)
            elif status is False:  # Trial expired
                if self.trial_manager.show_block_screen(self.main_window):
                    # App is blocked, stop monitoring
                    return
        
        # Schedule next check in 30 seconds
        if hasattr(self, 'main_window') and self.main_window.winfo_exists():
            self.main_window.after(30000, self.start_main_trial_monitor)  # Check every 30 seconds
    
    def show_page(self, page_name):
        # Check trial status first
        status = self.trial_manager.check_trial_status()
        if status is False:  # Trial expired
            self.trial_manager.show_block_screen(self.main_window)
            return
        
        # Clear current page
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Reset button colors
        buttons = [self.dashboard_btn, self.stock_btn, self.sales_btn, 
                  self.debts_btn, self.accounting_btn, self.manager_btn]
        
        for btn in buttons:
            btn.configure(fg_color="transparent")
        
        # Set active button color
        if page_name == "dashboard":
            self.dashboard_btn.configure(fg_color="#3498db")
            self.show_dashboard()
        elif page_name == "stock":
            self.stock_btn.configure(fg_color="#3498db")
            self.current_page = StockManagement(self.main_content, self.db, self.accounting_service)
        elif page_name == "sales":
            self.sales_btn.configure(fg_color="#3498db")
            self.current_page = SalesManagement(self.main_content, self.db, self.current_user, self.accounting_service)
        elif page_name == "debts":
            self.debts_btn.configure(fg_color="#3498db")
            self.current_page = DebtsManagement(self.main_content, self.db, self.accounting_service)
        elif page_name == "accounting":
            self.accounting_btn.configure(fg_color="#3498db")
            self.current_page = AccountingManagement(self.main_content, self.db, self.current_user, self.accounting_service)
        elif page_name == "manage_users":
            self.manager_btn.configure(fg_color="#3498db")
            self.current_page = UserManagement(self.main_content, self.db, self.current_user)
    
    def show_dashboard(self):
        # Dashboard container
        container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text="Dashboard",
            font=("Arial", 24, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            title_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            font=("Arial", 14),
            text_color="gray"
        ).pack(side="right", padx=10)
        
        # Stats cards
        stats_frame = ctk.CTkFrame(container, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        # Get stats from database
        stock_stats = self.db.get_stock_stats()
        sales_stats = self.db.get_today_sales_stats()
        debt_stats = self.db.get_debt_stats()
        
        # Stock card
        stock_card = ctk.CTkFrame(stats_frame, width=200, height=150, border_width=2, border_color="#68a2a6")
        stock_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        stock_card.pack_propagate(False)
        
        ctk.CTkLabel(
            stock_card,
            text="📦",
            font=("Arial", 30)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            stock_card,
            text=f"Total Items: {stock_stats[0] or 0}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            stock_card,
            text=f"Total Stock: {stock_stats[1] or 0}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            stock_card,
            text=f"Low Stock: {stock_stats[3] or 0}",
            font=("Arial", 12),
            text_color="#e74c3c" if stock_stats[3] else "gray"
        ).pack()
        
        # Sales card
        sales_card = ctk.CTkFrame(stats_frame, width=200, height=150, border_width=2, border_color="#68a2a6")
        sales_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        sales_card.pack_propagate(False)
        
        ctk.CTkLabel(
            sales_card,
            text="💰",
            font=("Arial", 30)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            sales_card,
            text=f"Today's Sales: ${sales_stats[1] or 0:.2f}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            sales_card,
            text=f"Total Sales: {sales_stats[0] or 0}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            sales_card,
            text=f"Balance Due: ${sales_stats[3] or 0:.2f}",
            font=("Arial", 12),
            text_color="#f39c12" if sales_stats[3] else "gray"
        ).pack()
        
        # Debts card
        debts_card = ctk.CTkFrame(stats_frame, width=200, height=150, border_width=2, border_color="#68a2a6")
        debts_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        debts_card.pack_propagate(False)
        
        ctk.CTkLabel(
            debts_card,
            text="💳",
            font=("Arial", 30)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            debts_card,
            text=f"Total Debts: Ksh {debt_stats[1] or 0:.2f}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            debts_card,
            text=f"Active Debts: {debt_stats[0] or 0}",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkLabel(
            debts_card,
            text=f"Balance: Ksh {debt_stats[3] or 0:.2f}",
            font=("Arial", 12),
            text_color="#e74c3c" if debt_stats[3] else "gray"
        ).pack()
        
        # Accounting card
        account_card = ctk.CTkFrame(stats_frame, width=200, height=150, border_width=2, border_color="#68a2a6")
        account_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        account_card.pack_propagate(False)
        
        ctk.CTkLabel(
            account_card,
            text="📊",
            font=("Arial", 30)
        ).pack(pady=10)
        
        # Get accounting stats
        income = self.db.fetch_one("SELECT SUM(amount) FROM accounting_transactions WHERE transaction_type = 'income'")[0] or 0
        expense = self.db.fetch_one("SELECT SUM(amount) FROM accounting_transactions WHERE transaction_type = 'expense'")[0] or 0
        
        ctk.CTkLabel(
            account_card,
            text=f"Income: Ksh {income:.2f}",
            font=("Arial", 12),
            text_color="#2ecc71"
        ).pack()
        
        ctk.CTkLabel(
            account_card,
            text=f"Expenses: Ksh {expense:.2f}",
            font=("Arial", 12),
            text_color="#e74c3c"
        ).pack()
        
        net = income - expense
        ctk.CTkLabel(
            account_card,
            text=f"Net: Ksh {net:.2f}",
            font=("Arial", 12),
            text_color="#3498db" if net >= 0 else "#e74c3c"
        ).pack()
        
        # Trial Info Card
        trial_info = self.trial_manager.get_trial_info()
        trial_card = ctk.CTkFrame(stats_frame, width=200, height=150, border_width=2, border_color="#f39c12")
        trial_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        trial_card.pack_propagate(False)
        
        ctk.CTkLabel(
            trial_card,
            text="⏰",
            font=("Arial", 30),
            text_color="#f39c12"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            trial_card,
            text="Trial Version",
            font=("Arial", 12, "bold"),
            text_color="#f39c12"
        ).pack()
        
        ctk.CTkLabel(
            trial_card,
            text=trial_info['remaining_time'],
            font=("Arial", 11)
        ).pack()
        
        ctk.CTkLabel(
            trial_card,
            text=f"Used: {trial_info['total_usage_minutes']} min",
            font=("Arial", 10),
            text_color="gray"
        ).pack(pady=5)
        
        # Add activation button if not activated
        if not trial_info['is_activated']:
            activate_btn = ctk.CTkButton(
                trial_card,
                text="Activate",
                command=lambda: self.trial_manager.show_activation_dialog(None, self.main_window),
                height=25,
                font=("Arial", 10),
                fg_color="#2ecc71",
                hover_color="#27ae60"
            )
            activate_btn.pack(pady=5)
        
        # Separator
        ctk.CTkFrame(container, height=2, fg_color="gray").pack(fill="x", pady=20)
        
        # Quick Actions
        ctk.CTkLabel(
            container,
            text="Quick Actions",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        actions_frame = ctk.CTkFrame(container, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        # Quick action buttons
        quick_actions = [
            ("📦 Manage Stock", "stock", "#3498db"),
            ("💰 New Sale", "sales", "#2ecc71"),
            ("💳 Add Debt", "debts", "#e74c3c"),
            ("📊 Accounting", "accounting", "#9b59b6")
        ]
        
        for text, page, color in quick_actions:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                command=lambda p=page: self.show_page(p),
                height=50,
                font=("Arial", 14),
                fg_color=color,
                hover_color=self.darken_color(color),
                corner_radius=10
            )
            btn.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    
    def darken_color(self, color):
        # Simple function to darken a hex color
        colors = {
            "#3498db": "#2980b9",
            "#2ecc71": "#27ae60",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad"
        }
        return colors.get(color, color)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.main_window.destroy()
            self.current_user = None
            self.setup_login_window()

if __name__ == "__main__":
    app = InventoryApp()