from django.utils.deprecation import MiddlewareMixin
from module.eaeo import constant as mcs
from module.eaeo import common as mcm
from social_django.models import UserSocialAuth
from main.models import *
import shortuuid

class PathHandlingMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if request.path in mcs.social_auth_complete_path and request.user.is_authenticated:
            social_auth = UserSocialAuth.objects.filter(user=request.user, provider='facebook').first()
            if social_auth != None and social_auth.extra_data['accounts'] != None:
                try:
                    accounts = social_auth.extra_data['accounts']['data']
                    userid = request.user.id
                    for account in accounts:
                        handle = account['instagram_business_account']['username']
                        ig_id = account['instagram_business_account']['id']
                        influencers_ = list(influencer.objects.filter(name=handle).values())
                        if len(influencers_) == 0:
                            new_params = {}
                            new_params['id'] = shortuuid.uuid()
                            new_params['influencer_userid'] = userid
                            new_params['name'] = handle
                            new_params['created_from'] = 1
                            influencer_obj = influencer(**new_params)
                            influencer_obj.save()
                            mcm.callback_sync_instagram_account(request, ig_id)
                        elif len(influencers_) >= 1:
                            influencer_ = influencers_[0]
                            influencer_id = influencer_['id']
                            influencer_obj = influencer.objects.get(pk=influencer_id)
                            if influencer_obj.created_from == 1:
                                continue
                            new_params = {}
                            new_params['influencer_userid'] = userid
                            new_params['created_from'] = 1
                            for key, value in new_params.items():
                                setattr(influencer_obj, key, value)
                            influencer_obj.save()
                            mcm.callback_sync_instagram_account(request, ig_id)
                        else:
                            print('no instagram accounts')
                except Exception as e:
                    print(str(e))
        return response