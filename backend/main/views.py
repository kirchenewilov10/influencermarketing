import os
import csv
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth
from pyfacebook.api import IgProApi
from module.eaeo import common as mcm
from module.eaeo import constant as mcs
from module.eaeo import instagram as itg
import json
from .models import *
import shortuuid
from django.shortcuts import render, redirect
from module.globe.ret_code import *
from html2pdf import pdf
from django.db import transaction as transaction_orm
from pdf2image import convert_from_path, convert_from_bytes

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):

        if self.request.user.is_authenticated:
            user_class = self.request.user.user_class
            if user_class != 3:
                self.template_name = "main/index.html"
                context = {}
                context['menu_data'] = mcm.get_user_menu_data(self.request)
                context['menu_id'] = 1
                return context
            else:
                self.template_name = 'main/influencer_index.html'
                context = {}
                context['menu_data'] = mcm.get_user_menu_data(self.request)
                context['menu_id'] = 1
                return context
        else:
            self.template_name = 'main/welcome.html'

def SigninView(request):
    try:
        key_ary = ['email', 'password']
        params = request.POST

        if not mcm.check_keys(key_ary, params):
            return render(request, 'main/signin.html')

        email = params['email']
        password = params['password']
        ret_code, user_obj = mcm.authenticate_user(email, password)
        time.sleep(1)
        if ret_code != AUTH_SUCCESS:
            return render(request, 'main/signin.html')

        django_login(request, user_obj)

        return redirect(reverse('main:index'))
    except:
        return render(request, 'main/signin.html')

def SignupView(request):
    try:
        key_ary = ['fullname', 'username', 'email', 'password']
        params = request.POST

        if not mcm.check_keys(key_ary, params):
            return render(request, 'main/signup.html')

        if params['fullname'] == '' or params['username'] == '' or params['email'] == '' or params['password'] == '':
            error = {'text': 'Blank field is not allowed'}
            return render(request, 'main/signup.html', error)

        if tbl_user.objects.filter(username=params['username']).count() > 0:
            warning = {'text': 'Username exists!'}
            return render(request, 'main/signup.html', warning)
        if tbl_user.objects.filter(email=params['email']).count() > 0:
            warning = {'text': 'Email exists!'}
            return render(request, 'main/signup.html', warning)

        new_params = {}
        new_params['first_name'] = params['fullname']
        new_params['username'] = params['username']
        new_params['email'] = params['email']
        new_params['user_class'] = 1

        user_obj = tbl_user(**new_params)
        user_obj.set_password(params['password'])
        user_obj.save()

        return redirect(reverse('main:index'))
    except:
        return render(request, 'main/signup.html')

def Influencer_signupView(request):
    return render(request, 'main/influencer_signup.html')

def social_error_url(request):
    return render(request, 'main/social_error_page.html')

def new_social_auth_user(request):
    new_params = {}
    new_params['user_class'] = 3
    userid = request.user.id
    user_obj = tbl_user.objects.get(pk=userid)
    for key, value in new_params.items():
        setattr(user_obj, key, value)
    user_obj.save()
    return redirect(reverse('main:index'))

def logout_view(request):
    django_logout(request)
    return redirect(reverse('main:index'))


class CampaignView(TemplateView):
    template_name = "main/campaign_list.html"
    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 4
        context['table_data'] = self.get_campaign_list()
        return context

    def get_campaign_list(self):
        campaign_list_ = mcm.get_campaigns(self.request)
        campaign_list = []
        for item in campaign_list_:
            locations = mcm.get_campaign_countries_from_codes(self.request, item['location_id'])
            campaign_list.append({
                'id': item['id'],
                'name': item['name'],
                'countries': ', '.join(locations),
                'gender': mcm.get_gender_name_from_id(self.request, item['gender']),
                'age': ', '.join(json.loads(item['age'])),
                'brand': mcm.get_brand_by_id(self.request, item['brand_id']),
                'status': mcm.get_campaign_status(self.request, item['status'])
            })
        return campaign_list

