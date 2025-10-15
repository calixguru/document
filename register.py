from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from pracs.models import *
from django.shortcuts import render
from django.utils.timezone import now, timedelta
import random
from . import questions, pins
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import uuid, re
from django.urls import reverse
from pracs import pins as p
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string

topics = [
    {'course': '', 'topic': '', 'date': '', 'yt': ''},
    {'topic': 'Functions', 'course': 'Mathematics', 'date': 'June 22, 2025 19:00:00', 'yt': 'yfWT-Vg8bYw?si=1qy-NaUYcdpxhYT2'},
    {'topic': 'Bryophytes, Pteridophytes, Gymnosperms and Angiosperms', 'course': 'Biology', 'date': 'June 22, 2025 21:00:00', 'yt': 'YT002'},
    {'topic': 'Functional groups, hybridization of hydrocarbons and systematic nomenclature', 'course': 'Chemistry', 'date': 'June 23, 2025 21:00:00', 'yt': 'YT003'},
    {'topic': 'Concept and dimension of education', 'course': 'Education', 'date': 'June 24, 2025 21:00:00', 'yt': 'YT004'},
    {'topic': 'Physics textbook chapters 1 to 3', 'course': 'Physics', 'date': 'June 25, 2025 21:00:00', 'yt': 'YT005'},
    {'topic': 'Legal reasoning and approach to problems', 'course': 'Legal Methods', 'date': 'June 26, 2025 21:00:00', 'yt': 'YT006'},
    {'topic': 'Nigerian People and culture, chapters 1 to 3', 'course': 'General Studies', 'date': 'June 27, 2025 19:00:00', 'yt': 'YT007'},
    {'topic': 'Nollywood/Hollywood', 'course': 'General Knowledge', 'date': 'June 27, 2025 21:30:00', 'yt': 'YT007'},
    {'topic': 'Differentiation', 'course': 'Mathematics', 'date': 'June 28, 2025 21:00:00', 'yt': 'YT008'},
    {'topic': 'Viruses, Bacteria, Algae, Lichen and Fungi', 'course': 'Biology', 'date': 'June 29, 2025 21:00:00', 'yt': 'YT009'},
    {'topic': 'Isomerism, determination of organic compounds, organic reactions', 'course': 'Chemistry', 'date': 'June 30, 2025 21:00:00', 'yt': 'YT010'},
    {'topic': 'Prospective in the nobility of teaching as a profession', 'course': 'Education', 'date': 'July 01, 2025 21:00:00', 'yt': 'YT011'},
    {'topic': 'Physics textbook chapters 4 to 6', 'course': 'Physics', 'date': 'July 02, 2025 21:00:00', 'yt': 'YT012'},
    {'topic': 'Fact finding and dispute resolution', 'course': 'Legal Methods', 'date': 'July 03, 2025 21:00:00', 'yt': 'YT013'},
    {'topic': 'Nigerian People and culture, chapters 4 to 6', 'course': 'General Studies', 'date': 'July 04, 2025 19:00:00', 'yt': 'YT007'},
    {'topic': 'African Music', 'course': 'General Knowledge', 'date': 'July 04, 2025 21:30:00', 'yt': 'YT014'},
    {'topic': 'Application of Differentiation', 'course': 'Mathematics', 'date': 'July 05, 2025 21:00:00', 'yt': 'YT015'},
    {'topic': 'Vertebrates', 'course': 'Biology', 'date': 'July 06, 2025 21:00:00', 'yt': 'YT016'},
    {'topic': 'Alkanes and Alkenes', 'course': 'Chemistry', 'date': 'July 07, 2025 21:00:00', 'yt': 'YT017'},
    {'topic': 'History of Education in Nigeria', 'course': 'Education', 'date': 'July 08, 2025 21:00:00', 'yt': 'YT018'},
    {'topic': 'Physics textbook chapters 7 to 9', 'course': 'Physics', 'date': 'July 09, 2025 21:00:00', 'yt': 'YT019'},
    {'topic': 'Legal reasoning in judicial process', 'course': 'Legal Methods', 'date': 'July 10, 2025 21:00:00', 'yt': 'YT020'},
    {'topic': 'Nigerian People and culture, chapters 7 to 9', 'course': 'General Studies', 'date': 'July 11, 2025 19:00:00', 'yt': 'YT007'},
    {'topic': 'Worldwide Celebrities', 'course': 'General Knowledge', 'date': 'July 11, 2025 21:30:00', 'yt': 'YT021'},
    {'topic': 'Integration', 'course': 'Mathematics', 'date': 'July 12, 2025 21:00:00', 'yt': 'YT022'},
    {'topic': 'Nutrition, respiration, excretion and reproduction in plants and animals', 'course': 'Biology', 'date': 'July 13, 2025 21:00:00', 'yt': 'YT023'},
    {'topic': 'Alkynes, Aromatic hydrocarbons', 'course': 'Chemistry', 'date': 'July 14, 2025 21:00:00', 'yt': 'YT024'},
    {'topic': 'Stages of Child and Adolescent development', 'course': 'Education', 'date': 'July 15, 2025 21:00:00', 'yt': 'YT025'},
    {'topic': 'Physics textbook chapters 10 to 12', 'course': 'Physics', 'date': 'July 16, 2025 21:00:00', 'yt': 'YT026'},
    {'topic': 'Legal reasoning in legislation', 'course': 'Legal Methods', 'date': 'July 17, 2025 21:00:00', 'yt': 'YT027'},
    {'topic': 'Nigerian People and culture, chapters 10 to 12', 'course': 'General Studies', 'date': 'July 18, 2025 19:00:00', 'yt': 'YT007'},
    {'topic': 'Sports', 'course': 'General Knowledge', 'date': 'July 18, 2025 21:30:00', 'yt': 'YT028'},
    {'topic': 'Application of Integration', 'course': 'Mathematics', 'date': 'July 19, 2025 21:00:00', 'yt': 'YT029'},
    {'topic': 'Protozoa, Cnidaria and Platyhelminthes', 'course': 'Biology', 'date': 'July 20, 2025 21:00:00', 'yt': 'YT030'},
    {'topic': 'Carbonyl compounds, group 1 to group 7 elements', 'course': 'Chemistry', 'date': 'July 21, 2025 21:00:00', 'yt': 'YT031'},
    {'topic': 'Human Learning from behaviourists, cognitive and sociocultural perspectives', 'course': 'Education', 'date': 'July 22, 2025 21:00:00', 'yt': 'YT032'},
    {'topic': 'Physics textbook chapters 13 to 15', 'course': 'Physics', 'date': 'July 23, 2025 21:00:00', 'yt': 'YT033'},
    {'topic': 'Sources of law in nigeria', 'course': 'Legal Methods', 'date': 'July 24, 2025 21:00:00', 'yt': 'YT034'},
    {'topic': 'Nigerian People and culture, chapters 13 to 15', 'course': 'General Studies', 'date': 'July 25, 2025 19:00:00', 'yt': 'YT007'},
    {'topic': 'Tech', 'course': 'General Knowledge', 'date': 'July 25, 2025 21:30:00', 'yt': 'YT036'},
    {'course': 'This is the last quiz', 'topic': '', 'date': 'July 26, 2025 21:00:00', 'yt': 'hij345'},
]


