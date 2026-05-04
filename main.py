from guests import add_guest, update_guest, list_guests
from rooms import list_rooms, update_room, available_rooms
from bookings import (make_booking, auto_assign_booking, find_available_rooms, 
                      check_room_availability, checkin, checkout, list_bookings, 
                      guest_booking_history)
from invoices import generate_invoice, list_invoices, unpaid_invoices, mark_invoice_paid
from reports import room_availability_report, revenue_report, service_usage_report, occupied_rooms_report
from services import add_service, list_services, assign_service_to_booking, view_booking_services

def main():
    while True:
        print("\n" + "="*30)
        print("   HOTEL MANAGEMENT SYSTEM   ")
        print("="*30)
        print("1. Guest Management")
        print("2. Room Management")
        print("3. Service Management")
        print("4. Booking Management")
        print("5. Invoice Management")
        print("6. Reports & Views")
        print("0. Exit")
        choice = input("Choose: ")

        if choice == '1':
            print("\n1. Add Guest  2. Update Guest  3. List Guests")
            c = input("Choose: ")
            if c == '1': add_guest()
            elif c == '2': update_guest()
            elif c == '3': list_guests()

        elif choice == '2':
            print("\n1. List Rooms  2. Update Room  3. Available Rooms")
            c = input("Choose: ")
            if c == '1': list_rooms()
            elif c == '2': update_room()
            elif c == '3': available_rooms()

        elif choice == '3':
            print("\n1. Add Service  2. List Services  3. Assign Service to Booking  4. View Booking Services")
            c = input("Choose: ")
            if c == '1': add_service()
            elif c == '2': list_services()
            elif c == '3': assign_service_to_booking()
            elif c == '4': view_booking_services()

        elif choice == '4':
            print("\n1. New Booking (Manual Room)")
            print("2. New Booking (Auto Assign Room)")
            print("3. Find Available Rooms")
            print("4. Check Room Availability")
            print("5. Check-in")
            print("6. Check-out")
            print("7. List Bookings")
            print("8. Guest Booking History")
            c = input("Choose: ")
            
            if c == '1': make_booking()
            elif c == '2': auto_assign_booking()
            elif c == '3': find_available_rooms()
            elif c == '4': check_room_availability()
            elif c == '5': checkin()
            elif c == '6': checkout()
            elif c == '7': list_bookings()
            elif c == '8': guest_booking_history()

        elif choice == '5':
            print("\n1. Generate Invoice  2. List Invoices  3. Unpaid Invoices  4. Mark Invoice Paid")
            c = input("Choose: ")
            if c == '1': generate_invoice()
            elif c == '2': list_invoices()
            elif c == '3': unpaid_invoices()
            elif c == '4': mark_invoice_paid()

        elif choice == '6':
            print("\n1. Room Availability Report  2. Revenue Report  3. Service Usage Report")
            print("4. Occupied Rooms (View 1)  5. Unpaid Invoices (View 2)  6. Guest Booking History (View 3)")
            c = input("Choose: ")
            if c == '1': room_availability_report()
            elif c == '2': revenue_report()
            elif c == '3': service_usage_report()
            elif c == '4': occupied_rooms_report()
            elif c == '5': unpaid_invoices()
            elif c == '6': guest_booking_history()

        elif choice == '0':
            print("Goodbye! Have a great day!")
            break

if __name__ == "__main__":
    main()