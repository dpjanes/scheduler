from datetime import date, timedelta
from util import generate_dates, generate_weekends

START_DATE = "2025-04-01"
END_DATE = "2025-06-03"
HOLIDAYS = ["2025-04-18", "2025-05-19", ]

def weekend_dates():
    return generate_weekends(START_DATE, END_DATE)

employees = [
    "McCarthy, J",
    "Tarhoni, M",
    "Smith, J",
    "Woodman, M",
    ## "Joshi, P",
    "Perry, J",
    "O'Donnell, K",
    "Mercer, S",
    "Babb, K",
    "Morrison, G",
]

## preferred but not required
soft_include = {
    # "Woodman, M": ["2025-02-07", "2025-02-08", "2025-02-09"],
    # "O'Donnell, K": generate_dates("2025-01-23", "2025-02-04") + generate_dates("2025-02-20", "2025-03-12"),
}  

## must be included on these dates
hard_include = {
}

## must not be included on these dates
hard_exclude = {
    "McCarthy, J": (
        generate_dates("2025-04-15", "2025-04-16") +
        generate_dates("2025-04-21", "2025-04-27") +
        generate_dates("2025-05-02", "2025-05-10") +
        generate_dates("2025-05-15", "2025-05-16")
    ),
    
    "Tarhoni, M": [],  # 'nil' means no unavailable dates
    
    "Smith, J": generate_dates("2025-05-01", "2025-05-05"),
    
    "Woodman, M": (
        ["2025-04-02", "2025-04-12", "2025-04-13", "2025-04-21", "2025-04-24", "2025-04-29"] +
        generate_dates("2025-05-02", "2025-05-04") +
        generate_dates("2025-05-07", "2025-05-08") +
        generate_dates("2025-05-12", "2025-05-28")
    ),
    
    "Mercer, S": (
        generate_dates("2025-05-03", "2025-05-12") +
        generate_dates("2025-05-21", "2025-06-02")
    ),
    
    "Perry, J": (
        generate_dates("2025-04-07", "2025-04-20") +
        generate_dates("2025-05-01", "2025-05-04") +
        generate_dates("2025-05-08", "2025-05-11") +
        generate_dates("2025-05-30", "2025-05-31")
    ),
    
    "O'Donnell, K": (
        generate_dates("2025-04-30", "2025-05-07") +
        ["2025-05-25"]
    ),
    
    "Morrison, G": (
        weekend_dates() +
        generate_dates("2025-04-08", "2025-04-15") +
        generate_dates("2025-06-02", "2025-06-03")
    ),
    
    "Babb, K": (
        weekend_dates() +
        ["2025-04-01"] +
        generate_dates("2025-05-01", "2025-05-14")
    )
}