class Create_campaignView(TemplateView):
    template_name = "main/create_campaign.html"

    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 4
        context['gender'] = mcs.gender
        context['safety_score'] = mcs.safety_score
        context['kpi'] = mcs.kpi
        context['age'] = mcs.age
        context['brand'] = self.get_brands_and_add()
        context['competitors'] = self.get_brands()
        context['geography'] = self.get_country_list()
        context['influencers'] = self.get_influencers()
        return context

    def get_brands_and_add(self):
        brands_list_ = mcm.get_brands(self.request)
        brands_list = []
        for item in brands_list_:
            brands_list.append({'id': item['id'], 'name': item['name']})
        brands_list.append({'id': 0, 'name': 'ADD NEW'})
        return brands_list

    def get_brands(self):
        brands_list_ = mcm.get_brands(self.request)
        brands_list = []
        for item in brands_list_:
            brands_list.append({'id': item['id'], 'name': item['name']})
        return brands_list

    def get_country_list(self):
        cn_list = mcm.get_countries_from_codes(self.request)
        return cn_list

    def get_influencers(self):
        influencers_ = mcm.get_influencers(self.request)
        influencers = []
        for item in influencers_:
            influencers.append({'id': item['id'], 'name': item['name']})
        return influencers

class Campaign_detailView(Create_campaignView):
    template_name = "main/campaign_detail.html"
    def get_context_data(self, **kwargs):
        campaign_id = kwargs['campaign_id']
        campaign_detail = self.get_campaign_detail(campaign_id)
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 4
        context['campaign_detail'] = campaign_detail
        context['campaign_negotive_keywords'] = self.get_negative_keyword(campaign_detail.negotive_keyowrds)
        context['gender'] = mcs.gender
        context['safety_score'] = mcs.safety_score
        context['kpi'] = mcs.kpi
        context['age'] = mcs.age
        context['brand'] = self.get_brands()
        context['geography'] = self.get_country_list()
        context['influencers'] = self.get_influencers()
        context['selected_influencers'] = self.get_selected_influencers(campaign_detail)
        context['campaign_id'] = campaign_id
        return context

    def get_negative_keyword(self, keywords):
        keyword_list = []
        if keywords != '':
            keyword_list = json.loads(keywords)
        res = ' '.join(keyword_list)
        return res

    def get_selected_influencers(self, campaign_detail):
        selected_ids = campaign_detail.influencers
        status_ = campaign_detail.influencers_status
        status = {} if status_ == '' else json.loads(status_)
        influencers_ = mcm.get_influencers_by_ids(self.request, selected_ids)
        influencers = []
        for item in influencers_:
            acc_rej_stat = -1 # 0: rejected, 1: accepted 2: connected 3: invited 4: analysed
            if item['id'] in status:
                acc_rej_stat = status[item['id']]
            if acc_rej_stat == -1 and item['created_from'] == 1:
                acc_rej_stat = 2
            if acc_rej_stat == -1 and item['created_from'] == 0:
                acc_rej_stat = 3
            influencers.append({'id': item['id'], 'name': item['name'], 'email': item['email'], 'acc_rej_stat': acc_rej_stat})
        return influencers

    def get_campaign_detail(self, campaign_id):
        campaign = mcm.get_campaign_by_id(self.request, campaign_id)
        return campaign

