import sqlite3

def initialize_db():
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY, active BOOLEAN, dll_path TEXT, token_name TEXT)")
    conn.commit()
    conn.close()

def fetch_profiles():
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_profile_by_id(profile_id):
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def fetch_active_profile():
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE active = 1 LIMIT 1")
    profile = cursor.fetchone()
    conn.close()
    return profile

def insert_profile(active, dll_path, token_name):
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (active, dll_path, token_name) VALUES (?, ?, ?)", (active, dll_path, token_name))
    conn.commit()
    conn.close()

def update_profile(profile_id, active, dll_path, token_name):
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE profiles SET active = ?, dll_path = ?, token_name = ? WHERE id = ?", (active, dll_path, token_name, profile_id))
    cursor.execute("UPDATE profiles SET active = ? WHERE id != ?", (False, profile_id))
    conn.commit()
    conn.close()

def delete_profile(profile_id):
    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    conn.commit()
    conn.close()