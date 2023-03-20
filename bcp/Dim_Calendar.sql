IF EXISTS (SELECT * FROM information_schema.tables WHERE Table_Name = 'Calendar' AND Table_Type = 'BASE TABLE')

DROP TABLE IF EXISTS [Calendar];


CREATE TABLE [Calendar]
(
    [CalendarDate] DATETIME
)

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



--DROP TABLE [Calendar]

/*
DECLARE @StartDate DATE;
DECLARE @EndDate DATE; 

SET @StartDate = '2020-01-01';
SET @EndDate = '2025-01-01';

--DECLARE @TableName sysname;
--SET @TableName = N'MyTable'

SELECT @StartDate = '2021-11-01', @EndDate = '2021-12-01'; 
WITH ListDates(AllDates) AS
(    SELECT DATEADD(DAY,1,@StartDate) AS DATE
    UNION ALL
    SELECT DATEADD(DAY,1,AllDates)
    FROM ListDates 
    WHERE AllDates < DATEADD(DAY,-1,@EndDate))
SELECT AllDates
FROM ListDates
GO
*/
/*
WITH seq(n) AS 
(
  SELECT 0 UNION ALL SELECT n + 1 FROM seq
  WHERE n < DATEDIFF(DAY, '20190101', DATEADD(DAY, -1, DATEADD(YEAR, 30, '20190101')) )
),
d(d) AS 
(
  SELECT DATEADD(DAY, n, '20190101') FROM seq
),
src AS
(
  SELECT
    TheDate         = CONVERT(date, d),
    TheDay          = DATEPART(DAY,       d),
    TheDayName      = DATENAME(WEEKDAY,   d),
    TheWeek         = DATEPART(WEEK,      d),
    TheISOWeek      = DATEPART(ISO_WEEK,  d),
    TheDayOfWeek    = DATEPART(WEEKDAY,   d),
    TheMonth        = DATEPART(MONTH,     d),
    TheMonthName    = DATENAME(MONTH,     d),
    TheQuarter      = DATEPART(Quarter,   d),
    TheYear         = DATEPART(YEAR,      d),
    TheFirstOfMonth = DATEFROMPARTS(YEAR(d), MONTH(d), 1),
    TheLastOfYear   = DATEFROMPARTS(YEAR(d), 12, 31),
    TheDayOfYear    = DATEPART(DAYOFYEAR, d)
  FROM d
),
dim AS
(
  SELECT
	Datekey				= Convert(CHAR(8),TheDate,112),
    TheDate, 
    TheDay,
    TheDayOfWeek,
    TheDayOfWeekInMonth = CONVERT(tinyint, ROW_NUMBER() OVER 
                            (PARTITION BY TheFirstOfMonth, TheDayOfWeek ORDER BY TheDate)),
    TheDayOfYear,
    IsWeekend           = CASE WHEN TheDayOfWeek IN (CASE @@DATEFIRST WHEN 1 THEN 6 WHEN 7 THEN 1 END,7) 
                            THEN 1 ELSE 0 END,
    TheWeek,
    TheISOweek,
    TheFirstOfWeek      = DATEADD(DAY, 1 - TheDayOfWeek, TheDate),
    TheLastOfWeek       = DATEADD(DAY, 6, DATEADD(DAY, 1 - TheDayOfWeek, TheDate)),
    TheWeekOfMonth      = CONVERT(tinyint, DENSE_RANK() OVER 
                            (PARTITION BY TheYear, TheMonth ORDER BY TheWeek)),
    TheMonth,
    TheMonthName,
    TheFirstOfMonth,
    TheLastOfMonth      = MAX(TheDate) OVER (PARTITION BY TheYear, TheMonth),
    TheFirstOfQuarter   = MIN(TheDate) OVER (PARTITION BY TheYear, TheQuarter),
    TheLastOfQuarter    = MAX(TheDate) OVER (PARTITION BY TheYear, TheQuarter),
    TheYear,
    TheISOYear          = TheYear - CASE WHEN TheMonth = 1 AND TheISOWeek > 51 THEN 1 
                            WHEN TheMonth = 12 AND TheISOWeek = 1  THEN -1 ELSE 0 END,      
    TheFirstOfYear      = DATEFROMPARTS(TheYear, 1,  1),
    TheLastOfYear

  FROM src
)
SELECT * FROM dim
  ORDER BY TheDate
 */