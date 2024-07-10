import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Create GUI components
        self.date_label = tk.Label(root, text="Date:")
        self.date_label.grid(row=0, column=0)
        self.date_entry = tk.Entry(root, width=20)
        self.date_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(root, width=20)
        self.category_entry.grid(row=1, column=1)

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=2, column=0)
        self.amount_entry = tk.Entry(root, width=20)
        self.amount_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.report_button = tk.Button(root, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=4, column=0, columnspan=2)

        self.visualization_button = tk.Button(root, text="Visualize Expenses", command=self.visualize_expenses)
        self.visualization_button.grid(row=5, column=0, columnspan=2)

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount REAL
            )
        """)
        self.conn.commit()

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        if date and category and amount:
            self.cursor.execute("""
                INSERT INTO expenses (date, category, amount)
                VALUES (?,?,?)
            """, (date, category, amount))
            self.conn.commit()
            self.date_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def generate_report(self):
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()
        report = ""
        for expense in expenses:
            report += f"Date: {expense[1]}, Category: {expense[2]}, Amount: {expense[3]}\n"
        messagebox.showinfo("Report", report)

    def visualize_expenses(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        expenses = self.cursor.fetchall()
        categories = [expense[0] for expense in expenses]
        amounts = [expense[1] for expense in expenses]
        plt.bar(categories, amounts)
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.title("Expense Visualization")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()