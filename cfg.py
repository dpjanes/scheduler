from datetime import date
from util import generate_dates

START_DATE = "2024-11-10"
END_DATE = "2025-01-18"
HOLIDAYS = ["2024-11-11", "2024-12-25", "2024-12-26", "2025-01-01", "2025-02-17" ]


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

soft_include = {
    "Mercer, S": generate_dates("2024-11-18", "2024-11-24") + generate_dates("2024-11-22", "2024-11-28"),
    "O'Donnell, K": generate_dates("2024-11-29", "2024-12-05") + generate_dates("2024-12-13", "2024-12-19") + generate_dates("2025-01-10", "2025-01-16"),
    "Woodman, M": generate_dates("2025-01-06", "2025-01-18")
}

hard_include = {
    "Woodman, M": ["2024-12-24", "2025-01-10", "2025-01-11", "2025-01-12"],
}

hard_exclude = {
    "Perry, J": [
        "2024-11-11", "2024-11-15", "2024-11-16", "2024-11-30", "2024-12-21",
        "2024-12-24", "2024-12-25", "2024-12-26", "2024-12-31", "2025-01-01"
    ],
    "McCarthy, J": [
        "2024-11-12", "2024-11-13", "2024-11-14", "2024-11-15", "2024-11-16", "2024-11-17"
    ],
    "Babb, K": [
        "2024-11-15", "2024-11-16"
    ],
    "Morrison, G": [
        "2024-11-15", "2024-11-16"
    ],
    "Pridham, A": [
        # Assuming Pridham is removed from the entire schedule, so this will be all dates in the call schedule range.
    ],
    "Mercer, S": [
        "2024-11-15", "2024-11-16"
    ],
    "O'Donnell, K": [
        "2024-11-15", "2024-11-16", "2024-11-21", "2024-11-22", "2024-11-23", 
        "2024-11-24", "2024-11-25", "2024-12-11"
    ]
}
hard_exclude["Joshi, P"] = generate_dates("2024-12-18", END_DATE)

