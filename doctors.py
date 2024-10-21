from ortools.sat.python import cp_model
from icecream import ic
import sys
from datetime import date, timedelta

def generate_dates(start_date: str, end_date: str) -> list:
    # Parse the start and end dates from the ISO format
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    
    # Create a list of dates
    delta = end - start
    date_list = [(start + timedelta(days=i)).isoformat() for i in range(delta.days + 1)]
    
    return date_list

# Example usage:
START_DATE = "2024-11-08"
END_DATE = "2025-02-28"
HOLIDAYS = ["2024-12-25", "2024-12-26", "2025-01-01", "2025-02-17" ]  # Example holidays

dates = generate_dates(START_DATE, END_DATE)
# print(result)
# sys.exit(0)

model = cp_model.CpModel()

employees = [
    "McCarthy, Jason",
    "Tarhoni, Mohamed",
    "Smith, Jennifer",
    "Woodman, Margie",
    "Joshi, Pradip",
    "Perry, Jennifer",
    "O'Donnell, Kathleen",
    "Mercer, Susan",
    "Babb, Kim",
    ## "Pridham, Allison",
    "Morrison, Gillian",
]

weekdays = [d for d in dates if date.fromisoformat(d).weekday() < 5]  # Monday to Friday are 0-4
weekends = [d for d in dates if date.fromisoformat(d).weekday() >= 5]  # Saturday and Sunday are 5-6

# employee/day
# employee/date schedule
schedule = {
    e: {
        d: model.NewBoolVar(f"schedule_{e}_{d}")
        for d in dates
    } for e in employees
}

## --
# Constraint: Exactly one doctor works each day
for d in dates:
    model.Add(sum(schedule[e][d] for e in employees) == 1)

## ---
# Constraint: No employee works two consecutive days
# for e in employees:
#     for i in range(len(dates) - 1):
#         model.Add(schedule[e][dates[i]] + schedule[e][dates[i + 1]] <= 1)

## ---
# Constraint: No employee works more than once in any 3-day period
for e in employees:
    for i in range(len(dates) - 2):  # Stop at len(dates) - 2 to avoid out-of-range error
        model.Add(schedule[e][dates[i]] + schedule[e][dates[i + 1]] + schedule[e][dates[i + 2]] <= 1)

## ---
# Calculate average number of weekday assignments per employee
total_weekdays = len(weekdays)
average_weekday_assignments = total_weekdays // len(employees)

# Add constraint for even distribution of weekday work
for e in employees:
    # Sum the number of weekday assignments for each employee
    num_weekday_assignments = sum(schedule[e][d] for d in weekdays)
    
    # Enforce that the number of weekday assignments is close to the average
    model.Add(num_weekday_assignments >= average_weekday_assignments)
    model.Add(num_weekday_assignments <= average_weekday_assignments + 1)

## ---
# Calculate the average number of weekend assignments per employee
total_weekends = len(weekends)
average_weekend_assignments = total_weekends // len(employees)

# Add constraint for even distribution of weekend work
for e in employees:
    # Sum the number of weekend assignments for each employee
    num_weekend_assignments = sum(schedule[e][d] for d in weekends)
    
    # Enforce that the number of weekend assignments is close to the average
    model.Add(num_weekend_assignments >= average_weekend_assignments)
    model.Add(num_weekend_assignments <= average_weekend_assignments + 1)


# Filter holidays that are within the schedule dates
holidays = [d for d in HOLIDAYS if d in dates]

## ---
# Calculate the average number of holiday assignments per employee
total_holidays = len(holidays)
average_holiday_assignments = total_holidays // len(employees)

# Add constraint for even distribution of holiday work
for e in employees:
    # Sum the number of holiday assignments for each employee
    num_holiday_assignments = sum(schedule[e][d] for d in holidays)
    
    # Enforce that the number of holiday assignments is close to the average
    model.Add(num_holiday_assignments >= average_holiday_assignments)
    model.Add(num_holiday_assignments <= average_holiday_assignments + 1)

ic(schedule)
# sys.exit(0)

## -------------------------------------------- ##
# Solve the model
solver = cp_model.CpSolver()
status = solver.solve(model)

# Assuming `solver` is defined and the model has been solved
# solver = cp_model.CpSolver()
# status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    # Loop through each date
    print("=== SHIFTS ===")
    for d in dates:
        # Get the day of the week
        weekday_name = date.fromisoformat(d).strftime('%A')  # Get full weekday name
        if weekday_name == "Monday":
            print()
        
        # Collect doctors working on this day
        working_doctors = [e for e in employees if solver.Value(schedule[e][d]) == 1]
        
        # Print the date, weekday, and doctors working
        print(f"{d} {weekday_name[:3]}: {', '.join(working_doctors) if working_doctors else 'None'}")

    print("\n=== TOTALS ===")
    for e in employees:
        total_shifts = sum(solver.Value(schedule[e][d]) for d in dates)
        weekday_shifts = sum(solver.Value(schedule[e][d]) for d in weekdays)
        weekend_shifts = sum(solver.Value(schedule[e][d]) for d in weekends)
        holiday_shifts = sum(solver.Value(schedule[e][d]) for d in holidays)
        
        print(f"Employee: {e}")
        print(f"  Total Shifts: {total_shifts}")
        print(f"  Weekday Shifts: {weekday_shifts}")
        print(f"  Weekend Shifts: {weekend_shifts}")
        print(f"  Holiday Shifts: {holiday_shifts}")
else:
    print("No feasible solution found.")