@csrf_exempt
def get_paystack_key(request):
    secret_key = settings.PAYSTACK_SECRET_KEY 
    return JsonResponse({'secret_key': secret_key})

current = 22
on = False

try:
    topic = topics[current]
except:
    topic = ''
c = {'Mathematics': "MTH",'Physics': "PHY",'General Studies': "GST", 'Legal Methods': 'JIL',
            'Chemistry':"CHM",'Biology': "BIO", 'Education': "EDU", 'General Knowledge': 'GK'}


def calcpay(amount):
    if amount <= 2500:
        return round(amount/0.975, 0)
    else:
        return round((amount+100)/0.975, 0)

@csrf_exempt
@login_required(login_url='login')
def initiate_payment(request):
    email = request.GET.get('email')
    amount = request.GET.get('amount')
    reason = request.GET.get('reason')

    if not all([email, amount, reason]):
        return redirect('home')  # or return error message

    # Generate unique reference
    reference = str(uuid.uuid4()).replace('-', '')[:16]

    # Save to DB
    Payment.objects.create(email=email, reference=reference, amount=int(amount), reason=reason)


    # Redirect to Streamlit with params
    streamlit_url = f"https://calixguru.github.io/payment/?email={email}&amount={amount}&reason={reason}&ref={reference}"
    return redirect(streamlit_url)

