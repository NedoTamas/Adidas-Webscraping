from curl_cffi import requests
from bs4 import BeautifulSoup
import asyncio
import time
from random import randint
import re
import pandas as pd
import os
import json
from datetime import date
from memory_handling import *

#Setting up variables

#---pathing---
root = os.getcwd()
bronze_path=os.path.join(root,"bronze")
silver_path=os.path.join(root,"silver")
gold_path=os.path.join(root,"gold")
memory_path=os.path.join(root,"memory_log")

#---time---
today=date.today()

#---naming the output---
product_data_path=os.path.join(bronze_path, str(today)+'_product_data.csv')
product_data_availability_path=os.path.join(bronze_path, str(today)+'_product_data_availability.csv')
memory=os.path.join(memory_path, str(today)+'_memory.txt')
SKU=os.path.join(memory_path, str(today)+'_SKU.txt')

#---memory---
block_occured=False


print(product_data_path)
print(product_data_availability_path)





#look for the "personalizationengine" POST request
#a cookie can survive circa 60 mins
#an ip can survive around 1000 requests for availability, after that you may have to get new cookies, or ip (connecting to a vpn)


#---Cookies / Headers from your browser---

cookies = {
    'mt.v': '5.023471563.1735173098104',
    'channelcloser': 'nonpaid',
    'x-browser-id': 'ef39a6f2-8314-4f82-a0fa-363e49a57267',
    'ab_qm': 'b',
    'wishlist': '%5B%5D',
    'notice_preferences': '%5B0%2C1%2C2%5D',
    '_gcl_au': '1.1.745756955.1735173104',
    '_ga': 'GA1.1.417081306.1735173100',
    '_scid': 'zniVhzQxtikyP_ORqzNgOBONUQNB32mF',
    '_pin_unauth': 'dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA',
    'QuantumMetricUserID': 'ce9e74e6acbef12e0916dd37bb958505',
    'newsletterShownOnVisit': 'true',
    '__olapicU': '194fc6145839464cb3a8a92f2b8bb16e',
    '_ScCbts': '%5B%5D',
    'x-commerce-next-id': '17a7b974-4e70-4f46-bba0-c6138f386218',
    'QSI_SI_0evq2NrkQkQaBb7_intercept': 'true',
    'geo_coordinates': 'lat=51.22, long=6.77',
    'gl-feat-enable': 'CHECKOUT_PAGES_ENABLED',
    'geo_ip': '2a02:908:952:ae0:9555:feea:d337:c5a6',
    'onesite_country': 'DE',
    'AKA_A2': 'A',
    'akacd_generic_prod_grayling_adidas': '3913810152~rv=58~id=1570e6ece04d1e6cb308b949654224d1',
    'bm_ss': 'ab8e18ef4e',
    'akacd_plp_prod_adidas_grayling': '3913810153~rv=64~id=c595ebca0321f4ebb91214de8d9617c4',
    'x-original-host': 'adidas.co.uk',
    'x-site-locale': 'en_GB',
    'x-session-id': 'ea32ecf2-d60d-4e51-86e1-c0f87e2b36c2',
    'wishlist': '%5B%5D',
    'bm_lso': 'E8A94B4E6F19CA202772C5677EA6862ABFA8B605ABE9A67069F0CBC7C3D1FFEE~YAAQyPIWAm+2sbeTAQAA1Zv2RgKP1QDK1UWUlawGLkCRqzZYYA7f/QP0yoFtOIsgFkpCPTtXHIqpEF9YeVMDRVmTocpYN2qQRENmh5DMLHoksdO020uBYYn+ej6AlGDqSttouVkCGbOVXQB/8ZTFjr/C80GwoEkOCK1jYx8Y9EupN5Wcsfo/kthWV+XALL7kc1OScotKFwsnL/C/9jFIN3w39qtS9OlUdefs4wSzWVv/9DOwp1sIwUCYGd1PkriP6RkfpFHC/J5Fx0D+BVfm8KyYp5auL/YxgFmWIlaXHKTz2CxJW/OM2mFTp0NtZDRoTuLAm/0MoICA6Ym72DjbVCjCPFRfcFn9L3UMXpmbEXmDeL9ZRTrJ0VLugBhtEbKbs1A81XjaJujO9GFLHjtu/lY7lIfGMzDeiC5FEe3U45hzRlXLDCvLKPZ7thPGN++3ERP8vL3p14t2FYeYHEuTReHd+txigdd1GwvWCJX3NlnlFsKx^1736357356398',
    'AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg': '1',
    'AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736962157%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736364557s%7CNONE%7CMCAID%7CNONE',
    's_cc': 'true',
    'geo_country': 'DE',
    'QuantumMetricSessionID': '11189dd934039a402f71e1c758104f7c',
    'akacd_pdp_prod_adidas_grayling': '3913810162~rv=24~id=411870ec2e76d18251111e6da7a3e0e3',
    'checkedIfOnlineRecentlyViewed': 'true',
    'persistentBasketCount': '0',
    'userBasketCount': '0',
    'pagecontext_cookies': '',
    'pagecontext_secure_cookies': '',
    'ak_bmsc': 'F49A2BC4FDEFE083AF23D0A77FF3E200~000000000000000000000000000000~YAAQyPIWAkW6sbeTAQAAqsn2RhqT5DeZeq5tT7U0zwfQ/3tnCliNC3HoCapWUWogIpWjNiDhrJtN0ZU+rF8Jf/vrNJODidgoyalmodhxluvUZ8hezba9ZrDI8lmZ4KTafHIFsyhfbk0zM2Keigaz+W4LwN30JJzj3VKYrNX/u+4td9nIRAp23S3Ek4Ta3mzxd3wuPqqer8AkPs0FKBb3PGN5rNslYxhMC1iKZJxTVLsJd5gJsPWIv486xyX0dmOyatqS6UdrOlleRrK+yy17wg8fc0yhNTzcY3EQxiAWFt33O8ysrxc24FYJCJxMrhD2pOKzQ1i4RvtHxfutbt2Hlj3HJouqNu/CqX/4FNS+GBagYx4AjodmsPOrnC80ukNjpWFGDhhJUZxuItnPbAgSIooWaqTqulvwd8RlHAiUfs8=',
    '_rdt_uuid': '1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7',
    'utag_main': 'v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:16$_se:7%3Bexp-session$_ss:0%3Bexp-session$_st:1736359169656%3Bexp-session$ses_id:1736357355042%3Bexp-session$_pn:3%3Bexp-session$_vpn:5%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:113%3Bexp-session$ab_dc:TEST%3Bexp-1741541369662$_prevpage:PRODUCT%7CSL%2072%20OG%20SCHUH%20(IE3425)%3Bexp-1736360970351',
    's_pers': '%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D8%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736359170542%3B',
    '_scid_r': '1fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9wA',
    '_ga_4DGGV4HV95': 'GS1.1.1736357357.18.1.1736357370.47.0.0',
    '_uetsid': '28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833',
    '_uetvid': 'c85e49c0c32011ef95a8e15267052ca8|arblxs|1736357372061|2|1|bat.bing.com/p/insights/c/e',
    'bm_s': 'YAAQyPIWAlC9sbeTAQAA3fH2RgIKizdmmloj/L/jncL7G87MB3HvpwLSnTep4dXfisJbgTHLp/F/cJ77aOW0KPOswXIkO2r/r7TGpaWhoJQ0E62dZmW1uH+zwg6UBBWPLku4sHJ+yx4k1Fpg+TMf0Dtm3lUGhv/cUERi1E7q1PUYfYVcBGQVI6FGcgttgvtgtCL9bJ5wTyD3V5LSkNZgXWjfZamXCQUiStDk6R1hgiRfQ5UCv4lK5O11kGCHkcF2EmOdkfpDiyUrmUVR74k0CYfDlpqeV0Hd3LcTi6o7DEv9TRzksSSuClGy6W6FT2w71kTHDHJOhC6fJ5o+/rn6NR97GVix',
    'bm_so': 'BF9EB2E2F7D130FB955E5DACD526B9DF325FB2EBE2629001EC589F680CA4F0E1~YAAQyPIWAlG9sbeTAQAA3fH2RgLr+EA+7ANELfEJ6qqNMVOeB4OP1grL27umJf1GAfBnSOYrryk+aFcgd02QjNEoU5JlreCWvD39flJ6iyHWAaRNH+xVqetm5k3ve2D/W9tDuewkubT/+0eT4czTLJYGL+9CRcfKwztjxM0O9ieQ5uGU2nYMA5FgUEkOK9wJZ77aNmHyQQXzY/cGXySlBfQgWVzkf6YYfxVzvuZEH+voz0DR+Eu9ojlaUfcJ8cE1xPE7GJNqtaNcv71XLT2AcDzSZkh/h41NkdA2ZNuISlFsWtEsHu55WFekXQoA4P0N1Do84hTVsxiKuvgcynJB03/DC9cbIBG6Blzj672DDQh2BfwaQhrFQfn/JC7EY69MyZsG/ALBP0uxvU/hM9m9e7/+VLVpDI0C5mtqv1GF2clAKuBcMH/XBA1+ZJOtJCRX/NIXtrF4V9XJdlpMaW3rx0H5W1ZrOSGIsuyCGP2fY6YAgIhW',
    'bm_sz': 'D5C6D13E22DB7F88AF809C958F1EA446~YAAQyPIWAlK9sbeTAQAA3fH2RhontXKV9ZCOjrDoGx5HEg3r9q11Mrvrc7Hsi3yKOoQnykEMN89x7c66bjSfime93+8zoXqTyOfqJc9jhXxF5TNcOWinqet1M2kZ25AjYWrg5YhgbBhNkdGTzeD+lPeLIIZJfwd4j0OTf0rvwHD/OZblkS46EuvbidP2hJCygMU+eBjiIlXtIIx/ZGqu0DUvo3Tl4mtl/Bi0vl5FNwUejcsbQVOKEH/Bzpw85mmUwVfYV7806ckTNj+9+90Q2Sviy7HoYnYsoOy2ulvpGIAPSPVmz8Lgf+opThWnQKt0SRD/oKs/B5qN8bKDRMf/hXIg+dREX+fST43l+5+WEiZnpyxZcbt3EHL7OZ04JVAAvvc+8xkOGxT7QQ2JW/Skbt6l5csFBq9mF+IDnoTLb6PheD+9W2ol8BjePeYiqiw1H1K8oVbpapaQXxgO+0PK+EYV/U8=~3227971~3425604',
    'RT': '"z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5o6c4c4&sl=2&tt=8sz&bcn=%2F%2F02179919.akstat.io%2F&ld=fql&hd=hw2"',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43_17ck_qsxJsDqQ7FI%3D-1141-v2',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43_17ck_qsxJsDqQ7FI%3D-1141-v2',
    '_abck': '55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQyPIWAnW9sbeTAQAA2fP2Rg2raBz0KP2TXxA5n5baOdqr44gMm12iPIK9iGfmQjUsQThQuo1H4pe+LWvz6y6koDaQbB8kaGur7ZonTImHGQiOLMWZuOV8x2Gx28RND/zeQJET5Uo0zBB8//hpTfLeDgENU2UHe7GwBe5qgTnXFvQaDuQkjXcYLyLrR6pZT6d+MLMiulKCK1F/lLidv8TyAi56uw1/Tz4KFSD1kIKWALtIy1yrquP/Ayj7f83cTyjFGT4VGZmYA2zyl3Tpz3zO4lQLylyStHOUWB3vF1f8ovHfiFHNx5eLcFtGAoYJvjsWnIItCMglutFhC5b6ArBhc7ICjyozoKQli4wLogYCmJo7+Px0rvRjn693jBm35lbKzZfHmr6al5bFLmFiVeXHagg2nwUDx+np842qI//R5mjneBA11c/p5ezlcLIVZW09mfXF3IWXAuTIZfTjJN8NMfkVWsIA9U4qEq0nf1iWnFVgRvG41amKxiE3lSnekWoyP7qf1RCccZKbS6YZhwMEuNGglzn8gVLcOvG7F9i7lCf0~-1~-1~1736360955',
    'UserSignUpAndSave': '51',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'mt.v=5.023471563.1735173098104; channelcloser=nonpaid; x-browser-id=ef39a6f2-8314-4f82-a0fa-363e49a57267; ab_qm=b; wishlist=%5B%5D; notice_preferences=%5B0%2C1%2C2%5D; _gcl_au=1.1.745756955.1735173104; _ga=GA1.1.417081306.1735173100; _scid=zniVhzQxtikyP_ORqzNgOBONUQNB32mF; _pin_unauth=dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA; QuantumMetricUserID=ce9e74e6acbef12e0916dd37bb958505; newsletterShownOnVisit=true; __olapicU=194fc6145839464cb3a8a92f2b8bb16e; _ScCbts=%5B%5D; x-commerce-next-id=17a7b974-4e70-4f46-bba0-c6138f386218; QSI_SI_0evq2NrkQkQaBb7_intercept=true; geo_coordinates=lat=51.22, long=6.77; gl-feat-enable=CHECKOUT_PAGES_ENABLED; geo_ip=2a02:908:952:ae0:9555:feea:d337:c5a6; onesite_country=DE; AKA_A2=A; akacd_generic_prod_grayling_adidas=3913810152~rv=58~id=1570e6ece04d1e6cb308b949654224d1; bm_ss=ab8e18ef4e; akacd_plp_prod_adidas_grayling=3913810153~rv=64~id=c595ebca0321f4ebb91214de8d9617c4; x-original-host=adidas.co.uk; x-site-locale=en_GB; x-session-id=ea32ecf2-d60d-4e51-86e1-c0f87e2b36c2; wishlist=%5B%5D; bm_lso=E8A94B4E6F19CA202772C5677EA6862ABFA8B605ABE9A67069F0CBC7C3D1FFEE~YAAQyPIWAm+2sbeTAQAA1Zv2RgKP1QDK1UWUlawGLkCRqzZYYA7f/QP0yoFtOIsgFkpCPTtXHIqpEF9YeVMDRVmTocpYN2qQRENmh5DMLHoksdO020uBYYn+ej6AlGDqSttouVkCGbOVXQB/8ZTFjr/C80GwoEkOCK1jYx8Y9EupN5Wcsfo/kthWV+XALL7kc1OScotKFwsnL/C/9jFIN3w39qtS9OlUdefs4wSzWVv/9DOwp1sIwUCYGd1PkriP6RkfpFHC/J5Fx0D+BVfm8KyYp5auL/YxgFmWIlaXHKTz2CxJW/OM2mFTp0NtZDRoTuLAm/0MoICA6Ym72DjbVCjCPFRfcFn9L3UMXpmbEXmDeL9ZRTrJ0VLugBhtEbKbs1A81XjaJujO9GFLHjtu/lY7lIfGMzDeiC5FEe3U45hzRlXLDCvLKPZ7thPGN++3ERP8vL3p14t2FYeYHEuTReHd+txigdd1GwvWCJX3NlnlFsKx^1736357356398; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736962157%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736364557s%7CNONE%7CMCAID%7CNONE; s_cc=true; geo_country=DE; QuantumMetricSessionID=11189dd934039a402f71e1c758104f7c; akacd_pdp_prod_adidas_grayling=3913810162~rv=24~id=411870ec2e76d18251111e6da7a3e0e3; checkedIfOnlineRecentlyViewed=true; persistentBasketCount=0; userBasketCount=0; pagecontext_cookies=; pagecontext_secure_cookies=; ak_bmsc=F49A2BC4FDEFE083AF23D0A77FF3E200~000000000000000000000000000000~YAAQyPIWAkW6sbeTAQAAqsn2RhqT5DeZeq5tT7U0zwfQ/3tnCliNC3HoCapWUWogIpWjNiDhrJtN0ZU+rF8Jf/vrNJODidgoyalmodhxluvUZ8hezba9ZrDI8lmZ4KTafHIFsyhfbk0zM2Keigaz+W4LwN30JJzj3VKYrNX/u+4td9nIRAp23S3Ek4Ta3mzxd3wuPqqer8AkPs0FKBb3PGN5rNslYxhMC1iKZJxTVLsJd5gJsPWIv486xyX0dmOyatqS6UdrOlleRrK+yy17wg8fc0yhNTzcY3EQxiAWFt33O8ysrxc24FYJCJxMrhD2pOKzQ1i4RvtHxfutbt2Hlj3HJouqNu/CqX/4FNS+GBagYx4AjodmsPOrnC80ukNjpWFGDhhJUZxuItnPbAgSIooWaqTqulvwd8RlHAiUfs8=; _rdt_uuid=1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7; utag_main=v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:16$_se:7%3Bexp-session$_ss:0%3Bexp-session$_st:1736359169656%3Bexp-session$ses_id:1736357355042%3Bexp-session$_pn:3%3Bexp-session$_vpn:5%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:113%3Bexp-session$ab_dc:TEST%3Bexp-1741541369662$_prevpage:PRODUCT%7CSL%2072%20OG%20SCHUH%20(IE3425)%3Bexp-1736360970351; s_pers=%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D8%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736359170542%3B; _scid_r=1fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9wA; _ga_4DGGV4HV95=GS1.1.1736357357.18.1.1736357370.47.0.0; _uetsid=28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833; _uetvid=c85e49c0c32011ef95a8e15267052ca8|arblxs|1736357372061|2|1|bat.bing.com/p/insights/c/e; bm_s=YAAQyPIWAlC9sbeTAQAA3fH2RgIKizdmmloj/L/jncL7G87MB3HvpwLSnTep4dXfisJbgTHLp/F/cJ77aOW0KPOswXIkO2r/r7TGpaWhoJQ0E62dZmW1uH+zwg6UBBWPLku4sHJ+yx4k1Fpg+TMf0Dtm3lUGhv/cUERi1E7q1PUYfYVcBGQVI6FGcgttgvtgtCL9bJ5wTyD3V5LSkNZgXWjfZamXCQUiStDk6R1hgiRfQ5UCv4lK5O11kGCHkcF2EmOdkfpDiyUrmUVR74k0CYfDlpqeV0Hd3LcTi6o7DEv9TRzksSSuClGy6W6FT2w71kTHDHJOhC6fJ5o+/rn6NR97GVix; bm_so=BF9EB2E2F7D130FB955E5DACD526B9DF325FB2EBE2629001EC589F680CA4F0E1~YAAQyPIWAlG9sbeTAQAA3fH2RgLr+EA+7ANELfEJ6qqNMVOeB4OP1grL27umJf1GAfBnSOYrryk+aFcgd02QjNEoU5JlreCWvD39flJ6iyHWAaRNH+xVqetm5k3ve2D/W9tDuewkubT/+0eT4czTLJYGL+9CRcfKwztjxM0O9ieQ5uGU2nYMA5FgUEkOK9wJZ77aNmHyQQXzY/cGXySlBfQgWVzkf6YYfxVzvuZEH+voz0DR+Eu9ojlaUfcJ8cE1xPE7GJNqtaNcv71XLT2AcDzSZkh/h41NkdA2ZNuISlFsWtEsHu55WFekXQoA4P0N1Do84hTVsxiKuvgcynJB03/DC9cbIBG6Blzj672DDQh2BfwaQhrFQfn/JC7EY69MyZsG/ALBP0uxvU/hM9m9e7/+VLVpDI0C5mtqv1GF2clAKuBcMH/XBA1+ZJOtJCRX/NIXtrF4V9XJdlpMaW3rx0H5W1ZrOSGIsuyCGP2fY6YAgIhW; bm_sz=D5C6D13E22DB7F88AF809C958F1EA446~YAAQyPIWAlK9sbeTAQAA3fH2RhontXKV9ZCOjrDoGx5HEg3r9q11Mrvrc7Hsi3yKOoQnykEMN89x7c66bjSfime93+8zoXqTyOfqJc9jhXxF5TNcOWinqet1M2kZ25AjYWrg5YhgbBhNkdGTzeD+lPeLIIZJfwd4j0OTf0rvwHD/OZblkS46EuvbidP2hJCygMU+eBjiIlXtIIx/ZGqu0DUvo3Tl4mtl/Bi0vl5FNwUejcsbQVOKEH/Bzpw85mmUwVfYV7806ckTNj+9+90Q2Sviy7HoYnYsoOy2ulvpGIAPSPVmz8Lgf+opThWnQKt0SRD/oKs/B5qN8bKDRMf/hXIg+dREX+fST43l+5+WEiZnpyxZcbt3EHL7OZ04JVAAvvc+8xkOGxT7QQ2JW/Skbt6l5csFBq9mF+IDnoTLb6PheD+9W2ol8BjePeYiqiw1H1K8oVbpapaQXxgO+0PK+EYV/U8=~3227971~3425604; RT="z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5o6c4c4&sl=2&tt=8sz&bcn=%2F%2F02179919.akstat.io%2F&ld=fql&hd=hw2"; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43_17ck_qsxJsDqQ7FI%3D-1141-v2; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43_17ck_qsxJsDqQ7FI%3D-1141-v2; _abck=55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQyPIWAnW9sbeTAQAA2fP2Rg2raBz0KP2TXxA5n5baOdqr44gMm12iPIK9iGfmQjUsQThQuo1H4pe+LWvz6y6koDaQbB8kaGur7ZonTImHGQiOLMWZuOV8x2Gx28RND/zeQJET5Uo0zBB8//hpTfLeDgENU2UHe7GwBe5qgTnXFvQaDuQkjXcYLyLrR6pZT6d+MLMiulKCK1F/lLidv8TyAi56uw1/Tz4KFSD1kIKWALtIy1yrquP/Ayj7f83cTyjFGT4VGZmYA2zyl3Tpz3zO4lQLylyStHOUWB3vF1f8ovHfiFHNx5eLcFtGAoYJvjsWnIItCMglutFhC5b6ArBhc7ICjyozoKQli4wLogYCmJo7+Px0rvRjn693jBm35lbKzZfHmr6al5bFLmFiVeXHagg2nwUDx+np842qI//R5mjneBA11c/p5ezlcLIVZW09mfXF3IWXAuTIZfTjJN8NMfkVWsIA9U4qEq0nf1iWnFVgRvG41amKxiE3lSnekWoyP7qf1RCccZKbS6YZhwMEuNGglzn8gVLcOvG7F9i7lCf0~-1~-1~1736360955; UserSignUpAndSave=51',
    'origin': 'https://www.adidas.de',
    'priority': 'u=1, i',
    'referer': 'https://www.adidas.de/sl-72-og-schuh/IE3425.html',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-instana-l': '1,correlationType=web;correlationId=bc90a695f5cb916a',
    'x-instana-s': 'bc90a695f5cb916a',
    'x-instana-t': 'bc90a695f5cb916a',
}


