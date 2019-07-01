import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()
"""
query = "SELECT * FROM users"
results = cursor.execute(query)

check_user_query = "SELECT username FROM users"
results = list(cursor.execute(check_user_query))
print(results)
for item in results:
    print(item)
"""

