from datetime import datetime

class AccountingService:
    def __init__(self, db):
        self.db = db
    
    def record_sale_transaction(self, sale_data):
        """Automatically record a sale as income"""
        try:
            # Check if transaction already exists for this sale
            existing = self.db.fetch_one(
                "SELECT id FROM accounting_transactions WHERE related_sale_id = ?",
                (sale_data['sale_id'],)
            )
            
            if existing:
                return True  # Already recorded
            
            # Insert accounting transaction
            transaction_id = self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_sale_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'income', 
                'Sales Revenue', 
                sale_data['total_amount'], 
                f"Sale to {sale_data['customer_name']}", 
                sale_data['invoice_number'],
                sale_data['sale_date'], 
                sale_data['created_by'], 
                1, 
                sale_data['sale_id']
            ))
            
            print(f"✅ Sale transaction recorded: {sale_data['invoice_number']} - Ksh {sale_data['total_amount']:,.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error recording sale transaction: {str(e)}")
            return False
    
    def record_debt_payment_transaction(self, payment_data):
        """Automatically record a debt payment as income"""
        try:
            # Insert accounting transaction
            transaction_id = self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_debt_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'income', 
                'Debt Collections', 
                payment_data['amount'], 
                f"Payment from {payment_data['customer_name']}", 
                f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                payment_data['payment_date'], 
                payment_data['created_by'], 
                1, 
                payment_data['debt_id']
            ))
            
            print(f"✅ Debt payment recorded: {payment_data['customer_name']} - Ksh {payment_data['amount']:,.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error recording debt payment transaction: {str(e)}")
            return False
    
    def record_bad_debt_transaction(self, debt_data):
        """Record bad debt as expense when a debt is written off"""
        try:
            # Insert accounting transaction
            transaction_id = self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_debt_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'expense', 
                'Bad Debt Expense', 
                debt_data['balance'], 
                f"Bad debt write-off for {debt_data['customer_name']}", 
                f"BAD-{debt_data['debt_id']}",
                datetime.now().strftime("%d/%m/%Y"), 
                debt_data['created_by'], 
                1, 
                debt_data['debt_id']
            ))
            
            print(f"⚠️ Bad debt recorded: {debt_data['customer_name']} - Ksh {debt_data['balance']:,.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error recording bad debt transaction: {str(e)}")
            return False
    
    def record_stock_purchase_transaction(self, purchase_data):
        """Record stock purchase as expense (Cost of Goods Sold)"""
        try:
            # Insert accounting transaction
            transaction_id = self.db.execute_query('''
                INSERT INTO accounting_transactions 
                (transaction_type, category, amount, description, reference, 
                 transaction_date, created_by, is_auto, related_stock_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'expense', 
                'Cost of Goods Sold', 
                purchase_data['total_cost'], 
                f"Stock purchase: {purchase_data['item_name']} ({purchase_data['model']})", 
                purchase_data['reference'],
                purchase_data['date'], 
                purchase_data['created_by'], 
                1, 
                purchase_data['stock_id']
            ))
            
            print(f"📦 Stock purchase recorded: {purchase_data['item_name']} - Ksh {purchase_data['total_cost']:,.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error recording stock purchase transaction: {str(e)}")
            return False
    
    def get_financial_summary(self, start_date=None, end_date=None):
        """Get financial summary for given period"""
        try:
            query = '''
                SELECT 
                    SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as total_expenses,
                    COUNT(*) as total_transactions
                FROM accounting_transactions
                WHERE 1=1
            '''
            
            params = []
            
            if start_date:
                query += " AND DATE(transaction_date) >= DATE(?)"
                params.append(start_date)
            
            if end_date:
                query += " AND DATE(transaction_date) <= DATE(?)"
                params.append(end_date)
            
            result = self.db.fetch_one(query, params)
            
            if result:
                return {
                    'total_income': result[0] or 0.0,
                    'total_expenses': result[1] or 0.0,
                    'total_transactions': result[2] or 0,
                    'net_profit': (result[0] or 0.0) - (result[1] or 0.0)
                }
            
            return {'total_income': 0.0, 'total_expenses': 0.0, 'total_transactions': 0, 'net_profit': 0.0}
            
        except Exception as e:
            print(f"❌ Error getting financial summary: {str(e)}")
            return {'total_income': 0.0, 'total_expenses': 0.0, 'total_transactions': 0, 'net_profit': 0.0}