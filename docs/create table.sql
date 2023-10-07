-- Create the Addresses table
CREATE TABLE Addresses (
    AddressID INTEGER PRIMARY KEY AUTOINCREMENT,
    AddressText VARCHAR(255) NOT NULL
);

-- Create the Meters table
CREATE TABLE Meters (
    MeterID INTEGER PRIMARY KEY AUTOINCREMENT,
    MeterName VARCHAR(255),
    AddressID INT,
    FOREIGN KEY (AddressID) REFERENCES Addresses(AddressID)
);

-- Create the Readings table
CREATE TABLE Readings (
    ReadingID INTEGER PRIMARY KEY AUTOINCREMENT,
    MeterID INT,
    ReadingValue INT NOT NULL,
    ReadingDate DATE NOT NULL,
    FOREIGN KEY (MeterID) REFERENCES Meters(MeterID)
);

CREATE UNIQUE INDEX IF NOT EXISTS MeterReadingDate on Readings (MeterID, ReadingDate)
