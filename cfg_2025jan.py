from datetime import date
from util import generate_dates

START_DATE = "2025-01-20"
END_DATE = "2025-03-31"
HOLIDAYS = ["2024-11-11", "2024-12-25", "2024-12-26", "2025-01-01", "2025-02-17"]

employees = [
    "McCarthy, J",
    "Tarhoni, M",
    "Smith, J",
    "Woodman, M",
    "Joshi, P",
    "Perry, J",
    "O'Donnell, K",
    "Mercer, S",
    "Babb, K",
    ## "Pridham, A",
    "Morrison, G",
]

## preferred but not required
soft_include = {
    "Woodman, M": ["2025-02-07", "2025-02-08", "2025-02-09"],
    "O'Donnell, K": generate_dates("2025-01-23", "2025-02-04") + generate_dates("2025-02-20", "2025-03-12"),
}  

## must be included on these dates
hard_include = {
}

## must not be included on these dates
hard_exclude = {
    "Perry, J": ["2025-01-25", "2025-02-01", "2025-02-02", "2025-03-06", "2025-03-07", "2025-03-08", "2025-03-09", "2025-03-10", "2025-03-25", "2025-03-26", "2025-03-27", "2025-03-28", "2025-03-29", "2025-03-30"],
    "McCarthy, J": ["2025-01-20", "2025-01-21", "2025-01-22", "2025-01-23", "2025-01-28", "2025-01-29", "2025-02-04", "2025-02-05", "2025-02-18", "2025-02-19", "2025-03-04", "2025-03-05", "2025-03-18", "2025-03-19"],
    "Babb, K": generate_dates("2025-02-05", "2025-02-07") + generate_dates("2025-02-20", "2025-02-28") + generate_dates("2025-03-25", "2025-03-31"),
    "Morrison, G": generate_dates("2025-02-04", "2025-03-03") + generate_dates("2025-03-25", "2025-03-31"),
    "Pridham, A": [],  # Not available for this schedule (on maternity leave)
    "Mercer, S": generate_dates("2025-01-20", "2025-02-07"),
    "O'Donnell, K": generate_dates("2025-03-15", "2025-03-23"),
    "Smith, J": ["2025-02-15"],
    "Joshi, P": [],  # On personal leave, not available
    "Woodman, M": ["2025-02-05", "2025-02-06", "2025-02-18", "2025-02-22", "2025-02-23"]
}
