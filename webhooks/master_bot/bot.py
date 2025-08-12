from webhooks.master_bot import configuration as config
from webhooks.master_bot.decorator import auth_staff,is_staff
from webhooks.master_bot import helper, render,markup
from webhooks.engine.bot import BotManager
from core.models import Language,EngineBotText,MasterBotText
from customers.models import *
from partners.models import *
from telebot import TeleBot,types

def initialize():
    global STAFF_INFO
    if config.ENABLE_WEBHOOK:
        staff.set_webhook(config.WEBHOOK_URL)
        STAFF_INFO = staff.get_me()

staff = TeleBot(config.STAFF_BOT_TOKEN,threaded=False,parse_mode='HTML',disable_web_page_preview=True)
staff.remove_webhook()
STAFF_INFO = None

@staff.message_handler(commands=['start'])
@auth_staff
def Command_Start(message,branch:Branch=None):
    staff.send_message(
        branch.telegram_id,
        render.StaffRender(
            branch.language.master.command_start,branch,map_flag=True
        ),reply_markup=markup.StaffMenu(branch)
    )

# @staff.message_handler(commands=['remove'])
# @auth_staff
# def Command_Remove(message,brach):
#     staff.send_message(
#         brach.telegram_id,render.StaffRender(static_text_admin.staff_remove_comfirm,brach),
#         reply_markup=markup.REMOVE_COMFIRM
#     )

@staff.message_handler(content_types=['text'])
@auth_staff
def handle_staff_menu_commands(message,branch:Branch=None):
    command = message.text
    if command == branch.language.master.btn_setting_group:
        _handle_group_setting(branch)
    # elif command == static_text_admin.btn_setting_service_type:
    #     staff.send_message(
    #         branch.telegram_id,render.StaffRender(static_text_admin.staff_service_type,branch),
    #         reply_markup=markup.Staff_Service_Type(branch)
    #     )
    # elif command == static_text_admin.btn_category:
    #     msg = staff.send_message(
    #         branch.telegram_id,render.StaffRender(static_text_admin.staff_category_command,branch),
    #         reply_markup=markup.Staff_Categories(branch),
    #     )
    #     try:
    #         if branch.message_callback:
    #             staff.delete_message(branch.telegram_id,branch.message_callback)
    #             staff.delete_message(branch.telegram_id,str(int(branch.message_callback)-1))
    #         branch.message_callback = msg.message_id
    #         branch.save()
    #     except:
    #         pass
    # elif command == static_text_admin.btn_notification:
    #     pass
    # elif command == static_text_admin.btn_statistic:
    #     pass
    # else:
    #     pass

def _handle_group_setting(brach:Branch):
    message_text = (
        render.StaffRender(brach.language.master.has_group, brach)
        if brach.group_id else 
        render.StaffRender(brach.language.master.has_no_group, brach)
    )
    staff.send_message(
        brach.telegram_id,
        message_text,
        reply_markup=None if brach.group_id else markup.AddGroup(brach)
    )

@staff.message_handler(content_types=['new_chat_members'])
@auth_staff
def handle_chat_member_add(message,brach:Branch):
    if brach.group_id:
       _handle_group_setting(brach)

    elif STAFF_INFO.id in [new_member.id for new_member in message.new_chat_members]:
        brach.group_id=message.chat.id
        brach.save()
        staff.send_message(
            message.chat.id,
            render.StaffRender(brach.language.master.group_confirmed,brach)
        )
        staff.send_message(
            brach.telegram_id,
            render.StaffRender(brach.language.master.new_group_confirmed,brach)
        )

# @staff.message_handler(content_types=['left_chat_member'])
# def handle_chat_member_leave(message):
#     left_member = message.left_chat_member
#     if left_member.id == STAFF_INFO.id:
#         group_id = message.chat.id
#         try:
#             brach = brach.objects.get(group_id=group_id)
#             brach.group_id = None
#             brach.save()
#             staff.send_message(
#                 brach.telegram_id,
#                 render.StaffRender(static_text_admin.staff_remove_success,brach)
#             )
#             print(f"Bot was removed from group {group_id}. brach updated.")
#         except:pass

