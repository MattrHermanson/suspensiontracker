from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Bike, Setup, Variation, Fork_Setting, Shock_Setting, Var_Note
from users.models import User
from django.urls import reverse
from .decorators import separate_url


def setup(request):

    return render(request, 'tracker/setup.html')


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
        if request.POST['progression'] != '':
            progression = int(request.POST['progression'])
            progression *= 0.01
        else:
            progression = 0


        new_bike = Bike(name=name, owner=user, brand=brand, front_travel=front_travel, rear_travel=rear_travel, progression=progression)
        new_bike.save()
        
        return redirect('tracker:tracker-bikes')

    users_bikes = list(user.bike_set.all())

    if len(users_bikes) == 0:
        has_bikes = False
    else:
        has_bikes = True
           
    print(f'has bikes: {has_bikes}')

    context = {
        'users_bikes' : users_bikes,
        'has_bikes' : has_bikes,
    }
    

    return render(request, 'tracker/bikes.html', context)

@login_required
@separate_url
def setups(request, bike_id, setup_id):

    variation_list = []
    latest_variation = []
    favorite_setup_ids = [setup.id for setup in list(Setup.objects.filter(bike_id=bike_id)) if setup.favorite]

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
            
            #-------------Record Settings Button-----------------

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

            #-------Create Setup Button-------------------

            name = request.POST['name']
            desc = request.POST['desc']

            new_setup = Setup(bike_id=bike_id, name=name, description=desc)
            new_setup.save()

            #fix redirect not giveing a ?bike=
            url = reverse('tracker:tracker-setups')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')
        
        elif 'edit_setup_button' in request.POST:
            
            name = request.POST['name']
            desc = request.POST['desc']

            selected_setup = Setup.objects.get(id=setup_id)
            if len(name) > 0:
                selected_setup.name = name
            if len(desc) > 0:
                selected_setup.description = desc
            selected_setup.save()

            url = reverse('tracker:tracker-setups')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')

        elif 'edit_bike_button' in request.POST:

            bike_name = request.POST['bike_name']
            bike_brand = request.POST['bike_brand']
            front_travel = request.POST['front_travel']
            rear_travel = request.POST['rear_travel']
            progression = request.POST['progression']

            selected_bike = Bike.objects.get(id=bike_id)

            if len(bike_name) > 0:
                selected_bike.name = bike_name
            if len(bike_brand) > 0:
                selected_bike.brand = bike_brand
            if len(front_travel) > 0:
                front_travel = int(front_travel)
                selected_bike.front_travel = front_travel
            if len(rear_travel) > 0:
                rear_travel = int(rear_travel)
                selected_bike.rear_travel = rear_travel
            if len(progression) > 0:
                progression = int(progression)
                progression *= 0.01
                selected_bike.progression = progression

            selected_bike.save()

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
        'current_bike' : Bike.objects.get(id=bike_id),
        'setup_id' : setup_id,
        'current_setup' : current_setup,
        'variation_list' : variation_list,
        'latest_variation' : latest_variation,
        'latest_fork_settings' : latest_fork_settings,
        'latest_shock_settings' : latest_shock_settings,
        'setups' : setups,
        'has_setups' : has_setups,
        'has_variations' : has_variations,
        'favorite_setup_ids' : favorite_setup_ids,
    }

    return render(request, 'tracker/setups.html', context)


@login_required
@separate_url
def delete_setup(request, bike_id, setup_id):


    selected_setup = Setup.objects.get(id=setup_id)

    connected_variations = list(Variation.objects.filter(setup_id=selected_setup.id))

    #deletes connected variations and fork/shock settings to clearn things up
    for v in connected_variations:
        Fork_Setting.objects.get(id=v.fork_setting_id).delete()
        Shock_Setting.objects.get(id=v.shock_setting_id).delete()
        v.delete()

    selected_setup.delete()

    
    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + '?setup=none')


@login_required
@separate_url
def revert_setup(request, bike_id, setup_id):

    current_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')
    current_variation.delete()


    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')

@login_required
@separate_url
def duplicate_setup(request, bike_id, setup_id):

    #copy setup
    current_setup = Setup.objects.get(id=setup_id)
    current_setup.id = None
    current_setup.description = f'A copy of {current_setup.name}'
    current_setup.name += ' copy'
    current_setup.favorite = False
    current_setup.save()

    copied_setup = Setup.objects.get(id=current_setup.id)

    #copy variation
    copied_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')
    copied_variation.id = None
    copied_variation.setup_id = copied_setup.id
    copied_variation.save()

    #copy fork/shock setting
    copied_fork_setting = Fork_Setting.objects.get(id=copied_variation.fork_setting_id)
    copied_fork_setting.id = None
    copied_fork_setting.save()
    

    copied_shock_setting = Shock_Setting.objects.get(id=copied_variation.shock_setting_id)
    copied_shock_setting.id = None
    copied_shock_setting.save()

    #sets copied variations fork/shock setting setings to copied fork/shock settings to keep them from refing the same model objects
    copied_variation.fork_setting_id = copied_fork_setting.id
    copied_variation.shock_setting_id = copied_shock_setting.id
    copied_variation.save()

    setup_id = copied_setup.id


    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')

