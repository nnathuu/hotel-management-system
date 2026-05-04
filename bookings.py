from db import get_connection
from datetime import date

def make_booking():
    guest_id = input("Guest ID: ")
    room_id = input("Room ID: ")
    checkin = input("Check-in Date (YYYY-MM-DD): ")
    checkout = input("Check-out Date (YYYY-MM-DD): ")
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if room is available before booking
    cursor.execute("SELECT IsRoomAvailable(%s, %s, %s)", (room_id, checkin, checkout))
    is_available = cursor.fetchone()[0]
    
    if is_available == 0:
        print("Room is not available for this period!")
        conn.close()
        return
    
    cursor.execute(
        "INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate) VALUES (%s,%s,%s,%s)",
        (guest_id, room_id, checkin, checkout)
    )
    conn.commit()
    print("Booking created! Trigger will auto-update room status to Occupied.")
    conn.close()

def auto_assign_booking():
    """Automatically assign an available room instead of manually entering RoomID"""
    guest_id = input("Guest ID: ")
    checkin = input("Check-in Date (YYYY-MM-DD): ")
    checkout = input("Check-out Date (YYYY-MM-DD): ")
    
    print("\nPreferred room type:")
    print("1. Single")
    print("2. Double")
    print("3. Suite")
    room_type_choice = input("Choose (1-3): ")
    
    room_type_map = {'1': 'Single', '2': 'Double', '3': 'Suite'}
    preferred_type = room_type_map.get(room_type_choice, 'Single')
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.callproc('AutoAssignRoom', (guest_id, checkin, checkout, preferred_type))
        
        # Get result from procedure
        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                room_id, price = rows[0]
                print(f"\nAuto-assigned Room {room_id} (Price: {price:,.0f} VND)")
        
        conn.commit()
        print("Booking created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

def find_available_rooms():
    """Find available rooms by date and room type"""
    checkin = input("Check-in Date (YYYY-MM-DD): ")
    checkout = input("Check-out Date (YYYY-MM-DD): ")
    
    print("\nRoom type (leave empty for all):")
    print("1. Single  2. Double  3. Suite  0. All")
    choice = input("Choose: ")
    
    room_type = None
    if choice == '1': room_type = 'Single'
    elif choice == '2': room_type = 'Double'
    elif choice == '3': room_type = 'Suite'
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc('FindAvailableRooms', (checkin, checkout, room_type))
    
    print(f"\n--- AVAILABLE ROOMS ({checkin} to {checkout}) ---")
    
    # Get results from procedure
    available = False
    for result in cursor.stored_results():
        rows = result.fetchall()
        if rows:
            available = True
            for row in rows:
                print(f"  Room {row[0]} | {row[1]} | {row[2]:,.0f} VND")
    
    if not available:
        print("  No rooms available for this period.")
    
    conn.close()

def check_room_availability():
    """Check if a specific room is available"""
    room_id = input("Room ID: ")
    checkin = input("Check-in Date (YYYY-MM-DD): ")
    checkout = input("Check-out Date (YYYY-MM-DD): ")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT IsRoomAvailable(%s, %s, %s)", (room_id, checkin, checkout))
    is_available = cursor.fetchone()[0]
    
    if is_available == 1:
        print(f"Room {room_id} is AVAILABLE from {checkin} to {checkout}")
    else:
        print(f"Room {room_id} is NOT AVAILABLE from {checkin} to {checkout}")
    
    conn.close()

def checkin():
    booking_id = input("Booking ID to Check-in: ")
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if booking exists
    cursor.execute("SELECT BookingID FROM Bookings WHERE BookingID = %s", (booking_id,))
    if not cursor.fetchone():
        print("Booking not found!")
        conn.close()
        return
    
    cursor.execute("CALL CheckIn(%s)", (booking_id,))
    conn.commit()
    print("Checked in! Room is now Occupied.")
    conn.close()

def checkout():
    booking_id = input("Booking ID to Check-out: ")
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get booking details
    cursor.execute("""
        SELECT b.GuestID, b.RoomID, b.CheckInDate, b.CheckOutDate, r.Price
        FROM Bookings b
        JOIN Rooms r ON b.RoomID = r.RoomID
        WHERE b.BookingID = %s
    """, (booking_id,))
    booking = cursor.fetchone()
    if not booking:
        print("Booking not found!")
        conn.close()
        return
    
    guest_id, room_id, checkin, checkout, room_price = booking
    
    # Calculate room cost using function
    cursor.execute("SELECT CalculateBookingCost(%s, %s, %s)", (room_id, checkin, checkout))
    room_cost = cursor.fetchone()[0]
    
    # Calculate service cost
    cursor.execute("""
        SELECT COALESCE(SUM(s.Price), 0)
        FROM Services s
        JOIN BookingServices bs ON s.ServiceID = bs.ServiceID
        WHERE bs.BookingID = %s
    """, (booking_id,))
    service_cost = cursor.fetchone()[0]
    
    total = room_cost + service_cost
    
    # Apply discount if any (10% for long stay > 5 days)
    days = (checkout - checkin).days
    discount_pct = 10 if days > 5 else 0
    
    cursor.execute("SELECT ApplyDiscount(%s, %s)", (total, discount_pct))
    final_total = cursor.fetchone()[0]
    
    print(f"\n--- CHECKOUT SUMMARY ---")
    print(f"  Check-in: {checkin}")
    print(f"  Check-out: {checkout}")
    print(f"  Nights stayed: {days}")
    print(f"  Room cost: {room_cost:,.0f} VND")
    print(f"  Service cost: {service_cost:,.0f} VND")
    print(f"  Discount: {discount_pct}%")
    print(f"  TOTAL: {final_total:,.0f} VND")
    
    # Generate invoice
    cursor.execute("CALL GenerateInvoice(%s, %s)", (guest_id, final_total))
    
    # Update room status to Available
    cursor.execute("CALL CheckOut(%s)", (booking_id,))
    conn.commit()
    print("Checked out! Invoice generated. Room is now Available.")
    conn.close()

def list_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BookingID, g.GuestName, r.RoomType, b.CheckInDate, b.CheckOutDate
        FROM Bookings b
        JOIN Guests g ON b.GuestID = g.GuestID
        JOIN Rooms r ON b.RoomID = r.RoomID
        LIMIT 20
    """)
    print("\n--- BOOKINGS ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Guest: {row[1]} | Room: {row[2]} | In: {row[3]} | Out: {row[4]}")
    conn.close()

def guest_booking_history():
    """View 3: Guest Booking History"""
    guest_id = input("Guest ID: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT GuestName, RoomType, CheckInDate, CheckOutDate FROM GuestBookingHistory WHERE GuestID = %s", (guest_id,))
    print(f"\n--- BOOKING HISTORY FOR GUEST {guest_id} ---")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"  Guest: {row[0]} | Room: {row[1]} | In: {row[2]} | Out: {row[3]}")
    else:
        print("  No booking history found.")
    conn.close()