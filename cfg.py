from datetime import date
from util import generate_dates

START_DATE = "2024-11-08"
END_DATE = "2025-02-28"
HOLIDAYS = ["2024-12-25", "2024-12-26", "2025-01-01", "2025-02-17" ]  # Example holidays


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

hard_include = {
    "Woodman, M": ["2025-01-10", "2025-01-11", "2025-01-12"],
}
hard_exclude = {
    "Perry, J": ["2024-11-11", "2024-11-30", "2024-12-21"],
    "McCarthy, J": ["2024-11-12", "2024-11-13", "2024-11-14", "2024-11-15", "2024-11-16", "2024-11-17"],    
}
hard_exclude["Joshi, P"] = generate_dates("2024-12-20", END_DATE)