@login_required
@separate_url
def delete_bike(request, bike_id, setup_id):

    bikes_setups = list(Setup.objects.filter(bike_id=bike_id))
    
    for setup in bikes_setups:
        
        selected_setup = Setup.objects.get(id=setup.id)

        connected_variations = list(Variation.objects.filter(setup_id=selected_setup.id))

        #deletes connected variations and fork/shock settings to clearn things up
        for v in connected_variations:
            Fork_Setting.objects.get(id=v.fork_setting_id).delete()
            Shock_Setting.objects.get(id=v.shock_setting_id).delete()
            Var_Note.objects.filter(variation_id=v.id).delete()
            v.delete()

        selected_setup.delete()

    bike_to_delete = Bike.objects.get(id=bike_id)
    bike_to_delete.delete()


    return redirect('tracker:tracker-bikes')

@login_required
@separate_url
def favorite_setup(request, bike_id, setup_id):

    selected_setup = Setup.objects.get(id=setup_id)
    if selected_setup.favorite:
        selected_setup.favorite = False
    else:
        selected_setup.favorite = True
    selected_setup.save()

    url = reverse('tracker:tracker-setups')
    return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')


@login_required
@separate_url
def timeline(request, bike_id, setup_id):

    def format_settings(setting_obj, sus_type:str) -> dict:
        if sus_type == 'fork':
            ALL_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'ramp_up']
        elif sus_type == 'shock':
            ALL_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'hbo']
        else:
            raise Exception('Invalid suspension type, use [fork or shock] only')
            ALL_SETTINGS = []
        
        formatted_settings = {}

        for setting in ALL_SETTINGS:
            formatted_settings[setting] = getattr(setting_obj, setting)

        return formatted_settings

    current_bike = Bike.objects.get(id=bike_id)
    current_setup = Setup.objects.get(id=setup_id)
    list_of_variations = list(Variation.objects.order_by('date_created').filter(setup_id=setup_id))

    fork_settings = {variation.id : format_settings(Fork_Setting.objects.get(id=variation.fork_setting.id), 'fork') for variation in list_of_variations}
    shock_settings = {variation.id : format_settings(Shock_Setting.objects.get(id=variation.shock_setting.id), 'shock') for variation in list_of_variations}
    variation_notes = {variation.id : list(Var_Note.objects.filter(variation_id=variation.id)) for variation in list_of_variations}


    if request.method == 'POST':
        if 'note_button' in request.POST:
            title = request.POST['title']
            body = request.POST['body']

            latest_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')

            new_note = Var_Note(variation_id=latest_variation.id, note_title=title, note_body=body)

            new_note.save()

            url = reverse('tracker:tracker-timeline')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')
        
        if 'variation_button' in request.POST:
            
            latest_variation = Variation.objects.filter(setup_id=setup_id).latest('date_created')
            setup_setting_keys = ['f_psi', 'f_hsc', 'f_lsc', 'f_hsr', 'f_lsr', 'f_tokens', 'f_rampup', 'r_psi', 'r_hsc', 'r_lsc', 'r_hsr', 'r_lsr', 'r_tokens', 'r_hbo']
            ALL_FORK_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'ramp_up']
            ALL_SHOCK_SETTINGS = ['psi', 'hsc', 'lsc', 'hsr', 'lsr', 'tokens', 'hbo']
            latest_fork_settings = {}
            latest_shock_settings = {}
            #make a dictionary of all settings and their values
            for setting in ALL_FORK_SETTINGS:
                latest_fork_settings[setting] = getattr(latest_variation.fork_setting, setting)
            
            for setting in ALL_SHOCK_SETTINGS:
                latest_shock_settings[setting] = getattr(latest_variation.shock_setting, setting)

            #-------------Record Settings Button-----------------

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

            if True: #remove if if nothing breaks
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

            if True: #remove if if nothing breaks
                for setting in ALL_SHOCK_SETTINGS:
                    if getattr(new_shock_setting, setting) == 0:
                        if latest_shock_settings[setting] != 0:
                            setattr(new_shock_setting, setting, latest_shock_settings[setting])


            new_shock_setting.save()

            new_shock = Shock_Setting.objects.latest('id')

            new_variation = Variation(setup_id=setup_id, fork_setting_id=new_fork.id, shock_setting_id=new_shock.id, change_desc=request.POST['desc'])
            new_variation.save()

            url = reverse('tracker:tracker-timeline')
            return redirect(url + f'?bike={bike_id}' + f'?setup={setup_id}')


    context = {
        'current_bike' : current_bike,
        'current_setup' : current_setup,
        'bike_id' : bike_id,
        'setup_id' : setup_id,
        'list_of_variations' : list_of_variations,
        'fork_settings' : fork_settings,
        'shock_settings' : shock_settings,
        'variation_notes' : variation_notes,
    }

    return render(request, 'tracker/timeline.html', context)