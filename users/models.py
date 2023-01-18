from django.db import models
from django.conf import settings

class LinkModel(models.Model):
    link_name = models.CharField(max_length=20)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.link_name

class ProfileModel(models.Model):
    gender = [('m', 'Male'), ('f','Female')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=20)

    number = models.IntegerField(null=True, blank=True)

    sex = models.TextField(choices=gender, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    dod = models.DateField(null=True, blank=True)
    job = models.CharField(null=True, blank=True, max_length=20)
    ethnicity = models.CharField(null=True, blank=True, max_length=20)
    location = models.CharField(null=True, blank=True, max_length=20)

    biography = models.CharField(null=True, blank=True, max_length=20)

    #Multiple
    stories = models.TextField(null=True, blank=True)
    video= models.TextField(null=True, blank=True)
 
    profile_link = models.ManyToManyField(LinkModel, blank=True)
    
    def __str__(self):
        return self.name

class bookmode(models.Model):
    about =  models.ManyToManyField(ProfileModel, blank=True)


# class family (models.Model):

    # mother = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # father = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    # mothers = models.ManyToManyField("Profile", blank=True)
    # fathers = models.ManyToManyField("Profile", blank=True)

#     friends 
#     mother
#     father
#     sister 
#     brother 
#     children 
