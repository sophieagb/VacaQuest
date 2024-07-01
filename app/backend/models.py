def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # Create user_info table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS user_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        starting_location VARCHAR(100),
        disabilities TEXT,
        phone_number VARCHAR(20),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()