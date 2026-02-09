# [file name]: trial_manager.py

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import json
import os
import sys
from pathlib import Path

class TrialManager:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        
        # Determine if running from PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # Running as EXE
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.embedded_trial_file = os.path.join(base_path, "trial_data.json")
        
        # Get writable user data directory
        if os.name == 'nt':  # Windows
            app_data_dir = os.path.join(os.environ.get('APPDATA', ''), 'ABSAM_SPARES')
        
        # Create directory if it doesn't exist
        os.makedirs(app_data_dir, exist_ok=True)
        
        # User data file (writable location)
        self.user_data_file = os.path.join(app_data_dir, "trial_data.json")
        
        self.trial_duration = timedelta(hours=1)  # 1 hour total trial
        self.notification_interval = timedelta(minutes=15)  # Notify every 15 minutes
        self.is_blocked = False 
        
        # Initialize trial data
        self.load_trial_data()
        
    def load_trial_data(self):
        """Load or initialize trial data"""
        # Try to load from user data file first (writable location)
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    self.trial_data = json.load(f)
                
                # Convert string dates back to datetime objects
                self.trial_data['first_run'] = datetime.fromisoformat(self.trial_data['first_run'])
                if self.trial_data['last_notification']:
                    self.trial_data['last_notification'] = datetime.fromisoformat(self.trial_data['last_notification'])
                else:
                    self.trial_data['last_notification'] = None
                
                # If already activated, return
                if self.trial_data.get('is_activated', False):
                    return
                    
            except (json.JSONDecodeError, KeyError, ValueError, IOError) as e:
                # User data file corrupted, will try embedded or reset
                print(f"Error loading user trial data: {e}")
        
        # Try embedded file (only for initial setup)
        try:
            if os.path.exists(self.embedded_trial_file):
                with open(self.embedded_trial_file, 'r') as f:
                    embedded_data = json.load(f)
                
                # Check if this is a new installation
                # Only use embedded data if no user data exists
                if not os.path.exists(self.user_data_file):
                    self.trial_data = embedded_data
                    
                    # Convert string dates back to datetime objects
                    if 'first_run' in self.trial_data:
                        self.trial_data['first_run'] = datetime.fromisoformat(self.trial_data['first_run'])
                    if 'last_notification' in self.trial_data:
                        if self.trial_data['last_notification']:
                            self.trial_data['last_notification'] = datetime.fromisoformat(self.trial_data['last_notification'])
                        else:
                            self.trial_data['last_notification'] = None
                    
                    # Save to user data file for future writes
                    self.save_trial_data()
                    return
        except (json.JSONDecodeError, KeyError, ValueError, IOError) as e:
            # Embedded file corrupted or inaccessible
            print(f"Error loading embedded trial data: {e}")
        
        # If all else fails, reset trial data
        self.reset_trial_data()
    
    def reset_trial_data(self):
        """Reset trial data (for first run or reset)"""
        self.trial_data = {
            'first_run': datetime.now(),
            'last_notification': None,
            'total_usage_time': 0,  # in seconds
            'is_activated': False,
            'activation_code': None
        }
        self.save_trial_data()
    
    def save_trial_data(self):
        """Save trial data to user's data file (writable location)"""
        try:
            # Convert datetime objects to strings
            data_to_save = self.trial_data.copy()
            data_to_save['first_run'] = data_to_save['first_run'].isoformat()
            if data_to_save['last_notification']:
                data_to_save['last_notification'] = data_to_save['last_notification'].isoformat()
            else:
                data_to_save['last_notification'] = None
            
            # Save to user's data file (writable location)
            with open(self.user_data_file, 'w') as f:
                json.dump(data_to_save, f, indent=2)
        except IOError as e:
            print(f"Error saving trial data: {e}")
            # Try fallback location
            try:
                # Try current directory as fallback
                fallback_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial_data_fallback.json")
                with open(fallback_file, 'w') as f:
                    json.dump(data_to_save, f, indent=2)
            except:
                pass
    
    def check_trial_status(self):
        """Check if trial is still valid"""
        if self.trial_data['is_activated']:
            return True  # App is activated
        
        current_time = datetime.now()
        elapsed_time = current_time - self.trial_data['first_run']
        
        # Update total usage time
        self.trial_data['total_usage_time'] = elapsed_time.total_seconds()
        
        # Check if trial has expired
        if elapsed_time >= self.trial_duration:
            self.is_blocked = True
            return False
        
        # Check if we need to show notification
        if (not self.trial_data['last_notification'] or 
            (current_time - self.trial_data['last_notification']) >= self.notification_interval):
            self.trial_data['last_notification'] = current_time
            self.save_trial_data()
            return "show_notification"
        
        return True
    
    def get_remaining_time(self):
        """Get remaining trial time"""
        if self.trial_data['is_activated']:
            return "Permanent License (Activated)"
        
        current_time = datetime.now()
        elapsed_time = current_time - self.trial_data['first_run']
        remaining_time = self.trial_duration - elapsed_time
        
        if remaining_time.total_seconds() <= 0:
            return "Trial Expired"
        
        # Convert to minutes
        remaining_minutes = int(remaining_time.total_seconds() / 60)
        hours = remaining_minutes // 60
        minutes = remaining_minutes % 60
        
        if hours > 0:
            return f"{hours} Hr(s) and {minutes} min(s) remaining"
        else:
            return f"{minutes}min remaining"
    
    def show_notification(self, parent_window=None):
        """Show trial notification"""
        remaining_time = self.get_remaining_time()
        
        notification_window = ctk.CTkToplevel(parent_window)
        notification_window.title("Trial Version Notification")
        notification_window.geometry("500x450")
        notification_window.transient(parent_window)
        notification_window.grab_set()
        
        # Center window
        notification_window.update_idletasks()
        width = notification_window.winfo_width()
        height = notification_window.winfo_height()
        x = (notification_window.winfo_screenwidth() // 2) - (width // 2)
        y = (notification_window.winfo_screenheight() // 2) - (height // 2)
        notification_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(notification_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon
        ctk.CTkLabel(
            content,
            text="⚠️",
            font=("Arial", 48),
            text_color="#f39c12"
        ).pack(pady=10)
        
        # Title
        ctk.CTkLabel(
            content,
            text="TRIAL VERSION",
            font=("Arial", 20, "bold"),
            text_color="#3498db"
        ).pack(pady=5)
        
        # Message
        message = f"""This is a trial version of ABSAM SPARES Inventory Management System.

Remaining Trial Time: {remaining_time}

Features:
• Full functionality for evaluation
• Time-limited access (1 hour total)
• Automatic notifications every 15 minutes

For the full version, please contact:
Developer: David Kofa
Email: davidkofa07@gmail.com
Phone: 0708010165

This software is protected by copyright law."""
        
        ctk.CTkLabel(
            content,
            text=message,
            font=("Arial", 12),
            justify="left",
            wraplength=450
        ).pack(pady=(5, 10),  fill="both", expand=True)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        # OK button
        ok_btn = ctk.CTkButton(
            btn_frame,
            text="Continue Trial",
            command=notification_window.destroy,
            height=40,
            font=("Arial", 14),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        ok_btn.pack(side="left", padx=10, pady=0)
        
        # Activate button
        activate_btn = ctk.CTkButton(
            btn_frame,
            text="Activate Now",
            command=lambda: self.show_activation_dialog(notification_window, parent_window),
            height=40,
            font=("Arial", 14),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        activate_btn.pack(side="left", padx=10, pady=0)
    
    def show_activation_dialog(self, notification_window=None, parent_window=None):
        """Show activation dialog"""
        if notification_window:
            notification_window.destroy()
        
        activation_window = ctk.CTkToplevel(parent_window)
        activation_window.title("Activate Software")
        activation_window.geometry("500x400")
        activation_window.transient(parent_window)
        activation_window.grab_set()
        
        # Center window
        activation_window.update_idletasks()
        width = activation_window.winfo_width()
        height = activation_window.winfo_height()
        x = (activation_window.winfo_screenwidth() // 2) - (width // 2)
        y = (activation_window.winfo_screenheight() // 2) - (height // 2)
        activation_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(activation_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content,
            text="Software Activation",
            font=("Arial", 20, "bold"),
            text_color="#3498db"
        ).pack(pady=10)
        
        # Information
        info_text = """To activate your copy of ABSAM SPARES Inventory System:

1. Contact the developer to purchase a license
2. You will receive an activation code
3. Enter the activation code below

Contact Information:
Developer: David Kofa
Email: davidkofa07@gmail.com
Phone: 0708010165"""
        
        ctk.CTkLabel(
            content,
            text=info_text,
            font=("Arial", 12),
            justify="left",
            wraplength=450
        ).pack(pady=10)
        
        # Activation code entry
        code_frame = ctk.CTkFrame(content, fg_color="transparent")
        code_frame.pack(pady=20)
        
        ctk.CTkLabel(
            code_frame,
            text="Activation Code:",
            font=("Arial", 14)
        ).pack(side="left", padx=(0, 10))
        
        self.activation_code_entry = ctk.CTkEntry(
            code_frame,
            width=250,
            font=("Arial", 12),
            placeholder_text="Enter activation code here"
        )
        self.activation_code_entry.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Activate button
        activate_btn = ctk.CTkButton(
            buttons_frame,
            text="Activate",
            command=lambda: self.activate_software(activation_window),
            width=120,
            height=40,
            font=("Arial", 14),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        activate_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=activation_window.destroy,
            width=120,
            height=40,
            font=("Arial", 14),
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        cancel_btn.pack(side="left", padx=10)
    
    def activate_software(self, activation_window):
        """Activate the software with provided code"""
        code = self.activation_code_entry.get().strip()
        
        if not code:
            messagebox.showerror("Error", "Please enter an activation code!")
            return
        
        # Simple validation (you should implement more secure validation)
        if self.validate_activation_code(code):
            self.trial_data['is_activated'] = True
            self.trial_data['activation_code'] = code
            self.save_trial_data()
            
            messagebox.showinfo("Success", "Software activated successfully!\nThank you for your purchase.")
            activation_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid activation code!\nPlease contact the developer.")
    
    def validate_activation_code(self, code):
        """Validate activation code (simplified for demo)"""
        # In a real system, this would be more complex and secure
        # For demo purposes, accept a simple pattern
        if len(code) >= 10 and code.startswith("ABSAM"):
            return True
        return False
    
    def show_block_screen(self, parent_window=None):
        """Show block screen when trial expires"""
        self.is_blocked = True
        
        # Create blocking window
        block_window = ctk.CTkToplevel(parent_window)
        block_window.title("Trial Expired")
        block_window.geometry("600x450")
        
        # Make it modal and always on top
        block_window.transient(parent_window)
        block_window.grab_set()
        
        # Remove window decorations (makes it harder to close)
        block_window.overrideredirect(True)
        
        # Center window
        block_window.update_idletasks()
        width = block_window.winfo_width()
        height = block_window.winfo_height()
        x = (block_window.winfo_screenwidth() // 2) - (width // 2)
        y = (block_window.winfo_screenheight() // 2) - (height // 2)
        block_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        content = ctk.CTkScrollableFrame(block_window, fg_color="#2c3e50")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon
        ctk.CTkLabel(
            content,
            text="⛔",
            font=("Arial", 72),
            text_color="#e74c3c"
        ).pack(pady=20)
        
        # Title
        ctk.CTkLabel(
            content,
            text="TRIAL PERIOD EXPIRED",
            font=("Arial", 24, "bold"),
            text_color="#e74c3c"
        ).pack(pady=10)
        
        # Message
        message = """Your trial period has expired.

The ABSAM SPARES Inventory Management System trial version is limited to 1 hour of usage. 
To continue using the software, you need to purchase a full license.

What happens now:
• The software will not function
• All features are disabled
• Data remains safe in the database

To activate your software:"""
        
        ctk.CTkLabel(
            content,
            text=message,
            font=("Arial", 12),
            text_color="white",
            justify="left",
            wraplength=550
        ).pack(pady=20, fill="both", expand=True)
        
        # Contact Information
        contact_frame = ctk.CTkFrame(content, fg_color="#34495e")
        contact_frame.pack(fill="x", pady=10, padx=10)
        
        contact_info = """Contact the developer to purchase a license:

Developer: David Kofa
Email: davidkofa07@gmail.com
Phone: 0708010165
Website: Coming Soon

You will receive an activation code to unlock the software permanently."""
        
        ctk.CTkLabel(
            contact_frame,
            text=contact_info,
            font=("Arial", 11),
            text_color="white",
            justify="left",
            wraplength=520
        ).pack(pady=10, padx=10)
        
        # Activation button
        activate_btn = ctk.CTkButton(
            content,
            text="Activate Software Now",
            command=lambda: self.show_activation_dialog(block_window, parent_window),
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            text_color="white"
        )
        activate_btn.pack(pady=20)
        
        # Quit button
        quit_btn = ctk.CTkButton(
            content,
            text="Exit Application",
            command=lambda: self.quit_application(parent_window, block_window),
            height=40,
            font=("Arial", 12),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white"
        )
        quit_btn.pack(pady=10)
        
        # Disable parent window
        if parent_window:
            parent_window.attributes('-disabled', True)
            block_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent closing
        
        return block_window
    
    def quit_application(self, parent_window, block_window):
        """Quit the application"""
        if parent_window:
            parent_window.destroy()
        if block_window:
            block_window.destroy()
        sys.exit(0)
    
    def start_trial_monitor(self, parent_window):
        """Start monitoring trial status (call this periodically)"""
        status = self.check_trial_status()
        
        if status == "show_notification":
            self.show_notification(parent_window)
        elif status is False:  # Trial expired
            self.show_block_screen(parent_window)
            return False
        
        return True
    
    def get_trial_info(self):
        """Get trial information for display"""
        info = {
            'is_activated': self.trial_data['is_activated'],
            'first_run': self.trial_data['first_run'].strftime("%Y-%m-%d %H:%M:%S"),
            'remaining_time': self.get_remaining_time(),
            'total_usage_minutes': int(self.trial_data['total_usage_time'] / 60),
            'status': "Activated" if self.trial_data['is_activated'] else "Trial"
        }
        return info
    
    def reset_trial(self):
        """Reset trial (for testing purposes only)"""
        self.reset_trial_data()
        self.is_blocked = False
        messagebox.showinfo("Trial Reset", "Trial has been reset for testing purposes.")