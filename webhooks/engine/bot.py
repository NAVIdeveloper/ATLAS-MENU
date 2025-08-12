from webhooks.engine.manager import BotManager
from webhooks.engine import helper,markup,render
from webhooks.engine import configuration as config
from webhooks.master_bot import bot as bot_staff
from core.models import *
from customers.models import *
from partners.models import *
from telebot import TeleBot, types
import telebot

def initialize():
    if config.ENABLE_WEBHOOK:
        for i in Partner.objects.all():
            BotManager.add_bot(i.bot_token,BotEngine(i.bot_token))

class BotEngine:
    def __init__(self,bot_token):
        self.token = bot_token
        self.bot = TeleBot(token=bot_token,threaded=False,parse_mode='HTML')
        self.bot.remove_webhook()
        self.bot.set_webhook(f"{config.URL_WEBHOOK_ENGINES}/{self.token}/")
        self.cafe = Partner.objects.get(bot_token=self.token)
        self._setup_handlers()
        # BotManager.add_bot(bot_token,self)
    
    def command_start(self,message:types.Message):
        user_id = message.from_user.id
        customer = helper.is_new_customer(user_id,self.cafe)
        if customer:
            self.lunch_main_menu(message,customer)
        else:
            self.bot.send_message(user_id,helper.Text.engine_ask_language,reply_markup=markup.Engine_Language_Choose())

## to send main command buttons when user clicked /start or after registered  
    def lunch_main_menu(self,message,customer):
        self.bot.send_message(
            message.from_user.id,
            render.LanguageRender(customer.language.label_main_menu,customer),
            reply_markup=markup.Engine_Main_Menu(customer)
        )

## only accept contact message to register
    def command_contact(self,message:types.Message):
        if message.from_user.id == message.contact.user_id:
            customer = Customer.objects.get(telegram_id=message.from_user.id)
            customer.phone = message.contact.phone_number
            customer.save()
            self.bot.send_message(
                message.from_user.id,
                render.LanguageRender(customer.language.success_phone,customer),
                reply_markup=markup.REMOVE
            )
            self.lunch_main_menu(message,customer)
        else:
            try:self.bot.delete_message(message.from_user.id,message.message_id)
            except:pass

