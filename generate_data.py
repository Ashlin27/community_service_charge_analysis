import csv
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_BOOKINGS = 100
# --- UPDATED: Set the script to run for the 2023/2024 Financial Year ---
START_DATE = datetime(2023, 4, 1)
END_DATE = datetime(2024, 3, 31)

# --- Data Definitions ---
EVENT_TYPES = {
    "Meeting": {"min_hours": 2, "max_hours": 5, "base_fee": 50.00, "per_hour_fee": 25.00},
    "Party": {"min_hours": 4, "max_hours": 6, "base_fee": 200.00, "per_hour_fee": 50.00},
    "Wedding": {"min_hours": 6, "max_hours": 10, "base_fee": 500.00, "per_hour_fee": 100.00},
    "Charity": {"min_hours": 3, "max_hours": 8, "base_fee": 0.00, "per_hour_fee": 10.00},
    "Conference": {"min_hours": 8, "max_hours": 8, "base_fee": 800.00, "per_hour_fee": 0},
}

EXPENDITURE_CATEGORIES = {
    "Utilities": {"type": "Indirect", "avg_cost": 400.00},
    "Insurance": {"type": "Indirect", "avg_cost": 600.00},
    "Maintenance": {"type": "Indirect", "avg_cost": 150.00},
    "Supplies": {"type": "Indirect", "avg_cost": 100.00},
    "Cleaning": {"type": "Direct", "avg_cost": 80.00},
    "Security": {"type": "Direct", "avg_cost": 200.00},
    "Specialist Hire": {"type": "Direct", "avg_cost": 300.00}
}


# --- Helper Functions ---
def random_date(start, end):
    """Generate a random datetime between two datetime objects."""
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# --- Main Data Generation ---
def generate_bookings_data(filename="bookings.csv"):
    """Generates a CSV file with mock booking data."""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['BookingID', 'EventDate', 'EventType', 'BookingHours', 'BookingFee', 'PaymentStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, NUM_BOOKINGS + 1):
            event_type_name = random.choice(list(EVENT_TYPES.keys()))
            event_details = EVENT_TYPES[event_type_name]

            booking_hours = random.randint(event_details["min_hours"], event_details["max_hours"])
            booking_fee = event_details["base_fee"] + (event_details["per_hour_fee"] * booking_hours) * (random.uniform(0.9, 1.1)) # slight variation
            payment_status = random.choices(["Paid", "Unpaid"], weights=[9, 1], k=1)[0]

            writer.writerow({
                'BookingID': 100 + i,
                'EventDate': random_date(START_DATE, END_DATE).strftime('%Y-%m-%d'),
                'EventType': event_type_name,
                'BookingHours': booking_hours,
                'BookingFee': f"{booking_fee:.2f}",
                'PaymentStatus': payment_status
            })
    print(f"Successfully generated {filename}")
    return filename


def generate_expenditures_data(bookings_filename="bookings.csv", filename="expenditures.csv"):
    """Generates a CSV file with mock expenditure data, linking some to bookings."""
    bookings = []
    with open(bookings_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bookings.append(row)

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ExpenseID', 'ExpenseDate', 'Category', 'Description', 'Amount', 'CostType', 'BookingID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        expense_id_counter = 5001

        # Generate direct costs linked to bookings
        for booking in bookings:
            # Not every booking will have a direct cost, let's say 70% do
            if random.random() <= 0.7:
                category_name = random.choice([cat for cat, val in EXPENDITURE_CATEGORIES.items() if val["type"] == "Direct"])
                category_details = EXPENDITURE_CATEGORIES[category_name]
                amount = category_details["avg_cost"] * random.uniform(0.8, 1.2)
                
                # Expense date should be close to the event date
                event_date = datetime.strptime(booking['EventDate'], '%Y-%m-%d')
                expense_date = event_date + timedelta(days=random.randint(0, 5))

                writer.writerow({
                    'ExpenseID': expense_id_counter,
                    'ExpenseDate': expense_date.strftime('%Y-%m-%d'),
                    'Category': category_name,
                    'Description': f"Description for {booking['BookingID']}",
                    'Amount': f"{amount:.2f}",
                    'CostType': 'Direct',
                    'BookingID': booking['BookingID']
                })
                expense_id_counter += 1

        # Generate indirect (overhead) costs for each month in the financial year
        current_date = START_DATE
        while current_date < END_DATE:
            for category_name, details in EXPENDITURE_CATEGORIES.items():
                if details['type'] == 'Indirect':
                    amount = details["avg_cost"] * random.uniform(0.9, 1.1)
                    # Place the indirect cost payment at a random day in the month
                    month_start = current_date.replace(day=1)
                    month_end = month_start + timedelta(days=30) # Approx
                    expense_date = random_date(month_start, month_end)
                    
                    writer.writerow({
                        'ExpenseID': expense_id_counter,
                        'ExpenseDate': expense_date.strftime('%Y-%m-%d'),
                        'Category': category_name,
                        'Description': f"Monthly {category_name}",
                        'Amount': f"{amount:.2f}",
                        'CostType': 'Indirect',
                        'BookingID': ''
                    })
                    expense_id_counter += 1
            # Move to the next month
            # A more robust way to advance the month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)


    print(f"Successfully generated {filename}")


# --- Run Script ---
if __name__ == "__main__":
    bookings_file = generate_bookings_data()
    generate_expenditures_data(bookings_file)