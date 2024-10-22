from ortools.sat.python import cp_model
from icecream import ic
import sys
from datetime import date, timedelta

from util import generate_dates
import cfg

class Scheduler:
    def __init__(self):
        self.cfg = cfg
        self.model = cp_model.CpModel()
        self.schedule = {
            e: {
                d: self.model.NewBoolVar(f"schedule_{e}_{d}")
                for d in cfg.dates
            } for e in cfg.employees
        }

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.solve(self.model)

        dates = self.cfg.dates
        employees = self.cfg.employees
        weekdays = self.cfg.weekdays
        weekends = self.cfg.weekends
        holidays = [d for d in self.cfg.HOLIDAYS if d in dates]

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