def payment_cancelled(request):
    messages.success(request, 'Payment cancelled')
    return redirect('home')  # Or custom page


def split_room_payment(input_str):
    match = re.match(r'([a-zA-Z_]+)(\d+)', input_str)
    if match:
        text_part = match.group(1)
        return f"{text_part}"
    else:
        return "Invalid input format"
def split_room_payment2(input_str):
    match = re.match(r'([a-zA-Z_]+)(\d+)', input_str)
    if match:
        number_part = int(match.group(2))
        return f"{number_part}"
    else:
        return "Invalid input format"
    
def extract(text):
    number, _ = text.split('_', 1)
    return number

def check_subs(text):
    if text.endswith('_subs'):
        return 'Yes'
    else:
        return 'No'

@login_required(login_url='login')
def process_payment(request):
    # for i in Pinbin2.objects.all():
    #     i.delete()
    # for i in Payment.objects.all():
    #     i.delete()
    plans = [
        {"amount": calcpay(500), "action": "weekly", "duration": 8},
        {"amount": calcpay(1500), "action": "monthly", "duration": 32},
        # {"amount": calcpay(1000), "action": 1},
        # {"amount": calcpay(2600), "action": 5},
        # {"amount": calcpay(3000), "action": 5},
        # {"amount": calcpay(5000), "action": 10},
        # {"amount": calcpay(7000), "action": 15},
    ]
    plans2 = [
        # {"amount": calcpay(500), "action": "weekly", "duration": 8},
        # {"amount": calcpay(1500), "action": "monthly", "duration": 32},
        {"amount": 1200, "action": 1},
        {"amount": 3500, "action": 5},
        {"amount": 4000, "action": 5},
        # {"amount": calcpay(5000), "action": 10},
        # {"amount": calcpay(7000), "action": 15},
    ]
    email = request.GET.get('email')
    amount = int(request.GET.get('amount'))
    reason = request.GET.get('reason')
    reference = request.GET.get('ref')
    pref = request.GET.get('pref')

    user = User.objects.get(email=email)

    # Payment.objects.create(email=email, reference=reference, amount=int(amount), reason=reason)
    if not reference:
        messages.error(request, "Payment failed. No reference found.")
        return redirect('home')
    try:
        payment = Payment.objects.get(reference=reference)
    except:
        messages.error(request, "Such payment does not exist")
        return redirect('home')  # Or custom page
    if payment.amount != int(amount):
        messages.error(request, 'Unmatched Payment')
        return redirect('home')
    if payment.paid == 2:
        messages.error(request, 'This payment was already verified and processed!')
        return redirect('home')

    # Verify Paystack Payment
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{pref}"
    response = requests.get(url, headers=headers).json()

    headers2 = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY2}",
    }
    url2 = f"https://api.paystack.co/transaction/verify/{pref}"
    response2 = requests.get(url2, headers=headers2).json()

    # try:
    if response2['data']['status'] != 'success' and payment.reason == 'competition_payment':
        pin = f'{random.randint(1111111,9999999)}{request.user.id}'
        request.session['payment_pin'] = str(pin)
        # Send email with a beautiful template
        subject = "Your Opal Rumble PIN"
        message = render_to_string("email/opal_template.html", {
            "user": user,
            "pin": pin
        })
        send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [request.user.email], html_message=message)
        messages.success(request, f"You have successfully paid for Opal Rumble pin")
        payment.paid = 2
        payment.save()
        Pays.objects.create(
                user=user,
                title = 'Competition',
                trace = f'{request.user.email} competition',
                amount= 3000,
                )
        return redirect('register_courses')
    
    
    elif response['data']['status'] == 'success' and split_room_payment(payment.reason) == 'downloads':
        idy = split_room_payment2(payment.reason)
        room = Cbtroom.objects.get(id=idy)
        request.user.has_downloaded = request.user.has_downloaded + 1
        room.total.append({'user': request.user.id, 'amount': room.downloads-500, 'reason': 'downloads'})
        room.pending = room.pending + (room.downloads-500)
        request.user.save()
        room.save()
        # Send email with a beautiful template
        subject = f"{room.name} Downloads"
        message = render_to_string("email/room_template.html", {
            "user": room.host,
            "message": f"{user.firstname} {user.lastname} just paid for downloads in your CBT room on Calixguru"
        })
        send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [room.host.email], html_message=message)
        messages.success(request, f"Payment for downloads from {room.name} was successful")
        Pays.objects.create(
                user=user,
                title = 'Room Online downloads',
                trace = f"{room.host.firstname}'s {room.name}-{room.id} download by {request.user.email}",
                amount= 500,
                )
        return redirect('cbtroom', room.id)
    elif response['data']['status'] == 'success' and check_subs(payment.reason) == 'Yes':
        # action = next((item['action'] for item in plans if item['amount'] == amount), None)
        # duration = next((item['duration'] for item in plans if item['amount'] == amount), None)
        # if isinstance(action, int):
        amt = int(extract(reason))
        action = next((item['action'] for item in plans2 if item['amount'] == amt), None)
        user.has_downloaded = user.has_downloaded+action
        user.save()
        messages.success(request, f"Payment for {action} downloads was successful")
        payment.paid = 2
        payment.save()
        Pays.objects.create(
                user=user,
                title = 'Online downloads',
                trace = f'{request.user.email} downloads',
                amount= 500*int(action),
                )
        return redirect('home')
        # else:
        #     values = Pins.objects.create(pin=request.user.id, name=request.user,
        #                             duration=action)
        #     values.save()
        #     values2 = Pinbin.objects.create(name=request.user, pin=request.user.id)
        #     values2.save()
        #     messages.success(request, f"Payment for {action} subscription was successful")
        #     payment.paid = 2
        #     payment.save()
        #     return redirect('home')
    elif response['data']['status'] == 'success' and split_room_payment(payment.reason) == split_room_payment(reason):
        user = User.objects.get(email=request.user.email)
        idy = split_room_payment2(reason)
        room = Cbtroom.objects.get(id=idy)
        room.allowed.append(request.user.email)
        room.total.append({'user': request.user.id, 'amount': room.subscription-500, 'reason': 'subscription'})
        room.pending = room.pending + (room.subscription-500)
        room.save()
        # Send email with a beautiful template
        subject = f"{room.name} Subscription"
        message = render_to_string("email/room_template.html", {
            "user": room.host,
            "message": f"{user.firstname} {user.lastname} just subscribed to your CBT room on Calixguru"
        })
        send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [room.host.email], html_message=message)
        messages.success(request, f"Subscription for {room.name} was successful")
        Pays.objects.create(
                user= user,
                title = 'Online Room Subscription',
                trace = f"{room.host.firstname}'s {room.name}-{room.id} subscription by {request.user.email}",
                amount = 500,
                )
        return redirect('cbtroom', room.id)
    else:
        messages.error(request, f"{payment.amount} Payment NOT verified")
        return redirect('home')
    # except:
    #     messages.error(request, f"Something went wrong")
    #     return redirect('home')

