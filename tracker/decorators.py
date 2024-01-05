

def separate_url(func):
    def wrapper(request):
        
        url_vars = request.GET['bike']
    
        bike_id = url_vars[0]
        setup_id = url_vars[(url_vars.index('=')+1):]

        print(f'Bike ID: {bike_id}\nSetup ID: {setup_id}\nSetup ID Type: {type(setup_id)}')

        func(request, bike_id, setup_id)
        return func(request, bike_id, setup_id)
    return wrapper

