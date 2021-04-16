import datetime as dt

def current_year(request):
    return {
        'year': dt.datetime.now().year,
    }