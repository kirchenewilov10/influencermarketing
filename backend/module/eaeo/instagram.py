from main.models import *
from module.eaeo import constant as mcs
from module.eaeo import common as mcm
import pycountry_convert
import json
from django.conf import settings
from social_django.models import UserSocialAuth
from pyfacebook.api import IgProApi
import sys

def find_instagram_influencer_by_igid(request, ig_id):
    try:
        api = IgProApi(app_id=settings.SOCIAL_AUTH_FACEBOOK_KEY, app_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                       long_term_token=mcm.get_facebook_token_for_media(request, ig_id),
                       instagram_business_id=ig_id)
        res = api.get_user_info(user_id=ig_id,
            fields='biography, id, ig_id, followers_count, follows_count, media_count, name, profile_picture_url, username, website'
        )
        data = res.as_dict()
        return data
    except:
        return -1


def get_user_meias(request, ig_id, influencer_detail):
    try:
        api = IgProApi(app_id=settings.SOCIAL_AUTH_FACEBOOK_KEY, app_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                       long_term_token=mcm.get_facebook_token_for_media(request, ig_id),
                       instagram_business_id=ig_id)

        caption_comments = api.get_user_medias(
            ig_id,
            fields='caption, id, comments_count, like_count, media_url, media_type, permalink, timestamp, comments.fields(hidden, id, text, timestamp, media), insights.metric(reach, impressions)',
            count=None,
            limit=50,
            return_json=True)
        return caption_comments
    except Exception as e:
        print(str(e))
        return -1

def get_user_audience_country(request, ig_id):
    try:
        api = IgProApi(app_id=settings.SOCIAL_AUTH_FACEBOOK_KEY, app_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                       long_term_token=mcm.get_facebook_token_for_media(request, ig_id),
                       instagram_business_id=ig_id)
        api_response = api.get_user_insights(ig_id, period="lifetime", metrics=["audience_country"])
        data = [item.as_dict() for item in api_response]
        return data
    except:
        return -1

def get_user_audience_gender_age(request, ig_id):
    try:
        api = IgProApi(app_id=settings.SOCIAL_AUTH_FACEBOOK_KEY, app_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                       long_term_token=mcm.get_facebook_token_for_media(request, ig_id),
                       instagram_business_id=ig_id)
        api_response = api.get_user_insights(ig_id, period="lifetime", metrics=["audience_gender_age"])
        data = [item.as_dict() for item in api_response]
        return data
    except:
        return -1

