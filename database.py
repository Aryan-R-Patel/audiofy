import sqlite3

DATABASE_FILE_NAME = "files.db"

def initialize_database():
    """
    Creates the database and an 'audio_files' table, if they do not exist. The table stores audio files in the form of BLOB.
    """
    connection = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = connection.cursor()
    command = """CREATE TABLE IF NOT EXISTS audio_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content BLOB NOT NULL
    )"""
    cursor.execute(command)
    connection.commit()
    connection.close()


def save_to_database(audio):
    """
    Saves audio data in the form of bytes into database. Returns the id of that row.
    """
    connection = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = connection.cursor()
    command = """INSERT INTO audio_files (content)
    VALUES (?)"""
    cursor.execute(command, (audio,))
    connection.commit()
    id = cursor.lastrowid
    connection.close()
    return id


def get_audio_from_database(id):
    """
    Gets the audio data from the database stored at the given 'id'.
    Returns None if no such record is found.
    """
    connection = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = connection.cursor()
    command = """SELECT content FROM audio_files WHERE id=?"""
    cursor.execute(command, (id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return row[0]
    return None