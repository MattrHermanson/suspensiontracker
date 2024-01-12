

def separate_url(func):
    def wrapper(request):
        
        url_vars = request.GET['bike']

        bike_id = url_vars[0:(url_vars.index('setup')-1)]

        setup_id = url_vars[(url_vars.index('=')+1):]

        return func(request, bike_id, setup_id)
    return wrapper

