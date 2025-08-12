from geopy.distance import great_circle
from core.models import *
from customers.models import *
from partners.models import *
from telebot import types
from webhooks.engine.bot import BotManager
import requests,time

def is_new_customer(user_id,cafe):
    customer = Customer.objects.filter(telegram_id=user_id,cafe=cafe)
    if customer.exists():return customer.first()
    else:return False

def list_of_cities():
    return [str(i) for i in City.objects.all()]

def city_by_name(name):
    for i in City.objects.all():
        if str(i) == name:
            return i
def get_customer_department(customer:Customer):
    return Cart.objects.filter(customer=customer).first().product.category.department

def check_location_distance(location:types.Location,customer:Customer):
    department = get_customer_department(customer)
    distance = great_circle((location.latitude,location.longitude),(department.location_lat,department.location_long))
    if distance.km <= department.max_distance:
        return round(distance.km,2)
    return False

def Send_Notification(message,user,bot,customers):
    note_message = message
    engine_bot = BotManager.get_bot(user.cafe.bot_token)
    _html_text = None
    _photo = None
    _caption = None
    _video = None
    print(customers)
    if note_message.text:
        _html_text = note_message.html_text
    elif note_message.photo:
        _photo = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{bot.get_file(note_message.photo[-1].file_id).file_path}").content
        _caption=note_message.html_caption if note_message.html_caption else ""
    elif note_message.video:
        _video = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{bot.get_file(note_message.video.file_id).file_path}").content
        _caption=note_message.html_caption if note_message.html_caption else ""
    try:
        if note_message.text:
            for i in customers:
                engine_bot.bot.send_message(
                    chat_id=i.telegram_id,
                    text=_html_text,
                )
        elif note_message.photo:
            for i in customers:
                engine_bot.bot.send_photo(
                    chat_id=i.telegram_id,
                    photo=_photo,
                    caption=_caption
                )
        elif note_message.video:
            for i in customers:
                engine_bot.bot.send_video(
                    chat_id=i.telegram_id,
                    video=_video,
                    caption=_caption
                )
    except:pass
    return True