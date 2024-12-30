from datetime import datetime, timedelta  # Import datetime and timedelta classes from datetime module
import pytz  # Import pytz module for timezone handling

ksa_timezone = pytz.timezone('Asia/Riyadh')  # Define the timezone for KSA (Kingdom of Saudi Arabia)

def get_date(days=0, specific_date=None):
    # If a specific date is provided, parse it into a datetime object
    if specific_date:
        date = datetime.strptime(specific_date, "%Y-%m-%d")
    else:
        # Get the current date and time in the KSA timezone
        date = datetime.now(ksa_timezone)
    
    # Return the date adjusted by the specified number of days
    return (date + timedelta(days=days)).strftime("%Y-%m-%d")

def get_day(date):
    # If the date is provided as a string, parse it into a datetime object
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    
    # Return the day of the week for the given date
    return date.strftime("%A")

# Example usage:
# print("Today's date:", get_date())  # Print today's date
# print("Today is:", get_day(get_date()))  # Print the day of the week for today
# print("Date 10 days from today:", get_date(10))  # Print the date 10 days from today
# print("Day 10 days from today:", get_day(get_date(10)))  # Print the day of the week 10 days from today
# print("Date 10 days before today:", get_date(-10))  # Print the date 10 days before today
# print("Day 10 days before today:", get_day(get_date(-10)))  # Print the day of the week 10 days before today
# print("Specific date (2023-10-01):", get_date(specific_date="2023-10-01"))  # Print the specific date 2023-10-01
# print("Day of specific date (2023-10-01):", get_day(get_date(specific_date="2023-10-01")))  # Print the day of the week for the specific date 2023-10-01
# print("Date 5 days after specific date (2023-10-01):", get_date(5, "2023-10-01"))  # Print the date 5 days after the specific date 2023-10-01
# print("Day 5 days after specific date (2023-10-01):", get_day(get_date(5, "2023-10-01")))  # Print the day of the week 5 days after the specific date 2023-10-01