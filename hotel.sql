CREATE DATABASE IF NOT EXISTS HotelManagement;
USE HotelManagement;

-- SECTION 1: CREATE DATABASE & TABLES
CREATE TABLE Guests (
    GuestID INT AUTO_INCREMENT PRIMARY KEY,
    GuestName VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    Address VARCHAR(200)
);

CREATE TABLE Rooms (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    RoomType VARCHAR(50),
    Status ENUM('Available','Occupied','Maintenance') DEFAULT 'Available',
    Price DECIMAL(10,2)
);

CREATE TABLE Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    GuestID INT,
    RoomID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

CREATE TABLE Services (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceName VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10,2)
);

CREATE TABLE Invoices (
    InvoiceID INT AUTO_INCREMENT PRIMARY KEY,
    GuestID INT,
    TotalAmount DECIMAL(10,2),
    PaymentDate DATE,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID)
);

CREATE TABLE BookingServices (
    BookingID INT,
    ServiceID INT,
    PRIMARY KEY (BookingID, ServiceID),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);

SHOW TABLES;

-- SECTION 2: INSERT SAMPLE DATA
-- Guests (10 rows)
INSERT INTO Guests (GuestName, PhoneNumber, Address) VALUES
('Nguyen Van A',  '0901234561', 'Ha Noi'),
('Tran Thi B',    '0901234562', 'Ho Chi Minh'),
('Le Van C',      '0901234563', 'Da Nang'),
('Pham Thi D',    '0901234564', 'Hue'),
('Hoang Van E',   '0901234565', 'Can Tho'),
('Vo Thi F',      '0901234566', 'Hai Phong'),
('Dang Van G',    '0901234567', 'Vung Tau'),
('Bui Thi H',     '0901234568', 'Nha Trang'),
('Do Van I',      '0901234569', 'Quy Nhon'),
('Nguyen Thi K',  '0901234570', 'Bien Hoa');

-- Rooms (10 rows)
INSERT INTO Rooms (RoomType, Status, Price) VALUES
('Single',     'Available',   500000),
('Single',     'Available',   500000),
('Double',     'Available',   800000),
('Double',     'Occupied',    800000),
('Suite',      'Available',  1500000),
('Suite',      'Occupied',   1500000),
('Single',     'Maintenance', 500000),
('Double',     'Available',   800000),
('Suite',      'Available',  1500000),
('Double',     'Occupied',    800000);

-- Services (10 rows)
INSERT INTO Services (ServiceName, Description, Price) VALUES
('Laundry',          'Wash and iron clothes',       50000),
('Room Service',     'Food delivery to room',      100000),
('Spa',              'Full body massage',           200000),
('Airport Shuttle',  'Pick up from airport',       150000),
('Breakfast',        'Continental breakfast',        80000),
('Gym',              'Access to fitness center',    60000),
('Swimming Pool',    'Pool access all day',         70000),
('Car Rental',       'Rent a car for sightseeing', 300000),
('Dry Cleaning',     'Dry cleaning service',        90000),
('Tour Guide',       'City tour with guide',       250000);

-- Bookings (10 rows)
INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate) VALUES
(1,  1, '2024-01-10', '2024-01-13'),
(2,  3, '2024-01-11', '2024-01-15'),
(3,  5, '2024-01-12', '2024-01-14'),
(4,  8, '2024-01-13', '2024-01-16'),
(5,  2, '2024-01-14', '2024-01-17'),
(6,  4, '2024-01-15', '2024-01-18'),
(7,  6, '2024-01-16', '2024-01-20'),
(8,  9, '2024-01-17', '2024-01-19'),
(9,  3, '2024-01-18', '2024-01-21'),
(10, 7, '2024-01-19', '2024-01-22');

INSERT INTO Invoices (GuestID, TotalAmount, PaymentDate) VALUES
(1,  1650000, '2024-01-13'),
(2,  3400000, '2024-01-15'),
(3,  3200000, '2024-01-14'),
(4,  2550000, '2024-01-16'),
(5,  1840000, '2024-01-17'),
(6,  2600000, '2024-01-18'),
(7,  6500000, '2024-01-20'),
(8,  3200000, '2024-01-19'),
(9,  2650000, '2024-01-21'),
(10, 1600000, '2024-01-22');

