from db import get_connection

def room_availability_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Status, COUNT(*) FROM Rooms GROUP BY Status")
    print("\n--- ROOM AVAILABILITY ---")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} rooms")
    conn.close()

def revenue_report():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute("SELECT SUM(TotalAmount), COUNT(*) FROM Invoices WHERE PaymentDate IS NOT NULL")
    row = cursor.fetchone()
    print(f"\n--- REVENUE REPORT ---")
    print(f"  Total Revenue : {row[0]:,.0f} VND")
    print(f"  Total Invoices: {row[1]}")
    
    # Monthly breakdown (2024)
    cursor.execute("""
        SELECT DATE_FORMAT(PaymentDate, '%Y-%m') as Month, 
               SUM(TotalAmount) as Revenue,
               COUNT(*) as Invoices
        FROM Invoices 
        WHERE PaymentDate IS NOT NULL
        GROUP BY DATE_FORMAT(PaymentDate, '%Y-%m')
        ORDER BY Month DESC
    """)
    print("\n--- MONTHLY BREAKDOWN (2024) ---")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:,.0f} VND ({row[2]} invoices)")
    conn.close()

def service_usage_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.ServiceName, COUNT(bs.ServiceID) as UsageCount
        FROM Services s
        JOIN BookingServices bs ON s.ServiceID = bs.ServiceID
        GROUP BY s.ServiceName
        ORDER BY UsageCount DESC
        LIMIT 10
    """)
    print("\n--- SERVICE USAGE ---")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} times")
    conn.close()

def occupied_rooms_report():
    """View 1: Currently occupied rooms"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OccupiedRooms")
    print("\n--- OCCUPIED ROOMS ---")
    for row in cursor.fetchall():
        print(f"  Room {row[0]} ({row[1]}) | Guest: {row[4]} | Until: {row[3]}")
    conn.close()