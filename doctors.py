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
    "McCarthy, J",
    "Tarhoni, M",
    "Smith, J",
    "Woodman, M",
    "Joshi, P",
    "Perry, J",
    "O'Donnell, K",
    "Mercer, S",
    "Babb, K",
    ## "Pridham, A",
    "Morrison, G",
]

hard_include = {
    "Woodman, M": ["2025-01-10", "2025-01-11", "2025-01-12"],
}
hard_exclude = {
    "Perry, J": ["2024-11-11", "2024-11-30", "2024-12-21"],
    "McCarthy, J": ["2024-11-12", "2024-11-13", "2024-11-14", "2024-11-15", "2024-11-16", "2024-11-17"],    
}

# Constraint: "Joshi, P" - Exclude all dates after 2024-12-20
hard_exclude["Joshi, P"] = generate_dates("2024-12-20", END_DATE)


weekdays = [d for d in dates if date.fromisoformat(d).weekday() < 5]  # Monday to Friday are 0-4
weekends = [d for d in dates if date.fromisoformat(d).weekday() >= 5]  # Saturday and Sunday are 5-6

excluded_dates = set()
for dates_list in hard_include.values():
    excluded_dates.update(dates_list)
for dates_list in hard_exclude.values():
    excluded_dates.update(dates_list)

# employee/day
# employee/date schedule
schedule = {
    e: {
        d: model.NewBoolVar(f"schedule_{e}_{d}")
        for d in dates
    } for e in employees
}

# Constraint: Enforce inclusion of specific dates for each doctor in hard_include
for doctor, include_dates in hard_include.items():
    for d in include_dates:
        if d in dates:
            model.Add(schedule[doctor][d] == 1)

# Constraint: Enforce exclusion of specific dates for each doctor in hard_exclude
for doctor, exclude_dates in hard_exclude.items():
    for d in exclude_dates:
        if d in dates:
            model.Add(schedule[doctor][d] == 0)


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
# for e in employees:
#     for i in range(len(dates) - 2):  # Stop at len(dates) - 2 to avoid out-of-range error
#         model.Add(schedule[e][dates[i]] + schedule[e][dates[i + 1]] + schedule[e][dates[i + 2]] <= 1)
# Constraint: No employee works more than once in any 3-day period, excluding hard include/exclude dates
for e in employees:
    for i in range(len(dates) - 2):
        # Check if any of the 3-day window dates are in the excluded set
        if dates[i] not in excluded_dates and dates[i + 1] not in excluded_dates and dates[i + 2] not in excluded_dates:
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

## -- 
# Constraint: Enforce specific dates for Woodman
specific_dates = ["2025-01-10", "2025-01-11", "2025-01-12"]

for d in specific_dates:
    if d in dates:
        model.Add(schedule["Woodman, M"][d] == 1)

# Range of dates between Jan 6 and Jan 18 (excluding specific_dates)
extra_dates_range = [d for d in dates if "2025-01-06" <= d <= "2025-01-18" and d not in specific_dates]

## -- 
# Constraint: Woodman should have exactly three additional call dates between Jan 6 and Jan 18
# model.Add(sum(schedule["Woodman, M"][d] for d in extra_dates_range) == 3)

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
