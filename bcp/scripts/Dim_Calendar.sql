

TRUNCATE TABLE [Calendar];


DECLARE @StartDate DATE
DECLARE @EndDate DATE
SET @StartDate = GETDATE()
SET @EndDate = DATEADD(d, 365, @StartDate)

WHILE @StartDate <= @EndDate
      BEGIN
             INSERT INTO [Calendar]
             (
                   CalendarDate
             )
             SELECT
                   @StartDate

             SET @StartDate = DATEADD(dd, 1, @StartDate)
      END

select 
	[Date]
	,[Datekey]    
    ,DATEPART(DAY, [Date]) AS [Day]
	,DATEPART(WEEK, [Date]) AS [Week]
	,DATEPART(MONTH, [Date]) AS [Month]
	,DATENAME(MONTH, [Date]) AS [MonthName]
	,DATEPART(YEAR, [Date]) AS [Year]
FROM ( 
select  
	CONVERT( Date, CalendarDate ) as [Date]
	, CONVERT( char(8) , CalendarDate , 112 ) as datekey
FROM [Calendar]
) as sub
