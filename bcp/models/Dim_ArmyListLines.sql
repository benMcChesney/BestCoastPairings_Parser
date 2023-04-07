
/*
select 
	ROW_NUMBER() OVER( ORDER BY player ) as Id 
	, *
	FROM ( 
		select distinct(playerName) as [player], eventId , playerListId 
		FROM pairingsData

	) as sub 
	WHERE PLAYER IS NOT NULL OR playerListId IS NOT NULL 
*/

select 
	[index] as Id 
	, [type] as [UnitType]
	, [unitsCount] 
	, [points]
	, [name] as [UnitName]
	, [Spell]
	, lpu.[listId]
	, lpu.[eventId] 
	, dl.Id as listFK 
FROM listParse_units as lpu
INNER JOIN Dim_List as dl 
ON lpu.listId = dl.listId