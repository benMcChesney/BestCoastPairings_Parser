
select 
	joins.*
	, dl.Id as ListFK 
	, CAST( joins.winCount as varchar(5) ) + '-' + CAST( joins.lossCount as varchar(5) ) + '-' + CAST( joins.tieCount as varchar(5) ) as recordResult
	, joins.winCount + joins.lossCount + joins.tieCount as totalGames 
FROM ( 
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
) as joins 
LEFT OUTER JOIN Dim_List as dl 
ON joins.playerListId = dl.listId
