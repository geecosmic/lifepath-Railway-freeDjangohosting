# api/utils.py
from datetime import datetime
from datetime import datetime, timedelta
from .models import YearlyPeriod
from django.shortcuts import render, get_object_or_404


from pyluach import dates
from datetime import datetime


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
    date =datetime.now()
    date=date.date()
    
    montth = (list(dates.HebrewDate.today()))[1]

    x = (list(dates.HebrewDate.today()))[0]
    y = (list(dates.HebrewDate.today()))[1]
    z = (list(dates.HebrewDate.today()))[2]

    k = ''
    m = ''
    q = ''

    u =0           
    x = str(x)
    for i in x :
        u+=int(i)
    v =0  
    for j in str(u) :
        v+=int(j)

    if y==13:
        y = "Adar II"
        gee='Pisces'
        k=12
        m='12L'

    if y==1:
        y = 'Nisan'
        gee='Aries'
        k=1
        m='1A'

    elif y==2:
        y = 'Iyar'
        gee='Taurus'
        k=2
        m='2B'

    elif y==3:
        y = 'Sivan'
        gee='Gemini'
        k=3
        m='3C'

    elif y==4:
        y = 'Tammuz'
        gee='Cancer'
        k=4
        m='4D'

    elif y==5:
        y = 'Av'
        gee='Leo'
        k=5
        m='5E'

    elif y==6:
        y = 'Elul'
        gee='Virgo'
        k=6
        m='6F'

    elif y==7:
        y = 'Tishre'
        gee='Libra'
        k=7
        m='7G'

    elif y==8:
        y = 'Heshvan'
        gee='Scorpio'
        k=8
        m='8H'

    elif y==9:
        y = 'Kishlev'
        gee='Sagittarius'
        k=9
        m='9I'

    elif y==10:
        y = 'Tevet'
        gee='Capricorn'
        k=10
        m='10J'
        q ='10jj'

    elif y==11:
        y = 'Shevat'
        gee='Aquarius'
        k=11
        m='11K'

    elif y==12:
        y= "Adar I"
        gee='Pisces'
        k=12
        m='12L'

    now = datetime.now() 
    hour = now.strftime("%H")
    if hour >=str(20):
        z=int(z)+1
    h = [2,22]   
    if z in h:
        year = (f'{z}nd of {y}, {x}')

    g = [1,21]   
    if z in g:
        year = (f'{z}st of {y}, {x}')

    l = [3,23]  
    if z in l:
        year = (f'{z}rd of {y}, {x}')

    p = [4,5,6,7,8,9,10,11,12,
            13,14,15,16,17,18,19,20,
            24,25,26,27,28,29,30]
        


    if z in p:
        year = (f'{z}th of {y}, {x}')

    return {
        # 'formatted_date': formatted_date,
        'year': year,
        'month_code': m,
        'month_code2': k,
        'month_code3': q,
        'montth':y,
        'gee':gee,
        'date':date
        # 'u': u,
        # 'v': v
    }    



# ----------for PERIODS EVERYWHERE ------------------------------

# utils.py
from datetime import datetime, timedelta
import pytz

def get_period_for_day_and_time(timezone='UTC'):
    now = datetime.now(pytz.timezone(timezone))

    # Calculate the precise length of each period in seconds (7 periods in a day)
    period_length_in_seconds = 86400 / 7  # 86400 seconds in 24 hours, divided by 7 periods

    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight of the current day
    elapsed_time_in_seconds = (now - start_time).total_seconds()
    period_index = int(elapsed_time_in_seconds // period_length_in_seconds)
   
    # Period mappings for each day
    period_mappings = {
        'Sunday': ['G', 'A', 'B', 'C', 'D', 'E', 'F'],
        'Monday': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
        'Tuesday': ['F', 'G', 'A', 'B', 'C', 'D', 'E'],
        'Wednesday': ['B', 'C', 'D', 'E', 'F', 'G', 'A'],
        'Thursday': ['E', 'H', 'C', 'A', 'B', 'C', 'D'],
        'Friday': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'Saturday': ['D', 'E', 'F', 'G', 'A', 'B', 'C'],
    }

    today = now.strftime("%A")
    periods = period_mappings.get(today, ['Invalid'])
    current_period_letter = periods[period_index] if 0 <= period_index < len(periods) else "Invalid period"

    return today, current_period_letter, period_index
# -----------------------------------------------------------------



def yearly_stuff():
    yearlyperiods= YearlyPeriod.objects.all() 
    # yearlyperiod= None

  
    
  

    return yearlyperiods
    