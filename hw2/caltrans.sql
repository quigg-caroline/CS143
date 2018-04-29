USE hw2;

SELECT highway, area FROM caltrans
	WHERE text LIKE "IS CLOSE%FOR THE WINTER%" OR text LIKE "IS CLOSED%DUE TO SNOW%"
	GROUP BY highway, area
	ORDER BY highway, area DESC
	LIMIT 20;


SELECT highway, area, (COUNT(reported)/365 * 100) as percentage FROM caltrans
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