@login_required(login_url='login')
def register_courses(request):
    
    try:
        League.objects.get(user=request.user)
        messages.success(request, 'You have already joined the rumble!')
        return redirect('competition')
    except:
        courses = ["MTH", "PHY", "CHM", "BIO", "EDU", "JIL"]
        courses_name = ['GK (General Knowledge)', 'GST (General Studies)', 'MTH (Mathematics)', 'PHY (Physics)', 'CHM (Chemistry)', 'BIO (Biology)', 'EDU (Education)', 'JIL (Legal Methods)']
        combo = []
        levels = ['100', '200','300', '400', '500', '600']
        compulsory = []#["GK", "GST"]
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                courses = []#data.get("courses", [])
                code = int(data.get("pin"))
                department = data.get("department")
                institution = data.get("institution")
                level = data.get("level")
                phone = data.get("phone")
                
                if not code or not department:
                    return JsonResponse({"message": "PIN and Department are required!"}, status=400)

                # if len(courses) < 1 or len(courses) > 1:
                #     return JsonResponse({"message": "Select only 1 course."}, status=400)


                # Save to database (assuming a Registration model)
                # Registration.objects.create(courses=courses, pin=pin, department=department)

                pin_session = request.session.get('payment_pin')
                if code in pins.pins or (pin_session and code == int(pin_session)):
                    League.objects.create(
                        user=request.user,
                        pin = code,
                        courses = [],
                        department = department,
                        institution = institution,
                        level = level,
                        phone = phone,
                        scores = [])
                    pin = code
                    # Send email with a beautiful template
                    subject = "Your Opal Rumble PIN"
                    message = render_to_string("email/opal_template.html", {
                        "user": request.user,
                        "pin": code
                    })
                    send_mail(subject, "", settings.DEFAULT_FROM_EMAIL, [request.user.email], html_message=message)
                    request.session.pop('payment_pin', None)
                    return JsonResponse({"message": f"Registration successful!"})
                else:
                    return JsonResponse({"message": f"Invalid Pin"})

            except json.JSONDecodeError:
                return JsonResponse({"message": "Invalid data"}, status=400)

        context = {'courses': courses, 'departments':pins.departments, 'cn':courses_name,
                   'payment_pin': request.session.get('payment_pin', None), 'comp': compulsory, 'levels': levels}
        return render(request, 'league/register.html', context)

