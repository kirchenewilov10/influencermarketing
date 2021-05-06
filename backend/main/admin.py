from django.contrib import admin

# Register your models here.
from .models import campaign, brand, influencer, negative_keyword, ad_keyword, tbl_user, metrics, instagram_user_profile,\
    instagram_user_audience_country, instagram_user_audience_gender_age, instagram_user_comments, instagram_user_medias
from django.contrib.auth.admin import UserAdmin

class campaignAdmin(admin.ModelAdmin):
    list_display = [field.name for field in campaign._meta.get_fields()]

class brandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in brand._meta.get_fields()]

class influencerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in influencer._meta.get_fields()]

class negativekeywordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in negative_keyword._meta.get_fields()]

class adkeywordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ad_keyword._meta.get_fields()]

class metricsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in metrics._meta.get_fields()]

class instagram_user_profileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in instagram_user_profile._meta.get_fields()]

class instagram_user_audience_countryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in instagram_user_audience_country._meta.get_fields()]

class instagram_user_audience_gender_ageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in instagram_user_audience_gender_age._meta.get_fields()]

class instagram_user_commentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in instagram_user_comments._meta.get_fields()]

class instagram_user_mediasAdmin(admin.ModelAdmin):
    list_display = [field.name for field in instagram_user_medias._meta.get_fields()]

admin.site.register(campaign, campaignAdmin)
admin.site.register(brand, brandAdmin)
admin.site.register(influencer, influencerAdmin)
admin.site.register(negative_keyword, negativekeywordAdmin)
admin.site.register(ad_keyword, adkeywordAdmin)
admin.site.register(metrics, metricsAdmin)
admin.site.register(tbl_user, UserAdmin)
admin.site.register(instagram_user_comments, instagram_user_commentsAdmin)
admin.site.register(instagram_user_medias, instagram_user_mediasAdmin)
admin.site.register(instagram_user_audience_gender_age, instagram_user_audience_gender_ageAdmin)
admin.site.register(instagram_user_audience_country, instagram_user_audience_countryAdmin)
admin.site.register(instagram_user_profile, instagram_user_profileAdmin)