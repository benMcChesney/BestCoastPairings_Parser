select
	[event] as event_nk
	,listId 
	,full_list_text
FROM ( 
select 
	SUBSTRING( list_url, 40 , 13 ) as listId
	, full_list_text 
	, [event] 
FROM event_army_lists_events 
) as a 
LEFT OUTER JOIN Dim_Events as de 
ON de.event_nk = a.[event]