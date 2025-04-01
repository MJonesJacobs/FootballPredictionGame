CREATE VIEW Actual_Table AS
	WITH PointsPerGame AS ( 
		SELECT 
			HomeTeam,
			AwayTeam,
			HomeScore,
			AwayScore,
			Season,
			CASE
				WHEN HomeScore = AwayScore THEN 1
				WHEN HomeScore > AwayScore THEN 3
				ELSE 0
			END AS HomeTeamPoints,
				CASE
				WHEN HomeScore = AwayScore THEN 1
				WHEN HomeScore < AwayScore THEN 3
				ELSE 0
			END AS AwayTeamPoints,
			HomeScore - AwayScore AS HomeGD,
			AwayScore - HomeScore AS AwayGD
			
		FROM Results
		WHERE ResultAdded = 1
		GROUP BY HomeTeam, AwayTeam, Season
	),

	Teams AS (
		SELECT DISTINCT(HomeTeam) AS Team,Season
		FROM PointsPerGame
	),

	HomeTable AS (
		SELECT 
			HomeTeam,
			Season,
			SUM(HomeTeamPoints) AS HomePoints,
			SUM(HomeGD) AS HomeGD
		FROM PointsPerGame
		GROUP BY HomeTeam, Season
	),

	AwayTable AS (
		SELECT 
			AwayTeam,
			Season,
			SUM(AwayTeamPoints) AS AwayPoints,
			SUM(AwayGD) AS AwayGD
		FROM PointsPerGame
		GROUP BY AwayTeam, Season
	),

	HomeJoin AS (
		SELECT 
			t.Team,
			t.Season,
			ht.HomePoints,
			ht.HomeGD
		FROM Teams AS t
		LEFT JOIN HomeTable AS ht ON t.Team = ht.HomeTeam AND t.Season = ht.Season
		),
	CompleteTable AS (
		SELECT 
			ht.Team,
			ht.Season,
			ht.HomePoints + at.AwayPoints as Points,	
			ht.HomeGD + at.AwayGD as GD
		FROM HomeJoin AS ht
		LEFT JOIN AwayTable AS at ON ht.Team = at.AwayTeam AND ht.Season = at.Season
	)
	SELECT
	*,
	RANK() OVER (PARTITION BY season ORDER BY Points DESC, GD DESC) AS Position
	FROM CompleteTable
;