@login_required()
def save_campaign(request):
    try:
        with transaction_orm.atomic():
            param = request.POST
            cp_name = param['cp_name']
            brand_info = json.loads(param['brand'])
            gender = param['gender']
            cp_kpi = param['cp_kpi']
            geography = json.loads(param['geography_'])
            age = json.loads(param['age'])
            competitive_brand_s = json.loads(param['competitive_brand_s'])
            competitive_brand_i = json.loads(param['competitive_brand_i'])
            safety_score = param['safety_score_']
            influencer_handle_s = json.loads(param['influencer_handle_s'])
            influencer_handle_i = json.loads(param['influencer_handle_i'])
            userid = request.user.id
            # 1. if brand is to add, save it first
            if brand_info['type'] == 0:
                new_params = {}
                new_params['id'] = shortuuid.uuid()
                new_params['userid'] = userid
                new_params['name'] = brand_info['value']
                if len(competitive_brand_s) > 0:
                    new_params['competitors'] = json.dumps(competitive_brand_s)
                if len(influencer_handle_s) > 0:
                    new_params['influencers'] = json.dumps(influencer_handle_s)
                brand_obj = brand(**new_params)
                brand_obj.save()

            # 2. save campaign with new brand id or selected brand id
            new_params = {}
            new_params['id'] = shortuuid.uuid()
            new_params['userid'] = userid
            new_params['name'] = cp_name
            new_params['gender'] = gender
            new_params['kpi'] = cp_kpi
            new_params['safety_score'] = safety_score
            new_params['age'] = json.dumps(age)
            new_params['location_id'] = json.dumps(geography)
            if brand_info['type'] == 1:
                brand_id = brand_info['value']
            else:
                brand_id = brand_obj.id
            new_params['brand_id'] = brand_id
            if len(competitive_brand_s) > 0:
                new_params['competitors'] = json.dumps(competitive_brand_s)
            if len(influencer_handle_s) > 0:
                new_params['influencers'] = json.dumps(influencer_handle_s)
            campaign_obj = campaign(**new_params)
            campaign_obj.save()

            # 3. update current brand(client)'s campaign list with created campaign's id
            updating_brand = brand.objects.get(pk=brand_id)
            brand_campaign_list_ = updating_brand.campaigns
            brand_campaign_list = []
            if brand_campaign_list_ != '':
                brand_campaign_list = json.loads(brand_campaign_list_)
            brand_campaign_list.append(campaign_obj.id)
            new_params = {}
            new_params['campaigns'] = json.dumps(brand_campaign_list)
            if brand_info['type'] == 1:
                if len(competitive_brand_s) > 0:
                    brand_competitors_ = updating_brand.competitors
                    brand_competitors = []
                    if brand_competitors_ != '':
                        brand_competitors = json.loads(brand_competitors_)
                    brand_competitors += competitive_brand_s
                    brand_competitors = list(dict.fromkeys(brand_competitors))
                    new_params['competitors'] = json.dumps(brand_competitors)
                if len(influencer_handle_s) > 0:
                    brand_influencers_ = updating_brand.influencers
                    brand_influencers = []
                    if brand_influencers_ != '':
                        brand_influencers = json.loads(brand_influencers_)
                    brand_influencers += influencer_handle_s
                    brand_influencers = list(dict.fromkeys(brand_influencers))
                    new_params['influencers'] = json.dumps(brand_influencers)
            for key, value in new_params.items():
                setattr(updating_brand, key, value)
            updating_brand.save()

            # 4.if influencer is to add, save it with campaign, brand id
            if len(influencer_handle_i) > 0:
                influencer_handle_i_ids = []
                for influencer_handle_i_item in influencer_handle_i:
                    if len(mcm.get_influencer_by_handle(request, influencer_handle_i_item)) > 0:
                        raise Exception
                    new_params = {}
                    new_params['id'] = shortuuid.uuid()
                    new_params['userid'] = request.user.id
                    new_params['name'] = influencer_handle_i_item
                    new_params['created_from'] = 0
                    influencer_obj = influencer(**new_params)
                    influencer_obj.save()
                    influencer_handle_i_ids.append(influencer_obj.id)

                # update current brand's influencers list with new influencer ids
                updating_brand = brand.objects.get(pk=brand_id)
                brand_influencers_list_ = updating_brand.influencers
                brand_influencers_list = []
                if brand_influencers_list_ != '':
                    brand_influencers_list = json.loads(brand_influencers_list_)
                brand_influencers_list += influencer_handle_i_ids
                brand_influencers_list = list(dict.fromkeys(brand_influencers_list))
                new_params = {}
                new_params['influencers'] = json.dumps(brand_influencers_list)
                for key, value in new_params.items():
                    setattr(updating_brand, key, value)
                updating_brand.save()

                # update new campaignn's influencers list with new influencer ids
                updating_campaign = campaign.objects.get(pk=campaign_obj.id)
                campaign_influencers_list_ = updating_campaign.influencers
                campaign_influencers_list = []
                if campaign_influencers_list_ != '':
                    campaign_influencers_list = json.loads(campaign_influencers_list_)
                campaign_influencers_list += influencer_handle_i_ids
                campaign_influencers_list = list(dict.fromkeys(campaign_influencers_list))
                new_params = {}
                new_params['influencers'] = json.dumps(campaign_influencers_list)
                for key, value in new_params.items():
                    setattr(updating_campaign, key, value)
                updating_campaign.save()

            # 5. competitive brand is to add, save it and update relation fields
            if len(competitive_brand_i) > 0:
                competitive_brand_i_ids = []
                for competitive_brand_i_item in competitive_brand_i:
                    new_params = {}
                    new_params['id'] = shortuuid.uuid()
                    new_params['userid'] = userid
                    new_params['name'] = competitive_brand_i_item
                    c_brand_obj = brand(**new_params)
                    c_brand_obj.save()
                    competitive_brand_i_ids.append(c_brand_obj.id)

                updating_brand = brand.objects.get(pk=brand_id)
                competitors_list_ = updating_brand.competitors
                competitors_list = []
                if competitors_list_ != '':
                    competitors_list = json.loads(competitors_list_)
                competitors_list += competitive_brand_i_ids
                competitors_list = list(dict.fromkeys(competitors_list))
                new_params = {}
                new_params['competitors'] = json.dumps(competitors_list)
                for key, value in new_params.items():
                    setattr(updating_brand, key, value)
                updating_brand.save()

                updating_campaign = campaign.objects.get(pk=campaign_obj.id)
                campaign_competitors_list_ = updating_campaign.competitors
                campaign_competitors_list = []
                if campaign_competitors_list_ != '':
                    campaign_competitors_list = json.loads(campaign_competitors_list_)
                campaign_competitors_list += competitive_brand_i_ids
                campaign_competitors_list = list(dict.fromkeys(campaign_competitors_list))
                new_params = {}
                new_params['competitors'] = json.dumps(campaign_competitors_list)
                for key, value in new_params.items():
                    setattr(updating_campaign, key, value)
                updating_campaign.save()

        return HttpResponse('success')
    except:
        return HttpResponse('fail')

