
select 
	sub.*
	, em.eventName
	, em.eventOwner
	, CONVERT( date , REPLACE( em.startDate  , ',' , '' ) ) as startDate 
	, CONVERT( date , REPLACE( em.endDate  , ',' , '' ) ) as endDate 
	, em.location
	, em.ticketPrice
	, et.totalPairings
	, et.totalPlayers
	, et.totalRounds
FROM ( 
select 
	el.[index] as [Id]
	, [url]
	, TRIM( REPLACE( url ,  'https://www.bestcoastpairings.com/event/' , '' ) ) as event_nk
FROM events_links as el 
) as sub 
LEFT OUTER JOIN [event_meta] as em  
ON sub.event_nk = em.eventId 
LEFT OUTER JOIN ( 
	select eventId , MAX( [round] ) as totalRounds
	, count( distinct pairingId ) as totalPairings
	, count( distinct playerListId ) as totalPlayers 
	FROM pairingsData
	GROUP BY eventId 
) as et  
ON et.eventId = sub.event_nk

-- February, 11, 2023
