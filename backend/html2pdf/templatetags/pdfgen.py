import os
from pathlib import Path
from django.conf import settings
from django import template
import requests
import json
from datetime import datetime
import textwrap
import collections
from module.eaeo import common as mcm
from module.eaeo import constant as mcs
from module.eaeo import instagram as itg

register = template.Library()

@register.inclusion_tag('pdfgen/influencer_profile.html', takes_context=True)
def influencer_profile_content(context):
    try:
        request = context.dicts[1]['request']
        influencer_id = context.dicts[1]['influencer_id']
        campaign_id = context.dicts[1]['campaign_id']
        influener_ig_id = context.dicts[1]['influener_ig_id']
        data = mcm.get_influencer_data_to_pdf(request, campaign_id, influencer_id, influener_ig_id)
        return data
    except Exception as e:
        return {'res': None}

@register.inclusion_tag('pdfgen/style.html', takes_context=True)
def influencer_profile_style(context):
    page_size = 'A4'
    page_width = 21
    page_height = 29.7
    page_orientation = 'portrait'
    background_path = os.path.join(settings.BASE_DIR, 'static/library/img/inf_pro_background.jpg')
    font_path = os.path.join(settings.BASE_DIR, 'static/library/font/Roboto/Roboto-Regular.ttf')
    styleconext = {}
    styleconext['page_size'] = page_size
    styleconext['page_orientation'] = page_orientation
    styleconext['background_path'] = background_path
    styleconext['font_path'] = font_path
    styleconext['pagesize'] = '%s %s' % (styleconext['page_size'], styleconext['page_orientation'])
    styleconext['margin_left'] = 0
    styleconext['margin_right'] = 0
    styleconext['margin_top'] = 4
    styleconext['margin_height'] = page_height - styleconext['margin_top']
    styleconext['margin_width'] = page_width - styleconext['margin_left'] - styleconext['margin_right']
    return styleconext