@login_required()
def edit_influencer_email(request):
    try:
        param = request.POST
        influencer_id = param['influencer_id']
        email = param['text']
        updating_inf = influencer.objects.get(pk=influencer_id)
        new_params = {}
        new_params['email'] = email
        for key, value in new_params.items():
            setattr(updating_inf, key, value)
        updating_inf.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

class Influencer_detailView(Campaign_detailView):
    template_name = "main/influencer_detail.html"
    def get_context_data(self, **kwargs):
        influencer_id = kwargs['influencer_id']
        campaign_id = kwargs['campaign_id']
        campaign_detail = self.get_campaign_detail(campaign_id)
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 4
        context['influener_deatil'] = self.get_influencer_by_id(influencer_id)
        context['selected_influencers'] = self.get_selected_influencers(campaign_detail)
        context['campaign_detail'] = campaign_detail
        context['campaign_id'] = campaign_id
        context['influencer_id'] = influencer_id
        context['editable_scores_range'] = mcs.editable_scores_range
        context['influener_ig_deatil'] = self.get_influencer_ig_by_handle(context['influener_deatil'].name)
        context['analysis_able'] = False
        if context['influener_ig_deatil'] == -1:
            return context

        context['geography'] = self.get_country_list()
        context['influencer_content'] = mcm.get_influencer_content(self.request, campaign_detail, influencer_id)
        context['influencer_campaignwriteup'] = mcm.get_influencer_campaign_writeup(self.request, campaign_detail, influencer_id)

        anaylsed = context['influener_ig_deatil']['analysed']
        context['analysis_able'] = True if anaylsed else False
        if not anaylsed:
            return context

        ig_id = context['influener_ig_deatil']['ig_id']
        user_medias = self.get_user_meias(ig_id)
        if user_medias == -1:
            context['analysis_able'] = False
            return context

        context['negative_keyword'] = self.get_negative_keyword_analysis(context['influener_ig_deatil'], user_medias)
        if context['negative_keyword'] == None:
            context['analysis_able'] = False
            return context

        context['ad_keyword'] = self.get_ad_keyword_analysis(context['influener_ig_deatil'], campaign_detail.competitors, user_medias)
        if context['ad_keyword'] == None:
            context['analysis_able'] = False
            return context
        context['metrics'] = self.get_metrics_info(campaign_detail, context['influener_ig_deatil'], context['influener_deatil'], user_medias)
        if context['metrics'] == None:
            context['analysis_able'] = False
            return context
        context['recent_posts'] = self.get_recent_posts(context['influener_ig_deatil'], user_medias)
        if context['recent_posts'] == None:
            context['analysis_able'] = False
            return context

        if context['analysis_able']:
            mcm.update_to_analysed(self.request, campaign_id, influencer_id)
        return context

    def get_metrics_info(self, campaign_detail, influener_ig_deatil, influencer_detail, user_medias):
        try:
            metrics_index = mcs.metrics_index
            calculated_values = mcm.get_metrics_value_by_key(self.request, user_medias, influener_ig_deatil, influencer_detail, campaign_detail)
            if calculated_values == None:
                return None
            influencer_score = 0
            metrics_ = list(metrics.objects.filter(campaign_id=campaign_detail.id, influencer_id=influencer_detail.id).values())
            for item in metrics_:
                influencer_score += item['score']

            for row in metrics_index:
                row['edited_value'] = self.get_manual_metrics_value(metrics_, row['id'])
                row['calc_value'] = '---'
                if row['id'] in mcs.calculated_metrics_index:
                    if calculated_values != None:
                        if row['id'] == 5:
                            row['calc_value'] = calculated_values['vf']
                        elif row['id'] == 7:
                            row['calc_value'] = calculated_values['ff']
                        elif row['id'] == 8:
                            row['calc_value'] = calculated_values['age_dmg_to_target']
                        elif row['id'] == 9:
                            row['calc_value'] = calculated_values['gender_dmg_to_target']
                        elif row['id'] == 10:
                            row['calc_value'] = calculated_values['cn_dmg_to_target']
                        elif row['id'] == 11:
                            row['calc_value'] = calculated_values['er']
                        elif row['id'] == 12:
                            row['calc_value'] = calculated_values['sf']
                        elif row['id'] == 13:
                            row['calc_value'] = calculated_values['cf']

            res = {
                'metrics_table': metrics_index,
                'influencer_score': influencer_score,
            }
            return res
        except:
            return None

    def get_manual_metrics_value(self, metrics, metrics_index):
        score = 0
        for item in metrics:
            if item['metrics_index'] == metrics_index:
                score = item['score']

        return score
    def get_user_meias(self, ig_id):
        res = mcm.get_instagram_user_medias(self.request, ig_id)
        return res

    def get_recent_posts(self, influencer_ig_detail, user_medias):
        try:
            if user_medias == -1:
                return None
            res_ = []
            for media in user_medias:
                params = {}
                params['caption'] = ''
                if 'caption' in media:
                    params['caption'] = media['caption']
                params['media_url'] = ''
                if 'media_url' in media:
                    params['media_url'] = media['media_url']
                params['media_type'] = ''
                if 'media_type' in media:
                    params['media_type'] = media['media_type']
                params['comments_count'] = media['comments_count']
                params['like_count'] = media['like_count']
                params['comments'] = None
                if 'comments' in media:
                    params['comments'] = media['comments']['data']

                followers_cn = influencer_ig_detail['followers_count']
                engagement_rate = round(100 * (params['comments_count'] + params['like_count']) / followers_cn, 2)  if followers_cn != 0 else 'N/a'

                params['engagement_rate'] = engagement_rate
                res_.append(params)

            i = len(res_)
            j = i // 2 if i % 2 == 0 else i // 2 + 1
            res = []
            for k in range(0, j):
                item = {}
                if k*2 < i:
                    item['fs'] = res_[k*2]
                if k*2+1 < i:
                    item['sc'] = res_[k*2+1]
                res.append(item)
            return res
        except:
            return None

    def get_negative_keyword_analysis(self, influener_ig_deatil, user_medias):
        if influener_ig_deatil == -1:
            return None
        if user_medias == -1:
            return None
        negative_keywords = mcm.get_negative_keywords(self.request)
        res = get_search_keyword(influener_ig_deatil, negative_keywords, user_medias)
        return res
    def get_ad_keyword_analysis(self, influencer_ig_detail, competitors_ids, user_medias):
        if influencer_ig_detail == -1:
            return None
        if user_medias == -1:
            return None
        ad_keywords = mcm.get_ad_keywords(self.request)
        competitors = []

        if competitors_ids != '':
            competitors_ids = json.loads(competitors_ids)
        else:
            competitors_ids = []

        for competitor in competitors_ids:
            competitor_brand = mcm.get_brand_by_id(self.request, competitor)
            competitors.append(competitor_brand.name)

        res = get_search_ad_keyword(influencer_ig_detail, ad_keywords, competitors, user_medias)
        return res

    def get_influencer_by_id(self, influencer_id):
        influencer_ = mcm.get_influencer_by_id(self.request, influencer_id)
        return influencer_

    def get_influencer_ig_by_handle(self, handle):
        res = mcm.find_instagram_influencer_by_handle_indb(handle)
        return res

    def get_influencers(self):
        influencers_ = mcm.get_influencers(self.request)
        influencers = []
        for item in influencers_:
            influencers.append({'id': item['id'], 'name': item['name']})
        return influencers

