USE hw2;

SELECT highway, area FROM caltrans
	WHERE text LIKE "IS CLOSE%FOR THE WINTER%" OR text LIKE "IS CLOSED%DUE TO SNOW%"
	GROUP BY highway,area
	ORDER BY highway DESC, area DESC
	LIMIT 20;


SELECT highway, area, (COUNT(DISTINCT reported)/365 * 100) as percentage FROM caltrans
	WHERE text LIKE "IS CLOSE%FOR THE WINTER%" OR text LIKE "IS CLOSED%DUE TO SNOW%"
	GROUP BY highway, area
	ORDER BY percentage DESC
	LIMIT 5;

SELECT trip_id, user_id, TIMEDIFF(end_time, start_time) as trip_length
FROM
(
	SELECT trip_starts.trip_id as trip_id,
	trip_starts.user_id as user_id,
	trip_starts.time as start_time,
	IFNULL(trip_ends.time, TIMESTAMPADD(HOUR, 24, trip_starts.time)) as end_time
	FROM trip_starts
	LEFT JOIN trip_ends ON trip_starts.trip_id = trip_ends.trip_id
)temp
LIMIT 5;

-- calculate trip costs per user
SELECT user_id, 
	IF(1 + .15 *CEILING(TIME_TO_SEC(trip_length)/60) > 100, 100, 1 + .15 *CEILING(TIME_TO_SEC(trip_length)/60) ) as trip_charge
	FROM
	(
		SELECT trip_starts.trip_id as trip_id,
		trip_starts.user_id as user_id,
		TIMEDIFF( 
		IFNULL(trip_ends.time, TIMESTAMPADD(HOUR, 24, trip_starts.time)), trip_starts.time  ) as trip_length
		FROM trip_starts
		LEFT JOIN trip_ends ON trip_starts.trip_id = trip_ends.trip_id
	)temp
LIMIT 5
;


-- calculate monthly trips cost 
SELECT user_id, SUM(trip_charge) as monthly_charge
FROM (
	SELECT user_id, 
	IF(1 + .15 *CEILING(TIME_TO_SEC(trip_length)/60) > 100, 100, 1 + .15 *CEILING(TIME_TO_SEC(trip_length)/60) ) as trip_charge
	FROM
	(
		SELECT trip_starts.trip_id as trip_id,
		trip_starts.user_id as user_id,
		TIMEDIFF( 
		IFNULL(trip_ends.time, TIMESTAMPADD(HOUR, 24, trip_starts.time)), trip_starts.time  ) as trip_length
		FROM trip_starts
		LEFT JOIN trip_ends ON trip_starts.trip_id = trip_ends.trip_id
		WHERE MONTH(trip_starts.time) =3
	)temp
)temp2
GROUP BY user_id
LIMIT 5;




