from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sign-in', views.SigninView, name='signin'),
    path('sign-up', views.SignupView, name='signup'),
    path('social_error_url', views.social_error_url, name='social_error_url'),

    path('new_social_auth_user', views.new_social_auth_user, name='new_social_auth_user'),
    path('influencer-sign-up', views.Influencer_signupView, name='influencer_signupview'),

    path('logout', views.logout_view, name='logout'),

    path('campaign', views.login_required(views.CampaignView.as_view()), name='campaign'),
    path('create_campaign', login_required(views.Create_campaignView.as_view()), name='create_campaign'),
    path('save_campaign', views.save_campaign, name='save_campaign'),
    path('campaign_detail/<campaign_id>', views.login_required(views.Campaign_detailView.as_view()), name='campaign'),
    path('edit_influencer_email', views.edit_influencer_email, name='edit_influencer_email'),
    path('campaign_detail/<campaign_id>/influencer_detail/<influencer_id>', views.login_required(views.Influencer_detailView.as_view()), name='inlfuencer'),

    path('accept_influencer', views.accept_influencer, name='accept_influencer'),
    path('reject_influencer', views.reject_influencer, name='reject_influencer'),

    path('brand', views.login_required(views.BrandView.as_view()), name='brand_view'),
    path('influencer', views.login_required(views.InfluencerListView.as_view()), name='influencer_view'),

    path('edit_influencer_metrics', views.edit_influencer_metrics, name='edit_influencer_metrics'),
    path('get_influencer_score', views.get_influencer_score, name='get_influencer_score'),

    path('profile', views.login_required(views.ProfileView.as_view()), name='profile'),
    path('stat', views.login_required(views.StatisticsView.as_view()), name='statistics'),
    path('notificatioin', views.login_required(views.NotificationView.as_view()), name='notification'),

    path('edit_influencer_ar', views.edit_influencer_ar, name='edit_influencer_ar'),
    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('edit_influencer_additional', views.edit_influencer_additional, name='edit_influencer_additional'),
    path('edit_influencer_content', views.edit_influencer_content, name='edit_influencer_content'),
    path('edit_influencer_campaign_writeup', views.edit_influencer_campaign_writeup, name='edit_influencer_campaign_writeup'),

    path('export_png', views.export_png, name='export_png'),
    path('add_influencer', views.add_influencer, name='add_influencer'),
    path('save_influencer', views.save_influencer, name='save_influencer'),

    path('influencer_detail/<influencer_id>', views.login_required(views.InfluencerView.as_view()), name='inlfuencerview'),
]