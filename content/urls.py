from content import CRUD_views, views, API_views
from django.urls import path


urlpatterns = [
    path('search_api/', API_views.SearchAPIView.as_view(), name='search'),

    path('radical/<int:pk>', CRUD_views.RadicalDetail.as_view(),
         name='radical-detail'),
    path('character/<int:pk>', CRUD_views.CharacterDetail.as_view(),
         name='character-detail'),
    path('word/<int:pk>', CRUD_views.WordDetail.as_view(),
         name='word-detail'),
    path('word_set/<int:pk>', CRUD_views.WordSetDetail.as_view(),
         name='wordset-detail'),
    path('word_set', CRUD_views.WordSetList.as_view(),
         name='wordset-list'),

    path('display/word/<int:pk>', views.WordDisplayView.as_view(),
         name='word_display'),
    path('display/character/<int:pk>', views.CharacterDisplayView.as_view(),
         name='character_display'),
    path('display/radical/<int:pk>', views.RadicalDisplayView.as_view(),
         name='radical_display'),
    path('display/question/<int:question_pk>',
         views.QuestionDisplayView.as_view(),
         name='question_display'),

    path('display/questions_by_set/<slug:set_pk>/<int:question_pk>',
         views.admin_display_question,
         name='admin_question_display'),
    path('display/questions_by_set/<slug:set_pk>',
         views.admin_display_question,
         name='admin_question_display'),

    path('display/wordset/<int:pk>/<int:word_pk>',
         views.SetDisplayView.as_view(),
         name='set_display'),
    path('display/wordset/<int:pk>',
         views.SetDisplayView.as_view(),
         name='set_display'),

    path('question/<int:pk>', API_views.QuestionView.as_view()),

    path('linked_field_autocomplete',
         API_views.LinkedFieldAutocomplete.as_view(),
         name='linked_field_autocomplete'),
    path('review_question_factory/<slug:question_type>/<int:ro_id>',
         views.ReviewQuestionFactoryView.as_view(),
         name='review_question_factory_view'),

    path('show_all_options_toggle',
         views.show_all_options_toggle,
         name='show_all_options_toggle'),
    path('split_wordset/<int:wordset_pk>',
         views.split_set_view,
         name='split_wordset'),
]
