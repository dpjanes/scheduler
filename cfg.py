from datetime import date, timedelta, datetime
from util import generate_dates, generate_weekends

START_DATE = "2025-09-10"
END_DATE = "2025-12-21"
HOLIDAYS = []  # No holidays specified in document

def weekend_dates():
    # Note: "Weekend" is now Friday, Saturday, and Sunday
    return generate_weekends(START_DATE, END_DATE, include_friday=True)

employees = [
    "McCarthy, J",
    "Tarhoni, M",
    "Smith, J",
    "Furey, A",
    "Woodman, M",
    "Mercer, S",
    "Perry, J",
    "O'Donnell, K",
    "Babb, K",
    "Morrison, G",
    "Pridham, A",
]

soft_include = {
    "Woodman, M": generate_dates("2025-09-26", "2025-09-28") +
                  generate_dates("2025-10-31", "2025-11-02"),
    "Mercer, S": generate_dates("2025-09-23", "2025-09-28") +
                 generate_dates("2025-10-06", "2025-10-12"),
    "Perry, J": generate_dates("2025-11-08", "2025-11-09") +
                generate_dates("2025-12-13", "2025-12-14"),
    "Morrison, G": generate_dates("2025-10-06", "2025-10-12") +
                   generate_dates("2025-11-17", "2025-11-24") +
                   generate_dates("2025-09-20", "2025-09-21"),
    "Pridham, A": generate_dates("2025-11-10", "2025-11-16") +
                  generate_dates("2025-12-19", "2025-12-21"),
}

hard_include = {
    # None currently defined
}

hard_exclude = {
    "McCarthy, J": (
        generate_dates("2025-09-12", "2025-09-14") +
        ["2025-09-20", "2025-09-27"] +
        generate_dates("2025-10-10", "2025-10-12") +
        generate_dates("2025-10-16", "2025-10-20") +
        generate_dates("2025-10-24", "2025-11-03") +
        generate_dates("2025-11-14", "2025-11-16")
    ),

    "Tarhoni, M": (
        generate_dates("2025-09-12", "2025-09-14") +
        ["2025-09-20", "2025-09-27"] +
        generate_dates("2025-10-10", "2025-10-12") +
        generate_dates("2025-10-16", "2025-10-20") +
        generate_dates("2025-10-24", "2025-11-03") +
        generate_dates("2025-11-14", "2025-11-16")
    ),

    "Smith, J": (
        generate_dates("2025-09-12", "2025-09-14") +
        ["2025-09-20", "2025-09-27"] +
        generate_dates("2025-10-10", "2025-10-12") +
        generate_dates("2025-10-16", "2025-10-20") +
        generate_dates("2025-10-24", "2025-11-03") +
        generate_dates("2025-11-14", "2025-11-16")
    ),

    "Furey, A": (
        ["2025-09-09", "2025-09-13", "2025-09-14", "2025-09-20", "2025-09-23", "2025-09-25", "2025-09-26", "2025-09-27", "2025-09-28", "2025-09-30", "2025-10-07"] +
        generate_dates("2025-10-08", "2025-10-15") +
        generate_dates("2025-10-24", "2025-10-26") +
        ["2025-10-29", "2025-11-01", "2025-11-02", "2025-11-11", "2025-11-15", "2025-11-23", "2025-11-24", "2025-11-26"]
    ),

    "Woodman, M": (
        generate_dates("2025-09-08", "2025-09-11") +
        generate_dates("2025-09-12", "2025-09-14") +
        generate_dates("2025-09-18", "2025-09-21") +
        generate_dates("2025-09-23", "2025-09-24") +
        ["2025-09-30", "2025-10-03", "2025-10-04", "2025-10-05", "2025-10-07", "2025-10-09"] +
        generate_dates("2025-10-17", "2025-10-19") +
        generate_dates("2025-11-03", "2025-11-06") +
        generate_dates("2025-11-07", "2025-11-09") +
        generate_dates("2025-11-10", "2025-11-13") +
        ["2025-11-14", "2025-11-16", "2025-11-19", "2025-11-26"] +
        generate_dates("2025-12-19", "2025-12-21")
    ),

    "Mercer, S": (
        generate_dates("2025-09-10", "2025-09-22") +
        generate_dates("2025-09-29", "2025-10-05") +
        generate_dates("2025-10-27", "2025-11-14") +
        generate_dates("2025-11-21", "2025-12-21")
    ),

    "Perry, J": (
        ["2025-11-28", "2025-11-29"] +
        generate_dates("2025-12-19", "2025-12-21")
    ),

    "O'Donnell, K": (
        generate_dates("2025-09-26", "2025-09-30") +
        generate_dates("2025-10-04", "2025-10-13") +
        generate_dates("2025-10-20", "2025-10-26")
    ),

    "Babb, K": (
        # Tuesdays between start and end date
    [
        d for d in generate_dates(START_DATE, END_DATE)
        if datetime.strptime(d, "%Y-%m-%d").weekday() == 1
    ] +
        generate_dates("2025-09-18", "2025-09-20") +
        generate_dates("2025-09-22", "2025-09-28") +
        generate_dates("2025-10-13", "2025-10-16") +
        ["2025-10-31"] +
        generate_dates("2025-11-08", "2025-11-23")
    ),

    "Morrison, G": (
        generate_dates("2025-10-13", "2025-11-09") +
        generate_dates("2025-12-05", "2025-12-21")
    ),

    "Pridham, A": (
        generate_dates("2025-09-09", "2025-09-13") +
        generate_dates("2025-09-24", "2025-09-29") +
        generate_dates("2025-10-10", "2025-10-20") +
        generate_dates("2025-10-22", "2025-11-03") +
        generate_dates("2025-12-10", "2025-12-15")
    ),
}