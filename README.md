# Small Business Inventory Management System

A comprehensive inventory management system designed specifically for small business dealerships. This application helps manage stock, sales, debts, accounting, and user management in an intuitive desktop interface.

## 🌟 Features

### Core Modules
- **Stock Management** - Track inventory levels, add/edit stock items, view low stock alerts
- **Sales Management** - Process sales with item search, cart system, and invoice generation
- **Debt Management** - Track customer debts, record payments, monitor outstanding balances
- **Accounting** - Automatic transaction recording, financial reports, income/expense tracking
- **User Management** - Multi-user system with role-based permissions (admin/staff)

### Key Features
- **Trial Version System** - 1-hour trial with periodic notifications
- **Automatic Accounting** - Sales and payments automatically recorded as transactions
- **Real-time Search** - Quick search across all modules
- **Data Export** - Export stock, sales, and debt data to CSV
- **Dashboard** - Overview of key business metrics
- **Responsive UI** - Modern dark theme interface using CustomTkinter

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- SQLite3 (included with Python)

### Step-by-Step Setup

1. **Clone or download the repository**
   ```bash
   git clone [<repository-url>](https://github.com/Kofa-code/Inventory-Management-System.git)
   cd absam-spares-inventory
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install customtkinter
   ```

4. **Initialize the database**
   ```bash
   python database.py
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Default Login Credentials

- **Admin User:**
  - Username: `admin`
  - Password: `1234`

- **Staff User (for testing):**
  - Username: `staff`
  - Password: `staff123`

## 🎯 Usage Guide

### 1. Login Screen
- Enter your username and password
- Use "Forgot Password?" if needed (requires admin password)
- View "About App" for trial information

### 2. Dashboard
- View key metrics at a glance
- Access quick actions for common tasks
- Monitor trial status and remaining time

### 3. Stock Management
- Add new stock items with name, model, quantity, price, and minimum stock level
- Search and filter stock items
- Edit existing items by double-clicking
- View stock transactions history

### 4. Sales Processing
- Select customer and payment method
- Search items using scrollable dropdown
- Add items to cart with quantities
- Process sales and generate invoices
- Automatically update stock levels

### 5. Debt Management
- Add new debts with customer details
- Record payments by double-clicking debts
- Track payment history
- Export debt reports

### 6. Accounting
- View automatic transactions from sales and payments
- Add manual income/expense transactions
- Generate financial reports
- Export transaction data

### 7. User Management (Admin Only)
- Add new users with roles (admin/staff)
- Update user information
- Delete users (with safeguards)
- View all users in the system

## 🔧 Trial System

### Trial Version Features
- **1 Hour Total Usage** - Full functionality for evaluation
- **Automatic Notifications** - Every 15 minutes
- **Activation Option** - Enter purchase code to unlock permanently
- **Graceful Expiry** - Blocks functionality after trial ends

### To Purchase Full Version
Contact:
- **Developer:** David Kofa
- **Email:** davidkofa07@gmail.com
- **Phone:** 0708010165

## 🗄️ Database Structure

The application uses SQLite with the following main tables:

- **users** - User accounts and permissions
- **stock** - Inventory items and quantities
- **sales** - Sales records
- **sale_items** - Individual sale line items
- **debts** - Customer debts
- **debt_payments** - Debt payment history
- **accounting_transactions** - Financial transactions
- **stock_transactions** - Stock movement history

## ⚙️ Configuration

### Database Configuration
- Default database file: `inventory.db`
- Automatic creation on first run
- Backup recommended before major updates

### UI Customization
- Dark theme with blue color scheme
- Responsive layout (1250x600)
- Customizable via `customtkinter` settings

## 🛠️ Development

### Project Structure
```
absam-spares-inventory/
├── main.py              # Main application entry point
├── database.py          # Database initialization and connection
├── modules/
│   ├── stock.py         # Stock management module
│   ├── sales.py         # Sales management module
│   ├── debts.py         # Debt management module
│   ├── accounting.py    # Accounting module
│   ├── accounting_service.py  # Accounting service
│   ├── user_management.py     # User management
│   ├── trial_manager.py       # Trial system
│   └── CTkScrollableDropdown.py  # Custom dropdown
└── README.md           # This file
```

### Adding New Features
1. Create new module in `modules/` directory
2. Import and integrate in `main.py`
3. Update database schema if needed
4. Add navigation button in sidebar

## 📊 Export Features

The application supports exporting data to CSV format:

- **Stock Data** - All inventory items with quantities and values
- **Sales Data** - Customer sales with payment status
- **Debt Data** - Outstanding debts and payment history
- **Accounting Data** - Financial transactions

## 🔐 Security Features

- **Role-based Access Control** - Admin vs Staff permissions
- **Password Protection** - User authentication required
- **Admin Password Reset** - Password recovery with admin verification
- **Trial Protection** - Time-based licensing system
- **Data Validation** - Input validation on all forms

## 🚨 Troubleshooting

### Common Issues

1. **"Database Error" on startup**
   - Delete `inventory.db` and restart
   - Ensure write permissions in directory

2. **Module Import Errors**
   - Verify all required modules are in the `modules/` directory
   - Check Python path and virtual environment

3. **Trial System Errors**
   - Delete `trial_data.json` to reset trial (for testing)
   - Check file permissions in application directory

4. **UI Display Issues**
   - Ensure CustomTkinter is installed: `pip install customtkinter`
   - Check screen resolution and scaling settings

### Performance Tips
- Keep stock items under 1000 for optimal search performance
- Regular database backups
- Clear old transaction records periodically

## 📝 License & Copyright

This is a trial version of ABSAM SPARES Inventory Management System.

**Developer:** David Kofa  
**Email:** davidkofa07@gmail.com  
**Phone:** 0708010165  

© 2024 All Rights Reserved. Unauthorized distribution prohibited.

## 🤝 Support

For technical support or purchase inquiries:
- Email: davidkofa07@gmail.com
- Phone: 0708010165

Please include:
- Screenshot of any error messages
- Steps to reproduce the issue
- Your operating system version
- Python version

---

*Note: This is a demo/trial version. Some features may be limited in the trial period. Purchase the full version for unlimited access and priority support.*
