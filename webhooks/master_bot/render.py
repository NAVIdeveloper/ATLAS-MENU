from core.models import *
from partners.models import Branch,Category
from customers.models import Customer

from webhooks.master_bot.configuration import USERNAME_BOT_STAFF
from webhooks.master_bot.helper import get_customer_department

def generate_yandex_map_link(latitude, longitude, zoom=18):
    # URL encode the parameters
    base_url = "https://yandex.com/maps/"
    ll = f"{longitude},{latitude}"
    pt = f"{longitude},{latitude},pm2dgl"
    
    # Construct the full URL
    url = f"{base_url}?ll={ll}&z={zoom}&pt={pt}"
    return url

def StaffRender(text: str, branch: Branch, map_flag: bool = False) -> str:
    static_tags = {
        "{{bot_staff}}": USERNAME_BOT_STAFF,
        "{{status_group}}": "✅" if branch.group_id else "❌",
    }
    dynamic_tags = {
        "{{partner}}": branch.partner.name,
        "{{city}}": branch.city.name,
        "{{location}}": branch.location,
        "{{count_user}}": str(Customer.objects.filter(partner=branch.partner).count()),
        "{{category}}": str(Category.objects.filter(branch=branch).count()),
    }
    if map_flag:
        dynamic_tags["{{map}}"] = generate_yandex_map_link(
            branch.location_lat, 
            branch.location_long
        )
    tags = {**static_tags, **dynamic_tags}
    for tag, value in tags.items():
        text = text.replace(tag, value)
    return text

# def StaffCategoryRender(text:str,category:Category):
#     text = StaffRender(text,category.department)
#     tags = {
#         "{{category_name}}":category.name,
#         "{{category_id}}":str(category.id),
#         "{{category_products}}":str(Product.objects.filter(category=category).count())
#     }
#     for tag in tags:
#         text = text.replace(tag,tags[tag])
#     return text
