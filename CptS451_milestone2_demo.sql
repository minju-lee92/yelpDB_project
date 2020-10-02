
--GLOSSARY
--table names
businesstable
usertable
tipstable
friendstable
checkin
businesscategory
businessattribute
businesshours

--some attribute names
zipcode
business_id
city  (business city)
name   (business name)
user_id
friend_id
numtips
numCheckins

user_id
tipcount  (user)
totallikes (user)

tipdate
tiptext
likes  (tip)

checkinyear
checkinmonth
checkinday
checkintime


--1.
SELECT COUNT(*) 
FROM  business;
SELECT COUNT(*) 
FROM  users;
SELECT COUNT(*) 
FROM  yelptip;
SELECT COUNT(*) 
FROM  friends;
SELECT COUNT(*) 
FROM  yelpcheckin;
SELECT COUNT(*) 
FROM  hascategory;
------------------------
-- team of 2 doesn't include this table
--SELECT COUNT(*)
--FROM  businessattribute;
-----------------------
SELECT COUNT(*) 
FROM  hashours;



--2. Run the following queries on your business table, checkin table and review table. Make sure to change the attribute names based on your schema. 

SELECT zip_code, count(business_id)
FROM business
GROUP BY zip_code
HAVING count(business_id) > 500
ORDER BY zip_code;

SELECT zip_code, COUNT(distinct C.category_type)
FROM business as B, hascategory as C
WHERE B.business_id = C.business_id
GROUP BY zip_code
HAVING count(distinct C.category_type)>300
ORDER BY zip_code;

----------------------------------------------
--SELECT zip_code, COUNT(distinct A.attribute)
--FROM businesstable as B, businessattribute as A
--WHERE B.business_id = A.business_id
--GROUP BY zipcode
--HAVING count(distinct A.attribute)>65;


--3. Run the following queries on your business table, checkin table and tips table. Make sure to change the attribute names based on your schema. 

SELECT users.user_id, count(friend_id)
FROM users, friends
WHERE users.user_id = friends.user_id AND
      users.user_id = 'zvQ7B3KZuFOX7pYLsOxhpA'
GROUP BY users.user_id;


SELECT business_id, business_name, city, num_of_tips, num_of_checkins
FROM business
WHERE business_id ='UvF68aNDfzCWQbxO6-647g' ;

SELECT user_id, user_name, tip_count, totalLikes
FROM users
WHERE user_id = 'i3bLA4sEdFk8j3Pq6tx8wQ'

-----------

SELECT COUNT(*) 
FROM yelpcheckin
WHERE business_id ='UvF68aNDfzCWQbxO6-647g';

SELECT count(*)
FROM yelptip
WHERE  business_id = 'UvF68aNDfzCWQbxO6-647g';



--4. 
--Type the following statements. Make sure to change the attribute names based on your schema. 

SELECT COUNT(*) 
FROM yelpcheckin
WHERE business_id ='M007_bAIM34x1yd138zhSQ';

SELECT business_id, business_name, city, num_of_checkins, num_of_tips
FROM business
WHERE business_id ='M007_bAIM34x1yd138zhSQ';

INSERT INTO yelpcheckin (business_id, checkin_year,checkin_month, checkin_day,checkin_time)
VALUES ('M007_bAIM34x1yd138zhSQ',’2020’,’03’,'27','15:00');


--5.
--Type the following statements. Make sure to change the attribute names based on your schema.  

SELECT business_id,business_name, city, num_of_checkins, num_of_tips
FROM business
WHERE business_id ='M007_bAIM34x1yd138zhSQ';

SELECT user_id, user_name, tip_count, totalLikes
FROM users
WHERE user_id = 'rRrFcSEZOTw6iZagsIwTFQ'


INSERT INTO yelptip (user_id, business_id, tip_date, tip_text, num_of_likes)
VALUES ('rRrFcSEZOTw6iZagsIwTFQ','M007_bAIM34x1yd138zhSQ', '2020-03-27 13:00','EVERYTHING IS AWESOME',0);

UPDATE yelptip
SET num_of_likes = num_of_likes+1
WHERE user_id = 'rRrFcSEZOTw6iZagsIwTFQ' AND 
      business_id = 'M007_bAIM34x1yd138zhSQ' AND 
      tip_date ='2020-03-27 13:00'
      