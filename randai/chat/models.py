import uuid
from django.db import models
from util.Settings import Settings
from django.db import models
from django.contrib.auth.models import User
settings = Settings()

class ApiKey(models.Model):
    api_key = models.CharField(max_length=255, primary_key=True)
    is_active = models.BooleanField()
    state = models.CharField(max_length=255, choices=settings.STATE_CHOICES)
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ApiOption(models.Model):
    url = models.CharField(max_length=255)
    api_key = models.ManyToManyField(ApiKey)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField()
    state = models.CharField(max_length=255, choices=settings.STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApiOwner(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    api_options_id = models.ManyToManyField(ApiOption, blank=True) 
    type_service = models.CharField(max_length=10, choices=settings.TYPE_CHOICES, default='text')
    type_price = models.CharField(max_length=255, choices=settings.TYPE_PRICE)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField()
    state = models.CharField(max_length=255, choices=settings.STATE_CHOICES)
    notes = models.TextField(blank=True)
    version = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompanyAI(models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField()
    description = models.TextField(blank=True)
    img_url = models.CharField(max_length=255, blank=True)
    website_url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Provider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField()
    state = models.CharField(max_length=255, choices=settings.STATE_CHOICES)
    priority = models.IntegerField()
    is_message_system = models.BooleanField()
    is_arabic = models.BooleanField()
    is_auth = models.BooleanField()
    is_cookies = models.BooleanField()
    is_stream = models.BooleanField()
    is_parameter = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Language(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    nativeName = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Character(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Prompt(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    lang_code = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



