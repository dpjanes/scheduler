

## ---
# Check if any of the 3-day window dates are in the excluded set
if False:
    for e in employees:
        for i in range(len(dates) - 2):
            if dates[i] not in special_dates and dates[i + 1] not in special_dates and dates[i + 2] not in special_dates:
                model.Add(schedule[e][dates[i]] + schedule[e][dates[i + 1]] + schedule[e][dates[i + 2]] <= 1)

def add_no_more_than_once_in_n_days_rule(model, schedule, employees, dates, excluded_dates, N):
    """
    Adds a constraint to the model ensuring that no employee works more than once
    in any N-day period, excluding the excluded_dates.
    """
    for e in employees:
        for i in range(len(dates) - N + 1):  # Stop at len(dates) - N + 1 to avoid out-of-range error
            # Check if any of the N-day window dates are in the excluded set
            if all(dates[i + j] not in excluded_dates for j in range(N)):
                # Sum up the N-day window for the employee and ensure it's at most 1
                model.Add(sum(schedule[e][dates[i + j]] for j in range(N)) <= 1)

# Apply the N-day rule with your desired N value (e.g., 3 for 3-day constraint)
if True:
    N = 7
    add_no_more_than_once_in_n_days_rule(model, schedule, employees, dates, special_dates, N)

## ---
# Calculate average number of weekday assignments per employee
if True:
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
if True:
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
if True:
    total_holidays = len(holidays)
    average_holiday_assignments = total_holidays // len(employees)

    # Add constraint for even distribution of holiday work
    for e in employees:
        # Sum the number of holiday assignments for each employee
        num_holiday_assignments = sum(schedule[e][d] for d in holidays)
        
        # Enforce that the number of holiday assignments is close to the average
        model.Add(num_holiday_assignments >= average_holiday_assignments)
        model.Add(num_holiday_assignments <= average_holiday_assignments + 1)

## ---
# Add a rule to ensure each employee gets scheduled evenly over weekdays in a round-robin fashion
if False:
    for shift_num in range(1, len(weekdays) // len(employees) + 1):
        for e in employees:
            # Count the number of weekday shifts for the current employee
            num_shifts_e = sum(schedule[e][d] for d in weekdays)

            # Ensure that employee `e` cannot be scheduled for their `shift_num`-th shift
            # until every other employee has had at least `shift_num - 1` shifts
            for other_employee in employees:
                if e != other_employee:
                    num_shifts_other = sum(schedule[other_employee][d] for d in weekdays)
                    model.Add(num_shifts_e <= num_shifts_other + 1)
