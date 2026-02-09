import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class UserManagement:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        
        # Check if user has admin privileges
        self.is_admin = current_user.get('role') == 'admin'
        
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        """Setup the user management interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="User Management",
            font=("Arial", 24, "bold")
        ).pack(side="left", padx=10)
        
        # Role indicator
        role_label = ctk.CTkLabel(
            title_frame,
            text=f"Logged in as: {self.current_user['role'].title()}",
            font=("Arial", 12),
            text_color="#3498db"
        )
        role_label.pack(side="right", padx=10)
        
        # Tab view
        self.tabview = ctk.CTkTabview(self.main_container, border_width=2, border_color="#68a2a6")
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tabview.add("View Users")
        self.tabview.add("Add User")
        self.tabview.add("Update User")
        self.tabview.add("Delete User")
        
        # Set up each tab
        self.setup_view_users_tab()
        self.setup_add_user_tab()
        self.setup_update_user_tab()
        self.setup_delete_user_tab()
        
        # Show permission warning if not admin
        if not self.is_admin:
            self.show_permission_warning()
    
    def show_permission_warning(self):
        """Show warning for non-admin users"""
        warning_frame = ctk.CTkFrame(self.main_container, fg_color="#f39c12", corner_radius=5)
        warning_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            warning_frame,
            text="⚠️ Admin privileges required for user management operations",
            font=("Arial", 12, "bold"),
            text_color="#000000"
        ).pack(pady=5)
    
    def setup_view_users_tab(self):
        """Setup the View Users tab"""
        tab = self.tabview.tab("View Users")
        
        # Search frame
        search_frame = ctk.CTkFrame(tab, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 12)).pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by username or full name...",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_users())
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_users,
            width=100
        )
        search_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.load_users,
            width=100
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Users table frame
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview with scrollbars
        tree_frame = ctk.CTkFrame(table_frame)
        tree_frame.pack(fill="both", expand=True)

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
        
        # Vertical scrollbar
        vsb = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        vsb.pack(side="right", fill="y")
        
        # Create Treeview
        columns = ("ID", "Username", "Full Name", "Role", "Created At")
        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            height=15
        )
        
        # Configure scrollbars
        vsb.configure(command=self.users_tree.yview)
        
        # Define headings
        for col in columns:
            self.users_tree.heading(col, text=col)
            if col == "ID":
                self.users_tree.column(col, width=50, minwidth=50)
            elif col == "Username":
                self.users_tree.column(col, width=150, minwidth=150)
            elif col == "Full Name":
                self.users_tree.column(col, width=200, minwidth=200)
            elif col == "Role":
                self.users_tree.column(col, width=100, minwidth=100)
            else:
                self.users_tree.column(col, width=200, minwidth=200)
        
        self.users_tree.pack(fill="both", expand=True)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Total Users: 0 | Admins: 0 | Staff: 0",
            font=("Arial", 12, "bold")
        )
        self.stats_label.pack()
    
    def setup_add_user_tab(self):
        """Setup the Add User tab"""
        tab = self.tabview.tab("Add User")
        
        # Check if user has permission
        if not self.is_admin:
            self.disable_tab_for_non_admin(tab)
            return
        
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(expand=True, padx=50, pady=50)
        
        # Username
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(username_frame, text="Username:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.add_username_entry = ctk.CTkEntry(username_frame, width=250, justify="center", fg_color="transparent")
        self.add_username_entry.pack(side="right")
        
        # Full Name
        fullname_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fullname_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(fullname_frame, text="Full Name:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.add_fullname_entry = ctk.CTkEntry(fullname_frame, width=250, justify="center", fg_color="transparent")
        self.add_fullname_entry.pack(side="right")
        
        # Password
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(password_frame, text="Password:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.add_password_entry = ctk.CTkEntry(password_frame, width=250, justify="center", show="*", fg_color="transparent")
        self.add_password_entry.pack(side="right")
        
        # Confirm Password
        confirm_pass_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        confirm_pass_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(confirm_pass_frame, text="Confirm Password:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.add_confirm_password_entry = ctk.CTkEntry(confirm_pass_frame, width=250, justify="center", show="*", fg_color="transparent")
        self.add_confirm_password_entry.pack(side="right")
        
        # Role
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(role_frame, text="User Role:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.add_role_var = ctk.StringVar(value="staff")
        ctk.CTkRadioButton(role_frame, text="Staff", variable=self.add_role_var, value="staff").pack(side="left", padx=(100, 10))
        ctk.CTkRadioButton(role_frame, text="Admin", variable=self.add_role_var, value="admin").pack(side="left", padx=0)
        
        # Add button
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ Add User",
            command=self.add_user,
            height=40,
            width=150,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_btn.pack(side="left", padx=(0, 20))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            command=self.clear_add_form,
            height=40,
            width=150,
            fg_color="transparent",
            border_width=2,
            border_color="#3498db",
            hover_color="#3498db"
        )
        clear_btn.pack(side="left", padx=(20, 0), pady=10)
    
    def setup_update_user_tab(self):
        """Setup the Update User tab"""
        tab = self.tabview.tab("Update User")
        
        # Check if user has permission
        if not self.is_admin:
            self.disable_tab_for_non_admin(tab)
            return
        
        # Main frame
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left frame - Select user
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(20, 10))
        
        ctk.CTkLabel(
            left_frame,
            text="Select User to Update",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # User listbox
        self.update_users_listbox = ctk.CTkScrollableFrame(left_frame, width=200, height=300)
        self.update_users_listbox.pack(pady=10, padx=10)
        
        # Right frame - Update form
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(
            right_frame,
            text="Update User Information",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_frame.pack(pady=20, padx=20)
        
        # Username (read-only)
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(username_frame, text="Username:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.update_username_entry = ctk.CTkEntry(username_frame, width=250, justify="center", fg_color="transparent")
        self.update_username_entry.pack(side="right")
        
        # Full Name
        fullname_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fullname_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(fullname_frame, text="Full Name:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.update_fullname_entry = ctk.CTkEntry(fullname_frame, width=250, justify="center", fg_color="transparent")
        self.update_fullname_entry.pack(side="right")
        
        # Password (optional)
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(password_frame, text="New Password (leave empty to keep current):", 
                     font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.update_password_entry = ctk.CTkEntry(password_frame, width=250, justify="center", show="*", fg_color="transparent")
        self.update_password_entry.pack(side="right")
        
        # Role
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(role_frame, text="User Role:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        self.update_role_var = ctk.StringVar(value="staff")
        ctk.CTkRadioButton(role_frame, text="Staff", variable=self.update_role_var, value="staff").pack(side="left", padx=(270, 10))
        ctk.CTkRadioButton(role_frame, text="Admin", variable=self.update_role_var, value="admin").pack(side="left", padx=0)
        
        # Update button
        button_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        update_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Update User",
            command=self.update_user,
            height=40,
            width=150,
            font=("Arial", 14, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        update_btn.pack()
    
    def setup_delete_user_tab(self):
        """Setup the Delete User tab"""
        tab = self.tabview.tab("Delete User")
        
        # Check if user has permission
        if not self.is_admin:
            self.disable_tab_for_non_admin(tab)
            return
        
        # Warning label
        warning_label = ctk.CTkLabel(
            tab,
            text="⚠️ WARNING: Deleting a user is permanent and cannot be undone!",
            font=("Arial", 14, "bold"),
            text_color="#e74c3c"
        )
        warning_label.pack(pady=(10, 20))
        
        # User selection frame
        selection_frame = ctk.CTkFrame(tab)
        selection_frame.pack(pady=(0, 20))
        
        ctk.CTkLabel(
            selection_frame,
            text="Select User to Delete:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # User listbox
        self.delete_users_listbox = ctk.CTkScrollableFrame(selection_frame, width=300, height=200)
        self.delete_users_listbox.pack(pady=10)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            tab,
            text="🗑️ Delete Selected User",
            command=self.delete_user,
            height=40,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        delete_btn.pack(pady=(0, 10))
        
        # Current user info (to prevent self-deletion)
        current_user_info = ctk.CTkLabel(
            tab,
            text=f"Currently logged in as: {self.current_user['username']} ({self.current_user['role']})",
            font=("Arial", 12),
            text_color="#3498db"
        )
        current_user_info.pack(pady=10)
    
    def disable_tab_for_non_admin(self, tab):
        """Disable tab content for non-admin users"""
        for widget in tab.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            tab,
            text="⛔ Admin privileges required",
            font=("Arial", 18, "bold"),
            text_color="#e74c3c"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            tab,
            text="Only users with admin role can manage users.",
            font=("Arial", 14)
        ).pack(pady=10)
    
    def load_users(self, search_query=None):
        """Load users from database"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Clear listboxes
        self.clear_listbox(self.update_users_listbox)
        self.clear_listbox(self.delete_users_listbox)
        
        # Build query
        query = "SELECT id, username, full_name, role, created_at FROM users"
        params = ()
        
        if search_query:
            query += " WHERE username LIKE ? OR full_name LIKE ?"
            params = (f'%{search_query}%', f'%{search_query}%')
        
        query += " ORDER BY created_at DESC"
        
        users = self.db.fetch_all(query, params)
        
        # Count stats
        total_users = len(users)
        admin_count = sum(1 for user in users if user[3] == 'admin')
        staff_count = total_users - admin_count
        
        # Update stats label
        self.stats_label.configure(text=f"Total Users: {total_users} | Admins: {admin_count} | Staff: {staff_count}")
        
        # Populate treeview
        for user in users:
            # Format date
            created_at = user[4]
            if created_at:
                try:
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                except:
                    created_at = str(created_at)
            
            self.users_tree.insert("", "end", values=user[:4] + (created_at,))
            
            # Add to update listbox (skip current user)
            if user[1] != self.current_user['username']:
                self.add_user_to_listbox(
                    self.update_users_listbox,
                    user[1],
                    lambda u=user: self.populate_update_form(u)
                )
            
            # Add to delete listbox (skip current user and admin)
            if user[1] != self.current_user['username'] and user[1] != 'admin':
                self.add_user_to_listbox(
                    self.delete_users_listbox,
                    user[1],
                    lambda u=user: self.select_user_for_deletion(u)
                )
    
    def clear_listbox(self, listbox_frame):
        """Clear all widgets from a listbox frame"""
        for widget in listbox_frame.winfo_children():
            widget.destroy()
    
    def add_user_to_listbox(self, listbox_frame, username, command):
        """Add a user button to a listbox frame"""
        btn = ctk.CTkButton(
            listbox_frame,
            text=username,
            command=command,
            height=30,
            anchor="w",
            fg_color="#227dd8",
            hover_color="#204161"
        )
        btn.pack(fill="x", padx=5, pady=2)
    
    def populate_update_form(self, user):
        """Populate the update form with user data"""
        self.selected_user_id = user[0]
        self.update_username_entry.delete(0, 'end')
        self.update_username_entry.insert(0, user[1])
        self.update_fullname_entry.delete(0, 'end')
        self.update_fullname_entry.insert(0, user[2] if user[2] else "")
        self.update_password_entry.delete(0, 'end')
        self.update_role_var.set(user[3])
    
    def select_user_for_deletion(self, user):
        """Select a user for deletion"""
        self.user_to_delete = {
            'id': user[0],
            'username': user[1],
            'full_name': user[2],
            'role': user[3]
        }
    
    def search_users(self):
        """Search users based on search query"""
        search_query = self.search_entry.get().strip()
        self.load_users(search_query if search_query else None)
    
    def add_user(self):
        """Add a new user"""
        # Validate admin access
        if not self.is_admin:
            messagebox.showerror("Permission Denied", "Only administrators can add new users!")
            return
        
        # Get form data
        username = self.add_username_entry.get().strip()
        full_name = self.add_fullname_entry.get().strip()
        password = self.add_password_entry.get()
        confirm_password = self.add_confirm_password_entry.get()
        role = self.add_role_var.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Username is required!")
            self.add_username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Password is required!")
            self.add_password_entry.focus()
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            self.add_password_entry.delete(0, 'end')
            self.add_confirm_password_entry.delete(0, 'end')
            self.add_password_entry.focus()
            return
        
        # Check if username already exists
        existing_user = self.db.fetch_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        
        if existing_user:
            messagebox.showerror("Error", f"Username '{username}' already exists!")
            self.add_username_entry.delete(0, 'end')
            self.add_username_entry.focus()
            return
        
        try:
            # Insert new user
            user_id = self.db.execute_query(
                "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                (username, password, full_name, role)
            )
            
            messagebox.showinfo("Success", f"User '{username}' added successfully!")
            
            # Clear form
            self.clear_add_form()
            
            # Refresh user list
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")
    
    def clear_add_form(self):
        """Clear the add user form"""
        self.add_username_entry.delete(0, 'end')
        self.add_fullname_entry.delete(0, 'end')
        self.add_password_entry.delete(0, 'end')
        self.add_confirm_password_entry.delete(0, 'end')
        self.add_role_var.set("staff")
        self.add_username_entry.focus()
    
    def update_user(self):
        """Update user information"""
        # Validate admin access
        if not self.is_admin:
            messagebox.showerror("Permission Denied", "Only administrators can update users!")
            return
        
        # Check if a user is selected
        if not hasattr(self, 'selected_user_id'):
            messagebox.showerror("Error", "Please select a user to update!")
            return
        
        # Get form data
        full_name = self.update_fullname_entry.get().strip()
        new_password = self.update_password_entry.get()
        role = self.update_role_var.get()
        
        # Validation
        if not full_name:
            messagebox.showerror("Error", "Full name is required!")
            self.update_fullname_entry.focus()
            return
        
        # Check if trying to update admin user (restrict some changes)
        current_user_data = self.db.fetch_one(
            "SELECT username FROM users WHERE id = ?",
            (self.selected_user_id,)
        )
        
        if current_user_data and current_user_data[0] == 'admin':
            if role != 'admin':
                messagebox.showerror("Error", "Cannot change the role of the admin user!")
                return
        
        try:
            # Build update query based on whether password is provided
            if new_password:
                self.db.execute_query(
                    "UPDATE users SET full_name = ?, password = ?, role = ? WHERE id = ?",
                    (full_name, new_password, role, self.selected_user_id)
                )
            else:
                self.db.execute_query(
                    "UPDATE users SET full_name = ?, role = ? WHERE id = ?",
                    (full_name, role, self.selected_user_id)
                )
            
            messagebox.showinfo("Success", "User updated successfully!")
            
            # Clear update form
            self.update_username_entry.delete(0, 'end')
            self.update_fullname_entry.delete(0, 'end')
            self.update_password_entry.delete(0, 'end')
            delattr(self, 'selected_user_id')
            
            # Refresh user list
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")
    
    def delete_user(self):
        """Delete a user"""
        # Validate admin access
        if not self.is_admin:
            messagebox.showerror("Permission Denied", "Only administrators can delete users!")
            return
        
        # Check if a user is selected
        if not hasattr(self, 'user_to_delete'):
            messagebox.showerror("Error", "Please select a user to delete!")
            return
        
        # Confirm deletion
        user_info = self.user_to_delete
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete user '{user_info['username']}'?\n\n"
            f"Name: {user_info['full_name']}\n"
            f"Role: {user_info['role']}\n\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        # Prevent deleting admin user
        if user_info['username'] == 'admin':
            messagebox.showerror("Error", "Cannot delete the admin user!")
            return
        
        # Prevent self-deletion
        if user_info['username'] == self.current_user['username']:
            messagebox.showerror("Error", "You cannot delete your own account while logged in!")
            return
        
        try:
            # Delete user
            self.db.execute_query(
                "DELETE FROM users WHERE id = ?",
                (user_info['id'],)
            )
            
            messagebox.showinfo("Success", f"User '{user_info['username']}' deleted successfully!")
            
            # Clear selection
            delattr(self, 'user_to_delete')
            
            # Refresh user list
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")