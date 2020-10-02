-- Customer is same as User 
CREATE TABLE Customer(
    user_id CHAR(22) PRIMARY KEY,
    name VARCHAR(100),
    yelping_since TIMESTAMP,
   	average_stars FLOAT,
	fans INT,
	tipcount INT
);

CREATE TABLE Business (
    business_id CHAR(22) PRIMARY KEY,
    name VARCHAR(225),
    address VARCHAR(225),
    city VARCHAR(50),
	state CHAR(2),
	postal_code INT,
	latitude FLOAT,
	longitude FLOAT,
	stars FLOAT,
	review_count INT,
	is_open BOOL
);

CREATE TABLE Category (
	type VARCHAR(255) PRIMARY KEY
);

CREATE TABLE YelpTip (
	business_id CHAR(22),
	user_id CHAR(22),
	date TIMESTAMP,
	likes INT,
	text TEXT,
	PRIMARY KEY (business_id,user_id),
	FOREIGN KEY (business_id) REFERENCES Business(business_id),
	FOREIGN KEY (user_id) REFERENCES Customer(user_id)
);

CREATE TABLE YelpCheckIn (
	business_id CHAR(22),
	date DATE,
	time TIME,
	PRIMARY KEY (business_id, date, time),
	FOREIGN KEY (business_id) REFERENCES Business(business_id)
);