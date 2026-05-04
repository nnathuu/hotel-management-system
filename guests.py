from db import get_connection

def add_guest():
    name = input("Guest Name: ")
    phone = input("Phone Number: ")
    address = input("Address: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Guests (GuestName, PhoneNumber, Address) VALUES (%s,%s,%s)",
        (name, phone, address)
    )
    conn.commit()
    print("Guest added successfully!")
    conn.close()

def update_guest():
    guest_id = input("Enter Guest ID to update: ")
    name = input("New Name: ")
    phone = input("New Phone: ")
    address = input("New Address: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Guests SET GuestName=%s, PhoneNumber=%s, Address=%s WHERE GuestID=%s",
        (name, phone, address, guest_id)
    )
    conn.commit()
    print("Guest updated!")
    conn.close()

def list_guests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guests LIMIT 20")
    print("\n--- GUESTS ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Address: {row[3]}")
    conn.close()