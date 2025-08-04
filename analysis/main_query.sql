/*
This query creates a final summary table for financial analysis.
It calculates direct costs, allocates indirect costs, and determines the net profit for each booking.
*/

-- Step 1: Calculate the total indirect costs for the period and the number of events to spread them across.
WITH IndirectCostAllocation AS (
    SELECT
        (SELECT SUM(Amount) FROM expenditures WHERE CostType = 'Indirect') AS TotalIndirectCosts,
        (SELECT COUNT(*) FROM bookings) AS TotalEvents
),

-- Step 2: Calculate the total direct costs for each individual booking.
DirectCostsPerBooking AS (
    SELECT
        BookingID,
        SUM(Amount) AS TotalDirectCost
    FROM expenditures
    WHERE CostType = 'Direct'
    GROUP BY BookingID
)

-- Step 3: Join everything together to create the final summary table.
SELECT
    b.BookingID,
    b.EventDate,
    b.EventType,
    b.BookingFee,
    -- If a booking had no direct costs, show 0 instead of NULL.
    COALESCE(d.TotalDirectCost, 0) AS TotalDirectCost,
    -- Calculate the allocated portion of indirect costs for this single event.
    i.TotalIndirectCosts / i.TotalEvents AS AllocatedIndirectCost,
    -- Calculate the total cost for the event.
    (COALESCE(d.TotalDirectCost, 0) + (i.TotalIndirectCosts / i.TotalEvents)) AS TotalEventCost,
    -- Calculate the final profit or loss.
    (b.BookingFee - (COALESCE(d.TotalDirectCost, 0) + (i.TotalIndirectCosts / i.TotalEvents))) AS NetProfit
FROM
    bookings b
LEFT JOIN
    DirectCostsPerBooking d ON b.BookingID = d.BookingID
CROSS JOIN
    IndirectCostAllocation i
ORDER BY
    b.EventDate;