import os
import random
import string
from datetime import datetime as dt

from fpdf import FPDF

from foodgram.settings import BASE_DIR
from foodgram.settings import STATIC_URL
from foodgram.settings import DOWNLOADS_DIR

def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# function input parameter - user_purchases is dict
def get_shop_list_pdf(user_purchases):
    pdf_shop_list = FPDF()
    pdf_shop_list.add_page()

    font_path = os.path.join(
        os.getcwd(),
        'recipes/static/recipes/fonts/DejaVuSansCondensed.ttf'
    )
    pdf_shop_list.add_font('DejaVu', '', font_path, uni=True)
    pdf_shop_list.set_font('DejaVu', '', 14)

    for purchase, amount in user_purchases.items():
        pdf_shop_list.cell(0, 10, f'( ) {purchase} - {amount}', 0, 1)

    date, random_string = dt.now().date(), get_random_string(8)
    shop_list_name = f'{date}_shop-list_{random_string}.pdf'
    shop_list_full_path = os.path.join(DOWNLOADS_DIR, shop_list_name)

    pdf_shop_list.output(shop_list_full_path)

    return shop_list_full_path