@login_required(login_url='login')
def competition(request):
    # for i in League.objects.all():
    #     i.delete()
    all = []
    for i in League.objects.all():
        all.append(i.user.email)
    # for i in League.objects.all():
    #     if i.user.email == 'calixotu@gmail.com':
    #         i.courses = ["MTH", "PHY", "CHM", "BIO", "EDU", "JIL", "GST", "GK"]
    #         i.save()
    # di = User.objects.get(email='uduakmojima@gmail.com')
    # person = League.objects.get(user=di)
    # person.delete()
    cos= "General Studies"
    top = "Nigerian People and culture, chapters 13 to 15"
    

    # chapter = questions.chapter13+questions.chapter14+questions.chapter15

    # qs = random.sample(chapter, min(45, len(chapter)))
    # for i in qs:
    #     Questions.objects.create(course = cos,
    #     topic = top,
    #     pre = i['question'],
    #     eqn = '',
    #     options = [
    #         i['opt1'],
    #         i['opt2'],
    #         i['opt3'],
    #         i['opt4']
    #     ],
    #     correct = i['correct'],
    #     )


    allq = Questions.objects.filter(topic='Nigerian People and culture, chapters 13 to 15')
    try:
        owner = League.objects.get(user=request.user)
        pin = owner.pin
        # if len(owner.courses) != 3:
        #     messages.error(request, 'Please edit your courses to 3')
        #     return redirect('all_con')
        # else:
        #     pass
        code_to_course = {v: k for k, v in c.items()}
        def filter_topics_by_codes(input_codes):
            selected_courses = {code_to_course[code] for code in input_codes if code in code_to_course}
            return [entry for entry in topics if entry.get('course') in selected_courses]

        # Example usage
        input_codes = owner.courses
        filtered = filter_topics_by_codes(input_codes)
    except:
        owner = []
        pin = ''
        filtered = []
    time = Questions.objects.filter(topic = topic['topic'])
    if topic['course'] == 'Mathematics':
        duration = round(60 * int(len(time)) / 60)
    elif topic['course'] == 'Physics':
        duration = round(45 * int(len(time)) / 60)
    else:
        duration = round(20 * int(len(time)) / 60)
    # Group and sum scores by ID
    try:
        dat = []
        for i in League.objects.all():
            for v in i.scores:
                dat.append(v)

        # Group scores by 'lid' and store the latest 'lid' for each ID
        grouped_scores = defaultdict(lambda: {'sum_scores': 0, 'lid': None})

        for entry in dat:
            user_id = entry['id']
            grouped_scores[user_id]['sum_scores'] += entry['main_score']
            grouped_scores[user_id]['lid'] = entry.get('lid', None)  # store lid

        # Create sorted list with id, sum_scores, and lid
        ranked_scores = sorted(
            [
                {
                    'id': k,
                    'sum_scores': v['sum_scores'],
                    'lid': v['lid']
                }
                for k, v in grouped_scores.items()
            ],
            key=lambda x: x['sum_scores'],
            reverse=True
        )



    except:
        dept = []
        dat = []
        ranked_scores = []
    try:
        board = []
        take = []
        taken =  TakenT.objects.filter(user=request.user)
        for i in taken:
            take.append(i.topic)
        if topic['topic'] in take:
            cbt = 'no'
        else:
            cbt = 'yes'
        for i in League.objects.all():
            board.append({'id':i.user.id,'name':f'{i.user.firstname} {i.user.lastname}',
                        'dept':i.department,'scores':i.scores,'courses':i.courses})

        context = {
            'pin': pin,
            'take': take,
            'topic': topics[current+1],
            'topic2': topics[current],
            'all': all,
            'rank': ranked_scores,
            'duration': duration,
            'allq': allq,
            'tt': filtered
        }
        if cbt == 'yes' and c[topic['course']] in owner.courses and on == True:
            return render(request, 'league/quiz.html', context)
        else:
            return render(request, 'league/competition.html', context)
    except:
        context = {
            'pin': pin,
            'topic': topics[current+1],
            'topic2': topics[current],
            'all': all,
            'rank': ranked_scores,
            'duration': duration,
            'owner': owner,
            'allq': allq,
            'tt': filtered
        }
        return render(request, 'league/competition.html', context)

