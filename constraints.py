from typing import List
from classes import Scheduler
from datetime import date, timedelta
from icecream import ic

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

def XXXconstraint_long_weekend_triplet(scheduler: Scheduler, penalty_weight=200):
    """
    Soft constraint: For any Friday–Saturday–Sunday block, if someone works
    any of the days, they should work all three.
    
    Exceptions:
    - Christmas (Dec 25)
    - Days explicitly excluded for that employee
    """
    from datetime import date, timedelta

    # ---- Build Friday–Saturday–Sunday triplets ----
    triplets = []
    all_dates = sorted(scheduler.xweekends)
    date_objs = {d: date.fromisoformat(d) for d in all_dates}

    for d in all_dates:
        dt = date_objs[d]
        if dt.weekday() == 4:  # Friday
            fri = d
            sat = (dt + timedelta(days=1)).isoformat()
            sun = (dt + timedelta(days=2)).isoformat()

            if sat in date_objs and sun in date_objs:
                triplets.append((fri, sat, sun))

    ic(triplets)

    # ---- Add constraints ----
    for employee in scheduler.employees:
        for fri, sat, sun in triplets:

            # Skip Christmas
            if any(
                (date.fromisoformat(d).month == 12 and
                 date.fromisoformat(d).day == 25)
                for d in (fri, sat, sun)
            ):
                continue

            # Skip if explicitly excluded
            if any(d in scheduler.hard_exclude[employee] for d in (fri, sat, sun)):
                continue

            w_fri = scheduler.schedule[employee][fri]
            w_sat = scheduler.schedule[employee][sat]
            w_sun = scheduler.schedule[employee][sun]

            wsum = w_fri + w_sat + w_sun

            # Bool vars detecting the allowed states
            is_zero = scheduler.model.NewBoolVar(f"{employee}_{fri}_wsum0")
            is_three = scheduler.model.NewBoolVar(f"{employee}_{fri}_wsum3")

            # Link: is_zero <=> (wsum == 0)
            scheduler.model.Add(wsum == 0).OnlyEnforceIf(is_zero)
            scheduler.model.Add(wsum != 0).OnlyEnforceIf(is_zero.Not())

            # Link: is_three <=> (wsum == 3)
            scheduler.model.Add(wsum == 3).OnlyEnforceIf(is_three)
            scheduler.model.Add(wsum != 3).OnlyEnforceIf(is_three.Not())

            # Allowed = is_zero OR is_three
            allowed = scheduler.model.NewBoolVar(f"{employee}_{fri}_allowed")
            scheduler.model.AddBoolOr([is_zero, is_three]).OnlyEnforceIf(allowed)
            scheduler.model.AddBoolAnd([is_zero.Not(), is_three.Not()]).OnlyEnforceIf(allowed.Not())

            # Penalty when NOT allowed
            penalty = scheduler.model.NewBoolVar(f"{employee}_{fri}_triplet_penalty")
            scheduler.model.Add(penalty == allowed.Not())

            scheduler.penalties.extend([penalty] * penalty_weight)

def constraint_long_weekend_triplet(scheduler: Scheduler, penalty_weight=100):
    """
    Soft constraint: If someone works any day of the 3-day weekend, they should work all three days.
    Uses a high penalty weight to strongly encourage full weekend assignment unless impossible.
    Exceptions:
    - Christmas (Dec 25)
    - Dates that are explicitly excluded for that employee
    
    Args:
        scheduler: Scheduler instance
        penalty_weight: Weight of the penalty (default: 100). Higher values make the constraint stronger.
    """
    from datetime import date
    
    # Group 3-day weekends properly by looking at the actual calendar dates
    weekend_triples = {}  # Dictionary to store Friday -> [Saturday, Sunday]
    
    for d in scheduler.xweekends:
        date_obj = date.fromisoformat(d)
        if date_obj.weekday() == 4:  # Friday
            weekend_triples[d] = [None, None]  # [Saturday, Sunday]
        elif date_obj.weekday() == 5:  # Saturday
            # Find the corresponding Friday
            for fri in list(weekend_triples.keys()):
                if weekend_triples[fri][0] is None:  # Unpaired Friday
                    fri_date = date.fromisoformat(fri)
                    if (date_obj - fri_date).days == 1:  # Adjacent days
                        weekend_triples[fri][0] = d
                        break
        elif date_obj.weekday() == 6:  # Sunday
            # Find the corresponding Friday
            for fri in list(weekend_triples.keys()):
                if weekend_triples[fri][1] is None:  # Missing Sunday
                    fri_date = date.fromisoformat(fri)
                    if (date_obj - fri_date).days == 2:  # Two days apart
                        weekend_triples[fri][1] = d
                        break
    
    # Convert the dictionary to list of triples [Friday, Saturday, Sunday]
    weekend_triples = [
        [fri, sat, sun] 
        for fri, (sat, sun) in weekend_triples.items() 
        if sat is not None and sun is not None
    ]
    
    for employee in scheduler.employees:
        for weekend in weekend_triples:
            # Skip if this is Christmas weekend and contains December 25
            is_christmas_weekend = any(
                date.fromisoformat(d).month == 12 and 
                date.fromisoformat(d).day == 25 
                for d in weekend
            )
            if is_christmas_weekend:
                continue
            
            # Skip if any day in the weekend is explicitly excluded for this employee
            if any(d in scheduler.hard_exclude[employee] for d in weekend):
                continue
            
            day1, day2, day3 = weekend
            works_day1 = scheduler.schedule[employee][day1]
            works_day2 = scheduler.schedule[employee][day2]
            works_day3 = scheduler.schedule[employee][day3]
            
            total_days_worked = works_day1 + works_day2 + works_day3
            
            # Create boolean variables for different scenarios
            works_zero = scheduler.model.NewBoolVar(f"works_zero_{employee}_{day1}")
            works_three = scheduler.model.NewBoolVar(f"works_three_{employee}_{day1}")
            penalty = scheduler.model.NewBoolVar(f"weekend_partial_penalty_{employee}_{day1}")
            
            # Define when works_zero is true (total = 0)
            scheduler.model.Add(total_days_worked == 0).OnlyEnforceIf(works_zero)
            scheduler.model.Add(total_days_worked != 0).OnlyEnforceIf(works_zero.Not())
            
            # Define when works_three is true (total = 3)
            scheduler.model.Add(total_days_worked == 3).OnlyEnforceIf(works_three)
            scheduler.model.Add(total_days_worked != 3).OnlyEnforceIf(works_three.Not())
            
            # Penalty is true if neither works_zero nor works_three (i.e., works 1 or 2 days)
            scheduler.model.AddBoolOr([works_zero, works_three, penalty])
            scheduler.model.AddBoolOr([works_zero.Not(), penalty.Not()])
            scheduler.model.AddBoolOr([works_three.Not(), penalty.Not()])
            
            # Add weighted penalty to the penalties list
            scheduler.penalties.extend([penalty] * penalty_weight)