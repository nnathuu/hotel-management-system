from db import get_connection

def list_rooms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Rooms LIMIT 20")
    print("\n--- ROOMS ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Type: {row[1]} | Status: {row[2]} | Price: {row[3]:,.0f} VND")
    conn.close()

def update_room():
    room_id = input("Enter Room ID to update: ")
    room_type = input("New Room Type (Single/Double/Suite): ")
    status = input("New Status (Available/Occupied/Maintenance): ")
    price = input("New Price: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Rooms SET RoomType=%s, Status=%s, Price=%s WHERE RoomID=%s",
        (room_type, status, price, room_id)
    )
    conn.commit()
    print("Room updated!")
    conn.close()

def available_rooms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Rooms WHERE Status='Available'")
    print("\n--- AVAILABLE ROOMS ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Type: {row[1]} | Price: {row[3]:,.0f} VND")
    conn.close()