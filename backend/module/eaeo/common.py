import os
import shortuuid
from datetime import datetime
from main.models import *
from django.db import transaction as transaction_orm
from module.eaeo import constant as mcs
from module.eaeo import instagram as itg
import pycountry_convert
import json
from django.conf import settings
from django.contrib.auth import authenticate
from social_django.models import UserSocialAuth
from pyfacebook.api import IgProApi
from module.globe.ret_code import *
import threading

def get_user_menu_data(request):
    userclass = request.user.user_class
    if userclass == 3:
        return mcs.influencer_menu_data
    else:
        return mcs.user_menu_data

def get_influencer_menu_data():
    return mcs.influencer_menu_data

def get_countries_from_codes(request):
    cn_codes = mcs.geography
    res = []
    for cn_code in cn_codes:
        try:
            cn_name = pycountry_convert.country_alpha2_to_country_name(cn_code)
            res.append({'id': cn_code, 'name': cn_name})
        except:
            pass
    return res


def get_campaign_countries_from_codes(request, location_id):
    res = []
    location_id = json.loads(location_id)
    for cn_code in location_id:
        try:
            res.append(pycountry_convert.country_alpha2_to_country_name(cn_code))
        except:
            pass
    return res

def get_gender_name_from_id(request, gender_id):
    res = ''
    for item in mcs.gender:
        if item['id'] == gender_id:
            res = item['name']
    return res

def get_brand_by_id(request, brand_id):
    return brand.objects.get(pk=brand_id)

#userclass 1: manager, 2: client, 3: influencer
def get_brands(request):
    userid = request.user.id
    userclass = request.user.user_class
    if userclass == 0 or userclass == 1:
        return list(brand.objects.all().values())
    elif userclass == 2:
        return list(brand.objects.filter(userid=userid).values())
    else:
        return []

def get_influencers(request):
    userid = request.user.id
    userclass = request.user.user_class
    if userclass == 0 or userclass == 1:
        return list(influencer.objects.all().values())
    elif userclass == 2:
        return list(influencer.objects.all().values())
    else:
        return []

def get_influencer_by_handle(request, handle):
    userid = request.user.id
    userclass = request.user.user_class
    if userclass == 0 or userclass == 1:
        return list(influencer.objects.filter(name=handle).values())
    elif userclass == 2:
        return list(influencer.objects.filter(name=handle).values())
    else:
        return list(influencer.objects.filter(name=handle).values())

def get_influencers_by_ids(request, selected_ids):
    userid = request.user.id
    ids = []
    if selected_ids != '':
        ids = json.loads(selected_ids)

    userclass = request.user.user_class
    if userclass == 0 or userclass == 1:
        return list(influencer.objects.filter(pk__in=ids).values())
    elif userclass == 2:
        return list(influencer.objects.filter(pk__in=ids).values())
    else:
        return []

def get_campaigns(request):
    userid = request.user.id
    userclass = request.user.user_class
    if userclass == 0 or userclass == 1:
        return list(campaign.objects.all().values())
    elif userclass == 2:
        return list(campaign.objects.filter(userid=userid).values())
    elif userclass == 3:
        return []
    else:
        return None

def get_negative_keywords(request):
    return list(negative_keyword.objects.all().values())

def get_ad_keywords(request):
    return list(ad_keyword.objects.all().values())

def get_campaign_by_id(request, campaign_id):
    return campaign.objects.get(pk=campaign_id)

def get_campaign_status(request, status):
    if status == '':
        return 'DRAFT'
    else:
        return ''

def get_influencer_by_id(request, influencer_id):
    influencer_ = influencer.objects.get(pk=influencer_id)
    return influencer_

def find_competitor_handle(competitors, post):
    for competitor in competitors:
        if competitor in post:
            return True
    return False

def get_facebook_token_for_media(request, ig_id):
    try:
        access_token = settings.SOCIAL_AUTH_ACCESS_TOKEN

        social_auths = list(UserSocialAuth.objects.all().values())
        token_found_flag = 0
        for social_auth in social_auths:
            if token_found_flag == 1:
                break
            if social_auth['extra_data']['accounts'] == None:
                continue

            accounts = social_auth['extra_data']['accounts']['data']
            for account in accounts:
                if token_found_flag == 1:
                    break
                if not 'instagram_business_account' in account:
                    continue
                if account['instagram_business_account'] == None:
                    continue
                if account['instagram_business_account']['id'] != ig_id:
                    continue

                access_token = social_auth['extra_data']['access_token']
                token_found_flag = 1

        print("access_token:" + str(access_token) + "\n ig_id:" + str(ig_id))
        return access_token
    except:
        print("not found")
        access_token = settings.SOCIAL_AUTH_ACCESS_TOKEN
        return access_token

