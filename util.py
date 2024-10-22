from datetime import date, timedelta

def generate_dates(start_date: str, end_date: str) -> list:
    # Parse the start and end dates from the ISO format
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    
    # Create a list of dates
    delta = end - start
    date_list = [(start + timedelta(days=i)).isoformat() for i in range(delta.days + 1)]
    
    return date_list
