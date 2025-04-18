import MySQLdb

# Connect to MySQL without specifying a database
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="1234"
)

cursor = db.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS github_clone_crypt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

print("Database 'github_clone_crypt' created successfully!")

db.close()