category=['sneakers','fussball-schuhe','outdoor-schuhe','running-schuhe','walking-schuhe','fitness_training-schuhe','tennis-schuhe']


#Old searching terms
#category=['manner-sneakers','frauen-sneakers','jungen-sneakers','manner-fitness_training-schuhe','manner-fussball-schuhe','manner-running-schuhe']
#Example url: https://www.adidas.de/manner-sneakers



def raw_codes(category_name):
    base_url=f'https://www.adidas.de/{category_name}'
    all_item_code=[]
    item_per_page=48
    a=-item_per_page
    next_page=True
    while next_page:
        try:
            a=a+item_per_page
            url=f'{base_url}?start={a}'
            response =  requests.get(url,  cookies=cookies, headers=headers)
            
            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.find_all("article", {"class": "product-card_product-card__a9BIh product-grid_product-card__8ufJk"})
            
            if not items:
                next_page = False
                print(f"{(a/item_per_page+1)} Pages were scraped")
                print(response)
                break

            for item in items:
                all_item_code.append(item.find("a").attrs["href"])
                print(item.find("a").attrs["href"])

        except Exception as e:
            print(f"An error has occurred: {e}")
            next_page=False

    return all_item_code

def codes(all_item_code):
    item_codes=[]
    for item in all_item_code:
        item_codes.append(item[-11:-5])
    df = pd.DataFrame(all_item_code)
    
    #Saving out the codes to have a backup. // !!! Use it later on when improving on the performance
    
    df.to_csv(SKU, index=False, mode='a')
    print('SKU list has been generated')
    return item_codes


