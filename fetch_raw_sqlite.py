#!/usr/bin/env python
# filepath: c:\Code\Hobbies\Portfolio-Vijay\fetch_raw_sqlite.py

import sqlite3
import json
import os

def fetch_all_tables():
    """Fetch all data from the SQLite3 database using raw SQL queries"""
    
    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    # Set row factory to return dict-like objects
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    tables = [t for t in tables if not t.startswith('sqlite_') and not t.startswith('django_')]
    
    # Dictionary to hold all data
    all_data = {}
    
    print(f"Found {len(tables)} tables in the database:")
    for table in sorted(tables):
        print(f"- {table}")
    
    print("\nFetching data from each table...")
    # For each table, get all rows
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            # Convert rows to dictionaries
            table_data = [{k: row[k] for k in row.keys()} for row in rows]
            all_data[table] = table_data
            print(f"  - {table}: {len(table_data)} rows")
        except sqlite3.Error as e:
            print(f"Error fetching data from {table}: {e}")
    
    # Save to JSON file
    with open('raw_database_data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    
    print("\nAll data has been fetched and saved to 'raw_database_data.json'")
    
    # Now print schema for each table
    print("\n--- Database Schema ---")
    for table in sorted(tables):
        try:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"\nTable: {table}")
            print("-" * (len(table) + 7))
            for col in columns:
                print(f"  - {col['name']} ({col['type']})")
        except sqlite3.Error as e:
            print(f"Error fetching schema for {table}: {e}")
    
    # Close connection
    conn.close()

def query_specific_table(table_name):
    """Query a specific table with custom SQL"""
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No data found in table '{table_name}'")
            return
            
        # Get column names
        column_names = rows[0].keys()
        
        # Print header
        print(f"\nData from {table_name}:")
        print("-" * 80)
        print(" | ".join(column_names))
        print("-" * 80)
        
        # Print rows
        for row in rows:
            values = [str(row[col]) for col in column_names]
            print(" | ".join(values))
            
    except sqlite3.Error as e:
        print(f"Error querying table {table_name}: {e}")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # If a table name is provided, query just that table
        query_specific_table(sys.argv[1])
    else:
        # Otherwise fetch all tables
        fetch_all_tables()
