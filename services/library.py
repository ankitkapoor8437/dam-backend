from core.db import DB

def list_all_images():
    conn = DB.get_sqlite_conn()
    conn.row_factory = lambda cursor, row: {
        "id": row[0],
        "filename": row[1],
        "filepath": row[2],
        "upload_timestamp": row[3],
        "embedded": True  # In our current sync flow, if it's in DB, it's embedded.
    }
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, filepath, upload_timestamp FROM images ORDER BY upload_timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
