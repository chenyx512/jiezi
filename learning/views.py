import datetime
import random
import requests
import time
import hashlib
import base64
import os.path
import json

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F, Max, DurationField, ExpressionWrapper
from django.contrib.auth import login, logout
from rest_framework import generics
from django.utils.decorators import method_decorator

from learning.models import Character, CharacterSet, Radical, Report
from accounts.models import User, UserCharacter, UserCharacterTag
from jiezi.utils.json_serializer import chenyx_serialize
from learning.learning_algorithm_constants import Constants
from .serializers import CharacterSerializer, CharacterSetSerializer, \
    RadicalSerializer


def display_character(request, character_pk, **context_kwargs):
    """ Display character with pk=character_pk, if it is not found,
    display the next one.
    context_kwargs are passed into render directly """
    try:
        Character.objects.get(pk=character_pk)
    except ObjectDoesNotExist:
        character = Character.objects.filter(pk__gt=character_pk).first()
        return redirect('display_character', character_pk=character.pk)

    character = Character.objects.filter(pk__gte=character_pk).first()
    radicals = [
        Radical.objects.get(pk=character.radical_1_id),
        Radical.objects.get(pk=character.radical_2_id)
        if character.radical_2_id else None,
        Radical.objects.get(pk=character.radical_3_id)
        if character.radical_3_id else None
    ]
    return render(
        request,
        'learning/display_character.html',
        {'character': character, 'radicals': radicals, **context_kwargs}
    )


def try_me(request):
    if request.user.is_authenticated:
        return start_learning(request)
    username = f'test_user_{random.randint(0, 1e6):06d}'
    password = 'test'
    user = User.objects._create_user(username, '', password, is_guest=True)
    login(request, user)
    CharacterSet.objects.get(name='try_me').add_to_user(user)
    return start_learning(request)


@login_required
def start_learning(request):
    # clears session data without logging out the user
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]
    request.session.cycle_key()

    # minutes_to_learn = int(request.POST.get('minutes_to_learn', 10))
    uc_tags_filter = json.loads(request.POST.get('uc_tags_filter'))
    assert isinstance(uc_tags_filter, list), 'uc_tags_filter must be list of ints'
    for uc_tag in uc_tags_filter:
        assert UserCharacterTag.objects.get(pk=uc_tag).user == request.user

    if request.user.last_study_time.date() == timezone.now().date() - \
            datetime.timedelta(days=1):
        request.user.study_streak += 1
    else:
        request.user.study_streak = 1

    request.user.last_study_duration = datetime.timedelta(seconds=0)
    request.user.last_study_vocab_count = 0
    request.user.save()

    request.session['last_record_time'] = timezone.now()
    request.session['uc_tags_filter'] = uc_tags_filter
    # request.session['end_learning_time'] = \
    #     timezone.now() + datetime.timedelta(minutes=minutes_to_learn)

    return redirect(f'/learning/status{request.session.session_key}')


@login_required
def review(request, character, field_name):
    other_uc = request.user.user_characters.exclude(character__pk=character.pk)
    # TODO calling list on QuerySet may be inefficient
    if len(other_uc) < 3:
        other_characters = Character.objects.exclude(pk=character.pk)
        other_characters = random.sample(list(other_characters), 3)
        if len(other_characters) < 3:
            raise Exception('Database should have at least 4 characters')
        choices = [getattr(c, field_name) for c in other_characters]
    else:
        other_uc = random.sample(list(other_uc), 3)
        choices = [getattr(c.character, field_name) for c in other_uc]
    random.shuffle(choices)
    correct_answer = random.randint(0, 3)
    choices.insert(correct_answer, getattr(character, field_name))
    request.session['correct_answer'] = correct_answer
    request.session['field_name'] = field_name
    return render(
        request,
        'learning/review.html',
        {
            'character': character.chinese,
            'type': field_name,
            'choices': choices
        }
    )


