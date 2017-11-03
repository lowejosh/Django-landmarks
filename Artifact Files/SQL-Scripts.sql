

INSERT INTO AdminViewer VALUES (user, firstName, lastName, gender, accountType, dateOfBirth, email, phoneNumber, address);

INSERT INTO Bug VALUES (subject, description);

INSERT INTO LocationSuggestion VALUES (locationName, latitude, longitude, locationAddress, locationBio, locationType, locationImagePath);

INSERT INTO Location VALUES (locationName, latitude, longitude, locationAddress, locationBio, locationType, locationImagePath);

INSERT INTO PostImage VALUES (title, image, content);

INSERT INTO Profile VALUES (user, firstName, lastName, gender, accountType, dateOfBirth, email, phoneNumber, address, password);

INSERT INTO Review VALUES (user, location, reviewText, rating);

SELECT (username, password) FROM Profile;
SELECT (accountType) FROM Profile WHERE user = '';
SELECT * FROM Location;
SELECT (locationType) FROM Location WHERE locationName = '';
SELECT (locationName) FROM Location;
SELECT * FROM Review;
SELECT * FROM locationSuggestion;
SELECT (firstName, lastName, emailAddress, phoneNumber, address) FROM Profiles WHERE user = '';
SELECT * FROM PostImage WHERE title='';

UPDATE Profiles
SET firstName = 'firstName'
WHERE user = '';

UPDATE Profiles
SET lastName = 'lastName'
WHERE user = '';

UPDATE Profiles
SET emailAddress = 'emailAddress'
WHERE user = '';
 
UPDATE Profiles
SET password = 'password'
WHERE user = '';

UPDATE Location
SET locationName = 'locationName', latitude = 'latitude', longitude = 'longitude', locationAddress = 'locationAddress', locationBio = 'locationBio', locationType = 'locationType', locationImagePath = 'locationImagePath' 
WHERE locationName = '';
 
UPDATE Review
SET location = 'location', reviewText = 'reviewText', rating = 'rating'
WHERE reviewID = '';

UPDATE Tag
SET location = 'location', tagText = 'tagText'
WHERE location ='' AND tagText = '';

UPDATE LocationSuggestion
SET locationName = 'locationName', latitude = 'latitude', longitude = 'longitude', locationAddress = 'locationAddress', locationBio = 'locationBio', locationType = 'locationType', locationImagePath = 'locationImagePath' 
WHERE locationName = '';

DELETE FROM Profiles
WHERE user='';

DELETE FROM Locations
WHERE locationName='';

DELETE FROM Tags
WHERE location ='' AND tagText = '';

DELETE FROM Reviews
WHERE reviewID='';

DELETE FROM Bugs
WHERE subject = '' AND description='';

DELETE FROM Email_forms
WHERE email='';

DELETE FROM Location_suggestions
WHERE locationName='';

DELETE FROM Post_images
WHERE title='';

DELETE FROM Subscriptions
WHERE firstName = '' AND email='';

