# Stage 3: Data Analysis with SQL

## Objective

Transform raw data files (`bookings.csv` and `expenditures.csv`) into a single, clean, analysis-ready dataset using SQL. This ensures data integrity and enables efficient aggregations and joins.

**Key steps:**
- Calculate total direct costs for each event.
- Allocate a fair portion of total indirect (overhead) costs to each event.
- Join all financial data to calculate net profit or loss for every booking.

The output is a clean data file, `financial_summary.csv`, which will be used for further financial modeling in Stage 4 (Excel).

## Tools Required

- **DB Browser for SQLite** (or any standard SQL client)

## Setup Instructions

1. **Install DB Browser for SQLite:**  
   Download and install from [here](https://sqlitebrowser.org/dl/).
2. **Create Database:**  
   Open the application and create a new database file (e.g., `analysis.db`) in the project root.
3. **Import Data:**  
   - Import `data/raw/bookings.csv` as table `bookings` (ensure "Column names in first line" is checked).
   - Import `data/raw/expenditures.csv` as table `expenditures`.
4. **Open Query Editor:**  
   Use the "Execute SQL" tab to run queries.

## The SQL Query

This query uses Common Table Expressions (CTEs) to build the final summary table step by step:

```sql
/*
Creates a summary table for financial analysis:
- Calculates direct costs
- Allocates indirect costs
- Determines net profit for each booking
*/

WITH IndirectCostAllocation AS (
    SELECT
        (SELECT SUM(Amount) FROM expenditures WHERE CostType = 'Indirect') AS TotalIndirectCosts,
        (SELECT COUNT(*) FROM bookings) AS TotalEvents
),
DirectCostsPerBooking AS (
    SELECT
        BookingID,
        SUM(Amount) AS TotalDirectCost
    FROM expenditures
    WHERE CostType = 'Direct'
    GROUP BY BookingID
)
SELECT
    b.BookingID,
    b.EventDate,
    b.EventType,
    b.BookingFee,
    COALESCE(d.TotalDirectCost, 0) AS TotalDirectCost,
    i.TotalIndirectCosts / i.TotalEvents AS AllocatedIndirectCost,
    (COALESCE(d.TotalDirectCost, 0) + (i.TotalIndirectCosts / i.TotalEvents)) AS TotalEventCost,
    (b.BookingFee - (COALESCE(d.TotalDirectCost, 0) + (i.TotalIndirectCosts / i.TotalEvents))) AS NetProfit
FROM
    bookings b
LEFT JOIN
    DirectCostsPerBooking d ON b.BookingID = b.BookingID
CROSS JOIN
    IndirectCostAllocation i
ORDER BY
    b.EventDate;
```

## Output and Next Steps

1. **Export Data:**  
   In DB Browser, use "Save results" to export the output as a CSV file:  
   - **File Name:** `financial_summary.csv`  
   - **Location:** `data/processed/`
2. **Save Query:**  
   Save the SQL code in a text file:  
   - **File Name:** `main_query.sql`  
   - **Location:** `analysis/`
