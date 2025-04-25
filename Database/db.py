import sqlite3
import discord
import datetime

# Function to establish and return a database connection
def get_db():
    conn = sqlite3.connect('Database/bot_database.db')
    conn.row_factory = sqlite3.Row  # Enables name-based access to columns
    return conn

# Function to set up the required tables in the database
def setup_database():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Create 'users' table with composite unique constraint (user_id + guild_id)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            username TEXT,
            join_date TEXT,
            guild_id INTEGER,
            UNIQUE(user_id, guild_id)
        )
        ''')

        conn.commit()
    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")
    finally:
        conn.close()


# Function to add a new user to the database or update the username if already exists
def add_user_to_database(member):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if user already exists for the given guild
        cursor.execute("SELECT * FROM users WHERE user_id = ? AND guild_id = ?", 
                      (member.id, member.guild.id))
        existing_user = cursor.fetchone()

        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not existing_user:
            cursor.execute('''
                INSERT INTO users (user_id, username, join_date, guild_id)
                VALUES (?, ?, ?, ?)
            ''', (member.id, member.name, join_date, member.guild.id))
            print(f"User added: {member.name}")
        else:
            if existing_user['username'] != member.name:
                cursor.execute('''
                    UPDATE users
                    SET username = ?
                    WHERE user_id = ? AND guild_id = ?
                ''', (member.name, member.id, member.guild.id))
                print(f"Username updated: {existing_user['username']} -> {member.name}")

        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding/updating user: {e}")
    finally:
        conn.close()