def check_keys(key_ary, dict_obj):
    for key in key_ary:
        if key not in dict_obj:
            return False
    return True

def authenticate_user(email, password):
    try:
        user_obj_list = list(tbl_user.objects.filter(email=email))
        if len(user_obj_list) == 0:
            return AUTH_ACCOUNT_NOT_FOUND, None
        user_obj = user_obj_list[0]
        if user_obj.is_active == 0:
            return AUTH_ACCOUNT_DISABLED, None

        user = authenticate(username=user_obj.username, password=password)
        if user == None:
            return AUTH_WRONG_PWD, None

        return AUTH_SUCCESS, user

    except Exception as e:
        return AUTH_UNKOWN_ERROR, None

def get_user_class(request):
    userclass = request.user.user_class
    if userclass == 1:
        return 'Manager'
    elif userclass == 3:
        return 'Influencer'
    elif userclass == 2:
        return 'Client'
    else:
        return None

def get_directory_name(request, level):
    directory_name = "static/d3sE4Oks3is83ngQjdENXcosd2e5pq89/"
    if level == 1:  # pdf
        directory_name += "3vh93g0svnbspqx9/"
    elif level == 2:  # png
        directory_name += "snw92f0sLSdQ2XsV/"

    directory_name += datetime.now().strftime("%Y-%m-%d") + "/"

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    return directory_name

def get_country_name_from_alpha2(request, code):
    try:
        res = pycountry_convert.country_alpha2_to_country_name(code)
        return res
    except:
        return code

def get_influencer_data_to_pdf(request, campaign_id, influencer_id, influener_ig_id):
    campaign_detail = get_campaign_by_id(request, campaign_id)
    res = get_influencer_profile_to_pdf(request, campaign_detail, influener_ig_id)
    if res['res'] == None:
        return res
    content = get_influencer_content(request, campaign_detail, influencer_id)
    res['content'] = content
    res['campaign_write_up'] = get_influencer_campaign_writeup(request, campaign_detail, influencer_id)
    influencer_detail = get_influencer_by_id(request, influencer_id)
    res['real_name'] = influencer_detail.real_name
    try:
        origin_cn = pycountry_convert.country_name_to_country_alpha3(
            pycountry_convert.country_alpha2_to_country_name(influencer_detail.origin_cn))
    except:
        origin_cn = influencer_detail.origin_cn
    res['origin_cn'] = origin_cn

    ig_user = find_instagram_influencer_by_handle_indb(handle=influencer_detail.name)
    dozenposts = get_instagram_user_medias(request, influener_ig_id)
    dozenposts = dozenposts[:12]

    i = len(dozenposts)
    j = i // 3 if i % 3 == 0 else i // 3 + 1
    res_ = []
    for k in range(0, j):
        item = {}
        if k*3 < i:
            item['fs'] = dozenposts[k*3]
        if k*3+1 < i:
            item['sc'] = dozenposts[k*3+1]
        if k*3+2 < i:
            item['th'] = dozenposts[k*3+2]
        res_.append(item)
    res['dozenposts'] = res_
    res['following'] = get_number_with_format(ig_user['follows_count'])
    res['eng'] = get_engagement_for_dozen_posts(dozenposts, ig_user['follows_count'])
    return res

def get_engagement_for_dozen_posts(dozenposts, following):
    if following == 0:
        return 'N/a'

    tt = 0
    for post in dozenposts:
        post_eng = 100 * (post['comments_count'] + post['like_count']) / following
        tt += post_eng

    res = round(tt / len(dozenposts), 2)
    return res

def get_number_with_format(num):
    if num < 1000:
        return str(num)
    elif num >= 1000:
        t = round(num / 1000, 1)
        v = round(num / 1000)
        if t == v:
            t = v
        return str(t) + 'K'

def get_influencer_campaign_writeup(request, campaign_detail, influencer_id):
    try:
        campaign_write_up_ = campaign_detail.influencers_campaign_writeup
        return campaign_write_up_
    except:
        return None

def get_influencer_content(request, campaign_detail, influencer_id):
    try:
        content_ = campaign_detail.influencers_content
        content = {} if content_ == '' else json.loads(content_)
        res = {}
        if influencer_id in content:
            res = content[influencer_id]

        return res
    except:
        return None