# @staff.callback_query_handler(func=lambda call: True)
# def handle_callback(call):
#     brach = is_staff(call.from_user.id).first()
#     if call.data == static_text_admin.btn_yes:
#         try:
#             staff.leave_chat(brach.group_id)
#         except:pass
#         brach.group_id = None
#         brach.save()
#         staff.send_message(
#             brach.telegram_id,render.StaffRender(static_text_admin.staff_remove_success,brach)
#         )
#         staff.delete_message(call.from_user.id,call.message.message_id)
#     elif call.data == static_text_admin.btn_no:
#         staff.delete_message(call.from_user.id,call.message.message_id)
#     else:
#         if 'service' in call.data:
#             serivice = ServiceType.objects.get(id=int(call.data.split('-')[1]))
#             if serivice in brach.services.all():
#                 for s in ServiceType.objects.filter(cell_of=serivice):
#                     brach.services.remove(s)
#                 brach.services.remove(serivice)
#             else:
#                 for s in ServiceType.objects.filter(cell_of=serivice):
#                     brach.services.add(s)
#                 brach.services.add(serivice)
#             staff.edit_message_reply_markup(
#                 call.from_user.id,call.message.message_id,
#                 reply_markup=markup.Staff_Service_Type(brach)
#             )
#         elif 'reject' in call.data:
#             order = Order.objects.get(id=call.data.split('-')[1])
#             engine = BotManager.get_bot(order.customer.cafe.bot_token)
#             order.status='X'
#             order.save()
#             engine.bot.send_message(
#                 order.customer.telegram_id,
#                 render.LanguageRender(order.customer.language.order_status,order.customer,order=order)
#             )
#             staff.edit_message_text(
#                 render.RemovedText(call.message.text),
#                 call.message.chat.id,call.message.message_id,reply_markup=None
#             )
#             order.delete()
#         elif 'accept' in call.data:
#             main_language = Language.objects.get(main=True)
#             order = Order.objects.get(id=call.data.split('-')[1])
#             engine = BotManager.get_bot(order.customer.cafe.bot_token)
#             order.status='A'
#             html_text = call.message.html_text
#             modified_text = html_text.replace(main_language.label_pending, main_language.label_accepted)
#             order.save()
#             engine.bot.send_message(
#                 order.customer.telegram_id,
#                 render.LanguageRender(order.customer.language.order_status,order.customer,order=order)
#             )
#             staff.edit_message_text(
#                 modified_text,
#                 call.message.chat.id,call.message.message_id,reply_markup=markup.Staff_Complete(order,main_language)
#             )
#         elif 'back-category' == call.data:
#             staff.edit_message_text(
#                 render.StaffRender(static_text_admin.staff_category_command,brach),
#                 chat_id=brach.telegram_id,message_id=call.message.message_id,
#                 reply_markup=markup.Staff_Categories(brach),
#             )
#         elif 'category' in call.data:
#             category = Category.objects.get(id=int(call.data.split('-')[1]))
#             staff.edit_message_text(
#                 render.StaffCategoryRender(static_text_admin.staff_category_detail,category),
#                 chat_id=brach.telegram_id,message_id=call.message.message_id,
#                 reply_markup=markup.Staff_Category_Markup(category),
#             )
#         elif 'product' in call.data:
#             product = Product.objects.get(id=int(call.data.split('-')[1]))
#             staff.edit_message_text(
#                 render.StaffProductRender(static_text_admin.staff_product_detail,product),
#                 chat_id=brach.telegram_id,message_id=call.message.message_id,
#                 reply_markup=markup.Staff_Procduct_Markup(product),
#             )
#         elif 'aviable' in call.data:
#             product = Product.objects.get(id=int(call.data.split('-')[1]))
#             if product.is_available:
#                 product.is_available = False
#             else:
#                 product.is_available = True
#             product.save()
#             call.data = f'product-{product.id}'
#             handle_callback(call)
