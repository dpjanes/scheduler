from typing import List
from classes import Scheduler

def constraint_hard_includes(scheduler:Scheduler):
    """
    Constraint: Enforce inclusion of specific dates for each doctor in hard_include
    """
    dates = scheduler.dates

    for doctor, include_dates in scheduler.cfg.hard_include.items():
        for d in include_dates:
            if d in dates:
                scheduler.model.Add(scheduler.schedule[doctor][d] == 1)

def constraint_hard_excludes(scheduler:Scheduler):
    """
    Constraint: Enforce exclusion of specific dates for each doctor in hard_exclude
    """
    dates = scheduler.dates

    for doctor, exclude_dates in scheduler.cfg.hard_exclude.items():
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
    dates = scheduler.dates
    employees = scheduler.employees
    dates = dates or scheduler.dates

    for e in employees:
        ignore_dates = set(scheduler.cfg.hard_exclude.get(e, []) + scheduler.cfg.hard_include.get(e, []))
        for i in range(len(dates) - N + 1): 
            scheduler.model.Add(sum(scheduler.schedule[e][dates[i + j]] for j in range(N) if dates[i + j] not in ignore_dates) <= 1)
