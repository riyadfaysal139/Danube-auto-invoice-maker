from datetime import datetime, timedelta
import pytz

ksa_timezone = pytz.timezone('Asia/Riyadh')

def get_date(days=0, specific_date=None):
    if specific_date:
        date = datetime.strptime(specific_date, "%Y-%m-%d")
    else:
        date = datetime.now(ksa_timezone)
    return (date + timedelta(days=days)).date()

def get_day(date):
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime("%A")

""" Example usage:
print("Today's date:", get_date())
print("Today is:", get_day(get_date()))
print("Date 10 days from today:", get_date(10))
print("Day 10 days from today:", get_day(get_date(10)))
print("Date 10 days before today:", get_date(-10))
print("Day 10 days before today:", get_day(get_date(-10)))
print("Specific date (2023-10-01):", get_date(specific_date="2023-10-01"))
print("Day of specific date (2023-10-01):", get_day(get_date(specific_date="2023-10-01")))
print("Date 5 days after specific date (2023-10-01):", get_date(5, "2023-10-01"))
print("Day 5 days after specific date (2023-10-01):", get_day(get_date(5, "2023-10-01")))"""