# _*_ coding:utf-8 _*_
from django.contrib import admin

# Register your models here.

from .models import UserProfile, EmailVerification, Banner


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nick_name', 'birthday', 'gender', 'address', 'mobile', 'add_time']
    list_filter = ['user', 'nick_name', 'gender']
    search_fields = ['user__username', 'nick_name', 'mobile']


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'send_type', 'send_time']
    list_filter = ['email', 'code', 'send_type']
    search_fields = ['email', 'code', 'send_type', 'send_time']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_url', 'order']
    list_filter = ['banner_url', 'order']
    search_fields = ['banner_url', 'order']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)
admin.site.register(Banner, BannerAdmin)
