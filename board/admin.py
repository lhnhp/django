from django.contrib import admin
from .models import Board
from .models import Reply
# Register your models here.
admin.site.register(Board)
admin.site.register(Reply)