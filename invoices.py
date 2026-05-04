from db import get_connection

def generate_invoice():
    guest_id = input("Guest ID: ")
    amount = input("Total Amount: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CALL GenerateInvoice(%s, %s)", (guest_id, amount))
    conn.commit()
    print("Invoice generated!")
    conn.close()

def list_invoices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Invoices LIMIT 20")
    print("\n--- INVOICES ---")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | Guest: {row[1]} | Amount: {row[2]:,.0f} VND | Date: {row[3]}")
    conn.close()

def unpaid_invoices():
    """View 2: Unpaid Invoices (PaymentDate is NULL)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UnpaidInvoices")
    print("\n--- UNPAID INVOICES ---")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"  Invoice ID: {row[0]} | Guest: {row[1]} | Amount: {row[2]:,.0f} VND")
    else:
        print("  No unpaid invoices.")
    conn.close()

def mark_invoice_paid():
    invoice_id = input("Invoice ID to mark as paid: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Invoices SET PaymentDate = CURDATE() WHERE InvoiceID = %s",
        (invoice_id,)
    )
    conn.commit()
    print(f"Invoice {invoice_id} marked as paid on {date.today()}")
    conn.close()