def update_to_analysed(request, campaign_id, influencer_id):
    try:
        influencer_ = get_influencer_by_id(request, influencer_id)
        campaign_ = get_campaign_by_id(request, campaign_id)
        status_ = campaign_.influencers_status
        status = {} if status_ == '' else json.loads(status_)
        stat = -1
        if influencer_id in status:
            stat = status[influencer_id]
        if stat == -1 and influencer_.created_from == 1:
            stat = 2
        if stat == -1 and influencer_.created_from == 0:
            stat = 3
        if stat == 3 or stat == 2:
            status[influencer_id] = 4
            status_str = json.dumps(status)
            new_params = {}
            new_params['influencers_status'] = status_str
            for key, value in new_params.items():
                setattr(campaign_, key, value)
            campaign_.save()

    except Exception as e:
        print(str(e))


def store_instagram_data(request = None, ig_id = None):
    try:
        with transaction_orm.atomic():
            res = itg.find_instagram_influencer_by_igid(request, ig_id)
            if res == -1:
                raise Exception
            new_params = {}
            new_params['id'] = shortuuid.uuid()
            new_params['username'] = res['username']
            new_params['ig_id'] = res['id']
            new_params['biography'] = '' if not res['biography'] else res['biography']
            new_params['ig_num_id'] = res['ig_id']
            new_params['followers_count'] = res['followers_count']
            new_params['follows_count'] = res['follows_count']
            new_params['media_count'] = res['media_count']
            new_params['name'] = res['name']
            new_params['profile_picture_url'] = '' if not res['profile_picture_url'] else res['profile_picture_url']
            new_params['website'] = '' if not res['website'] else res['profile_picture_url']

            iup_ = list(instagram_user_profile.objects.filter(ig_id=ig_id).values())
            if len(iup_) == 0:
                iup_obj = instagram_user_profile(**new_params)
                iup_obj.save()
            elif len(iup_) == 1:
                new_params.pop('username')
                new_params.pop('id')
                iup_obj = instagram_user_profile.objects.get(pk=iup_[0]['id'])
                for key, value in new_params.items():
                    setattr(iup_obj, key, value)
                iup_obj.save()

            instagram_user_medias.objects.filter(ig_id=ig_id).delete()
            instagram_user_comments.objects.filter(ig_id=ig_id).delete()
            instagram_user_audience_gender_age.objects.filter(ig_id=ig_id).delete()
            instagram_user_audience_country.objects.filter(ig_id=ig_id).delete()

            res = itg.get_user_meias(request=request, ig_id=ig_id, influencer_detail=None)
            if res == -1:
                raise Exception
            for item in res:
                new_params = {}
                new_params['id'] = shortuuid.uuid()
                new_params['ig_id'] = ig_id
                new_params['caption'] = '' if not 'caption' in item else item['caption']
                new_params['media_id'] = item['id']
                new_params['comments_count'] = item['comments_count']
                new_params['like_count'] = item['like_count']
                new_params['media_url'] = '' if not 'media_url' in item else item['media_url']
                new_params['media_type'] = '' if not 'media_type' in item else item['media_type']
                new_params['permalink'] = '' if not 'permalink' in item else item['permalink']
                new_params['timestamp'] = item['timestamp']
                try:
                    impressions = list(filter(lambda x: x['name'] == 'impressions', item['insights']['data']))
                    new_params['impression'] = impressions[0]['values'][0]['value']
                except:
                    new_params['impression'] = ''
                try:
                    reach = list(filter(lambda x: x['name'] == 'reach', item['insights']['data']))
                    new_params['reach'] = reach[0]['values'][0]['value']
                except:
                    new_params['reach'] = ''

                instagram_user_medias_obj = instagram_user_medias(**new_params)
                instagram_user_medias_obj.save()

                if not 'comments' in item:
                    continue

                comments = item['comments']['data']
                for comment in comments:
                    new_params = {}
                    new_params['id'] = shortuuid.uuid()
                    new_params['ig_id'] = ig_id
                    new_params['post_id'] = item['id']
                    new_params['comment_id'] = comment['id']
                    new_params['hidden'] = comment['hidden']
                    new_params['text'] = comment['text']
                    new_params['timestamp'] = comment['timestamp']
                    instagram_user_comments_obj = instagram_user_comments(**new_params)
                    instagram_user_comments_obj.save()

            res = itg.get_user_audience_country(request, ig_id)
            if res == -1:
                raise Exception
            if len(res) > 0:
                new_params = {}
                new_params['id'] = shortuuid.uuid()
                new_params['ig_id'] = ig_id
                new_params['lifetime_id'] = res[0]['id']
                new_params['name'] = res[0]['name']
                new_params['period'] = res[0]['period']
                try:
                    new_params['values'] = json.dumps(res[0]['values'][0]['value'])
                except:
                    new_params['values'] = ''
                instagram_user_audience_country_obj = instagram_user_audience_country(**new_params)
                instagram_user_audience_country_obj.save()

            res = itg.get_user_audience_gender_age(request, ig_id)
            if res == -1:
                raise Exception
            if len(res) > 0:
                new_params = {}
                new_params['id'] = shortuuid.uuid()
                new_params['ig_id'] = ig_id
                new_params['lifetime_id'] = res[0]['id']
                new_params['name'] = res[0]['name']
                new_params['period'] = res[0]['period']
                try:
                    new_params['values'] = json.dumps(res[0]['values'][0]['value'])
                except:
                    new_params['values'] = ''
                instagram_user_audience_gender_age_obj = instagram_user_audience_gender_age(**new_params)
                instagram_user_audience_gender_age_obj.save()

            iup_ = list(instagram_user_profile.objects.filter(ig_id=ig_id).values())
            iup_obj = instagram_user_profile.objects.get(pk=iup_[0]['id'])
            new_params = {}
            new_params['analysed'] = 1
            for key, value in new_params.items():
                setattr(iup_obj, key, value)
            iup_obj.save()
            print('finish')
            return 1
    except Exception as e:
        print(str(e))
        return 0

