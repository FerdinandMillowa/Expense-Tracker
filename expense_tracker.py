import sys
import json
import os
from datetime import datetime

FILE_NAME = 'expenses.json'

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as file:
        return json.load(file)
    
def save_expenses(expenses):
    with open(FILE_NAME, 'w') as file:
        json.dump(expenses, file, indent=4)


def add_expense(description, amount):
    expenses = load_expenses()
    try:
        amount = float(amount)
        if amount < 0:
            print("Error: Amount must be positive.")
            return
    except ValueError:
        print("Error: Amount must be a valid number.")
        return
    
    new_id = max([e['id'] for e in expenses], default=0) + 1
    new_expense = {
        'id': new_id,
        'description': description,
        'amount': amount,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id}).")

def show_summary(month=None):
    expenses = load_expenses()
    if month:
        month_str = f"-{int(month):02d}-"
        filtered = [e['amount'] for e in expenses if month_str in e['date']]
        total = sum(filtered)
        print(f"Total expenses for month {month}: ${total:.2f}")
    else:
        total = sum(e['amount'] for e in expenses)
        print(f"Total expenses: ${total:.2f}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python expense_tracker.py [add/summary/delete]")
        return
    
    command = sys.argv[1]

    if command == 'add':
        add_expense(sys.argv[2], sys.argv[3])
    elif command == 'list':
        for e in load_expenses():
            print(f"ID: {e['id']} | Description: {e['description']} | Amount: ${e['amount']:.2f} | Date: {e['date']}")
    elif command == 'summary':
        month = sys.argv[2] if len(sys.argv) > 2 else None
        show_summary(month)
    elif command == 'delete':
        expenses = load_expenses()
        try:
            expense_id = int(sys.argv[2])
            expenses = [e for e in expenses if e['id'] != expense_id]
            save_expenses(expenses)
            print(f"Expense with ID {expense_id} deleted successfully.")
        except ValueError:
            print("Error: ID must be a valid number.")

if __name__ == "__main__":
    main()