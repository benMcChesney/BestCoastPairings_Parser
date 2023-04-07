

select 
	ROW_NUMBER() OVER( ORDER BY player ) as Id 
	, *
	FROM ( 
		select distinct(playerName) as [player], eventId , playerListId 
		FROM pairingsData

	) as sub 
	WHERE PLAYER IS NOT NULL OR playerListId IS NOT NULL 