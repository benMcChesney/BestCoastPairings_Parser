DROP TABLE IF EXISTS Dim_Calendar ;
DECLARE @StartDate  date = '20150101';

DECLARE @CutoffDate date = DATEADD(DAY, -1, DATEADD(YEAR, 30, @StartDate));

;WITH seq(n) AS 
(
  SELECT 0 UNION ALL SELECT n + 1 FROM seq
  WHERE n < DATEDIFF(DAY, @StartDate, @CutoffDate)
),
d(d) AS 
(
  SELECT DATEADD(DAY, n, @StartDate) FROM seq
),
src AS
(
  SELECT
    [Date]         = CONVERT(date, d),
    [Day]          = DATEPART(DAY,       d),
    [DayName]      = DATENAME(WEEKDAY,   d),
    [Week]         = DATEPART(WEEK,      d),
    [ISOWeek]      = DATEPART(ISO_WEEK,  d),
    [DayOfWeek]    = DATEPART(WEEKDAY,   d),
    [Month]        = DATEPART(MONTH,     d), 
    [MonthName]    = DATENAME(MONTH,     d),
    [Quarter]      = DATEPART(Quarter,   d),
    [Year]         = DATEPART(YEAR,      d),
    [FirstOfMonth] = DATEFROMPARTS(YEAR(d), MONTH(d), 1),
    [LastOfYear]   = DATEFROMPARTS(YEAR(d), 12, 31),
    [DayOfYear]    = DATEPART(DAYOFYEAR, d)
  FROM d
)

SELECT 
	CONVERT( int , CONVERT( varchar( 8 ) , [Date] , 112 )  ) as dateKey 
	,  * 
INTO Dim_Calendar
FROM src
  ORDER BY Date
  OPTION (MAXRECURSION 0);
