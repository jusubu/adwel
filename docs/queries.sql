--
-- Insert Reading data (MeterName,AddressText,ReadingValue,ReadingDate)
--

PRAGMA foreign_keys = ON; -- Enable foreign key constraints if not enabled

-- Step 1: Insert the AddressText into the Addresses table (if it doesn't exist)
-- Replace 'YourAddressText' with the actual address text
INSERT OR IGNORE INTO Addresses (AddressText) VALUES ('A14');

-- Step 2: Insert the MeterName into the Meters table (if it doesn't exist)
-- Replace 'YourMeterName' with the actual meter name
INSERT OR IGNORE INTO Meters (MeterName, AddressID)
SELECT 'A14_E03@22', AddressID
FROM Addresses
WHERE AddressText = 'A14';

-- Step 3: Insert the reading into the Readings table
-- Replace 'YourMeterName', 123, and '2023-09-09' with the actual values
INSERT OR IGNORE INTO Readings (MeterID, ReadingValue, ReadingDate)
VALUES (
    (SELECT MeterID FROM Meters WHERE MeterName = 'A14_E03@22'),
    336684,  -- Integer value
    '2023-09-10T00:00:00'
);


--
-- Get usage for given AddressText between StartDate and EndDate
--

WITH StartEndReadings AS (
    SELECT
        Meters.MeterID,
        Meters.MeterName,
        (
            SELECT ReadingValue
            FROM Readings AS StartReading
            WHERE StartReading.MeterID = Meters.MeterID
                AND StartReading.ReadingDate = (
                    SELECT MIN(ReadingDate)
                    FROM Readings
                    WHERE MeterID = Meters.MeterID
                        AND ReadingDate >= '2023-09-01T00:00:00' -- Replace with the desired StartDate
                )
        ) AS StartReadingValue,
        (
            SELECT ReadingValue
            FROM Readings AS EndReading
            WHERE EndReading.MeterID = Meters.MeterID
                AND EndReading.ReadingDate = (
                    SELECT MAX(ReadingDate)
                    FROM Readings
                    WHERE MeterID = Meters.MeterID
                        AND ReadingDate <= '2023-09-10T00:00:00' -- Replace with the desired Enddate
                )
        ) AS EndReadingValue
    FROM
        Meters
    JOIN
        Addresses ON Meters.AddressID = Addresses.AddressID
    WHERE
        Addresses.AddressText = 'A19'  -- Replace with the desired AddressText
)
SELECT
    MeterID,
    MeterName,
	EndReadingValue,
	StartReadingValue,
    (EndReadingValue - StartReadingValue) AS ReadingValueDifference
FROM
    StartEndReadings;


--
-- Get latest ReadingValue(s) for given AddressText
--

SELECT r.ReadingValue
FROM Readings r
INNER JOIN Meters m ON r.MeterID = m.MeterID
INNER JOIN Addresses a ON m.AddressID = a.AddressID
WHERE a.AddressText = 'A19'  -- Replace with the desired AddressText
AND r.ReadingDate = (
    SELECT MAX(r2.ReadingDate)
    FROM Readings r2
    INNER JOIN Meters m2 ON r2.MeterID = m2.MeterID
    INNER JOIN Addresses a2 ON m2.AddressID = a2.AddressID
    WHERE a2.AddressText = 'A19'  -- Replace with the desired AddressText
);

-- sqlalchemy -> sqlitis
-- select([r.c.ReadingValue]).select_from(Readings.join(Meters, r.c.MeterID == m.c.MeterID).join(Addresses, m.c.AddressID == a.c.AddressID)).where(and_(a.c.AddressText == text('A19'), r.c.ReadingDate == select([Readings.join(Meters, r2.c.MeterID == m2.c.MeterID).join(Addresses, m2.c.AddressID == a2.c.AddressID)]).where(a2.c.AddressText == text('A19'))))