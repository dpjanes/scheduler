from ortools.sat.python import cp_model
from icecream import ic
import sys
from datetime import date, timedelta

from util import generate_dates

class Scheduler:
    def __init__(self, cfg):
        self.dates = generate_dates(cfg.START_DATE, cfg.END_DATE)
        self.weekdays = [d for d in self.dates if date.fromisoformat(d).weekday() < 5]  # Monday to Friday are 0-4
        self.weekends = [d for d in self.dates if date.fromisoformat(d).weekday() >= 5]  # Saturday and Sunday are 5-6
        self.holidays = [d for d in cfg.HOLIDAYS if d in self.dates]
        self.employees = cfg.employees

        self.hard_include = dict()
        self.hard_exclude = dict()
        for employee in self.employees:
            self.hard_include[employee] = set(cfg.hard_include.get(employee) or [])
            self.hard_exclude[employee] = set(cfg.hard_exclude.get(employee) or [])
        
        self.cfg = cfg
        self.model = cp_model.CpModel()
        self.schedule = {
            e: {
                d: self.model.NewBoolVar(f"schedule_{e}_{d}")
                for d in self.dates
            } for e in cfg.employees
        }

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.solve(self.model)

        dates = self.dates
        employees = self.employees
        weekdays = self.weekdays
        weekends = self.weekends
        holidays = self.holidays

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Loop through each date
            print("=== SHIFTS ===")
            for d in dates:
                # Get the day of the week
                weekday_name = date.fromisoformat(d).strftime('%A')  # Get full weekday name
                if weekday_name == "Monday":
                    print()
                
                # Collect doctors working on this day
                working_doctors = [e for e in employees if solver.Value(self.schedule[e][d]) == 1]
                
                # Print the date, weekday, and doctors working
                print(f"{d} {weekday_name[:3]}: {', '.join(working_doctors) if working_doctors else 'None'}")

            print("\n=== TOTALS ===")
            for e in employees:
                total_shifts = sum(solver.Value(self.schedule[e][d]) for d in dates)
                weekday_shifts = sum(solver.Value(self.schedule[e][d]) for d in weekdays)
                weekend_shifts = sum(solver.Value(self.schedule[e][d]) for d in weekends)
                holiday_shifts = sum(solver.Value(self.schedule[e][d]) for d in holidays)
                
                print(f"Employee: {e}")
                print(f"  Total Shifts: {total_shifts}")
                print(f"  Weekday Shifts: {weekday_shifts}")
                print(f"  Weekend Shifts: {weekend_shifts}")
                print(f"  Holiday Shifts: {holiday_shifts}")
        else:
            print("No feasible solution found.")