@login_required
@csrf_exempt
def learning_process(request, session_key):
    """ This is the main view that controls the learning process
    Note session['next'] stores a list of dicts {'func', 'args'} and
    they should be called before transition_stage happens """

    def transition_stage():
        """ this function decides whether to learn or review,
        :return (mode, data)
        mode is 'learn', 'review', or None (do nothing)
        learning data is uc
        review data is (uc, test_field)
        """
        tagged_ucs = request.user.user_characters.filter(
            tag__in=request.session.get('uc_tags_filter'), mastered=False)
        uc_to_learn = tagged_ucs.filter(learned=False).first()

        ucs_to_review = tagged_ucs.filter(learned=True)
        uc_in_progress_cnt = ucs_to_review.count()
        uc_to_review = None
        field_to_review = None
        global_max_weighted_duration = datetime.timedelta(seconds=0)
        for test_field in Character.TEST_FIELDS:
            if not ucs_to_review.exists():
                continue
            annoatated_ucs = ucs_to_review.annotate(
                weighted_duration=ExpressionWrapper(
                    (timezone.now() - F(test_field + '_time_last_studied'))
                    / (F(test_field + '_in_a_row') + 1)
                    + Constants.ADDED_DURATION,
                    output_field=DurationField()
                )
            )
            local_max_weighted_duration = annoatated_ucs.aggregate(
                Max('weighted_duration')
            )['weighted_duration__max']
            if local_max_weighted_duration > global_max_weighted_duration:
                uc_to_review = annoatated_ucs.filter(
                    weighted_duration=local_max_weighted_duration).first()
                field_to_review = test_field
                global_max_weighted_duration = local_max_weighted_duration

        learn_rv = ('learn', uc_to_learn)
        review_rv = ('review', (uc_to_review, field_to_review))
        if not uc_to_learn and not uc_to_review:
            return None, None
        elif not uc_to_learn:
            return review_rv
        elif not uc_to_review:
            return learn_rv
        elif uc_in_progress_cnt >= Constants.MAX_UC_IN_PROGRESS_CNT:
            return review_rv
        elif uc_in_progress_cnt < Constants.MIN_UC_IN_PROGRESS_CNT:
            return learn_rv
        else:
            return learn_rv if random.random() < Constants.LEARN_PROB \
                            else review_rv


    def end_learning(msg=''):
        return render(request, 'simple_response.html', {
            'content': msg
        })

    def check_answer():
        correct_answer = request.session['correct_answer']
        is_correct = int(request.POST.get('user_answer')) == correct_answer

        uc = UserCharacter.objects.get(pk=request.session['uc_pk'])
        if not request.session['is_tolerant']:
            uc.update(is_correct, request.session['field_name'])

        if not is_correct and not request.session['is_tolerant']:
            request.session['next'] = [{
                'func': display_character,
                'kwargs':{'character_pk':uc.character.pk, 'is_next':True}
            }]
        return JsonResponse({'correct_answer': correct_answer})

    # prevents the user from resuming into previous session
    if request.session.session_key != session_key:
        return redirect('404')

    # record stats
    delta_time = timezone.now() - request.session['last_record_time']
    request.session['last_record_time'] = timezone.now()
    request.user.last_study_duration += delta_time
    request.user.total_study_duration += delta_time
    request.user.last_study_time = timezone.now()
    request.user.save()

    # if request.session['end_learning_time'] < timezone.now():
    #     if request.user.is_guest:
    #         logout(request)
    #     return end_learning(
    #         '<p style="text-align:center; font-size:16px;">'
    #         'Time is up!<br>'
    #         'Congratulations on learning these new characters!<br>' +
    #         'To save your progress, sign up now.<br>' +
    #         '(Solved is completely free!)' if request.user.is_guest else ''
    #         '</p>'
    #     )

    if request.method == 'POST':
        if request.POST.get('i_know_this', False):
            character_pk = int(request.POST.get('character_pk'))
            uc = UserCharacter.objects.get(user=request.user,
                                           character__pk=character_pk)
            uc.delete()
            request.session['next']=None
        else:
            return check_answer()

    next_value = request.session.get('next', [])
    if next_value:
        request.session['next'] = next_value[1:]
        func = next_value[0]['func']
        kwargs = next_value[0]['kwargs']
        return func(request, **kwargs)

    mode, data = transition_stage()
    if mode is None: # this set is done
        uc_tags_filter = request.session['uc_tags_filter']
        msg = ('Congratulations on finishing these character sets:<br>'
            if len(uc_tags_filter) > 1 else
            'Congratulations on finishing this character set:<br>')
        for uc_tag_pk in uc_tags_filter:
            msg += f'{UserCharacterTag.objects.get(pk=uc_tag_pk).name}<br>'
        if request.user.is_guest:
            msg += 'To save your progress, sign up now.<br>' + \
                   '(Solved is completely free!)'
            logout(request)
        return end_learning(
            '<p style="text-align:center; font-size:16px;">'
             + msg +'</p>'
        )

    if mode == 'learn':  # here learn only means learning for first time
        uc = data
        request.session['uc_pk'] = uc.pk
        request.user.last_study_vocab_count += 1
        request.user.save()
        request.session['is_tolerant'] = True
        request.session['next'] = []
        uc.learned = True
        for test_field in Character.TEST_FIELDS:
            request.session['next'].append({
                'func': review,
                'kwargs': {'character': uc.character, 'field_name': test_field}
            })
            setattr(uc, test_field + '_time_last_studied', timezone.now())
        uc.save()
        return display_character(request, uc.character.pk, is_next=True)
    elif mode == 'review':
        uc, test_field = data
        request.session['uc_pk'] = uc.pk
        request.session['is_tolerant'] = False
        return review(request, uc.character, test_field)


