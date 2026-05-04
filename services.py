from db import get_connection

def add_service():
    name = input("Service Name: ")
    desc = input("Description: ")
    price = input("Price: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Services (ServiceName, Description, Price) VALUES (%s, %s, %s)",
        (name, desc, price)
    )
    conn.commit()
    print("Service added successfully!")
    conn.close()

def list_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Services LIMIT 20")
    print("\n--- SERVICES ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Name: {row[1]} | Price: {row[3]:,.0f} VND")
    conn.close()

def assign_service_to_booking():
    booking_id = input("Booking ID: ")
    service_id = input("Service ID: ")
    conn = get_connection()
    cursor = conn.cursor()
    # Check if already exists
    cursor.execute(
        "SELECT * FROM BookingServices WHERE BookingID=%s AND ServiceID=%s",
        (booking_id, service_id)
    )
    if cursor.fetchone():
        print("Service already assigned to this booking!")
    else:
        cursor.execute(
            "INSERT INTO BookingServices (BookingID, ServiceID) VALUES (%s, %s)",
            (booking_id, service_id)
        )
        conn.commit()
        print("Service assigned to booking!")
    conn.close()

def view_booking_services():
    booking_id = input("Booking ID: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.ServiceID, s.ServiceName, s.Price
        FROM Services s
        JOIN BookingServices bs ON s.ServiceID = bs.ServiceID
        WHERE bs.BookingID = %s
    """, (booking_id,))
    print(f"\n--- SERVICES FOR BOOKING {booking_id} ---")
    total = 0
    for row in cursor.fetchall():
        print(f"  {row[1]}: {row[2]:,.0f} VND")
        total += row[2]
    print(f"  Total service cost: {total:,.0f} VND")
    conn.close()