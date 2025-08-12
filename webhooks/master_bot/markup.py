from partners.models import Branch
from webhooks.master_bot.configuration import JOIN_GROUP_URL
from telebot import types

def StaffMenu(branch:Branch):
    STAFF_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True)
    STAFF_MENU.add(types.KeyboardButton(branch.language.master.btn_dashboard))
    STAFF_MENU.add(types.KeyboardButton(branch.language.master.btn_statistic))
    STAFF_MENU.add(types.KeyboardButton(branch.language.master.btn_setting_group))
    return STAFF_MENU

def AddGroup(branch:Branch):
    ADD_GROUP = types.InlineKeyboardMarkup()
    ADD_GROUP.add(
        types.InlineKeyboardButton(
            branch.language.master.btn_add_group,
            url=JOIN_GROUP_URL
        )
    )
    return ADD_GROUP