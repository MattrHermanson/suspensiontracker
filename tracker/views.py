from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Bike, Setup, Variation, Fork_Setting, Shock_Setting
from users.models import User
from django.urls import reverse

@login_required
def setup(request):

    return render(request, 'tracker/setup.html')

@login_required
def home(request):

    return render(request, 'tracker/home.html')

@login_required
def bikes(request):

    user = User.objects.get(email=request.user.email)

    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        front_travel = request.POST['front_travel']
        rear_travel = request.POST['rear_travel']
        if request.POST['progression'] != 0:
            progression = int(request.POST['progression'])
            progression *= 0.01
        else:
            progression = 0


        new_bike = Bike(name=name, owner=user, brand=brand, front_travel=front_travel, rear_travel=rear_travel, progression=progression)
        new_bike.save()
        
        return redirect('tracker:tracker-bikes')


    context = {
        'users_bikes' : list(user.bike_set.all())
    }
    

    return render(request, 'tracker/bikes.html', context)

@login_required
def setups(request):

    #terrible way of getting info from url
    url_vars = request.GET['bike']
    
    bike_id = url_vars[0]
    setup_id = url_vars[(url_vars.index('=')+1):]

    variation_list = []
    latest_variation = []
    

    ALL_FORK_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'ramp_up']
    ALL_SHOCK_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'hbo']
    latest_fork_settings = {}
    latest_shock_settings = {}


    bike_id = int(bike_id)
    if setup_id != 'none':
        setup_id = int(setup_id)
        variation_list = list(Variation.objects.filter(setup_id=setup_id))
        if len(variation_list) > 0:
            latest_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')

            #make a dictionary of all settings and their values
            for setting in ALL_FORK_SETTINGS:
                latest_fork_settings[setting] = getattr(latest_variation.fork_setting, setting)
            
            for setting in ALL_SHOCK_SETTINGS:
                latest_shock_settings[setting] = getattr(latest_variation.shock_setting, setting)
            
            has_variations = True
        else:
            has_variations = False

    if request.method == 'POST':

        setup_setting_keys = ['f_psi', 'f_hsc', 'f_lsc', 'f_hsr', 'f_lsr', 'f_tokens', 'f_rampup', 'r_psi', 'r_hsc', 'r_lsc', 'r_hsr', 'r_lsr', 'r_tokens', 'r_hbo']

        if 'variation_button' in request.POST:
            
            setup_setting = dict.fromkeys(setup_setting_keys, 0)

            for setting in setup_setting_keys:
                if request.POST[setting]:
                    setup_setting[setting] = request.POST[setting]

            new_fork_setting = Fork_Setting()
            new_fork_setting.psi = setup_setting['f_psi']
            new_fork_setting.hsc = setup_setting['f_hsc']
            new_fork_setting.lsc = setup_setting['f_lsc']
            new_fork_setting.hsr = setup_setting['f_hsr']
            new_fork_setting.lsr = setup_setting['f_lsr']
            new_fork_setting.tokens = setup_setting['f_tokens']
            new_fork_setting.ramp_up = setup_setting['f_rampup']

            if has_variations:
                for setting in ALL_FORK_SETTINGS:
                    if getattr(new_fork_setting, setting) == 0:
                        if latest_fork_settings[setting] != 0:
                            setattr(new_fork_setting, setting, latest_fork_settings[setting])

            new_fork_setting.save()

            new_fork = Fork_Setting.objects.latest('id')

            new_shock_setting = Shock_Setting()
            new_shock_setting.psi = setup_setting['r_psi']
            new_shock_setting.hsc = setup_setting['r_hsc']
            new_shock_setting.lsc = setup_setting['r_lsc']
            new_shock_setting.hsr = setup_setting['r_hsr']
            new_shock_setting.lsr = setup_setting['r_lsr']
            new_shock_setting.tokens = setup_setting['r_tokens']
            new_shock_setting.hbo = setup_setting['r_hbo']

            if has_variations:
                for setting in ALL_SHOCK_SETTINGS:
                    if getattr(new_shock_setting, setting) == 0:
                        if latest_shock_settings[setting] != 0:
                            setattr(new_shock_setting, setting, latest_shock_settings[setting])


            new_shock_setting.save()

            new_shock = Shock_Setting.objects.latest('id')

            new_variation = Variation(setup_id=setup_id, fork_setting_id=new_fork.id, shock_setting_id=new_shock.id, change_desc=request.POST['desc'])
            new_variation.save()

            url = reverse('tracker:tracker-setups')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')

        elif 'setup_button' in request.POST:
            name = request.POST['name']
            desc = request.POST['desc']

            new_setup = Setup(bike_id=bike_id, name=name, description=desc)
            new_setup.save()

            #fix redirect not giveing a ?bike=
            url = reverse('tracker:tracker-setups')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')
    
    #get all setups
    
    setups = list(Setup.objects.filter(bike_id=bike_id))
    if len(setups) == 0:
        has_setups = False
        current_setup = ''
        has_variations = False
    else:
        has_setups = True
        if setup_id != 'none':
            current_setup = Setup.objects.get(id=setup_id)
        else:
            current_setup = ''
            has_variations = False




    context = {
        'bike_id' : bike_id,
        'setup_id' : setup_id,
        'current_setup' : current_setup,
        'variation_list' : variation_list,
        'ALL_FORK_SETTINGS' : ALL_FORK_SETTINGS,
        'ALL_SHOCK_SETTINGS': ALL_SHOCK_SETTINGS,
        'latest_variation' : latest_variation,
        'latest_fork_settings' : latest_fork_settings,
        'latest_shock_settings' : latest_shock_settings,
        'setups' : setups,
        'has_setups' : has_setups,
        'has_variations' : has_variations
    }

    return render(request, 'tracker/setups.html', context)


@login_required
def delete_setup(request):

    url_vars = request.GET['bike']
    
    bike_id = url_vars[0]
    setup_id = url_vars[(url_vars.index('=')+1):]

    selected_setup = Setup.objects.filter(id=setup_id)
    selected_setup.delete()

    
    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + '?setup=none')

@login_required
def revert_setup(request):

    url_vars = request.GET['bike']
    
    bike_id = url_vars[0]
    setup_id = url_vars[(url_vars.index('=')+1):]


    current_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')
    current_variation.delete()


    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')