def details(item_codes, category_name):
    
    block_occured = False
    i = 0
    product_list = []
    for item in item_codes:
        url = f'https://www.adidas.de/api/product-list/{item}'
        response = requests.get(url, cookies=cookies, headers=headers)
        

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                product_data = data[0]  # Access the first item in the list
                product_info = {
                    "name": product_data.get("name", None),
                    "id": product_data.get("id", None),
                    "price": product_data.get("pricing_information", {}).get("currentPrice", None),
                    "category": category_name,
                    "image_url": product_data.get("view_list", [{}])[0].get("image_url", None),
                    "color": product_data.get("attribute_list", {}).get("color", None),
                    "weight": product_data.get('attribute_list', {}).get('weight', None),
                    "gender": product_data.get('attribute_list', {}).get('gender', None),
                    "best_for_wear": next(iter(product_data.get("attribute_list", {}).get("best_for_ids", [])), None),
                    "date": str(today)
                }
                i=i+1
                print(f"{i} {product_info}")

                #Implemented sleep to prevent ip blocks. //  !!! May lower in the future to secure smooth running
                if i%500==0:
                    time.sleep(randint(100, 150))

                product_list.append(product_info)
            else:
                print(f"No data found for item {item}")
        else:
            print(f"Failed to retrieve data for item {item}: {response.status_code}")
            if response.status_code == 403:
                block_occured = True
                break
    return product_list, block_occured

