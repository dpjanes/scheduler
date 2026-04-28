"""
Important:
Instructions for AI:

I have the following program for scheduling. 
I need to update it with new data, which will come from a DOCX/PDF I am uploading. 
Please replace the constraints that are in _this_ python file with the new ones. 
There are other constraints that are mentioned - these can be ignored for now, 
as there is other code to deal with that.

Note that the date range changes, and the doctor list may be slightly different.
"""

from datetime import date, timedelta, datetime
from util import generate_dates, generate_weekends

# Updated from DOCX
START_DATE = "2026-01-05"
END_DATE = "2026-05-04"
# Start Date: Mon Jan 5
# End Date: Mon May 4
HOLIDAYS = []

def weekend_dates():
    # Weekend is Fri/Sat/Sun for all MDs
    return generate_weekends(START_DATE, END_DATE, include_friday=True)

employees = [
    "McCarthy",
    "Tarhoni",
    "Smith",
    "Furey",
    "Woodman",
    # "Mercer",
    "Perry",
    "O'Donnell",
    "Babb",
    "Morrison",
    "Pridham",
]

# ------------------------------------------------------------
#  PREFER CALL  (soft_include)
# ------------------------------------------------------------
soft_include = {
    "Woodman": (
        generate_dates("2025-09-26", "2025-09-28") +
        generate_dates("2025-10-31", "2025-11-02")
    ),

    # "Mercer": (
    #     generate_dates("2025-09-23", "2025-09-28") +
    #     generate_dates("2025-10-06", "2025-10-12")
    # ),

    "Perry": (
        generate_dates("2025-11-08", "2025-11-09") +
        generate_dates("2025-12-13", "2025-12-14")
    ),

    "Morrison": (
        generate_dates("2025-10-06", "2025-10-12") +
        generate_dates("2025-11-17", "2025-11-24") +
        generate_dates("2025-09-20", "2025-09-21")
    ),

    "Pridham": (
        generate_dates("2025-11-10", "2025-11-16") +
        generate_dates("2025-09-19", "2025-09-21") +
        generate_dates("2025-12-19", "2025-12-21")
    ),
}

# ------------------------------------------------------------
#  HARD INCLUDE (none given)
# ------------------------------------------------------------
hard_include = {}


# ------------------------------------------------------------
#  NO CALL (hard_exclude)
# ------------------------------------------------------------
hard_exclude = {

    # McCarthy: NONE LISTED IN DOC
    "McCarthy": [],

    # Tarhoni: NONE
    "Tarhoni": [],

    # Smith
    "Smith": (
        generate_dates("2025-09-12", "2025-09-14") +
        ["2025-09-20"] +
        ["2025-09-27"] +
        generate_dates("2025-10-10", "2025-10-12") +
        generate_dates("2025-10-16", "2025-10-20") +
        generate_dates("2025-10-24", "2025-11-03") +
        generate_dates("2025-11-14", "2025-11-16")
    ),

    # Furey
    "Furey": (
        ["2025-09-09"] +
        generate_dates("2025-09-13", "2025-09-14") +
        ["2025-09-20", "2025-09-23"] +
        generate_dates("2025-09-25", "2025-09-28") +
        ["2025-09-30"] +
        generate_dates("2025-10-07", "2025-10-15") +
        generate_dates("2025-10-24", "2025-10-26") +
        ["2025-10-29"] +
        generate_dates("2025-11-01", "2025-11-02") +
        ["2025-11-11", "2025-11-15"] +
        generate_dates("2025-11-23", "2025-11-24") +
        ["2025-11-26"]
    ),

    # Woodman
    "Woodman": (
        generate_dates("2025-09-12", "2025-09-14") +
        generate_dates("2025-09-19", "2025-09-21") +
        generate_dates("2025-10-03", "2025-10-05") +
        generate_dates("2025-10-17", "2025-10-19") +
        generate_dates("2025-11-07", "2025-11-09") +
        generate_dates("2025-11-14", "2025-11-16") +
        generate_dates("2025-12-19", "2025-12-21") +
        generate_dates("2025-09-08", "2025-09-11") +
        ["2025-09-18"] +
        generate_dates("2025-09-23", "2025-09-24") +
        ["2025-09-30"] +
        ["2025-10-07", "2025-10-09"] +
        generate_dates("2025-11-03", "2025-11-06") +
        generate_dates("2025-11-10", "2025-11-13") +
        ["2025-11-19", "2025-11-26"]
    ),

    # Mercer
    # "Mercer": (
    #     generate_dates("2025-09-10", "2025-09-22") +
    #     generate_dates("2025-09-29", "2025-10-05") +
    #     generate_dates("2025-10-27", "2025-11-14") +
    #     generate_dates("2025-11-21", "2025-12-21")
    # ),

    # Perry
    "Perry": (
        ["2025-11-28", "2025-11-29"] +
        generate_dates("2025-12-19", "2025-12-21")
    ),

    # O'Donnell
    "O'Donnell": (
        generate_dates("2025-09-26", "2025-09-30") +
        generate_dates("2025-10-04", "2025-10-13") +
        generate_dates("2025-10-20", "2025-10-26")
    ),

    # Babb
    "Babb": (
        # All Tuesdays
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

    # Morrison
    "Morrison": (
        generate_dates("2025-10-13", "2025-11-09") +
        generate_dates("2025-12-05", "2025-12-21")
    ),

    # Pridham
    "Pridham": (
        generate_dates("2025-12-10", "2025-12-15") +
        generate_dates("2025-09-24", "2025-09-29") +
        generate_dates("2025-09-09", "2025-09-13") +
        generate_dates("2025-10-10", "2025-10-20") +
        generate_dates("2025-10-22", "2025-11-03")
    ),
}