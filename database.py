import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'staff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stock table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                model TEXT,
                description TEXT,
                quantity INTEGER DEFAULT 0,
                price DECIMAL(10,2) DEFAULT 0.00,
                cost_price DECIMAL(10,2) DEFAULT 0.00,
                min_stock_level INTEGER DEFAULT 5,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stock transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_id INTEGER,
                transaction_type TEXT, -- 'IN' or 'OUT'
                quantity INTEGER,
                price DECIMAL(10,2),
                reference TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (stock_id) REFERENCES stock(id)
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE,
                date TEXT,
                customer_name TEXT,
                total_amount DECIMAL(10,2),
                paid_amount DECIMAL(10,2),
                balance DECIMAL(10,2),
                payment_method TEXT,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')
        
        # Sale items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                stock_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                total_price DECIMAL(10,2),
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (stock_id) REFERENCES stock(id)
            )
        ''')
        
        # Debts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT,
                total_amount DECIMAL(10,2) DEFAULT 0.00,
                paid_amount DECIMAL(10,2) DEFAULT 0.00,
                balance DECIMAL(10,2) DEFAULT 0.00,
                due_date DATE,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Debt payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS debt_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                debt_id INTEGER,
                amount DECIMAL(10,2),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT,
                notes TEXT,
                FOREIGN KEY (debt_id) REFERENCES debts(id)
            )
        ''')
        
        # Accounting transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounting_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT, -- 'income' or 'expense'
                category TEXT,
                amount DECIMAL(10,2),
                description TEXT,
                reference TEXT,
                transaction_date TEXT, -- Store as DD/MM/YYYY
                created_by INTEGER,
                is_auto INTEGER DEFAULT 0, -- 0 = manual, 1 = auto
                related_sale_id INTEGER,
                related_debt_id INTEGER,
                related_stock_id INTEGER,
                FOREIGN KEY (created_by) REFERENCES users(id),
                FOREIGN KEY (related_sale_id) REFERENCES sales(id),
                FOREIGN KEY (related_debt_id) REFERENCES debts(id),
                FOREIGN KEY (related_stock_id) REFERENCES stock(id)
            )
        ''')
        
        # Insert default admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                ('admin', '1234', 'Administrator', 'admin')
            )
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_stock_stats(self):
        query = '''
            SELECT 
                COUNT(*) as total_items,
                SUM(quantity) as total_quantity,
                SUM(quantity * price) as total_value,
                SUM(CASE WHEN quantity <= min_stock_level THEN 1 ELSE 0 END) as low_stock_items
            FROM stock
        '''
        return self.fetch_one(query)
    
    def get_today_sales_stats(self):
        query = '''
            SELECT 
                COUNT(*) as total_sales,
                SUM(total_amount) as total_amount,
                SUM(paid_amount) as total_paid,
                SUM(balance) as total_balance
            FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        '''
        return self.fetch_one(query)
    
    def get_debt_stats(self):
        query = '''
            SELECT 
                COUNT(*) as total_debts,
                SUM(total_amount) as total_debt_amount,
                SUM(paid_amount) as total_paid,
                SUM(balance) as total_balance
            FROM debts
            WHERE status = 'pending'
        '''
        return self.fetch_one(query)