@login_required()
def accept_influencer(request):
    try:
        params = request.POST
        campaign_id = params['campaign_id']
        influencer_id = params['influencer_id']
        campaign_ = mcm.get_campaign_by_id(request, campaign_id)
        status_ = campaign_.influencers_status
        status = {} if status_ == '' else json.loads(status_)
        status[influencer_id] = 1
        status_str = json.dumps(status)

        updating_campaign = campaign.objects.get(pk=campaign_id)
        new_params = {}
        new_params['influencers_status'] = status_str
        for key, value in new_params.items():
            setattr(updating_campaign, key, value)
        updating_campaign.save()

        return HttpResponse('success')
    except:
        return HttpResponse('fail')

@login_required()
def reject_influencer(request):
    try:
        params = request.POST
        campaign_id = params['campaign_id']
        influencer_id = params['influencer_id']
        campaign_ = mcm.get_campaign_by_id(request, campaign_id)
        status_ = campaign_.influencers_status
        status = {} if status_ == '' else json.loads(status_)
        status[influencer_id] = 0
        status_str = json.dumps(status)

        updating_campaign = campaign.objects.get(pk=campaign_id)
        new_params = {}
        new_params['influencers_status'] = status_str
        for key, value in new_params.items():
            setattr(updating_campaign, key, value)
        updating_campaign.save()

        return HttpResponse('success')
    except:
        return HttpResponse('fail')


