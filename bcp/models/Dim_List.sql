

select
	[index] as [Id]
	, listId 
	, faction
	, [Grand Strategy] as GrandStrategy  
	, COALESCE( Triumph , triumphs ) as triumph
	, subfaction
	, [Mortal Realm] as MortalRealm
	, eventId 
FROM listParse_factions