quiz_sessions = {}


def verify_pin(request):
    """Verify the user-entered PIN before starting the quiz."""
    pin = int(request.GET.get("pin"))
    try:
        owner = League.objects.get(user=request.user)
        if pin == int(owner.pin):
            user_id = request.session.session_key or request.session.create()

            # Set the start time if not already set
            if user_id not in quiz_sessions:
                quiz_sessions[user_id] = {"start_time": request.session.get("quiz_start_time")}
                request.session["quiz_start_time"] = request.session.get("quiz_start_time") or request.session.get("quiz_start_time")

            return JsonResponse({"valid": True})

        return JsonResponse({"valid": False})
    except:
        return JsonResponse({"valid": False})


def get_random_questions(request):
    aoc = topic['topic']
    q = []
    for i in Questions.objects.filter(topic=aoc):
        q.append({'id' :i.id,
                  'pre' :i.pre,
                  'eqn' :i.eqn,
                  'options' :i.options,
                  'correct' :i.correct,
        })
    selected_questions = q  # Pick 5 random questions
    return JsonResponse({"questions": selected_questions})

def submit_quiz(request):
    """Receives score as an integer and processes it."""
    if request.method == "POST":

        questions = request.POST.get("questions")
        q = []
        for i in eval(questions):
            q.append(i)
        user_id = request.POST.get("user_id")
        answers = request.POST.get("answers")
        try:
            score = float(request.POST.get("score"))
        except:
            score = 0.00
        punishment = int(request.POST.get("punishment"))
        percent = 5
        main_score = score - (((percent*punishment)/100)*(score))
        owner = League.objects.get(user=request.user)
        owner.scores.append({'course':topic['course'], 'topic':topic['topic'],
                             'id': request.user.id, 'lid': owner.id,
                             'q': questions, 'ans': answers, 'score': score,
                            'punish': punishment, 'main_score': main_score})
        owner.save()
        TakenT.objects.create(user=request.user, topic=topic['topic'])
        messages.success(request, "Your score have been submitted")

    return redirect ('competition')

@login_required(login_url='login')
def show_history(request, user_id):
    origin = User.objects.get(id=user_id)
    owner = League.objects.get(user=origin)
    if request.method == 'POST':
        my_list = owner.scores
        position = int(request.POST.get('position'))
        index = position - 1
        if 0 <= index < len(my_list):
            my_list.pop(index)
            owner.save()
            messages.success(request, "Record deleted successfully")
        else:
            messages.error(request, "Invalid Position")

        print("Updated list:", my_list)
    context = {'owner': owner, 'on': on, 'topic': topic}
    return render(request, 'league/show_history.html', context)

@login_required  # Optional: require login
def get_topic_rankings(request):
    topic = request.GET.get('topic')

    if not topic:
        return JsonResponse({'error': 'No topic specified'}, status=400)

    scores = []
    for i in League.objects.all():
        scores.append(i.scores)

    def group_by_topic(data, selected_topic):
        result = []

        # Flatten the nested list and filter by topic
        for user_records in data:
            for record in user_records:
                if record['topic'] == selected_topic:
                    result.append({
                        'topic': record['topic'],
                        'firstname': User.objects.get(id=int(record['id'])).firstname,
                        'lastname': User.objects.get(id=int(record['id'])).lastname,
                        'department': League.objects.get(id=int(record['lid'])).department,
                        'main_score': record['main_score'],
                        'score': record['score'],
                        'punish': record['punish'],
                        'lid': record['lid'],
                    })

        # Sort by main_score in descending order
        sorted_result = sorted(result, key=lambda x: x['main_score'], reverse=True)

        return sorted_result


    results = group_by_topic(scores, topic)

    return JsonResponse({'results': results, 'scores': scores})


