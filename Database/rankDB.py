import sqlite3

# SQLite database file path
DB_FILE = "Database/levels.db"

def create_rank_db():
    """Creates the database and the required tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the levels table (per user per guild)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS levels (
        user_id INTEGER,
        guild_id INTEGER,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, guild_id)
    );
    """)

    conn.commit()
    conn.close()

def get_user_level(user_id, guild_id):
    """Fetches the user's level and XP. Creates a new entry if not found."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT level, xp FROM levels WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    result = cursor.fetchone()

    if result is None:
        # If user does not exist, insert with default level and xp
        cursor.execute("INSERT INTO levels (user_id, guild_id, level, xp) VALUES (?, ?, 1, 0)", (user_id, guild_id))
        conn.commit()
        conn.close()
        return {"level": 1, "xp": 0}

    conn.close()
    return {"level": result[0], "xp": result[1]}

def add_xp(user_id, guild_id, xp_to_add):
    """Adds XP to the user and checks for level up."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get current level and XP
    user_data = get_user_level(user_id, guild_id)
    current_xp = user_data["xp"]
    level = user_data["level"]

    # Calculate new XP total
    new_xp = current_xp + xp_to_add

    # XP requirement increases with each level
    xp_required = 20 + (level * 50)

    # Check for level up
    if new_xp >= xp_required:
        level += 1
        new_xp -= xp_required  # Remaining XP carries over
        cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?", (new_xp, level, user_id, guild_id))
        conn.commit()
        conn.close()
        return level, new_xp

    # Update only XP if no level up
    cursor.execute("UPDATE levels SET xp = ? WHERE user_id = ? AND guild_id = ?", (new_xp, user_id, guild_id))
    conn.commit()
    conn.close()

    return level, new_xp