def get_search_keyword(ig_user, negative_keywords, caption_comments):
    try:
        res = []
        for keyword in negative_keywords:
            keyword = keyword['text']

            caption_count = 0
            comment_count = 0
            for post in caption_comments:
                if 'caption' in post and keyword in post['caption']:
                    caption_count += 1
                if 'comments' in post:
                    for comment in post['comments']['data']:
                        if keyword in comment['text']:
                            comment_count += 1


            bio_count = 0
            if keyword in ig_user['biography']:
                bio_count += 1

            total_cn = caption_count + comment_count + bio_count

            param = {'keyword': keyword, 'count': total_cn}
            res.append(param)
        return res
    except:
        return None

def get_search_ad_keyword(ig_user, ad_keywords, competitors, caption_comments):
    try:
        res = []
        for keyword in ad_keywords:
            keyword = keyword['text']

            caption_count = 0
            comment_count = 0
            for post in caption_comments:
                if 'caption' in post and keyword in post['caption'] and mcm.find_competitor_handle(competitors, post['caption']):
                    caption_count += 1
                if 'comments' in post:
                    for comment in post['comments']['data']:
                        if keyword in comment['text'] and mcm.find_competitor_handle(competitors, comment['text']):
                            comment_count += 1

            bio_count = 0
            if keyword in ig_user['biography'] and mcm.find_competitor_handle(competitors, ig_user['biography']):
                bio_count += 1

            total_cn = caption_count + comment_count + bio_count

            param = {'keyword': keyword, 'count': total_cn}
            res.append(param)
        return res
    except:
        return None

class BrandView(TemplateView):
    template_name = 'main/brand_list.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 5
        context['table_data'] = self.get_brands()
        return context

    def get_brands(self):
        brands_list_ = mcm.get_brands(self.request)
        brand_list = []
        for item in brands_list_:
            brand_list.append({'id': item['id'], 'name': item['name']})
        return brand_list

class InfluencerListView(TemplateView):
    template_name = 'main/influencer_list.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 6
        context['table_data'] = self.get_influencers()
        return context

    def get_influencers(self):
        influencers_ = mcm.get_influencers(self.request)
        influencers = []
        for item in influencers_:
            if item['created_from'] == 1:
                status = 'Yes'
            elif item['created_from'] == 0:
                status = 'No'
            else:
                status = 'Unknown'
            influencers.append({'id': item['id'], 'name': item['name'], 'email': item['email'], 'api_status': status})
        return influencers

@login_required()
def edit_influencer_metrics(request):
    try:
        params = request.POST
        userid = request.user.id
        influencer_id = params['influencer_id']
        campaign_id = params['campaign_id']
        value = float(params['value'])
        index = int(params['metrics_index'])

        metrics_ = list(metrics.objects.filter(campaign_id=campaign_id, influencer_id=influencer_id, metrics_index=index).values())
        if len(metrics_) == 0:
            new_params = {}
            new_params['id'] = shortuuid.uuid()
            new_params['userid'] = request.user.id
            new_params['campaign_id'] = campaign_id
            new_params['influencer_id'] = influencer_id
            new_params['metrics_index'] = index
            new_params['score'] = value
            metrics_obj = metrics(**new_params)
            metrics_obj.save()
        elif len(metrics_) == 1:
            metrics_obj = metrics.objects.get(pk=metrics_[0]['id'])
            new_params = {}
            new_params['score'] = value
            for key, value in new_params.items():
                setattr(metrics_obj, key, value)
            metrics_obj.save()
        else:
            return HttpResponse('duplicate')
        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('fail')

@login_required()
def get_influencer_score(request):
    params = request.GET
    userid = request.user.id
    campaign_id = params['campaign_id']
    influencer_id = params['influencer_id']
    influencer_score = 0
    metrics_ = list(metrics.objects.filter(campaign_id=campaign_id, influencer_id=influencer_id).values())
    for item in metrics_:
        influencer_score += item['score']
    return HttpResponse(influencer_score)