def report(request):
    report = Report(origin=request.POST.get('origin'),
                    description_1=request.POST.get('description_1'),
                    description_2=request.POST.get('description_2'))
    if isinstance(request.user, User):
        report.user = request.user
    report.save()
    return render(request, 'simple_response.html', {
        'content': 'Thank you for your response!'
    })
    return redirect('404')


def getAudio(request):
    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    AUE = "lame"
    APPID = "5d2407a2"
    API_KEY = "1194c50ae845b966ade10e8b47ece15e"

    def getHeader():
        curTime = str(int(time.time()))
        # ttp=ssml
        param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"aisxping\",\"speed\":\"10\",\"engine_type\":\"intp65\"}"

        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')

        m2 = hashlib.md5()
        m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))

        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBody(text):
        data = {'text': text}
        return data

    def writeFile(file, content):
        with open(file, 'wb') as f:
            f.write(content)
        f.close()

    def requestAudio(character):
        r = requests.post(URL, headers=getHeader(), data=getBody(character))

        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
            sid = r.headers['sid']
            if AUE == "raw":
                writeFile("media/audio/" + request.GET.get("pk") + ".wav",
                          r.content)
            else:
                writeFile("media/audio/" + request.GET.get("pk") + ".mp3", r.content)
            return True
        else:
        #   error-code reference: https://www.xfyun.cn/document/error-code
            return False

    audioKey = request.GET.get("pk")
    if os.path.exists('media/audio/' + audioKey + '.mp3'):
        return JsonResponse({'success': True})
    else:
        res = requestAudio(request.GET.get("t"))
        if res:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


"""
@api {POST} /search/ Search
@apiDescription search characters using ONE given keyword, it will be search 
    against pinyin (without accent), chinese, 3 definitions
@apiGroup general

@apiParam   {String}        key_word  the keyword to be searched

@apiSuccess {Object[]} characters list of serialized Character objects
"""


@csrf_exempt
def search(request):
    keyword = request.POST.get('keyword')
    characters_1 = Character.objects.filter(
        Q(pinyin__unaccent__iexact=keyword) | Q(chinese__exact=keyword)
    )
    characters_2 = Character.objects.filter(
        Q(definition_1__icontains=keyword) |
        Q(definition_2__icontains=keyword) |
        Q(definition_3__icontains=keyword) |
        Q(pinyin__unaccent__icontains=keyword)
    ).difference(characters_1)
    return JsonResponse({
        'characters': chenyx_serialize(characters_1) +
                      chenyx_serialize(characters_2)
    })


"""
@api {POST} /learning/start_learning/  Start Learning
@apiDescription Start Learning, this should be done with an actual form submission
@apiGroup learning

@apiParam  {int[]}   uc_tags_filter the ids of UserCharacterTags to INCLUDE


@apiSuccessExample learning/review.html
context dictionary:
'choices': a list of 4 strings
'question': string of the question

Display the question and choices with no next button
After the user selects an answer, ajax POST to the same url with following args:
    'user_answer': integer with range [0, 4), representing user's answer
The server responds with 'correct_answer', which is in the same range,
    display the result, provide next button, and when the user clicks next, 
    submit GET request with no args
refer to old master review page for how to do specific things
    https://github.com/chenyx512/jiezi/blob/old-master/jiezi/templates/learning/review_interface.html

@apiSuccessExample learning/display_character.html:
There shouldn't be any ajax in this
In context dictionary, if 'is_next', provide an next button that submits
    GET form to original url, otherwise keep the next button the same as before
"""

class CharacterDetail(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class RadicalDetail(generics.RetrieveAPIView):
    queryset = Radical.objects.all()
    serializer_class = RadicalSerializer

class CharacterSetDetail(generics.RetrieveAPIView):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
