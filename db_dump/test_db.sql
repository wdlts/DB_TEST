CREATE TABLE People (
	Index SERIAL PRIMARY KEY,
	FirstName VARCHAR(255) NOT NULL CHECK (FirstName <> '') CHECK (FirstName <> ' '),
	LastName VARCHAR(255) NOT NULL CHECK (LastName <> '') CHECK (LastName <> ' '),
	DateOfBirth DATE NOT NULL CHECK (DateOfBirth <= NOW())

);