@login_required()
def edit_influencer_ar(request):
    try:
        param = request.POST
        campaign_id = param['campaign_id']
        influencer_id = param['influencer_id']
        value = param['value']
        campaign_ = mcm.get_campaign_by_id(request, campaign_id)
        status_ = campaign_.influencers_status
        status = {} if status_ == '' else json.loads(status_)
        status[influencer_id] = int(value)
        status_str = json.dumps(status)

        new_params = {}
        new_params['influencers_status'] = status_str
        for key, value in new_params.items():
            setattr(campaign_, key, value)
        campaign_.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

class ProfileView(TemplateView):
    template_name = 'main/myprofile.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['is_superuser'] = self.request.user.is_superuser
        context['username'] = self.request.user.username
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['userclass'] = mcm.get_user_class(self.request)
        return context

class StatisticsView(TemplateView):
    template_name = 'main/statistics.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        return context

class NotificationView(TemplateView):
    template_name = 'main/notification.html'
    def get_context_data(self, **kwargs):
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        return context

@login_required()
def export_pdf(request):
    params = request.POST
    campaign_id = params['campaign_id']
    influencer_id = params['influencer_id']
    influener_ig_id = params['influener_ig_id']

    context = {}
    context['request'] = request
    context['campaign_id'] = campaign_id
    context['influencer_id'] = influencer_id
    context['influener_ig_id'] = influener_ig_id
    context['content_alias'] = 'influencer_profile'

    directory_name = mcm.get_directory_name(request, 1)
    pdf_filename = directory_name + "snap_" + datetime.now().strftime("%m%d%Y_%H%M%S") + '.pdf'
    pdf.render_pdf(context, pdf_filename)
    return HttpResponse(pdf_filename)

@login_required()
def edit_influencer_additional(request):
    try:
        param = request.POST
        influencer_id = param['influencer_id']
        cn_code = param['cn_code']
        rel_name = param['rel_name']
        influencer_ = mcm.get_influencer_by_id(request, influencer_id)
        new_params = {}
        new_params['real_name'] = rel_name
        new_params['origin_cn'] = cn_code
        for key, value in new_params.items():
            setattr(influencer_, key, value)
        influencer_.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

@login_required()
def edit_influencer_campaign_writeup(request):
    try:
        param = request.POST
        campaign_id = param['campaign_id']
        campaign_writeup_txt = param['campaign_writeup']
        campaign_ = mcm.get_campaign_by_id(request, campaign_id)
        new_params = {}
        new_params['influencers_campaign_writeup'] = campaign_writeup_txt
        for key, value in new_params.items():
            setattr(campaign_, key, value)
        campaign_.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

@login_required()
def edit_influencer_content(request):
    try:
        param = request.POST
        influencer_id = param['influencer_id']
        campaign_id = param['campaign_id']
        inf_cam_ytb = int(param['inf_cam_ytb'])
        inf_cam_insp = int(param['inf_cam_insp'])
        inf_cam_inss = int(param['inf_cam_inss'])

        campaign_ = mcm.get_campaign_by_id(request, campaign_id)
        content_ = campaign_.influencers_content
        content = {} if content_ == '' else json.loads(content_)
        content[influencer_id] = {
            'inf_cam_ytb': inf_cam_ytb,
            'inf_cam_insp': inf_cam_insp,
            'inf_cam_inss': inf_cam_inss,
        }
        content_str = json.dumps(content)

        new_params = {}
        new_params['influencers_content'] = content_str
        for key, value in new_params.items():
            setattr(campaign_, key, value)
        campaign_.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

@login_required()
def export_png(request):
    try:
        params = request.POST
        campaign_id = params['campaign_id']
        influencer_id = params['influencer_id']
        influener_ig_id = params['influencer_ig_id']

        context = {}
        context['request'] = request
        context['campaign_id'] = campaign_id
        context['influencer_id'] = influencer_id
        context['influener_ig_id'] = influener_ig_id
        context['content_alias'] = 'influencer_profile'

        directory_name = mcm.get_directory_name(request, 1)
        pdf_filename = directory_name + "snap_" + datetime.now().strftime("%m%d%Y_%H%M%S") + '.pdf'
        pdf.render_pdf(context, pdf_filename)

        out_directory_name = mcm.get_directory_name(request, 2)
        out_filename = out_directory_name + "snap_" + datetime.now().strftime("%m%d%Y_%H%M%S") + '.png'

        images = convert_from_path(os.path.join(settings.BASE_DIR, pdf_filename))
        for image in images:
            image.save(out_filename)
            break

        os.remove(os.path.join(settings.BASE_DIR, pdf_filename))
        return HttpResponse(out_filename)
    except Exception as e:
        print(str(e))
        return HttpResponse('fail')

