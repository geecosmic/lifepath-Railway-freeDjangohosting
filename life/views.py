# api/views.py
# from rest_framework.response import Response
from django.shortcuts import render
# from rest_framework.decorators import api_view
from .utils import reduce_to_single_digit,get_period_for_day_and_time
from datetime import datetime
from datetime import datetime, timedelta
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView
from .forms import DateConversionForm
from django.shortcuts import render, get_object_or_404
from .models import Period,YearlyPeriod
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.decorators.csrf import csrf_exempt
from .utils import get_period_for_day_and_time
import pytz
from django.views.decorators.http import require_http_methods

from django.shortcuts import render
from .utils import hebrew_date_info,yearly_stuff


# from .forms import CustomUserCreationForm

def get_period_view(request):
    # Read the timezone from the cookie
    timezone = request.COOKIES.get('timezone', 'UTC')  # Default to UTC if no timezone cookie is found

    # Call the function to get the period data
    today, period_letter, period_index = get_period_for_day_and_time(timezone=timezone)

    # Render your template with the period information
    return JsonResponse({
        'day': today,
        'period_letter': period_letter,
        'period_index': period_index,
    })

@csrf_exempt
def get_period(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        timezone = data.get('timezone', 'UTC')  # Default to UTC if no timezone provided

        try:
            # Validate the timezone
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            return JsonResponse({"error": "Invalid Time Zone"}, status=400)

        # Get the period based on the provided timezone
        today, period_letter, period_index = get_period_for_day_and_time(timezone=timezone)

        return JsonResponse({
            'day': today,
            'period_letter': period_letter,
            'period_index': period_index
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


def privacy_page(request):
    
    return render(request, 'privacy.html')

def donate(request):
    
    return render(request, 'donate.html')



def main_page(request, id=None, type=None):

    timezone = request.COOKIES.get('timezone', 'UTC')
    # --------------------yearly_cycle------------------

    start_date = None
    month_input=None
    date_input=None
    cycle_periods = []

    yearlyperiods= YearlyPeriod.objects.all()
    
    # if request.method == "POST":
    if request.method == "POST" and 'month' in request.POST:
        # Get the user inputs
        month_input = request.POST.get('month').title()
        date_input = request.POST.get('date')
        
        # Convert the month and date into a valid datetime object
        try:
            # Combine month and date with the current year
            start_date = datetime.strptime(f"{month_input} {date_input}", '%B %d')
            # Adjust the start date to the current year
            start_date = start_date.replace(year=datetime.now().year)
        except ValueError:
            start_date = None
        
        if start_date:
            # Calculate exactly 7 periods of 52 days each
            current_date = start_date + timedelta(days=1)  # Start period one day after the given date
            period_index = 1

            while period_index <= 7:
                # Calculate the end date for the current period (52 days starting from the next day of start_date)
                end_date = current_date + timedelta(days=51)  # 52 days including the start date
                
                # Append the start and end of each 52-day period to the cycle list
                cycle_periods.append({
                    'period_number': period_index,
                    # 'start_date': current_date.strftime("%B %d, %Y"),
                    'start_date': current_date.strftime("%b %d"),
                    # 'end_date': end_date.strftime("%B %d, %Y")
                    'end_date': end_date.strftime("%b %d")
                })
                
                # Move to the next period start date (52 days later)
                current_date = end_date + timedelta(days=1)  # The next period starts the day after the current period ends
                period_index += 1

    # --------------------yearly_cycle- ends-------------------

    today, current_period_letter, period_index = get_period_for_day_and_time(timezone=timezone)

    periods = Period.objects.all()  # Retrieve all periods
    period = None

    yearlyperiods= YearlyPeriod.objects.all() 
    yearlyperiod= None

    # if id:
    #     period = get_object_or_404(Period, id=id)
    #     yearlyperiod = get_object_or_404(YearlyPeriod, id=id)


    if id and type == 'period':
        period = get_object_or_404(Period, id=id)
    elif id and type == 'yearlyperiod':
        yearlyperiod = get_object_or_404(YearlyPeriod, id=id)


    context = {
        'periods': periods,
        'selected_period': period,  # Pass the selected period details to the template

        # -----------# for periods autodisplay---------------------
        'today': today,
        'current_period_letter':current_period_letter ,
        'period_index': period_index,
        'cycle_periods': cycle_periods,
        'start_date':  start_date,
        "month_input":month_input,
        'date_input':date_input,
        'yearlyperiods':yearlyperiods,
        'selected_yearlyperiod': yearlyperiod,

        
    }

    return render(request, 'main_page.html', context)






def tikkun(request):

    yearlyperiods = yearly_stuff()
    # yearlyperiods= YearlyPeriod.objects.all() 
    date_info = hebrew_date_info()

    context = {
        'year': date_info['year'],
        'month_code': date_info['month_code'],
        'month_code2': date_info['month_code2'],
        'month_code3': date_info['month_code3'],
        'montth'  : date_info['montth'],
        'gee'  : date_info['gee'],
        'date':date_info['date'],

        'yearlyperiods' : yearlyperiods,
        # 'selected_yearlyperiod' :yearlyperiods

    }
    return render(request, 'tikkun.html', context)





def path_numbers(request):
    yearlyperiods= YearlyPeriod.objects.all() 


    result = result_py = None  # Initialize the variables
    result2 = result3 = result4= None  # Initialize the variables
    current_yearx = datetime.now().year
    current_year = datetime.now().year

    # First form handling
    if request.method == "POST" and 'day' in request.POST:
        day = request.POST.get('day', '').strip()
        month = request.POST.get('month', '').strip()
        year = request.POST.get('year', '').strip()
  
        # Ensure all fields are filled and valid integers
        if day and month and year:
            try:
                day = int(day)
                month = int(month)
                year = int(year)

                # Sum the values
                result = day + month + year
                result2 = day
                 

                # Reduce to a single digit
                while result >= 10:
                    result = sum(int(digit) for digit in str(result))

                while result2 >= 10:
                    result2 = sum(int(digit) for digit in str(result2))

            except ValueError:
                # Handle the case where day, month, or year is not a valid integer
                result = None

    # Second form handling
    if request.method == "POST" and 'month2' in request.POST:
        day2 = request.POST.get('day2', '').strip()
        month2 = request.POST.get('month2', '').strip()
        year2 = request.POST.get('year2', '').strip()

        # Ensure all fields are filled and valid integers
        if day2 and month2 and year2:
            try:
                day2 = int(day2)
                month2 = int(month2)
                year2 = int(year2)

                # Sum the values
                result_py = day2 + month2 + year2

                # Reduce to a single digit
                while result_py >= 10:
                    result_py = sum(int(digit) for digit in str(result_py))

            except ValueError:
                # Handle invalid integers
                result_py = None
    # Third form handling
    if request.method == "POST" and 'month3' in request.POST:
        month3 = request.POST.get('month3', '').strip()
        year3 = request.POST.get('year3', '').strip()

        # Ensure all fields are filled and valid integers
        if month3 and year3:
            try:
                month3 = int(month3)
                year3 = int(year3)

                # Sum the values
                result3 = month3 + year3

                # Reduce to a single digit
                while result3 >= 10:
                    result3 = sum(int(digit) for digit in str(result3))

            except ValueError:
                # Handle invalid integers
                result3 = None
    # Forth form handling
    if request.method == "POST" and 'month4' in request.POST:
        month4 = request.POST.get('month4', '').strip()
        year4 = request.POST.get('year4', '').strip()

        # Ensure all fields are filled and valid integers
        if month4 and year4:
            try:
                month4 = int(month4)
                year4 = int(year4)

                # Sum the values
                result4 = month4 + year4

                # Reduce to a single digit
                while result4 >= 10:
                    result4 = sum(int(digit) for digit in str(result4))

            except ValueError:
                # Handle invalid integers
                result4 = None

    # Reduce the current year to a single digit
    while current_year >= 10:
        current_year = sum(int(digit) for digit in str(current_year))
        
    # while current_yearx >= 10:
    #     current_yearx = sum(int(digit) for digit in str(current_yearx))

    # Context to pass to the template
    context = {
        'current_yearx': current_yearx,
        'current_year': current_year,
        'result': result,
        'result2': result2,
        'result3': result3,
        'result4': result4,
        'result_py': result_py,
        'yearlyperiods' : yearlyperiods,
    }

    return render(request, 'path_numbers.html', context)






# ----------------new daily & yearly----------------------------------
from django.shortcuts import render
from datetime import datetime, timedelta

def all_period(request):
    # periods = Period.objects.all()

# -------------------jewish birthday-----------------------------
        

    if request.method == 'POST':
        # Get the single input field for the birthday (in YYYY-MM-DD format from the date picker)
        birthday = request.POST.get('birthday')

        if birthday:
            try:
                # Split the input to extract year, month, and day
                year, month, day = map(int, birthday.split('-'))

                # Create a Gregorian date using Python's datetime module (order should be year, month, day)
                gregorian_birthday = datetime(year, month, day)

                # Convert the Gregorian date to a Hebrew date using pyluach
                hebrew_date = dates.GregorianDate(year, month, day).to_heb()

                # Format the Hebrew date for display (day, month, year)
                hebrew_birthday = f"{hebrew_date.day} {hebrew_date.month_name()} {hebrew_date.year}"

            except (ValueError, TypeError):
                # Handle invalid date input
                hebrew_birthday = "Invalid date format. Please use YYYY-MM-DD."


        
    date_info = hebrew_date_info()

   

    context = {
        

        'year': date_info['year'],
        'month_code': date_info['month_code'],
        'month_code2': date_info['month_code2'],
        'montth'  : date_info['montth'],
        'gee'  : date_info['gee'],
        'date':date_info['date']
    }

    return render(request, 'jewishbirthday.html', context)


# --------------------to display yearly cycly--------------------------------













from django.shortcuts import render
from pyluach import dates

def get_zodiac_image(request):
    # Hebrew date today
    hebrew_date = dates.HebrewDate.today()

    # Get the month, day, and year
    month = hebrew_date.month
    day = hebrew_date.day

    # Calculate which 5-day period we're in
    period_index = (day - 1) // 5  # Integer division to determine the period

    # Define Zodiac sign and image mappings (example: 1=Aries, 2=Taurus, etc.)
    zodiac_signs = {
        1: 'aries',
        2: 'taurus',
        3: 'gemini',
        4: 'cancer',
        5: 'leo',
        6: 'virgo',
        7: 'libra',
        8: 'scorpio',
        9: 'sagittarius',
        10: 'capricorn',
        11: 'aquarius',
        12: 'pisces'
    }

    # Get the zodiac sign for the month
    zodiac = zodiac_signs.get(month, 'aries')  # Fallback to Aries if not found

    # Image index (1 to 6)
    image_index = (period_index % 6) + 1  # Ensure the index is within 1-6

    # Build the image path
    image_path = f"images/zodiac/{zodiac}/{image_index}.png"

    context = {
        'image_path': image_path,
        'hebrew_date': hebrew_date,
        'zodiac': zodiac,
        'image_index': image_index

    }

    return render(request, 'display_image.html', context)






# ----------------------DESTINy NUMBER--------------

from django.shortcuts import render
from datetime import datetime

# Function to convert letters to numbers
def letter_to_number(letter):
    letter = letter.upper()  # Convert to uppercase
    if letter.isalpha():  # Ensure it's a letter
        return (ord(letter) - ord('A') + 1)
    return 0

# Function to reduce numbers to a single digit or master number
def reduce_to_single_digit(num):
    while num > 9 and num not in [11, 22]:  # Keep master numbers 11 and 22
        num = sum(int(digit) for digit in str(num))
    return num

# Function to calculate the destiny number
def calculate_destiny_number(full_name):
    total = sum(letter_to_number(letter) for letter in full_name if letter.isalpha())
    return reduce_to_single_digit(total)

# View to handle form submission and calculate destiny number
def destiny_number_view(request):
    result = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')  # Get the full name from the form
        if full_name:  # Ensure full_name is provided
            result = calculate_destiny_number(full_name)

    current_year = datetime.now().year  # For additional context if needed
    context = {
        'result_destiny': result,
        'current_year': current_year
    }

    # return render(request, 'destiny_number.html', context)
    return render(request, 'path_numbers.html', context)


# def YearlyPeriod(request):

# def yearly_cycle(request):

#     hebrew_birthday = None

#     # -----------jewish-birthday  script ---------------------

#     if request.method == 'POST':
#         # Get the single input field for the birthday (in YYYY-MM-DD format)
#         birthday = request.POST.get('birthday')

#         if birthday:
#             try:
#                 # Split the input to extract year, month, and day
#                 year, month, day = map(int, birthday.split('-'))

#                 # Create a Gregorian date using Python's datetime module
#                 gregorian_birthday = datetime(year, month, day)

#                 # Convert the Gregorian date to a Hebrew date using pyluach
#                 hebrew_date = dates.GregorianDate(year, month, day).to_heb()

#                 # Format the Hebrew date for display (day, month, year)
#                 hebrew_birthday = f"{hebrew_date.day} {hebrew_date.month_name()} {hebrew_date.year}"

#             except (ValueError, TypeError):
#                 hebrew_birthday = "Invalid date format. Please use YYYY-MM-DD."
                
                
    # -------------------birthday ends----------------------------


    # date_info = hebrew_date_info()            
    
    # context = {
    #     # 'current_day': today,
    #     # 'current_period_letter': current_period_letter,
    #     'hebrew_birthday':hebrew_birthday,
       
    #     # ------------------------------yearly_cycle------------
    # }
    
    # return render(request, 'yearly_cycle.html', context)

