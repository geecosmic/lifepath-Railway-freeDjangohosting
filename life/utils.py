# api/utils.py
from datetime import datetime, timedelta
from .models import YearlyPeriod
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import pytz
from pyluach import dates


def reduce_to_single_digit(n):
    # Keep summing the digits until the result is a single digit
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
    
    return n


from datetime import datetime, timedelta

def get_yearly_cycle(month_input, date_input):
    # Initialize variables
    start_date = None
    cycle_periods = []
    
    # Convert the month and date into a valid datetime object
    try:
        # Combine month and date with the current year
        start_date = datetime.strptime(f"{month_input} {date_input}", '%B %d')
        # Adjust the start date to the current year
        start_date = start_date.replace(year=datetime.now().year)
    except ValueError:
        return None, []

    if start_date:
        # Calculate exactly 7 periods of 52 days each
        current_date = start_date + timedelta(days=1)  # Start period one day after the given date
        period_index = 1

        while period_index <= 7:
            # Calculate the end date for the current period
            end_date = current_date + timedelta(days=51)
            
            # Append the period to the cycle list
            cycle_periods.append({
                'period_number': period_index,
                'start_date': current_date.strftime("%B %d, %Y"),
                'end_date': end_date.strftime("%B %d, %Y")
            })
            
            # Move to the next period start date
            current_date = end_date + timedelta(days=1)
            period_index += 1
    
    return start_date, cycle_periods





def hebrew_date_info():
    """Return Hebrew date information with English month name, zodiac, and custom codes."""
    
    # Get current Hebrew date
    heb = dates.HebrewDate.today()
    
    year = heb.year
    month_num = heb.month
    day = heb.day

    # Month mapping: (English name, Zodiac, month_code2, month_code)
    month_map = {
        1:  ("Nisan",       "Aries",       1,  "1b"),
        2:  ("Iyar",        "Taurus",      2,  "2b"),
        3:  ("Sivan",       "Gemini",      3,  "3b"),
        4:  ("Tammuz",      "Cancer",      4,  "4b"),
        5:  ("Av",          "Leo",         5,  "5b"),
        6:  ("Elul",        "Virgo",       6,  "6b"),
        7:  ("Tishre",      "Libra",       7,  "7b"),
        8:  ("Heshvan",     "Scorpio",     8,  "8b"),
        9:  ("Kishlev",     "Sagittarius", 9,  "9b"),
        10: ("Tevet",       "Capricorn",   10, "10b"),
        11: ("Shevat",      "Aquarius",    11, "11b"),
        12: ("Adar I",      "Pisces",      12, "12b"),
        13: ("Adar II",     "Pisces",      12, "12b"),
    }

    month_name, zodiac, month_code2, month_code = month_map.get(
        month_num, ("Unknown", None, None, None)
    )
    
    # month_code3 = "10jj" if month_num == 10 else ""

    # Day ordinal suffix
    if day in (2, 22):
        suffix = "nd"
    elif day in (1, 21):
        suffix = "st"
    elif day in (3, 23):
        suffix = "rd"
    else:
        suffix = "th"

    formatted_date = f"{day}{suffix} of {month_name}, {year}"

    return {
        'year': formatted_date,
        'month_code': month_code,
        'month_code2': month_code2,
        # 'month_code3': month_code3,
        'montth': month_name,
        'gee': zodiac,
        'date': datetime.now().date()
    }





# ----------for PERIODS EVERYWHERE ------------------------------


from datetime import datetime, timedelta
import pytz

def get_period_for_day_and_time(timezone='UTC'):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    # Midnight of the current day
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    period_length = timedelta(seconds=86400 / 7)
    
    # Calculate current period
    elapsed = now - start_of_day
    period_index = int(elapsed.total_seconds() // period_length.total_seconds())
    
    # Start and end times
    period_start = start_of_day + (period_index * period_length)
    period_end = period_start + period_length
    
    # Period letter
    period_mappings = {
        'Sunday':    ['G', 'A', 'B', 'C', 'D', 'E', 'F'],
        'Monday':    ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
        'Tuesday':   ['F', 'G', 'A', 'B', 'C', 'D', 'E'],
        'Wednesday': ['B', 'C', 'D', 'E', 'F', 'G', 'A'],
        'Thursday':  ['E', 'H', 'C', 'A', 'B', 'C', 'D'],
        'Friday':    ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'Saturday':  ['D', 'E', 'F', 'G', 'A', 'B', 'C'],
    }

    today = now.strftime("%A")
    periods = period_mappings.get(today, ['Invalid'])
    current_period = periods[period_index] if 0 <= period_index < len(periods) else "Invalid"

    # Calculate remaining time safely
    remaining = period_end - now
    hours = int(remaining.total_seconds() // 3600)
    minutes = int((remaining.total_seconds() % 3600) // 60)
    seconds = int(remaining.total_seconds() % 60)
    
    return {
        'day': today,
        'period': current_period,
        'period_index': period_index,
        'start_time': period_start,
        'end_time': period_end,
        'start_formatted': period_start.strftime("%H:%M"),
        'end_formatted': period_end.strftime("%H:%M"),
        # 'end_formatted': period_end.strftime("%H:%M:%S"),
        'remaining_formatted': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    }

# utils.py
# from datetime import datetime, timedelta
# import pytz

# def get_period_for_day_and_time(timezone='UTC'):
#     now = datetime.now(pytz.timezone(timezone))

#     # Calculate the precise length of each period in seconds (7 periods in a day)
#     period_length_in_seconds = 86400 / 7  # 86400 seconds in 24 hours, divided by 7 periods

#     start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight of the current day
#     elapsed_time_in_seconds = (now - start_time).total_seconds()
#     period_index = int(elapsed_time_in_seconds // period_length_in_seconds)
   
#     # Period mappings for each day
#     period_mappings = {
#         'Sunday': ['G', 'A', 'B', 'C', 'D', 'E', 'F'],
#         'Monday': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
#         'Tuesday': ['F', 'G', 'A', 'B', 'C', 'D', 'E'],
#         'Wednesday': ['B', 'C', 'D', 'E', 'F', 'G', 'A'],
#         'Thursday': ['E', 'H', 'C', 'A', 'B', 'C', 'D'],
#         'Friday': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
#         'Saturday': ['D', 'E', 'F', 'G', 'A', 'B', 'C'],
#     }

#     today = now.strftime("%A")
#     periods = period_mappings.get(today, ['Invalid'])
#     current_period_letter = periods[period_index] if 0 <= period_index < len(periods) else "Invalid period"

#     return today, current_period_letter, period_index
# -----------------------------------------------------------------



def yearly_stuff():
    yearlyperiods= YearlyPeriod.objects.all() 
    # yearlyperiod= None

    return yearlyperiods
    