@login_required(login_url='login')
def leagueans(request):
    idy = int(request.GET.get('owner'))
    index = int(request.GET.get('index')) - 1
    user = User.objects.get(id=idy)
    owner = League.objects.get(user=user)
    data = owner.scores
    # Convert JSON fields to dictionaries


    q_data = eval(data[index]['q'])
    ans_data = eval(data[index]['ans'])

    merged_list = []

    # Get keys from q_data and match them with ans_data in order
    for (q_id, correct), (_, choice) in zip(q_data.items(), ans_data.items()):
        merged_list.append({'id': int(q_id), 'correct': correct, 'choice': choice})

    main_datas = []
    for i in merged_list:
        main_datas.append(
            {'id': Questions.objects.get(id=i['id']).id,
             'pre': Questions.objects.get(id=i['id']).pre,
             'eqn': Questions.objects.get(id=i['id']).eqn,
             'options': Questions.objects.get(id=i['id']).options,
             'correct': i['correct'],
             'choice': i['choice']
             },
        )

    context = {'owner': user,"data": data,
               'merged_data': merged_list, 'main_datas': main_datas}
    return render(request, 'league/leagueans.html', context)




def q_list(request):
    posts = Questions.objects.all()
    context = {'posts': posts}
    return render(request, 'questions/q_list.html', context)

def q_detail(request, pk):
    try:
        post = Questions.objects.get(id=pk)
        context = {'post': post}
        return render(request, 'questions/q_detail.html', context)
    except:
        messages.error(request, 'Unable to fetch that question')
        return redirect(request.META.get('HTTP_REFERER', '/'))

def q_create(request):
    categories = ['Mathematics','Physics', 'General Studies', 'Legal Methods','Chemistry', 'Biology', 'Education', 'General Knowledge']
    if request.method == 'POST':
        pre = eval(request.POST.get('q'))
        try:
            Questions.objects.create(course = request.POST.get('course'),
            topic = request.POST.get('topic'),
            pre = pre['question'],
            eqn = pre['eqn'],
            options = [
                pre['opt1'],
                pre['opt2'],
                pre['opt3'],
                pre['opt4']
            ],
            correct = pre['correct'],
            )
            messages.success(request, 'Question created successfully')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except:
            messages.error(request, 'Question failed to create')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'questions/q_form.html', {'categories': categories})

def q_update(request, pk):
    post = get_object_or_404(Questions, pk=pk)
    if request.method == 'POST':
        qq = eval(request.POST.get('q'))
        try:
            q = eval(qq)
            post.pre = q['question']
            post.eqn = q['eqn']
            post.options = [
                q['opt1'],
                q['opt2'],
                q['opt3'],
                q['opt4']
            ]
            post.correct = int(q['correct'])
            post.save()
            messages.success(request, 'Question modified successfully')
            return redirect('q_list')
        except:
            messages.error(request, 'Something went wrong')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'questions/q_form.html', {'post': post})

def q_delete(request, pk):
    post =Questions.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Question successfully deleted')
        return redirect('q_list')
    return render(request, 'questions/q_confirm_delete.html', {'post': post})


def all_con(request):
    courses = ["MTH", "PHY", "CHM", "BIO", "EDU", "JIL"]
    all = League.objects.all()
    taken = len(TakenT.objects.all())
    if request.method == 'POST':
        course = request.POST.get('courses')
        if course != None:
            contestant = League.objects.get(user=request.user)
            contestant.courses = [course, 'GK', 'GST']
            contestant.save()
            messages.success(request, 'Courses successfully modified')
            return redirect('all_con')
        else:
            messages.error(request, 'You must select a valid course')
            return redirect('all_con')
    context = {'all': all, 'taken': taken, 'courses': courses}
    return render(request, 'league/all.html', context)

