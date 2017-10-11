CREATE TABLE Profile (
	username VARCHAR(50) NOT NULL,
	firstName VARCHAR(20) NOT NULL,
	lastName VARCHAR(20) NOT NULL,
	gender ENUM('Male', 'Female', 'Other') NOT NULL,
	accountType ENUM('Student', 'Businessman', 'Tourist', 'Premium') NOT NULL,
	phoneNumber CHAR(10) NOT NULL,
	residentialAddress VARCHAR(200) NOT NULL,
	password CHAR(256) NOT NULL,
	emailAddress VARCHAR(200) NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE Locations (
	locationName VARCHAR(100) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	locationAddress VARCHAR(200) NOT NULL,
	locationBio VARCHAR(300) NOT NULL,
	locationType ENUM('Library', 'Hotel', 'Museum', 'University', 'Public') NOT NULL,
	locationImagePath VARCHAR(200) NOT NULL,
	PRIMARY KEY (locationName)
);

CREATE TABLE Reviews (
	reviewID INT(30) NOT NULL,
	locationName VARCHAR(100) NOT NULL,
	reviewBio VARCHAR(300) NOT NULL,
	reviewRating ENUM('1', '2', '3', '4', '5') NOT NULL,
	username VARCHAR(50) NOT NULL,
	favouriteStatus BOOLEAN NOT NULL,
	PRIMARY KEY (reviewID),
	FOREIGN KEY (locationName) REFERENCES Locations(locationName),
	FOREIGN KEY (username) REFERENCES Profiles(username),
);

CREATE TABLE Admin_Profile (
	username VARCHAR(50) NOT NULL,
	firstName VARCHAR(20) NOT NULL,
	lastName VARCHAR(20) NOT NULL,
	password CHAR(256) NOT NULL,
	staffStatus BOOLEAN NOT NULL,
	emailAddress VARCHAR(200) NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE Favourites (
	favouriteID INT(30) NOT NULL,	
	PRIMARY KEY (favouriteID),
);

CREATE TABLE Bug_Report (
	reportID INT(30) NOT NULL,
	subject VARCHAR(50) NOT NULL,
	description VARCHAR(300) NOT NULL,
	PRIMARY KEY (reportID)
);