## function to check callback handlers
    def handle_callback(self,call:types.CallbackQuery):
        user_id = call.from_user.id
        splited = call.data.split('-')
        try:
            if 'language' in splited:
                customer = helper.is_new_customer(user_id,self.cafe)
                language = Language.objects.get(id=splited[1])
                self.bot.send_message(user_id,language.info)
                try:
                    self.bot.delete_message(user_id,call.message.message_id)
                    self.bot.delete_message(user_id,call.message.message_id-1)
                except:
                    pass
                if not customer:
                    customer = Customer.objects.create(telegram_id=user_id,cafe=self.cafe,fullname=call.from_user.first_name)
                    self.bot.send_message(
                        user_id,
                        render.LanguageRender(language.ask_phone,customer),
                        reply_markup=markup.Engine_Ask_Phone(language)
                    )
                customer.language = language
                customer.save()
            elif 'city' in splited:
                customer = Customer.objects.get(telegram_id=user_id)
                city = City.objects.get(id=splited[1])
                self.bot.edit_message_text(
                    render.LanguageRender(customer.language.ask_department,customer),
                    chat_id=user_id,message_id=call.message.message_id,
                    reply_markup=markup.Engine_Departments(customer,city)
                )
            elif 'department' in splited:
                customer = Customer.objects.get(telegram_id=user_id)
                department = Branch.objects.get(id=splited[1])
                carts = Cart.objects.filter(customer=customer)
                if department.is_open:
                    if carts.exists():
                        if carts.first().product.category.department.id == department.id:
                            self.bot.edit_message_text(
                                render.LanguageRender(
                                    customer.language.label_open,
                                    customer=customer,department=department
                                ),
                                chat_id=user_id,message_id=call.message.message_id,
                                reply_markup=markup.Engine_Detail_Department(customer,department)
                            )
                        else:
                            self.bot.edit_message_text(
                                render.LanguageRender(
                                    customer.language.error_many_department,customer=customer,
                                    department=carts.first().product.category.department
                                ),
                                chat_id=user_id,message_id=call.message.message_id,reply_markup=None,
                            
                            )
                    else:
                        self.bot.edit_message_text(
                            render.LanguageRender(customer.language.label_open,customer,department=department),
                            chat_id=user_id,message_id=call.message.message_id,
                            reply_markup=markup.Engine_Detail_Department(customer,department)
                        )
                else:
                    self.bot.edit_message_text(
                        render.LanguageRender(customer.language.label_close,customer,department=department),
                        chat_id=user_id,message_id=call.message.message_id,
                        reply_markup=None
                    )
            elif 'clear' in splited:
                try:
                    customer = Customer.objects.get(telegram_id=user_id)
                    Cart.objects.filter(customer=customer).delete()
                    self.bot.edit_message_text(
                        render.LanguageRender(customer.language.label_cart_cleared,customer),
                        chat_id=customer.telegram_id,message_id=call.message.message_id,
                        reply_markup=None,
                    )
                except:pass
            elif 'comfirm-cart' == call.data:
                customer = Customer.objects.get(telegram_id=user_id)
                self.bot.edit_message_text(
                    render.LanguageRender(customer.language.ask_service_type,customer),
                    user_id,call.message.message_id,reply_markup=markup.Engine_Ask_Service(customer)
                )
            elif 'service' in splited:
                customer = Customer.objects.get(telegram_id=user_id)
                service_type = ServiceType.objects.get(id=splited[1])
                try:self.bot.delete_message(chat_id=user_id,message_id=call.message.message_id)
                except:pass
                if service_type.ask_location:
                    self.bot.send_message(
                        chat_id=user_id,reply_markup=markup.Engine_Ask_Location(customer),
                        text=render.LanguageRender(customer.language.ask_delivery_location,customer)
                    )
                else:
                    self.bot.send_message(
                        chat_id=user_id,reply_markup=markup.Engine_Ask_Time(customer),
                        text=render.LanguageRender(customer.language.ask_takeaway_time,customer)
                    )
                self.bot.register_next_step_handler(call.message,self.step_ordering_location_and_time,service_type=service_type)
            elif 'back' in splited:
                customer = Customer.objects.get(telegram_id=user_id)
                self.bot.edit_message_text(
                    render.LanguageRender(customer.language.ask_city,customer),
                    chat_id=user_id,message_id=call.message.message_id,
                    reply_markup=markup.Engine_Cities(customer)
                )
        except Exception as e:
            print(e)
    def step_ordering_location_and_time(self,message,service_type):
        customer = Customer.objects.get(telegram_id=message.from_user.id)
        if service_type.ask_location:
            dist = helper.check_location_distance(message.location,customer)
            if dist:
                self.bot.reply_to(
                    message,
                    render.LanguageRender(customer.language.info_distance,customer=customer,distance=dist),
                )
                self.bot.send_message(
                    customer.telegram_id,reply_markup=markup.Engine_Ask_Comment(customer),
                    text=render.LanguageRender(customer.language.ask_comment,customer)
                )
                self.bot.register_next_step_handler(message,self.step_ordering_comment,location=message.location)
            else:
                self.bot.send_message(
                    customer.telegram_id,
                    render.LanguageRender(customer.language.error_distance,customer),
                )
                self.lunch_main_menu(message,customer)
        else:
            self.bot.send_message(
                customer.telegram_id,reply_markup=markup.Engine_Ask_Comment(customer),
                text=render.LanguageRender(customer.language.ask_comment,customer)
            )
            self.bot.register_next_step_handler(message,self.step_ordering_comment,datetime=message.text)
    
    def step_ordering_comment(self,message,location=None,datetime=None):
        customer = Customer.objects.get(telegram_id=message.from_user.id)
        self.bot.send_message(
            customer.telegram_id,
            render.LanguageRender(
                customer.language.ask_inform,customer,
                cart=Cart.objects.filter(customer=customer),
                department=helper.get_customer_department(customer),comment=message.text,
            ),reply_markup=markup.Engine_Ask_Inform(customer)
        )
        self.bot.register_next_step_handler(
            message,self.step_ordering_inform,
            location=location,datetime=datetime,comment=message.text
        )

    def step_ordering_inform(self,message,location,datetime,comment):
        customer = Customer.objects.get(telegram_id=message.from_user.id)
        if message.text == customer.language.btn_yes:
            carts = Cart.objects.filter(customer=customer)
            department = helper.get_customer_department(customer)
            order = Order.objects.create(customer=customer,department=department)
            if location:
                order.service_type = ServiceType.objects.get(ask_location=True,language=customer.language)
                order.location_lat = location.latitude
                order.location_long = location.longitude
            else:
                order.service_type = ServiceType.objects.get(ask_location=False,language=customer.language)
                order.takeaway_time = datetime
            order.save()
            total_price = 0
            for c in carts:
                item = OrderItem.objects.create(order=order,product=c.product,quantity=c.quantity)
                total_price+=c.product.price*c.quantity
            order.total_price = total_price
            order.save()
            carts.delete()
            self.bot.send_message(
                customer.telegram_id,reply_markup=markup.Engine_Main_Menu(customer),
                text=render.LanguageRender(customer.language.order_informed,customer,order_id=order.id)
            )
            if location:
                msg_loc = bot_staff.staff.send_location(department.group_id,latitude=location.latitude,longitude=location.longitude)
                bot_staff.staff.send_message(
                    department.group_id,reply_markup=markup.Staff_Accept(order=order),
                    text=render.LanguageRender(
                        customer.language.order_info,customer,department=department,order=order,
                        language=Language.objects.get(main=True),comment=comment
                    ),reply_to_message_id=msg_loc.message_id
                )
                msgg = self.bot.send_message(
                    customer.telegram_id,
                    text=render.LanguageRender(
                        customer.language.order_info,customer,department=department,order=order,comment=comment
                    )
                )
                order.message_id = msgg.message_id
            elif datetime:
                bot_staff.staff.send_message(
                    department.group_id,reply_markup=markup.Staff_Accept(order=order),
                    text=render.LanguageRender(
                        customer.language.order_info_takeaway,customer,department=department,order=order,
                        language=Language.objects.get(main=True),comment=comment,datetime=datetime
                    )
                )
                msgg = self.bot.send_message(
                    customer.telegram_id,
                    text=render.LanguageRender(
                        customer.language.order_info_takeaway,customer,department=department,order=order,comment=comment,datetime=datetime
                    )
                )
                order.message_id = msgg.message_id
            order.save()
        else:
            self.lunch_main_menu(message,customer)
            

    def handle_buttons(self,message):
        customer = Customer.objects.get(telegram_id=message.from_user.id)
        if message.text == customer.language.btn_menu:
            self.action_btn_menu(customer)

        elif message.text == customer.language.btn_cart:
            self.action_btn_cart(customer)

        else:
            try:self.bot.delete_message(message.from_user.id,message.message_id)
            except:pass
    
