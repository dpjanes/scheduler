from datetime import date, timedelta

def generate_dates(start_date: str, end_date: str) -> list:
    # Parse the start and end dates from the ISO format
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    
    # Create a list of dates
    delta = end - start
    date_list = [(start + timedelta(days=i)).isoformat() for i in range(delta.days + 1)]
    
    return date_list


def generate_weekends(start_date: str, end_date: str):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    delta = timedelta(days=1)
    
    weekends = []
    current = start
    while current <= end:
        if current.weekday() in (5, 6):  # 5 = Saturday, 6 = Sunday
            weekends.append(current.isoformat())
        current += delta
    
    return weekends
