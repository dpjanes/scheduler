from datetime import date, timedelta
from util import generate_dates, generate_weekends

START_DATE = "2025-06-04"
END_DATE = "2025-09-09"
HOLIDAYS = []  # None specified

def weekend_dates():
    return generate_weekends(START_DATE, END_DATE)

employees = [
    "Babb, K",
    "Pridham, A",
    "Morrison, G",
    "Perry, J",
    "Smith, J",
    "O'Donnell, K",
    "Woodman, M",
    "Mercer, S",
    "Taylor, A",
    "Tarhoni, M",
    "McCarthy, J",
]

soft_include = {
    # (none currently defined)
}

hard_include = {
    # (none currently defined)
}

hard_exclude = {
    "Babb, K": weekend_dates(),

    "Pridham, A": weekend_dates(),

    "Morrison, G": (
        weekend_dates() +
        generate_dates("2025-06-14", "2025-06-16") +
        generate_dates("2025-06-27", "2025-06-29") +
        generate_dates("2025-07-28", "2025-07-31") +
        generate_dates("2025-08-01", "2025-08-08")
    ),

    "Perry, J": (
        ["2025-06-25"] +
        generate_dates("2025-06-28", "2025-06-30") +
        generate_dates("2025-07-01", "2025-07-15") +
        generate_dates("2025-08-01", "2025-08-04") +
        ["2025-08-12"]
    ),

    "Smith, J": (
        generate_dates("2025-06-26", "2025-06-29") +
        generate_dates("2025-07-25", "2025-07-31") +
        generate_dates("2025-08-01", "2025-08-10") +
        generate_dates("2025-08-15", "2025-08-17") +
        generate_dates("2025-09-05", "2025-09-07")
    ),

    "O'Donnell, K": generate_dates("2025-07-11", "2025-07-20"),

    "Woodman, M": (
        ["2025-06-04"] +
        generate_dates("2025-06-21", "2025-06-22") +
        generate_dates("2025-06-26", "2025-06-30") +
        generate_dates("2025-07-03", "2025-07-06") +
        ["2025-07-10", "2025-07-15"] +
        generate_dates("2025-07-19", "2025-07-20") +
        generate_dates("2025-07-23", "2025-07-29") +
        generate_dates("2025-08-01", "2025-08-03") +
        ["2025-08-14", "2025-08-19"] +
        generate_dates("2025-08-21", "2025-08-26") +
        generate_dates("2025-09-05", "2025-09-10")
    ),

    "Mercer, S": (
        generate_dates("2025-06-04", "2025-06-23") +
        ["2025-07-29"] +
        generate_dates("2025-08-13", "2025-08-20") +
        generate_dates("2025-08-27", "2025-08-31") +
        ["2025-09-01"]
    ),

    "Taylor, A": (
        generate_dates("2025-06-03", "2025-06-06") +
        generate_dates("2025-06-10", "2025-06-11") +
        generate_dates("2025-06-15", "2025-06-17") +
        generate_dates("2025-06-20", "2025-06-26") +
        generate_dates("2025-06-28", "2025-06-29") +
        generate_dates("2025-07-01", "2025-07-02") +
        generate_dates("2025-07-05", "2025-07-06") +
        generate_dates("2025-07-12", "2025-07-15") +
        generate_dates("2025-07-19", "2025-07-27") +
        generate_dates("2025-07-30", "2025-07-31") +
        ["2025-08-02", "2025-08-04", "2025-08-05", "2025-08-06"] +
        generate_dates("2025-08-16", "2025-08-17") +
        generate_dates("2025-08-20", "2025-08-21") +
        ["2025-08-26", "2025-08-30", "2025-08-31", "2025-09-01"]
    ),

    "Tarhoni, M": [],

    "McCarthy, J": [],
}