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
    'AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg': '1',
    'AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736962157%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736364557s%7CNONE%7CMCAID%7CNONE',
    's_cc': 'true',
    'geo_country': 'DE',
    'akacd_pdp_prod_adidas_grayling': '3913810162~rv=24~id=411870ec2e76d18251111e6da7a3e0e3',
    'checkedIfOnlineRecentlyViewed': 'true',
    'persistentBasketCount': '0',
    'userBasketCount': '0',
    'pagecontext_cookies': '',
    'pagecontext_secure_cookies': '',
    'ak_bmsc': 'F108E8FD5DCCC071F3E43D2E545A9474~000000000000000000000000000000~YAAQyPIWAsu9sbeTAQAA7ff2RhqmyILOAcmalAPa5YiZ5K3nq0Yqe+e6/CNJhqGGgMJ8cwUjwTzLw7pxns0J42wPnN5yRItwzrnUiQP/XDLg/wRkCx0J7jKEgyGpcOEvTxHpwSqFRRM8yz8WJZb7f/ywTZcqmdnOd+az9Wo7zTtjz0T42FNN94ctPf9GXVcSSRTfkeirI4Nnfgdqi9kiuVTCuFHa91x+hpo0BM2zSDCBscoBwEkbKgypwgjjXYDmDtx48zjm2Vv8XrZubp5m736eeEKwDVYjMrrUneI6t1w8pZVnnKi4tjR+we2mehSGJeMPqCj5uFJxhgOJQisKqJiQDXqdweA+vQY99YZ29UCL0cJOuvtzj306bKtNVp6Lbtiss1VF4fwkvpn6ajqx9qic/uNZaMKkjUYFmACY4Bs=',
    'bm_lso': 'BF9EB2E2F7D130FB955E5DACD526B9DF325FB2EBE2629001EC589F680CA4F0E1~YAAQyPIWAlG9sbeTAQAA3fH2RgLr+EA+7ANELfEJ6qqNMVOeB4OP1grL27umJf1GAfBnSOYrryk+aFcgd02QjNEoU5JlreCWvD39flJ6iyHWAaRNH+xVqetm5k3ve2D/W9tDuewkubT/+0eT4czTLJYGL+9CRcfKwztjxM0O9ieQ5uGU2nYMA5FgUEkOK9wJZ77aNmHyQQXzY/cGXySlBfQgWVzkf6YYfxVzvuZEH+voz0DR+Eu9ojlaUfcJ8cE1xPE7GJNqtaNcv71XLT2AcDzSZkh/h41NkdA2ZNuISlFsWtEsHu55WFekXQoA4P0N1Do84hTVsxiKuvgcynJB03/DC9cbIBG6Blzj672DDQh2BfwaQhrFQfn/JC7EY69MyZsG/ALBP0uxvU/hM9m9e7/+VLVpDI0C5mtqv1GF2clAKuBcMH/XBA1+ZJOtJCRX/NIXtrF4V9XJdlpMaW3rx0H5W1ZrOSGIsuyCGP2fY6YAgIhW^1736357379413',
    '_rdt_uuid': '1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7',
    '_scid_r': '1viVhzQxtikyP_ORqzNgOBONUQNB32mFZit9wQ',
    '_uetsid': '28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833',
    'QuantumMetricSessionID': '09f0879c17170bd8ba4b625ea9a9eb5d',
    '_uetvid': 'c85e49c0c32011ef95a8e15267052ca8|1njkn52|1736360430417|1|1|bat.bing.com/p/insights/c/e',
    'utag_main': 'v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:17$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1736362232913%3Bexp-session$ses_id:1736360432913%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:114%3Bexp-session$ab_dc:TEST%3Bexp-1741541381265$_prevpage:PRODUCT%7CSL%2072%20OG%20SCHUH%20(IE3425)%3Bexp-1736360983187',
    's_pers': '%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D9%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736362232933%3B',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43-m4_17ck_6a476uL8m9Y%3D-8959-v2',
    'geo_coordinates': 'lat=50.12, long=8.68',
    'bm_s': 'YAAQiXcQAkB5AEWUAQAAEcYlRwLI59IcfS1jM3b29huAHHuqYzhzr+ia/V5BZr258qtrniI3THLM7+JY/CMPFvNE9RM5HJp7sAN7TFt4FZd/6s3L/YPq8QmeP9S2WCvYFlE4m5nSUvC70LD12g6ohjL99ActWPA72Xd40g72btQ7aDN45YYhCZKXWobL/Avanp6tF5BEMm3dybtsgFKyeQk1D0iyx+JDwZ2joP0x4fOEH3tyhIzAsdMxCMONNYnisdif8pNPVmUfg1MMgrs9RsUzObYPQilgN3DagN/E9ynwo0dJG5qLaPhuJUwEm67fuefB3+rpiJtkN5bQoNFMgbXsxb3Q',
    'bm_so': 'CAD2573C3583F1E89498085C9AD1106768EDECF41CBA637C19B68FFA3FD37979~YAAQiXcQAkF5AEWUAQAAEcYlRwJ7pHBXHbE1IlGJ0bu5c94Os06RzQ9RCpe/dJVIpfo31gcpfTKPAhAeROrnw1Ro12QSaK/nDKcQPg+4fM5mBrKe3JVbUPpQct0FHpPUruizgu3pmesYbdCH9jmzFjLpX9guuTtzRPQ7gZD5/RwTGiuzCRLeDIFR7DoLSyu/YrnGrSRWrkPmFaYN9KNZ9yXQk7mnJAtXf0UATVzt8K4vertNVArb+oux3J0+aJHhcDdTgmDK7EUiBM5bKgXIudEyQMSsIAtRvBPQri6Y7o0T4dZ9cUcFY+tNztxOXp9VNuY07FpgapJVn02Ar18/mQdS4stbVK2j5Dio3oMTomHgnPxSaKn1w22ekS1YAuZZ3hlPzJrYNV3TydsMhZ1muwTXUrazivt/b2SieDUi2OjYwR/XAsn/sQ+UUBE7LAvUayJ3K1cSzZgw8/Dzag==',
    'RT': '"z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5o6clx4&sl=0&tt=0&bcn=%2F%2F684dd329.akstat.io%2F&hd=1tseb"',
    '_ga_4DGGV4HV95': 'GS1.1.1736360445.19.0.1736360445.60.0.0',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736360445799__UDF43-m4_17ck',
    '_abck': '55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQiXcQAnZ5AEWUAQAA5sglRw1oG5BcMGdA1MXbAmsmzzo/rKuRjNNqGmguJhSFD2F25qAwsClc6bMI/qTtrFBRc9eVhB0M6cgmcapncucYESTKIVjyEcCSADGzGvekYFHwOempycjR3RGOXsN42hV67a1YPE/i+bQEyk87NZhgT8JMo2d1p7cxggJWSosM+IaZbBQg5sVsYUX7QoW5GlzjlPmxVt9XXO9e6LSweXi8allaDxeJ9CG1rNaKJoaMSUV9z1O9WRHBRRtCUTkmHdgG6ltYobD8UVVw6XTPmuQh5XrovvNAqhZUqybhLiUxqwNuIs/eV6/CSmL0rUgGstGa/rKtmy25I4zbM0X40ANZjbirg65SoZjWrcqBCnhKC4ZKPir/7uUTxcz67QQ4kTCIjG9CJRVJBJABRjR1v44JI5UqMkwR8rvbgXmsxwMRPgzjkXZkWenuoQsbGuaiuaAvMZfnl9DfLd9hej5trmqIkXSpN5TzvQymp45sMV4pvT/Nezr7IPUaGlqr8VGjGlQMIKuX3PqT8tP9IKZrDUTteVUaKg==~-1~||0||~1736360955',
    'bm_sz': 'D5C6D13E22DB7F88AF809C958F1EA446~YAAQiXcQAnd5AEWUAQAA5sglRxpzPhBiIBicdcSGIuVbKZM+wftpBDuwvpg8C8RyfNCHppGMmWt6IL/gCwui1cvfKkOtW2Zhlk2C9cnTn0ddSZDNBylFZVpJbjU1vn040TS8QwbzyQpDKcSahQ34qm3ZFgAfZi8ugDO6juyNaI5Y275gg1CBJhgWx/DSR+mrb+dn7TDyPwKajIBg9IAbDGaBe1kiSzXi13/QXUIVgNqXFeUMLQuqquGDc6kjjqpKjNBvNAplERmC1HqoOACVQoZEDB6frH2mdPZdiyPI3e6hhde6jk/hKYnBluf+o6iMh9wnFSA19YoOzMAxUvQu/vetVnqCBmKB6A395xkkBc4ZXqZ0MVB8FS+yVLEeFcPqQ25M78cKRJDjmKCVTz5F4bVxNzMx/dZ7Q33kXDgU9hD39dSCPUfOgPxPMPGpbEyAsOcXigeB5SavT4Y=~3227971~3425604',
    'UserSignUpAndSave': '52',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'mt.v=5.023471563.1735173098104; channelcloser=nonpaid; x-browser-id=ef39a6f2-8314-4f82-a0fa-363e49a57267; ab_qm=b; wishlist=%5B%5D; notice_preferences=%5B0%2C1%2C2%5D; _gcl_au=1.1.745756955.1735173104; _ga=GA1.1.417081306.1735173100; _scid=zniVhzQxtikyP_ORqzNgOBONUQNB32mF; _pin_unauth=dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA; QuantumMetricUserID=ce9e74e6acbef12e0916dd37bb958505; newsletterShownOnVisit=true; __olapicU=194fc6145839464cb3a8a92f2b8bb16e; _ScCbts=%5B%5D; x-commerce-next-id=17a7b974-4e70-4f46-bba0-c6138f386218; QSI_SI_0evq2NrkQkQaBb7_intercept=true; gl-feat-enable=CHECKOUT_PAGES_ENABLED; geo_ip=2a02:908:952:ae0:9555:feea:d337:c5a6; onesite_country=DE; AKA_A2=A; akacd_generic_prod_grayling_adidas=3913810152~rv=58~id=1570e6ece04d1e6cb308b949654224d1; bm_ss=ab8e18ef4e; akacd_plp_prod_adidas_grayling=3913810153~rv=64~id=c595ebca0321f4ebb91214de8d9617c4; x-original-host=adidas.co.uk; x-site-locale=en_GB; x-session-id=ea32ecf2-d60d-4e51-86e1-c0f87e2b36c2; wishlist=%5B%5D; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736962157%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736364557s%7CNONE%7CMCAID%7CNONE; s_cc=true; geo_country=DE; akacd_pdp_prod_adidas_grayling=3913810162~rv=24~id=411870ec2e76d18251111e6da7a3e0e3; checkedIfOnlineRecentlyViewed=true; persistentBasketCount=0; userBasketCount=0; pagecontext_cookies=; pagecontext_secure_cookies=; ak_bmsc=F108E8FD5DCCC071F3E43D2E545A9474~000000000000000000000000000000~YAAQyPIWAsu9sbeTAQAA7ff2RhqmyILOAcmalAPa5YiZ5K3nq0Yqe+e6/CNJhqGGgMJ8cwUjwTzLw7pxns0J42wPnN5yRItwzrnUiQP/XDLg/wRkCx0J7jKEgyGpcOEvTxHpwSqFRRM8yz8WJZb7f/ywTZcqmdnOd+az9Wo7zTtjz0T42FNN94ctPf9GXVcSSRTfkeirI4Nnfgdqi9kiuVTCuFHa91x+hpo0BM2zSDCBscoBwEkbKgypwgjjXYDmDtx48zjm2Vv8XrZubp5m736eeEKwDVYjMrrUneI6t1w8pZVnnKi4tjR+we2mehSGJeMPqCj5uFJxhgOJQisKqJiQDXqdweA+vQY99YZ29UCL0cJOuvtzj306bKtNVp6Lbtiss1VF4fwkvpn6ajqx9qic/uNZaMKkjUYFmACY4Bs=; bm_lso=BF9EB2E2F7D130FB955E5DACD526B9DF325FB2EBE2629001EC589F680CA4F0E1~YAAQyPIWAlG9sbeTAQAA3fH2RgLr+EA+7ANELfEJ6qqNMVOeB4OP1grL27umJf1GAfBnSOYrryk+aFcgd02QjNEoU5JlreCWvD39flJ6iyHWAaRNH+xVqetm5k3ve2D/W9tDuewkubT/+0eT4czTLJYGL+9CRcfKwztjxM0O9ieQ5uGU2nYMA5FgUEkOK9wJZ77aNmHyQQXzY/cGXySlBfQgWVzkf6YYfxVzvuZEH+voz0DR+Eu9ojlaUfcJ8cE1xPE7GJNqtaNcv71XLT2AcDzSZkh/h41NkdA2ZNuISlFsWtEsHu55WFekXQoA4P0N1Do84hTVsxiKuvgcynJB03/DC9cbIBG6Blzj672DDQh2BfwaQhrFQfn/JC7EY69MyZsG/ALBP0uxvU/hM9m9e7/+VLVpDI0C5mtqv1GF2clAKuBcMH/XBA1+ZJOtJCRX/NIXtrF4V9XJdlpMaW3rx0H5W1ZrOSGIsuyCGP2fY6YAgIhW^1736357379413; _rdt_uuid=1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7; _scid_r=1viVhzQxtikyP_ORqzNgOBONUQNB32mFZit9wQ; _uetsid=28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833; QuantumMetricSessionID=09f0879c17170bd8ba4b625ea9a9eb5d; _uetvid=c85e49c0c32011ef95a8e15267052ca8|1njkn52|1736360430417|1|1|bat.bing.com/p/insights/c/e; utag_main=v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:17$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1736362232913%3Bexp-session$ses_id:1736360432913%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:114%3Bexp-session$ab_dc:TEST%3Bexp-1741541381265$_prevpage:PRODUCT%7CSL%2072%20OG%20SCHUH%20(IE3425)%3Bexp-1736360983187; s_pers=%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D9%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736362232933%3B; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736357376682__UDF43-m4_17ck_6a476uL8m9Y%3D-8959-v2; geo_coordinates=lat=50.12, long=8.68; bm_s=YAAQiXcQAkB5AEWUAQAAEcYlRwLI59IcfS1jM3b29huAHHuqYzhzr+ia/V5BZr258qtrniI3THLM7+JY/CMPFvNE9RM5HJp7sAN7TFt4FZd/6s3L/YPq8QmeP9S2WCvYFlE4m5nSUvC70LD12g6ohjL99ActWPA72Xd40g72btQ7aDN45YYhCZKXWobL/Avanp6tF5BEMm3dybtsgFKyeQk1D0iyx+JDwZ2joP0x4fOEH3tyhIzAsdMxCMONNYnisdif8pNPVmUfg1MMgrs9RsUzObYPQilgN3DagN/E9ynwo0dJG5qLaPhuJUwEm67fuefB3+rpiJtkN5bQoNFMgbXsxb3Q; bm_so=CAD2573C3583F1E89498085C9AD1106768EDECF41CBA637C19B68FFA3FD37979~YAAQiXcQAkF5AEWUAQAAEcYlRwJ7pHBXHbE1IlGJ0bu5c94Os06RzQ9RCpe/dJVIpfo31gcpfTKPAhAeROrnw1Ro12QSaK/nDKcQPg+4fM5mBrKe3JVbUPpQct0FHpPUruizgu3pmesYbdCH9jmzFjLpX9guuTtzRPQ7gZD5/RwTGiuzCRLeDIFR7DoLSyu/YrnGrSRWrkPmFaYN9KNZ9yXQk7mnJAtXf0UATVzt8K4vertNVArb+oux3J0+aJHhcDdTgmDK7EUiBM5bKgXIudEyQMSsIAtRvBPQri6Y7o0T4dZ9cUcFY+tNztxOXp9VNuY07FpgapJVn02Ar18/mQdS4stbVK2j5Dio3oMTomHgnPxSaKn1w22ekS1YAuZZ3hlPzJrYNV3TydsMhZ1muwTXUrazivt/b2SieDUi2OjYwR/XAsn/sQ+UUBE7LAvUayJ3K1cSzZgw8/Dzag==; RT="z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5o6clx4&sl=0&tt=0&bcn=%2F%2F684dd329.akstat.io%2F&hd=1tseb"; _ga_4DGGV4HV95=GS1.1.1736360445.19.0.1736360445.60.0.0; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736360445799__UDF43-m4_17ck; _abck=55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQiXcQAnZ5AEWUAQAA5sglRw1oG5BcMGdA1MXbAmsmzzo/rKuRjNNqGmguJhSFD2F25qAwsClc6bMI/qTtrFBRc9eVhB0M6cgmcapncucYESTKIVjyEcCSADGzGvekYFHwOempycjR3RGOXsN42hV67a1YPE/i+bQEyk87NZhgT8JMo2d1p7cxggJWSosM+IaZbBQg5sVsYUX7QoW5GlzjlPmxVt9XXO9e6LSweXi8allaDxeJ9CG1rNaKJoaMSUV9z1O9WRHBRRtCUTkmHdgG6ltYobD8UVVw6XTPmuQh5XrovvNAqhZUqybhLiUxqwNuIs/eV6/CSmL0rUgGstGa/rKtmy25I4zbM0X40ANZjbirg65SoZjWrcqBCnhKC4ZKPir/7uUTxcz67QQ4kTCIjG9CJRVJBJABRjR1v44JI5UqMkwR8rvbgXmsxwMRPgzjkXZkWenuoQsbGuaiuaAvMZfnl9DfLd9hej5trmqIkXSpN5TzvQymp45sMV4pvT/Nezr7IPUaGlqr8VGjGlQMIKuX3PqT8tP9IKZrDUTteVUaKg==~-1~||0||~1736360955; bm_sz=D5C6D13E22DB7F88AF809C958F1EA446~YAAQiXcQAnd5AEWUAQAA5sglRxpzPhBiIBicdcSGIuVbKZM+wftpBDuwvpg8C8RyfNCHppGMmWt6IL/gCwui1cvfKkOtW2Zhlk2C9cnTn0ddSZDNBylFZVpJbjU1vn040TS8QwbzyQpDKcSahQ34qm3ZFgAfZi8ugDO6juyNaI5Y275gg1CBJhgWx/DSR+mrb+dn7TDyPwKajIBg9IAbDGaBe1kiSzXi13/QXUIVgNqXFeUMLQuqquGDc6kjjqpKjNBvNAplERmC1HqoOACVQoZEDB6frH2mdPZdiyPI3e6hhde6jk/hKYnBluf+o6iMh9wnFSA19YoOzMAxUvQu/vetVnqCBmKB6A395xkkBc4ZXqZ0MVB8FS+yVLEeFcPqQ25M78cKRJDjmKCVTz5F4bVxNzMx/dZ7Q33kXDgU9hD39dSCPUfOgPxPMPGpbEyAsOcXigeB5SavT4Y=~3227971~3425604; UserSignUpAndSave=52',
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
    'x-instana-l': '1,correlationType=web;correlationId=5a202ec1af1d691a',
    'x-instana-s': '5a202ec1af1d691a',
    'x-instana-t': '5a202ec1af1d691a',
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
                print(f"{i}.th item in this cycle\n{product_info}")

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
        #Previous tries: 2min/500r, 2min/350, 10m/700r
        if i%700==0:
            time.sleep(randint(1200, 1300))


        #Enable it when I find a solution for proxy rotation
        #if response.status_code == 403:
            #rotate_VPN(settings)


        if response.status_code == 200:
            print(f'{i}.th item in this cycle\n')
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





