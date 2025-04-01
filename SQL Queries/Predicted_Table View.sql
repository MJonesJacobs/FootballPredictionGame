
CREATE VIEW Predicted_Table AS
	WITH PointsPerGame AS ( 
	SELECT 
		*,
		CASE
			WHEN HomePrediction = AwayPrediction THEN 1
			WHEN HomePrediction > AwayPrediction THEN 3
			ELSE 0
		END AS HomeTeamPredictedPoints,
			CASE
			WHEN HomePrediction = AwayPrediction THEN 1
			WHEN HomePrediction < AwayPrediction THEN 3
			ELSE 0
		END AS AwayTeamPredictedPoints,
		HomePrediction - AwayPrediction AS HomeGD,
		AwayPrediction - HomePrediction AS AwayGD
		
	FROM Results
	WHERE ResultAdded = 1
	),

	Teams AS (
		SELECT DISTINCT(HomeTeam) AS Team,Season
		FROM PointsPerGame
	),

	HomeTable AS (
	SELECT 
		HomeTeam,
		Player,
		Season,
		SUM(HomeTeamPredictedPoints) AS HomePoints,
		SUM(HomeGD) AS HomeGD
	FROM PointsPerGame
	GROUP BY HomeTeam, Player, Season
	),

	AwayTable AS (
	SELECT 
		AwayTeam,
		Player,
		Season,
		SUM(AwayTeamPredictedPoints) AS AwayPoints,
		SUM(AwayGD) AS AwayGD
	FROM PointsPerGame
	GROUP BY AwayTeam, Player, Season
	),

	HomeJoin AS (
	SELECT 
		t.Team,
		t.Season,
		ht.player,
		ht.HomePoints,
		ht.HomeGD
	FROM Teams AS t
	LEFT JOIN HomeTable AS ht ON t.Team = ht.HomeTeam AND t.Season = ht.Season
	),

	CompleteTable AS (
	SELECT 
		ht.Team,
		ht.Season,
		ht.player,
		ht.HomePoints + at.AwayPoints as Points,	
		ht.HomeGD + at.AwayGD as GD
	FROM HomeJoin AS ht
	LEFT JOIN AwayTable AS at ON ht.Team = at.AwayTeam AND ht.Season = at.Season AND ht.player = at.player
	)
	SELECT
	*,
	RANK() OVER (PARTITION BY player, season ORDER BY Points DESC, GD DESC) AS Position
	FROM CompleteTable
;