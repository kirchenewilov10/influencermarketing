user_menu_data = [
        {
            'id': 1,
            'url': '/',
            'name': 'Home',
            'icon': 'fa fa-dashboard',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 2,
            'url': '/stat',
            'name': 'Stats',
            'icon': 'fa fa-bar-chart',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 3,
            'url': '/notificatioin',
            'name': 'Notifications',
            'icon': 'fa  fa-warning',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 4,
            'url': '/campaign',
            'name': 'Campaigns',
            'icon': 'fa big-icon fa-gear icon-wrap',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 5,
            'url': '/brand',
            'name': 'Brands',
            'icon': 'fa fa-amazon',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 6,
            'url': '/influencer',
            'name': 'Influencers',
            'icon': 'fa fa-users',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 7,
            'url': '/profile',
            'name': 'Profile',
            'icon': 'fa fa-user',
            'parent': 0,
            'has_child': 0
        }
    ]

influencer_menu_data = [
        {
            'id': 1,
            'url': '/',
            'name': 'Home',
            'icon': 'fa fa-dashboard',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 7,
            'url': '/profile',
            'name': 'Profile',
            'icon': 'fa fa-user',
            'parent': 0,
            'has_child': 0
        }
    ]
safety_score = [
    {'id': 'R', 'name': 'RED'},
    {'id': 'A', 'name': 'AMBER'},
    {'id': 'G', 'name': 'GREEN'},
]

kpi = [
    {'id': 'ct', 'name': 'Content'},
    {'id': 'an', 'name': 'Awareness'},
    {'id': 'cv', 'name': 'Conversions'},
]

gender = [
    {'id': 'A', 'name': 'All'},
    {'id': 'M', 'name': 'Male'},
    {'id': 'F', 'name': 'Female'},
]

geography = ['HU', 'SI', 'PT', 'DK', 'UA', 'CH', 'SG', 'AE', 'PK', 'SE', 'IL', 'AT', 'NL', 'BE', 'IQ', 'CR', 'TH', 'NG', 'RU', 'IE', 'KR', 'NO', 'SA', 'CO', 'ZA', 'IR', 'CL', 'MY', 'NZ', 'FR', 'ES', 'AR', 'MX', 'TR', 'PH', 'IN', 'JP', 'IT', 'DE', 'ID', 'BR', 'CA', 'GB', 'AU', 'US']

age = ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']

metrics_index = [
    {'id': 0, 'name': 'Does the influencer fit the brand image?'},
    {'id': 1, 'name': 'Google Keyword Analysis'},
    {'id': 2, 'name': 'Twitter Keyword Analysis'},
    {'id': 3, 'name': 'They contain explicit/sexualised/controversial content'},
    {'id': 4, 'name': 'Is there a clear/widespread negative viewpoint from the audience in the comments towards the influencer?'},
    {'id': 5, 'name': 'Average Instagram Post Impressions to Follower Ratio'},
    {'id': 6, 'name': 'What percentage of their content do they feature in'},
    {'id': 7, 'name': 'Following to Follower ratio'},
    {'id': 8, 'name': 'The age demographic on their account matches the campaign target market(Percentage match)'},
    {'id': 9, 'name': 'The gender demographic on their account matches the campaign target market(Percentage match)'},
    {'id': 10, 'name': 'The location demographic on their account matches the campaign target market(Percentage match)'},
    {'id': 11, 'name': 'Average Instagram engagement rate'},
    {'id': 12, 'name': 'Average Instagram Story Slide views to follower ratio'},
    {'id': 13, 'name': 'Comments to followers rate'},
    {'id': 14, 'name': 'Genuine comments percentage'},
    {'id': 15, 'name': 'Have their Instagram followers grown organically/steadily over time?'},
    {'id': 16, 'name': 'Does the influencer and their audience have a clear affinity with the brand?'},
    {'id': 17, 'name': 'Does the influencer have a personal story which really connects the influencer with the brand?'},
    {'id': 18, 'name': 'The photo/video quality across their Instagram'},
    {'id': 19, 'name': 'Monthly Google searches of their name / nickname'},
    {'id': 20, 'name': 'They have strong TV/Film celebrity status'},
    {'id': 21, 'name': 'They engage with their audience within the comments'},
    {'id': 22, 'name': 'They directly talk to their audience in videos or post captions on Instagram'},
    {'id': 23, 'name': 'They communicate clearly in Instagram videos'},
    {'id': 24, 'name': 'They use correct good grammar, spelling in captions'},
    {'id': 25, 'name': 'Their captions actually describe what is happening in the post, something relating to the post'},
    {'id': 26, 'name': 'They go in-depth on their captions'},
    {'id': 27, 'name': 'They collaborate with other Instagrammers'},
    {'id': 28, 'name': 'They have recently worked with similar/competing brands'},
    {'id': 29, 'name': 'They have 33%+ sponsored content and brand deals'},
    {'id': 30, 'name': 'They have published sponsored content on behalf of a brand that has no relation/affinity to them or their audience'},
    {'id': 31, 'name': 'They have a popular YouTube channel?'},
    {'id': 32, 'name': 'They have a popular blog/personal website'},
    {'id': 33, 'name': 'Their content goes live regularly, on the same days each week, not sporadically (Assess over the last 30 days)'},
    {'id': 34, 'name': 'Are they verified on Instagram?'},
]
calculated_metrics_index = [5, 7, 8, 9, 10, 11, 12, 13]

editable_scores_range = [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]

social_auth_complete_path = [
    '/complete/facebook/'
]

instagram_sync_period = 3600

auto_sync = True