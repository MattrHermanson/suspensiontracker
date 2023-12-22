from django.db import models
from users.models import User

class Bike(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    brand = models.CharField(max_length=30)
    front_travel = models.IntegerField()
    rear_travel = models.IntegerField()
    progression = models.DecimalField(max_digits=2, decimal_places=2)
    eye_to_eye = models.DecimalField(max_digits=5, decimal_places=2)
    stroke = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Fork(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    damper = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Shock(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    tier = models.CharField(max_length=50) #factory or ultimate - the level of adjustments available

    def __str__(self):
        return self.name

class Fork_Setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    psi = models.DecimalField(max_digits=4, decimal_places=1)
    hsc = models.IntegerField()
    lsc = models.IntegerField()
    hsr = models.IntegerField()
    lsr = models.IntegerField()
    tokens = models.IntegerField()
    ramp_up = models.DecimalField(max_digits=4, decimal_places=1)

class Shock_Setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    psi = models.DecimalField(max_digits=4, decimal_places=1)
    hsc = models.IntegerField()
    lsc = models.IntegerField()
    hsr = models.IntegerField()
    lsr = models.IntegerField()
    tokens = models.IntegerField()
    hbo = models.IntegerField()


class Setup(models.Model):
    id = models.BigAutoField(primary_key=True)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Variations(models.Model):
    id = models.BigAutoField(primary_key=True)
    setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
    fork = models.ForeignKey(Fork, on_delete=models.CASCADE)
    shock = models.ForeignKey(Shock, on_delete=models.CASCADE)
    fork_setting = models.ForeignKey(Fork_Setting, on_delete=models.CASCADE)
    shock_setting = models.ForeignKey(Shock_Setting, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    change_desc = models.TextField()

