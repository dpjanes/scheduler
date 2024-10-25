from classes import Scheduler
import constraints
import cfg

scheduler = Scheduler(cfg)

constraints.constraint_hard_includes(scheduler)
constraints.constraint_hard_excludes(scheduler)
constraints.constraint_one_doctor_per_day(scheduler)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=scheduler.weekdays)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=8, dates=scheduler.weekends)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=7, dates=scheduler.holidays)
constraints.constraint_no_more_than_once_in_n_days(scheduler, N=3, dates=scheduler.dates)
constraints.constraint_equal_work_distribution(scheduler, tolerance=2, dates=scheduler.weekdays)
constraints.constraint_equal_work_distribution(scheduler, tolerance=5, dates=scheduler.weekends)
constraints.constraint_weekend_pairing(scheduler, penalty_weight=100)

scheduler.solve()
