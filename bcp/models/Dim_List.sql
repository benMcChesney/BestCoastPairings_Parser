
with CTE as
( 

select 
	playerListId
	, SUM( winCount ) as winCount
	, SUM( lossCount ) as lossCount
	, SUM( tieCount ) as tieCount 
FROM ( 
select *
, CASE
	WHEN playerResult = 'Win'
		THEN 1
		ELSE 0 
	END as WinCount
, CASE
	WHEN playerResult = 'Loss'
		THEN 1
		ELSE 0 
	END as LossCount
, CASE
	WHEN playerResult = 'Tie'
		THEN 1
		ELSE 0 
	END as TieCount
FROM ( 
select * 
FROM pairingsData
) as sub1
WHERE playerListId IS NOT NULL 
) as sub 
GROUP BY playerListId
) 

select
	[index] as [Id]
	, listId 
	, faction
	, [Grand Strategy] as GrandStrategy  
	, COALESCE( Triumph , triumphs ) as triumph
	, subfaction
	, [Mortal Realm] as MortalRealm
	, eventId 
	, cte.* 
FROM listParse_factions as a 
LEFT OUTER JOIN cte 
ON cte.playerListId = a.listId




