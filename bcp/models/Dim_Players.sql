

select 
	ROW_NUMBER() OVER( ORDER BY player ) as Id 
	, [player]
	FROM ( 
		select distinct(player1) as [player]
		FROM pairings

		UNION 

		select distinct(player2 ) as [player]
		FROM pairings
	) as sub 
	WHERE PLAYER IS NOT NULL 