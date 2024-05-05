import pymysql

# Database connection settings
db_settings = {
    "host": "",
    "user": "",
    "password": "",
    "db": ""
}

# Function to update the status of duplicates with a limit
def update_duplicates_status(cursor, duplicates, batch_size=100):
    for i in range(0, len(duplicates), batch_size):
        # Forming a batch of IDs for update
        batch = duplicates[i:i + batch_size]
        format_strings = ','.join(['%s'] * len(batch))
        cursor.execute(f"UPDATE article SET status = 'off' WHERE id IN ({format_strings})", tuple(batch))

# Connecting to the database and extracting data
try:
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()

    cursor.execute("SELECT id, LEFT(description, 150) as snippet FROM article")
    articles = cursor.fetchall()

    # Dictionary to store the first 150 characters of descriptions and their IDs
    description_dict = {}
    duplicates = []

    for article in articles:
        article_id, snippet = article

        if snippet in description_dict:
            # Storing ID as duplicates
            duplicates.append(article_id)
        else:
            description_dict[snippet] = article_id

    # Updating the status of duplicates with a limit
    update_duplicates_status(cursor, duplicates)

    conn.commit()
    print(f"Status updated for {len(duplicates)} duplicates.")

except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if conn:
        conn.close()
