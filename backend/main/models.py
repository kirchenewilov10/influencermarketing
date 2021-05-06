from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser

class tbl_user(AbstractUser):
    user_class = models.IntegerField(default=0)

class campaign(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    userid = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True)
    brand_id = models.CharField(max_length=255, blank=True)
    location_id = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)
    kpi = models.CharField(max_length=255, blank=True)
    safety_score = models.CharField(max_length=255, blank=True)
    competitors = models.CharField(max_length=255, blank=True)
    negotive_keyowrds = models.CharField(max_length=255, blank=True)
    influencers = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    influencers_status = models.CharField(max_length=255, blank=True)
    influencers_content = models.CharField(max_length=255, blank=True)
    influencers_campaign_writeup = models.CharField(max_length=255, blank=True)

class brand(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    userid = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True)
    campaigns = models.CharField(max_length=255, blank=True)
    influencers = models.CharField(max_length=255, blank=True)
    competitors = models.CharField(max_length=255, blank=True)
    safety_score = models.CharField(max_length=255, blank=True)

class influencer(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    userid = models.IntegerField(default=0)
    influencer_userid = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True, unique=True)
    brands = models.CharField(max_length=255, blank=True)
    campaigns = models.CharField(max_length=255, blank=True)
    google_keyword = models.CharField(max_length=255, blank=True)
    most_recent_posts = models.CharField(max_length=255, blank=True)
    most_recent_images = models.CharField(max_length=255, blank=True)
    highest_search_results = models.CharField(max_length=255, blank=True)
    google_trends = models.CharField(max_length=255, blank=True)
    following_to_follwer_ratio = models.FloatField(blank=True, default=0)
    age_demo_of_audience = models.IntegerField(default=0)
    location_of_audience = models.CharField(max_length=255, blank=True)
    gender_demographic_of_audience = models.CharField(max_length=255, blank=True)
    engagement_rate_of_audience = models.CharField(max_length=255, blank=True)
    follower_change = models.CharField(max_length=255, blank=True)
    accounts = models.CharField(max_length=255, blank=True)
    associated_influencers = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    api_connect_stat = models.IntegerField(default=0)
    created_from = models.IntegerField(default=0)
    real_name = models.CharField(max_length=255, blank=True)
    origin_cn = models.CharField(max_length=255, blank=True)

class negative_keyword(models.Model):
    text = models.CharField(max_length=255, blank=True)

class ad_keyword(models.Model):
    text = models.CharField(max_length=255, blank=True)

class metrics(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    userid = models.IntegerField(default=0)
    campaign_id = models.CharField(max_length=255, blank=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    metrics_index = models.IntegerField(default=0)
    score = models.FloatField(default=0)

class instagram_user_profile(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True, unique=True)
    ig_id = models.CharField(max_length=255, blank=True, unique=True)
    biography = models.TextField(blank=True)
    ig_num_id = models.CharField(max_length=255, blank=True)
    followers_count = models.BigIntegerField(default=0)
    follows_count = models.BigIntegerField(default=0)
    media_count = models.BigIntegerField(default=0)
    name = models.CharField(max_length=255, blank=True)
    profile_picture_url = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    analysed = models.IntegerField(default=0)

class instagram_user_medias(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    ig_id = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    media_id = models.CharField(max_length=255, blank=True)
    comments_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    media_url = models.TextField(blank=True)
    media_type = models.CharField(max_length=255, blank=True)
    permalink = models.TextField(blank=True)
    timestamp = models.CharField(max_length=255, blank=True)
    impression = models.BigIntegerField(default=0)
    reach = models.BigIntegerField(default=0)

class instagram_user_comments(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    ig_id = models.CharField(max_length=255, blank=True)
    post_id = models.CharField(max_length=255, blank=True)
    comment_id = models.CharField(max_length=255, blank=True)
    hidden = models.BooleanField(default=False)
    text = models.TextField(blank=True)
    timestamp = models.CharField(max_length=255, blank=True)

class instagram_user_audience_country(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    ig_id = models.CharField(max_length=255, blank=True, unique=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    lifetime_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    period = models.CharField(max_length=255, blank=True)
    values = models.TextField(blank=True)

class instagram_user_audience_gender_age(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    influencer_id = models.CharField(max_length=255, blank=True)
    ig_id = models.CharField(max_length=255, blank=True, unique=True)
    lifetime_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    period = models.CharField(max_length=255, blank=True)
    values = models.TextField(blank=True)

