# context_processors.py
from .models import Period,YearlyPeriod
 
def periods_processor(request):
    # periods = Period.objects.all().order_by('-id')  
    periods = Period.objects.all().order_by('-title')  
    # yearlyperiods = YearlyPeriod.objects.all('-title')
    # periods = Period.objects.all() 
# Fetch all periods or filter as needed
    # return {'periods': periods,'yearlyperiods': yearlyperiods}
    return {'periods': periods}