def callback_sync_instagram_account(request = None, ig_id = None):
    th = threading.Thread(target=store_instagram_data, args=(request, ig_id))
    th.start()

def manual_sync_instagram_account(request = None, ig_id = None):
    th = threading.Thread(target=store_instagram_data, args=(request, ig_id))
    th.start()

def scheduled_sync_instagram_accounts(request = None):
    influencers_ = list(influencer.objects.filter(created_from=1).values('name'))
    flag = 1
    for influencer_ in influencers_:
        handle = influencer_['name']
        res = store_instagram_data(request, handle)
        if res == 0:
            flag = 0
    return flag


def find_instagram_influencer_by_handle_indb(handle):
    try:
        res = list(instagram_user_profile.objects.filter(username=handle).values())
        if len(res) == 0:
            return -1
        return res[0]
    except:
        return -1

def get_instagram_user_medias(request, ig_id):
    try:
        posts = list(instagram_user_medias.objects.filter(ig_id=ig_id).values())

        new_posts = []
        for post in posts:
            comments = list(instagram_user_comments.objects.filter(ig_id=ig_id, post_id=post['media_id']).values())
            post['comments'] = {}
            post['comments']['data'] = comments
            new_posts.append(post)
        return new_posts
    except:
        return -1

def get_instagram_audience_gender_age_by_ig_id(request, ig_id):
    try:
        res = list(instagram_user_audience_gender_age.objects.filter(ig_id=ig_id).values())
        if len(res) == 0:
            return None
        return res[0]
    except:
        return None

def get_instagram_audience_country_by_ig_id(request, ig_id):
    try:
        res = list(instagram_user_audience_country.objects.filter(ig_id=ig_id).values())
        if len(res) == 0:
            return None
        return res[0]
    except:
        return None

def get_metrics_value_by_key(request, user_medias, ig_user, influencer_detail, campaign_detail):
    try:
        if user_medias == -1:
            return None

        ig_id = ig_user['ig_id']
        followers = ig_user['followers_count']
        followings = ig_user['follows_count']

        # get av impressions
        total_impressions = 0
        total_comments = 0
        total_likes = 0
        total_story_slide = 0
        media_cn = len(user_medias)
        for post in user_medias:
            total_impressions += post['impression']
            total_comments += post['comments_count']
            total_likes += post['like_count']
            if post['media_type'] == 'STORY':
                total_story_slide += post['impression']

        av_impressions = total_impressions / media_cn if media_cn != 0 else 'N/a'
        av_story_slide = total_story_slide / media_cn if media_cn != 0 else 'N/a'

        # get age group
        res = get_instagram_audience_gender_age_by_ig_id(request, ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])

        age_dmg_to_target = 0
        gender_dmg_to_target = 0
        gender = campaign_detail.gender
        age_list = [] if campaign_detail.age == '' else json.loads(campaign_detail.age)
        for item in data_sorted:
            for age in age_list:
                if item[0].find(age) >= 0:
                    age_dmg_to_target += item[1]
            if item[0].find(gender) >= 0:
                gender_dmg_to_target += item[1]

        res = get_instagram_audience_country_by_ig_id(request, ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])


        cn_dmg_to_target = 0
        locaiton_list = [] if campaign_detail.location_id == '' else json.loads(campaign_detail.location_id)
        for item in data_sorted:
            for location in locaiton_list:
                if item[0].find(location) >= 0:
                    cn_dmg_to_target += item[1]

        # get country group
        ff = round(followers / followings, 2) if followings != 0 else 'N/a'
        vf = round(av_impressions / followers, 2) if followers != 0 and av_impressions != 'N/a' else 'N/a'
        sf = round(av_story_slide / followers, 2) if followers != 0 and av_story_slide != 'N/a' else 'N/a'
        cf = round(total_comments / followers, 2) if followers != 0 else 'N/a'
        er = round((total_likes + total_comments) / media_cn, 2) if media_cn != 0 else 'N/a'

        res = {
            'ff': ff,
            'vf': vf,
            'sf': sf,
            'cf': cf,
            'er': er,
            'age_dmg_to_target': age_dmg_to_target,
            'gender_dmg_to_target': gender_dmg_to_target,
            'cn_dmg_to_target': cn_dmg_to_target,
        }
        return res
    except Exception as e:
        print(str(e))
        return None

