
select 
	* 
	, TRIM( REPLACE( url ,  'https://www.bestcoastpairings.com/event/' , '' ) ) as event_nk
FROM events_links

