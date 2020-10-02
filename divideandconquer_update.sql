---- Calculating and updating----------

-- updating number of check-ins in busines table --
UPDATE business
SET num_of_checkins = (SELECT count(*)
					   FROM yelpcheckin
					   WHERE business.business_id = yelpcheckin.business_id);

-- updating number of tips in business table --
UPDATE business
SET num_of_tips = (SELECT count(*)
				   FROM yelptip
				   WHERE business.business_id = yelptip.business_id);

-- checking the business table --
SELECT *
From business;

-- updating total likes and tip_count in users table --
UPDATE Users
SET totalLikes = R.sum, tip_count = R.count
FROM (SELECT user_id, sum(num_of_likes),count(*)
	  FROM yelptip
	  GROUP BY user_id) as R
WHERE Users.user_id = R.user_id;

-- checkign the users table -- 
SELECT totalLikes,tip_count
FROM Users;