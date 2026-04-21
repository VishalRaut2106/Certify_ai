#!/usr/bin/env python3
import sqlite3
import json

conn = sqlite3.connect('certificate_verification.db')
cursor = conn.cursor()

# Get a sample certificate to check the data format
cursor.execute("SELECT * FROM certificates WHERE verification_status != 'pending' LIMIT 1")
result = cursor.fetchone()

if result:
    columns = [description[0] for description in cursor.description]
    cert_dict = dict(zip(columns, result))
    
    print('Sample Certificate Data:')
    print('=' * 50)
    for key, value in cert_dict.items():
        if key == 'metadata' and value:
            print(f'{key}: {str(value)[:100]}...')
        else:
            print(f'{key}: {value}')
else:
    print('No processed certificates found')

conn.close()