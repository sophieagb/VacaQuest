from .utils import get_db_connection


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
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )

    # Create travel_plans table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS travel_plans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        destination VARCHAR(100),
        plan_details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()
