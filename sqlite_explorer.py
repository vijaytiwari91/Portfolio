# SQLite3 Database Explorer for Django Project
# Run this script in your Django project directory

import sqlite3
import os
from tabulate import tabulate  # You might need to install: pip install tabulate

def explore_database():
    # Path to your SQLite database
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("Database file not found! Make sure you're in the Django project directory.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== EXPLORING YOUR DJANGO DATABASE ===\n")
    
    # 1. Get all table names
    print("1. ALL TABLES IN YOUR DATABASE:")
    print("-" * 40)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_names = []
    for table in tables:
        table_name = table[0]
        table_names.append(table_name)
        print(f"• {table_name}")
    
    print(f"\nTotal tables: {len(table_names)}\n")
    
    # 2. For each table, show structure and data
    for table_name in table_names:
        print(f"=== TABLE: {table_name} ===")
        
        # Get table structure
        print("\nTable Structure:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print("Column Name       | Type        | Not Null | Default")
        print("-" * 55)
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            not_null = "YES" if col[3] else "NO"
            default = col[4] if col[4] else "None"
            print(f"{col_name:<17} | {col_type:<11} | {not_null:<8} | {default}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        print(f"\nTotal rows: {row_count}")
        
        # Show sample data (first 5 rows)
        if row_count > 0:
            print("\nSample Data (first 5 rows):")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            
            # Get column names for headers
            column_names = [col[1] for col in columns]
            
            if rows:
                print(tabulate(rows, headers=column_names, tablefmt="grid"))
            else:
                print("No data found.")
        else:
            print("No data in this table.")
        
        print("\n" + "="*60 + "\n")
    
    conn.close()
    print("Database exploration complete!")

def show_specific_table(table_name):
    """Function to show all data from a specific table"""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get all data from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n=== ALL DATA FROM {table_name} ===")
        if rows:
            print(tabulate(rows, headers=column_names, tablefmt="grid"))
        else:
            print("No data found in this table.")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def search_table_data(table_name, search_column, search_value):
    """Function to search for specific data in a table"""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {search_column} LIKE ?;", (f"%{search_value}%",))
        rows = cursor.fetchall()
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n=== SEARCH RESULTS FROM {table_name} ===")
        if rows:
            print(tabulate(rows, headers=column_names, tablefmt="grid"))
        else:
            print("No matching data found.")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Run the main exploration
    explore_database()
    
    # Example usage for specific table
    # show_specific_table('auth_user')
    
    # Example usage for searching
    # search_table_data('auth_user', 'username', 'admin')