-- BookingServices (10 rows)
INSERT INTO BookingServices (BookingID, ServiceID) VALUES
(1, 1),(2, 2),(3, 3),(4, 4),(5, 5),
(6, 6),(7, 7),(8, 8),(9, 9),(10,10);

INSERT INTO Invoices (GuestID, TotalAmount, PaymentDate)
VALUES (1, 2000000, NULL),
       (2, 3500000, NULL),
       (3, 1800000, NULL);

-- SECTION 3: FILL PROCEDURES + CALL
DELIMITER //
CREATE PROCEDURE FillGuests()
BEGIN
    DECLARE i INT DEFAULT 11;
    WHILE i <= 510 DO
        INSERT INTO Guests (GuestName, PhoneNumber, Address)
        VALUES (
            CONCAT('Guest ', i),
            CONCAT('090', LPAD(i, 7, '0')),
            ELT(1 + (i % 5), 'Ha Noi','Ho Chi Minh','Da Nang','Hue','Can Tho')
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FillRooms()
BEGIN
    DECLARE i INT DEFAULT 11;
    WHILE i <= 510 DO
        INSERT INTO Rooms (RoomType, Status, Price)
        VALUES (
            ELT(1 + (i % 3), 'Single','Double','Suite'),
            ELT(1 + (i % 3), 'Available','Occupied','Maintenance'),
            ELT(1 + (i % 3), 500000, 800000, 1500000)
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FillServices()
BEGIN
    DECLARE i INT DEFAULT 11;
    WHILE i <= 510 DO
        INSERT INTO Services (ServiceName, Description, Price)
        VALUES (
            CONCAT('Service ', i),
            CONCAT('Description for service ', i),
            (i % 10 + 1) * 50000
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FillBookings()
BEGIN
    DECLARE i INT DEFAULT 11;
    WHILE i <= 510 DO
        INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate)
        VALUES (
            1 + (i % 10),
            1 + (i % 10),
            DATE_ADD('2024-01-01', INTERVAL i DAY),
            DATE_ADD('2024-01-01', INTERVAL i+2 DAY)
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FillInvoices()
BEGIN
    DECLARE i INT DEFAULT 11;
    WHILE i <= 510 DO
        INSERT INTO Invoices (GuestID, TotalAmount, PaymentDate)
        VALUES (
            1 + (i % 10),
            (i % 10 + 1) * 500000,
            DATE_ADD('2024-01-01', INTERVAL i DAY)
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

CALL FillGuests();
CALL FillRooms();
CALL FillServices();
CALL FillBookings();
CALL FillInvoices();

SELECT COUNT(*) FROM Guests;
SELECT COUNT(*) FROM Rooms;
SELECT COUNT(*) FROM Services;
SELECT COUNT(*) FROM Bookings;
SELECT COUNT(*) FROM Invoices;


-- SECTION 4: INDEXES
CREATE INDEX idx_room_status ON Rooms(Status);
CREATE INDEX idx_booking_guest ON Bookings(GuestID);
CREATE INDEX idx_booking_checkin ON Bookings(CheckInDate);
CREATE INDEX idx_invoice_guest ON Invoices(GuestID);

-- SECTION 5: VIEWS
-- View 1: Rooms are in used
CREATE VIEW OccupiedRooms AS
SELECT r.RoomID, r.RoomType, r.Price, 
       b.CheckInDate, b.CheckOutDate, 
       g.GuestName
FROM Rooms r
JOIN Bookings b ON r.RoomID = b.RoomID
JOIN Guests g ON b.GuestID = g.GuestID
WHERE r.Status = 'Occupied';

-- View 2: Bills are not paid
CREATE VIEW UnpaidInvoices AS
SELECT i.InvoiceID, g.GuestName, i.TotalAmount
FROM Invoices i
JOIN Guests g ON i.GuestID = g.GuestID
WHERE i.PaymentDate IS NULL;

-- View 3: Booking history
CREATE VIEW GuestBookingHistory AS
SELECT g.GuestName, r.RoomType, 
       b.CheckInDate, b.CheckOutDate
FROM Bookings b
JOIN Guests g ON b.GuestID = g.GuestID
JOIN Rooms r ON b.RoomID = r.RoomID;

-- SECTION 6: STORED PROCEDURES
-- Procedure 1: Check-in
DELIMITER //
CREATE PROCEDURE CheckIn(IN p_BookingID INT)
BEGIN
    DECLARE v_RoomID INT;
    SELECT RoomID INTO v_RoomID 
    FROM Bookings WHERE BookingID = p_BookingID;
    UPDATE Rooms SET Status = 'Occupied' 
    WHERE RoomID = v_RoomID;
END //
DELIMITER ;

-- Procedure 2: Check-out
DELIMITER //
CREATE PROCEDURE CheckOut(IN p_BookingID INT)
BEGIN
    DECLARE v_RoomID INT;
    SELECT RoomID INTO v_RoomID 
    FROM Bookings WHERE BookingID = p_BookingID;
    UPDATE Rooms SET Status = 'Available' 
    WHERE RoomID = v_RoomID;
END //
DELIMITER ;

-- Procedure 3: Making bills
DELIMITER //
CREATE PROCEDURE GenerateInvoice(
    IN p_GuestID INT, 
    IN p_Amount DECIMAL(10,2))
BEGIN
    INSERT INTO Invoices (GuestID, TotalAmount, PaymentDate)
    VALUES (p_GuestID, p_Amount, CURDATE());
END //
DELIMITER ;

-- Procedure 4: find the list of available rooms by date and room type
DROP PROCEDURE IF EXISTS FindAvailableRooms;

DELIMITER //

CREATE PROCEDURE FindAvailableRooms(
    IN p_CheckIn DATE,
    IN p_CheckOut DATE,
    IN p_RoomType VARCHAR(50)
)
BEGIN
    SELECT r.RoomID, r.RoomType, r.Price
    FROM Rooms r
    WHERE (p_RoomType IS NULL OR r.RoomType = p_RoomType)
      AND r.Status != 'Maintenance'
      AND NOT EXISTS (
          SELECT 1 FROM Bookings b
          WHERE b.RoomID = r.RoomID
            AND (
                (b.CheckInDate <= p_CheckOut AND b.CheckOutDate >= p_CheckIn)
            )
      );
END //

DELIMITER ;

-- Procedure 5: auto assign room
DROP PROCEDURE IF EXISTS AutoAssignRoom;

DELIMITER //

CREATE PROCEDURE AutoAssignRoom(
    IN p_GuestID INT,
    IN p_CheckInDate DATE,
    IN p_CheckOutDate DATE,
    IN p_PreferredRoomType VARCHAR(50)
)
BEGIN
    DECLARE v_RoomID INT DEFAULT NULL;
    DECLARE v_Price DECIMAL(10,2);
    
    -- Find available room base on type
    SELECT RoomID, Price INTO v_RoomID, v_Price
    FROM Rooms 
    WHERE RoomType = p_PreferredRoomType 
      AND Status = 'Available'
    LIMIT 1;
    
    -- if not, auto find an available room
    IF v_RoomID IS NULL THEN
        SELECT RoomID, Price INTO v_RoomID, v_Price
        FROM Rooms 
        WHERE Status = 'Available'
        LIMIT 1;
    END IF;
    
    -- if there is no room
    IF v_RoomID IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No available rooms for this period';
    ELSE
        -- create booking
        INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate)
        VALUES (p_GuestID, v_RoomID, p_CheckInDate, p_CheckOutDate);
        
        -- info
        SELECT v_RoomID AS AssignedRoomID, v_Price AS RoomPrice;
    END IF;
    
END //

DELIMITER ;



-- SECTION 7: FUNCTIONS
-- Function 1: IsRoomAvaiLable
DELIMITER //

CREATE FUNCTION IsRoomAvailable(
    p_RoomID INT,
    p_CheckIn DATE,
    p_CheckOut DATE
)
RETURNS TINYINT(1)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_BookingCount INT DEFAULT 0;
    
    -- Check if the room is double-booked
    SELECT COUNT(*) INTO v_BookingCount
    FROM Bookings
    WHERE RoomID = p_RoomID
      AND (
          (CheckInDate <= p_CheckOut AND CheckOutDate >= p_CheckIn)
      );
    
    -- Return 1 if there is no overlapping booking, 0 if there is
    IF v_BookingCount = 0 THEN
        RETURN 1;  -- Available
    ELSE
        RETURN 0;  -- Not available
    END IF;
END //

DELIMITER ;
-- Function 2: Charge the room based on the number of nights
DELIMITER //
CREATE FUNCTION CalculateBookingCost(
    p_RoomID INT, 
    p_CheckIn DATE, 
    p_CheckOut DATE)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_Price DECIMAL(10,2);
    DECLARE v_Days INT;
    SELECT Price INTO v_Price 
    FROM Rooms WHERE RoomID = p_RoomID;
    SET v_Days = DATEDIFF(p_CheckOut, p_CheckIn);
    RETURN v_Price * v_Days;
END //
DELIMITER ;

-- Function 3: After discount
DELIMITER //
CREATE FUNCTION ApplyDiscount(
    p_Amount DECIMAL(10,2), 
    p_DiscountPct INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN p_Amount * (1 - p_DiscountPct / 100);
END //
DELIMITER ;

-- SECTION 8: TRIGGERS
-- Trigger 1: automatically Occupied when there is a new booking
DELIMITER //
CREATE TRIGGER AfterBookingInsert
AFTER INSERT ON Bookings
FOR EACH ROW
BEGIN
    UPDATE Rooms SET Status = 'Occupied' 
    WHERE RoomID = NEW.RoomID;
END //
DELIMITER ;

-- Trigger 2: automatically Available after deleting booking
DELIMITER //
CREATE TRIGGER AfterBookingDelete
AFTER DELETE ON Bookings
FOR EACH ROW
BEGIN
    UPDATE Rooms SET Status = 'Available' 
    WHERE RoomID = OLD.RoomID;
END //
DELIMITER ;

-- check Views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- check Procedures
SHOW PROCEDURE STATUS WHERE Db = 'HotelManagement';

-- check Functions
SHOW FUNCTION STATUS WHERE Db = 'HotelManagement';

-- check Triggers
SHOW TRIGGERS;

-- SECTION 9: SECURITY
-- create 3 user
CREATE USER 'receptionist'@'localhost' IDENTIFIED BY 'recept123';
CREATE USER 'manager'@'localhost'      IDENTIFIED BY 'manager123';
CREATE USER 'accountant'@'localhost'   IDENTIFIED BY 'account123';

-- receptionist: view + add booking, guests, rooms
GRANT SELECT, INSERT, UPDATE 
    ON HotelManagement.Guests   TO 'receptionist'@'localhost';
GRANT SELECT, INSERT, UPDATE 
    ON HotelManagement.Bookings TO 'receptionist'@'localhost';
GRANT SELECT                  
    ON HotelManagement.Rooms    TO 'receptionist'@'localhost';

-- manager: all
GRANT ALL PRIVILEGES 
    ON HotelManagement.* TO 'manager'@'localhost';

-- accountant: view & edit invoices
GRANT SELECT, INSERT, UPDATE 
    ON HotelManagement.Invoices TO 'accountant'@'localhost';

FLUSH PRIVILEGES;

-- SECTION 10: ENCRYPTION + OPTIMIZE
-- create table to save key
SET @encryption_key = 'HotelSecretKey123';
SET @phone = '0909999999';
-- encrypt
SELECT HEX(AES_ENCRYPT(@phone, @encryption_key)) AS Encrypted_HEX;
SELECT CAST(AES_DECRYPT(AES_ENCRYPT(@phone, @encryption_key), @encryption_key) AS CHAR) AS Decrypted;

SELECT User, Host FROM mysql.user 
WHERE User IN ('receptionist','manager','accountant');

-- Check privileges for each user
SHOW GRANTS FOR 'receptionist'@'localhost';
SHOW GRANTS FOR 'manager'@'localhost';
SHOW GRANTS FOR 'accountant'@'localhost';

