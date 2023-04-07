/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
	[rank] as placingRank 
	,CASE
		WHEN countBattleTactic IS NOT NULL 
			THEN 'Swiss Points'
		ELSE
			'Battle Points'
	END AS [PointsSystem] 
	,[WINS SOS]
	,[BATTLE POINTS SOS]
	,[WINS EXTENDED SOS]
	,[BATTLE POINTS EXTENDED SOS]
	,countBattleTactic
	,countGrandStrategy
	,swissPoints
	,marginOfVictory
	, dl.Id as [ListFK]
	, de.event_nk as [EventFK]
	, dp.id as [PlayerFK]
	, cal.datekey 
	FROM placingsData as pd
	LEFT OUTER JOIN Dim_List as dl 
	ON pd.listId = dl.listId 
	LEFT OUTER JOIN Dim_Events as de 
	ON dl.eventId = de.event_nk  
	LEFT OUTER JOIN Dim_Players as dp 
	ON ISNULL( pd.playerName, -1 )  = ISNULL( dp.Player, -1 ) 
	AND ISNULL( de.event_nk, -1 ) = ISNULL( de.event_nk, -1 ) 
	INNER JOIN Dim_Calendar as cal 
	ON cal.date = de.startDate