def export(product_list):

    
    df = pd.DataFrame(product_list)

    #if theres no existing file with this name, it saves the headers, otherwise just the records
    file_exists = os.path.isfile(product_data_path)

    df.to_csv(product_data_path, mode='a', header=not file_exists, index=False)

    print(f"product_data.csv generated in {bronze_path}")


def availability():
    i=0

    file_exists = os.path.isfile(product_data_availability_path)
    if file_exists:
        df = pd.read_csv(product_data_availability_path)
    else:
        df = pd.read_csv(product_data_path)
        print("There is no availability record stored. --- for now ;) ")

    if 'availability' not in df.columns:
        df['availability'] = None

    non_null_count = df['availability'].count()
    print(f"Number of non-null cells in 'availability' column: {non_null_count}")

    for index, row in df.iloc[non_null_count:].iterrows():
        i=i+1
        id = row["id"]
        url = f'https://www.adidas.de/api/products/{id}/availability'
        
        response = requests.get(url, cookies=cookies, headers=headers, impersonate="chrome120")

        #After 1000 requests we cause the server to block us. To prevent it implement waiting times.
        #Previous tries: 2min/500r
        if i%350==0:
            time.sleep(randint(100, 150))


        #Enable it when I find a solution for proxy rotation
        #if response.status_code == 403:
            #rotate_VPN(settings)


        if response.status_code == 200:
            print(f'{i}.th item in this cycle \n')
            try:
                data = json.loads(response.text)
                variation_list = data.get('variation_list', [])
                
                if variation_list:
                    availability_data = []
                    for variation in variation_list:
                        availability_data.append({
                            'size': variation['size'],
                            'availability': variation['availability']
                            
                        })
                    df.at[index, 'availability'] = json.dumps(availability_data)  # Store as JSON string
                    print(f"Data found for {id}")
                else:
                    print(f"No variation list found for product {id}")
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for product {id}")
            except KeyError as e:
                print(f"Unexpected response structure for product {id}: {e}")
        else:
            print(f"Failed to retrieve data for item {id}. response code: {response.status_code}")
            print("The script is quiting.")
            break
    print(f"Total data collected: {i-1}")
    df.to_csv(product_data_availability_path, index=False)
    print("Updated the availability.")


        
def main():
    i=0
    last_successful_item = get_last_successful_item()
    start_index = category.index(last_successful_item) + 1 if last_successful_item in category else 0
    for category_name in category[start_index:]:
        i=i+1
        all_item_code = raw_codes(category_name)
        item_codes = codes(all_item_code)
        product_list, block_occured = details(item_codes, category_name)
        memory_decision(block_occured, category_name)
        if block_occured:
            break
        export(product_list)

    if i==0:
        print("Today's category data gathering was already successful.") 
    else:
        print(f"{i} categories data were collected in this cycle.")

    availability()

main()