## starting functions to commit what happens when user send command by keyboard buttons or slash(/) commands
    def action_btn_menu(self,customer):
        self.bot.send_message(
            customer.telegram_id,
            render.LanguageRender(customer.language.ask_city,customer),
            reply_markup=markup.Engine_Cities(customer)
        )
    def action_btn_cart(self,customer):
        cart = Cart.objects.filter(customer=customer)
        if cart.exists():
            self.bot.send_message(
                customer.telegram_id,
                render.LanguageRender(customer.language.cart_info,customer,cart=cart),
                reply_markup=markup.Engine_Clean(customer)
            )
        else:
            self.bot.send_message(
                customer.telegram_id,
                render.LanguageRender(customer.language.empty_cart,customer),
            )

## initilizing message handlers         
    def _setup_handlers(self):
        self.bot.message_handler(commands=['start'])(
            self.command_start
        )
        self.bot.callback_query_handler(func=lambda call: True)(
            self.handle_callback
        )
        self.bot.message_handler(content_types=['contact'])(
            self.command_contact
        )
        self.bot.message_handler(content_types=['text'])(
            self.handle_buttons
        )
        self.bot.message_handler(content_types=['web_app_data'])(
            self.web_app_data
        )
    def web_app_data(self,message):
        print("Hello world")