from typing import List
from classes import Scheduler
from datetime import date, timedelta

def constraint_hard_includes(scheduler:Scheduler):
    """
    Constraint: Enforce inclusion of specific dates for each doctor in hard_include
    """
    dates = scheduler.dates

    for doctor, include_dates in scheduler.hard_include.items():
        for d in include_dates:
            if d in dates:
                scheduler.model.Add(scheduler.schedule[doctor][d] == 1)

def constraint_hard_excludes(scheduler:Scheduler):
    """
    Constraint: Enforce exclusion of specific dates for each doctor in hard_exclude
    """
    dates = scheduler.dates

    for doctor, exclude_dates in scheduler.hard_exclude.items():
        for d in exclude_dates:
            if d in dates:
                scheduler.model.Add(scheduler.schedule[doctor][d] == 0)

def constraint_one_doctor_per_day(scheduler:Scheduler):
    """
    Constraint: Ensure that only one doctor is scheduled per day
    """
    dates = scheduler.dates
    employees = scheduler.employees

    for d in dates:
        scheduler.model.Add(sum(scheduler.schedule[e][d] for e in employees) == 1)

def OLD_constraint_no_more_than_once_in_n_days(scheduler:Scheduler, N:int=7, dates:List[str]=None):
    """
    Constraint: Make sure over some date range, no doctor is scheduled more than once.

    We exclude dates that are in the hard_exclude or hard_include lists for that doctor
    (mabe hard_exclude should be ignored?)
    """
    dates = scheduler.dates
    employees = scheduler.employees
    dates = dates or scheduler.dates

    for e in employees:
        ignore_dates = scheduler.hard_exclude.get(e) | scheduler.hard_include.get(e)| scheduler.soft_include.get(e)
        for i in range(len(dates) - N + 1): 
            scheduler.model.Add(sum(scheduler.schedule[e][dates[i + j]] for j in range(N) if dates[i + j] not in ignore_dates) <= 1)

def constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=None):
    """
    Constraint: Make sure over some date range, no doctor is scheduled more than once per N days.

    We exclude dates that are in the hard_exclude or hard_include lists for that doctor.

    Args:
        scheduler (Scheduler): The scheduling object containing dates, doctors, and constraints.
        N (int): Number of days in the period.
        dates (List[str]): The list of dates to consider (optional).
    """
    dates = dates or scheduler.dates
    employees = scheduler.employees

    for e in employees:
        # Combine all ignore_dates from various sources
        ignore_dates = set(scheduler.hard_exclude.get(e, []) | scheduler.hard_include.get(e, []) | scheduler.soft_include.get(e, []))

        # Loop over each date range of N days
        for i in range(len(dates) - N + 1):
            if dates[i] in ignore_dates:
                continue

            # Merge Saturday and Sunday into a single day for the calculation
            merged_days = set()
            for j in range(N):
                current_date = dates[i + j]
                current_day = date.fromisoformat(current_date).weekday()

                # Treat Saturday and Sunday as the same day by using the first occurrence in the pair
                if current_day == 5:  # Saturday
                    merged_days.add(current_date)  # Add the first occurrence of the weekend
                elif current_day == 6:  # Sunday
                    # If the previous day is already in the set and it's Saturday, skip adding this Sunday separately
                    if i + j > 0 and dates[i + j - 1] in merged_days and date.fromisoformat(dates[i + j - 1]).weekday() == 5:
                        continue
                    merged_days.add(current_date)  # If not paired with a Saturday, treat this as a separate "day"
                else:
                    merged_days.add(current_date)

            # Add the constraint, ignoring excluded dates
            scheduler.model.Add(sum(scheduler.schedule[e][day] for day in merged_days if day not in ignore_dates) <= 1)

def constraint_equal_work_distribution(scheduler: Scheduler, dates:List[str]=None, tolerance: int = 1):
    """
    Constraint: Ensure that, excluding excluded days, each doctor roughly works the same amount.
    The difference between the maximum and minimum number of shifts should not exceed a specified tolerance.
    
    Args:
        scheduler (Scheduler): The scheduling object containing dates, doctors, and constraints.
        tolerance (int): The maximum allowed difference between the number of shifts worked by any two doctors.
    """
    dates = dates or scheduler.dates
    employees = scheduler.employees

    # Calculate the number of shifts for each doctor, ignoring hard_exclude days
    total_shifts = {
        e: sum(scheduler.schedule[e][d] for d in dates if d not in scheduler.hard_exclude.get(e, []))
        for e in employees
    }

    # Add constraints to ensure the difference in shifts between any two doctors is within the tolerance
    for e1 in employees:
        for e2 in employees:
            if e1 != e2:
                scheduler.model.Add(total_shifts[e1] - total_shifts[e2] <= tolerance)
                scheduler.model.Add(total_shifts[e2] - total_shifts[e1] <= tolerance)

def constraint_weekend_pairing(scheduler:Scheduler, penalty_weight=100):
    """
    Soft constraint: If someone works one day of the weekend, they should work both days.
    Uses a high penalty weight to strongly encourage weekend pairing unless impossible.
    
    Exceptions:
    - Christmas (Dec 25)
    - Dates that are explicitly excluded for that employee
    
    Args:
        scheduler: Scheduler instance
        penalty_weight: Weight of the penalty (default: 100). Higher values make the constraint stronger.
    """
    from datetime import date
    
    # Group weekends properly by looking at the actual calendar dates
    weekend_pairs = {}  # Dictionary to store Saturday -> Sunday pairs
    for d in scheduler.weekends:
        date_obj = date.fromisoformat(d)
        if date_obj.weekday() == 5:  # Saturday
            weekend_pairs[d] = None
        elif date_obj.weekday() == 6:  # Sunday
            # Find the corresponding Saturday
            for sat in list(weekend_pairs.keys()):
                if weekend_pairs[sat] is None:  # Unpaired Saturday
                    sat_date = date.fromisoformat(sat)
                    if (date_obj - sat_date).days == 1:  # Adjacent days
                        weekend_pairs[sat] = d
                        break
    
    # Convert the dictionary to list of pairs
    weekend_pairs = [[sat, sun] for sat, sun in weekend_pairs.items() if sun is not None]
    # print(weekend_pairs)
    
    for employee in scheduler.employees:
        for weekend in weekend_pairs:
            # Skip if this is Christmas weekend and contains December 25
            is_christmas_weekend = any(
                date.fromisoformat(d).month == 12 and 
                date.fromisoformat(d).day == 25 
                for d in weekend
            )
            if is_christmas_weekend:
                continue
                
            # Skip if any day in the weekend is explicitly excluded for this employee
            # print("D", weekend)
            if any(d in scheduler.hard_exclude[employee] for d in weekend):
                continue
            
            day1, day2 = weekend
            works_day1 = scheduler.schedule[employee][day1]
            works_day2 = scheduler.schedule[employee][day2]
            
            # Add penalty if working exactly one day
            penalty = scheduler.model.NewBoolVar(f"weekend_single_day_penalty_{employee}_{day1}")
            
            # penalty = 1 if (works_day1 + works_day2) == 1
            scheduler.model.Add(works_day1 + works_day2 != 1).OnlyEnforceIf(penalty.Not())
            scheduler.model.Add(works_day1 + works_day2 == 1).OnlyEnforceIf(penalty)
            
            # Add weighted penalty to the penalties list
            scheduler.penalties.extend([penalty] * penalty_weight)