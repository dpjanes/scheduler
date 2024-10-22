from classes import Scheduler
import constraints

scheduler = Scheduler()

constraints.constraint_hard_includes(scheduler)
constraints.constraint_hard_excludes(scheduler)
constraints.constraint_one_doctor_per_day(scheduler)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=scheduler.cfg.weekdays)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=scheduler.cfg.weekends)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=scheduler.cfg.holidays)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=3, dates=scheduler.cfg.dates)

scheduler.solve()