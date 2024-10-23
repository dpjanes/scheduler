from typing import List
from classes import Scheduler

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

def constraint_no_more_than_once_in_n_days(scheduler:Scheduler, N:int=7, dates:List[str]=None):
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

def constraint_equal_work_distribution(scheduler: Scheduler, tolerance: int = 1):
    """
    Constraint: Ensure that, excluding excluded days, each doctor roughly works the same amount.
    The difference between the maximum and minimum number of shifts should not exceed a specified tolerance.
    
    Args:
        scheduler (Scheduler): The scheduling object containing dates, doctors, and constraints.
        tolerance (int): The maximum allowed difference between the number of shifts worked by any two doctors.
    """
    dates = scheduler.dates
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