def get_influencer_profile_to_pdf(request, campaign_detail, influener_ig_id):
    try:
        total_dmg_to_target = 0
        gender_dmg_to_target = 0
        gender = campaign_detail.gender
        age_list = [] if campaign_detail.age == '' else json.loads(campaign_detail.age)
        location_list = [] if campaign_detail.location_id == '' else json.loads(campaign_detail.location_id)

        res = list(instagram_user_profile.objects.filter(ig_id=influener_ig_id).values())
        if len(res) == 0:
            return {'res': None}
        data = res[0]
        inf_profile = data['biography']
        name = data['name']
        profile_picture_url = data['profile_picture_url']

        res = get_instagram_audience_gender_age_by_ig_id(request, influener_ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])

        for item in data_sorted:
            total_dmg_to_target += item[1]
            if item[0].find(gender) >= 0:
                gender_dmg_to_target += item[1]

        age_dmg_list = []
        for age in age_list:
            tmp = 0
            for item in data_sorted:
                if item[0].find(age) >= 0:
                    tmp += item[1]
            if tmp > 0:
                res = {'key': age, 'value': round(100 * tmp / total_dmg_to_target, 3) if total_dmg_to_target != 0 else 'N/a'}
                age_dmg_list.append(res)

        age_dmg_list = sorted(age_dmg_list, key=lambda i: i['value'], reverse=True)
        age_dmg_list = age_dmg_list[:3]

        # get country group
        res = get_instagram_audience_country_by_ig_id(request, influener_ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])

        cn_dmg_to_target = 0
        for item in data_sorted:
            cn_dmg_to_target += item[1]

        cn_dmg_list = []
        for location in location_list:
            tmp = 0
            for item in data_sorted:
                if item[0].find(location) >= 0:
                    tmp += item[1]
            try:
                location_name = pycountry_convert.country_name_to_country_alpha3(pycountry_convert.country_alpha2_to_country_name(location))
            except:
                location_name = location
            if tmp > 0:
                res = {'key': location_name, 'value': round(100 * tmp / cn_dmg_to_target, 3) if cn_dmg_to_target != 0 else 'N/a'}
                cn_dmg_list.append(res)

        cn_dmg_list = sorted(cn_dmg_list, key=lambda i: i['value'], reverse=True)
        cn_dmg_list = cn_dmg_list[:3]

        if gender == 'A':
            gender_dmg_to_target = total_dmg_to_target

        gender_percent = round(100 * gender_dmg_to_target / total_dmg_to_target, 3) if total_dmg_to_target != 0 else 'N/a'
        if gender == 'M':
            gender = 'Male'
        elif gender == 'F':
            gender = 'Female'
        else:
            gender = 'ALL'

        age_dmg_list_res = False
        if len(age_list) > 0:
            age_dmg_list_res = True
        location_dmg_res = False
        if len(location_list) > 0:
            location_dmg_res = True

        res = {'age_dmg_list_res': age_dmg_list_res, 'age_pecent_list': age_dmg_list, 'gender_percent': gender_percent,
               'gender': gender, 'res': 'ok', 'name': name, 'inf_profile': inf_profile, 'profile_picture_url': profile_picture_url,
               'location_dmg_res': location_dmg_res, 'cn_dmg_list': cn_dmg_list}
        return res
    except:
        return {'res': None}