@login_required()
def add_influencer(request):
    context = {}
    context['menu_data'] = mcm.get_user_menu_data(request)
    context['menu_id'] = 6
    return render(request, 'main/add_influencer.html', context)

@login_required()
def save_influencer(request):
    try:
        param = request.POST
        handle = param['handle']
        if len(mcm.get_influencer_by_handle(request, handle)) > 0:
            raise Exception
        new_params = {}
        new_params['id'] = shortuuid.uuid()
        new_params['userid'] = request.user.id
        new_params['name'] = handle
        new_params['created_from'] = 0

        influencer_obj = influencer(**new_params)
        influencer_obj.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')

class InfluencerView(Influencer_detailView):
    template_name = 'main/influencer.html'
    def get_context_data(self, **kwargs):
        influencer_id = kwargs['influencer_id']
        context = {}
        context['menu_data'] = mcm.get_user_menu_data(self.request)
        context['menu_id'] = 6
        context['influencer_id'] = influencer_id
        context['influencer_basic'] = self.get_influencer_by_id(self.request, influencer_id)

        influencer_ig_detail = self.get_influencer_ig_by_handle(context['influencer_basic']['handle'])
        context['influencer_ig_detail'] = influencer_ig_detail

        ig_id = influencer_ig_detail['ig_id']
        user_medias = self.get_user_meias(ig_id)
        context['user_medias'] = user_medias

        context['negative_keyword'] = self.get_negative_keyword_analysis(influencer_ig_detail, user_medias)
        context['ad_keyword'] = mcm.get_ad_keywords(self.request)
        context['geography'] = self.get_country_list()
        context['metrics_table'] = mcs.metrics_index
        context['audience_gender_age'] = self.get_audience_gender_age(self.request, ig_id)
        context['audience_country'] = self.get_audience_country(self.request, ig_id)
        context['recent_posts'] = self.get_recent_posts(influencer_ig_detail, user_medias)
        context['campaigns'] = self.get_campaigns_by_influencer(self.request, influencer_id)
        return context

    def get_campaigns_by_influencer(self, request, influencer_id):
        campaigns = mcm.get_campaigns(request)
        new_array = []
        for campaign in campaigns:
            if influencer_id in campaign['influencers']:
                new_param = {
                    'id': campaign['id'],
                    'name': campaign['name'],
                    'brand': mcm.get_brand_by_id(self.request, campaign['brand_id']),
                    'status': mcm.get_campaign_status(self.request, campaign['status'])
                }
                new_array.append(new_param)
        return new_array

    def get_audience_country(self, request, ig_id):
        res = mcm.get_instagram_audience_country_by_ig_id(request, ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])
        new_array = []
        for item in data_sorted:
            new_params = {'key': item[0], 'value': item[1]}
            new_array.append(new_params)
        return new_array

    def get_audience_gender_age(self, request, ig_id):
        res = mcm.get_instagram_audience_gender_age_by_ig_id(request, ig_id)
        data_sorted = []
        if res != None and res['values'] != '':
            values = json.loads(res['values'])
            data_sorted = sorted(values.items(), key=lambda x: x[1])
        new_array = []
        for item in data_sorted:
            new_params = {'key': item[0], 'value': item[1]}
            new_array.append(new_params)
        return new_array

    def get_influencer_by_id(self, request, influecer_id):
        res = mcm.get_influencer_by_id(request, influecer_id)
        result = {}
        result['handle'] = res.name
        result['country'] = mcm.get_country_name_from_alpha2(request, res.origin_cn)
        result['origin_cn'] = res.origin_cn
        result['name'] = res.real_name
        result['connect_stat'] = 'YES' if res.created_from == 1 else 'NO'
        return result

    def get_recent_posts(self, influencer_ig_detail, user_medias):
        try:
            if user_medias == -1:
                return None
            res_ = []
            for media in user_medias:
                params = {}
                params['caption'] = ''
                if 'caption' in media:
                    params['caption'] = media['caption']
                params['media_url'] = ''
                if 'media_url' in media:
                    params['media_url'] = media['media_url']
                params['media_type'] = ''
                if 'media_type' in media:
                    params['media_type'] = media['media_type']
                params['comments_count'] = media['comments_count']
                params['like_count'] = media['like_count']
                params['comments'] = None
                if 'comments' in media:
                    params['comments'] = media['comments']['data']

                followers_cn = influencer_ig_detail['followers_count']
                engagement_rate = round(100 * (params['comments_count'] + params['like_count']) / followers_cn, 2)  if followers_cn != 0 else 'N/a'

                params['engagement_rate'] = engagement_rate
                res_.append(params)

            return res_
        except:
            return None

