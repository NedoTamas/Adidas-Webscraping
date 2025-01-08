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

#---memory---
block_occured=False


print(product_data_path)
print(product_data_availability_path)





#look for the "personalizationengine" POST request
#a cookie can survive circa 30 mins
#an ip can survive around 1000 requests for availability


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
    'gl-feat-enable': 'CHECKOUT_PAGES_ENABLED',
    'geo_ip': '2a02:908:952:ae0:7981:9e6:a06f:3bad',
    'onesite_country': 'DE',
    'akacd_generic_prod_grayling_adidas': '3913732872~rv=94~id=3336b890b330edab770b061a66e958c6',
    'akacd_plp_prod_adidas_grayling': '3913732872~rv=68~id=a9762bc9929f43752474b06e398d7c91',
    'x-session-id': '6844e51b-229e-4575-a00c-e8eb3845c5c8',
    'wishlist': '%5B%5D',
    'AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg': '1',
    's_cc': 'true',
    'QSI_SI_0evq2NrkQkQaBb7_intercept': 'true',
    'x-site-locale': 'de_DE',
    'x-original-host': 'www.adidas.de',
    'x-environment': 'production',
    'akacd_pdp_prod_adidas_grayling': '3913733001~rv=86~id=097dffb1c40917fdb98c4bccd5d7220d',
    'checkedIfOnlineRecentlyViewed': 'true',
    'persistentBasketCount': '0',
    'userBasketCount': '0',
    'pagecontext_cookies': '',
    'pagecontext_secure_cookies': '',
    's_sess': '%5B%5BB%5D%5D',
    'QuantumMetricSessionID': 'e1f7ee138d2291cd3f0b1eea95ab0e66',
    'bm_ss': 'ab8e18ef4e',
    'ak_bmsc': 'D8D4484297FD7D117252EC73A04910AC~000000000000000000000000000000~YAAQRiTDF0YjeO6TAQAAzNFgQxr4viKE0UaSwbo/ClyjXpkpouFolcrO7nnvnXoKcYxZXfuHcAi7xptF0PC3DtHCyAMFBXn7jk741ISnsg9QQnAOGWg7isunzK1hhg4I35o3I7CMrEW4apFkphJU0VEY5VKwzJ0JQzqHNkd/Ck1h+WaFev1xU9ETx6tXaeXrbyZt7AY77aunU/eNuHQYPLM7Agodzhzg5i2yocBoNiAxOTREGcBb+3Fo9UD6u1AUfHhuk08HoWLQPfEfXbzfsQQztXem4Ixm5sACkg2/J7NcRRNJiGFwaBYLyoKAVxXBfxEz8pXXh6Gv7Tt1Y3sintVxuRWX/cNtMPe7A3DaIIlAlKTuXckdiOGc3QsHtzQ6NhswhXIND0JBZQ==',
    's_pers': '%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D7%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736299012018%3B',
    'utag_main': 'v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:15$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1736299011555%3Bexp-session$ses_id:1736297211555%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:108%3Bexp-session$ab_dc:TEST%3Bexp-1741481211564$_prevpage:PRODUCT%7CSAMBA%20OG%20SCHUH%20(JI2734)%3Bexp-1736300811969',
    'bm_lso': '9F00459A29C41905B2A3FC3C3FF1463FAEA4BBC3B6BAC1A4EC27261B6A4EF0FF~YAAQRiTDF/8ceO6TAQAAN8FgQwIn1mkCgIDOjHk2CZdi9sYQTG4Lz6laNO2Ot/eqkFMvjEJ2B2BIXPWYoJegHIpX6zSo9KpxDbH4M5NNV7Bh7Q3ManBnXBpJO6oaJYzcbpRrBbtswqqkiT5aAhEIhvU5q6AU6+AUEogBDAZrsGoQHpOVIBHikXoOJWEsk7Jz5hjRs+LHIfsF8iANzx5WB3d5vW3ZYJEcYymVuAhXkdpp6ed6cvRbLbA4f3Rxej+1q5TsuAwO6GQUc5ughA+CCFGrnP95ISv++m4SvIdNkMsvUtLZkcEQv93/OCohtzceaj62dBJEHgzAamzemO9VtB86sn4rS744FUxY+6F7p6cmPiq2mguGeiz7dLutIkO38zmjy4mt2s33vIKcLs/JMmjSj7cnpnsL4uEXBZiLewmlmFv07zhHym5uWD9U5cdk2lvjep4QC7f0evyNwjQ=^1736297212110',
    '_uetsid': '28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833',
    '_uetvid': 'c85e49c0c32011ef95a8e15267052ca8|9yjkhb|1736297213055|3|1|bat.bing.com/p/insights/c/o',
    '_rdt_uuid': '1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7',
    'AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736902014%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736304414s%7CNONE%7CMCAID%7CNONE',
    '_scid_r': '0fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9zA',
    'geo_country': 'DE',
    'geo_coordinates': 'lat=51.22, long=6.77',
    'bm_s': 'YAAQRiTDF7VFeO6TAQAAcDRhQwIg6bkQKlQ44m59H2E13ItEAxRkhh6+TIWnZS/JHI4/Qah99S9AQt5AE8wM0PSC0pDu4Q76zB/oOuSp5J0090etNCLhQfRDITaRKOUci5JNoYAgsDV02AAmKVPHSBWIaAoxY5pkC6spMn6w2RoIzmPgAFiRyWkt7PX57NEzNqsHVofPjyHv3DRviTWGTmkrSqZnrJoI5/W5Pw4+xYv95GMK90sXbtw3ry0Xb8sZmQndAdu8AQfubzyxKF0ovXUrA6ukt3PVtE0S2Z2R9M26rRX+6AUO2mkWtfPoCL5EFUozdeiF1vq2ip8nqnOeRO1F4NI+',
    'bm_so': '8AB6CBF265CCBE3661E3CFF449388802AAE15F1C252D7F3BFFCBB5B2D52E5615~YAAQRiTDF7ZFeO6TAQAAcDRhQwK5ViEVBqkdC3J+xCOvMYiWMPqptvwu0e6MklvYodc69gO8ZtDvlWXr+R/iDX/dDcxwiuP8nTn/BuKpal1BwuS9BXQgXloQH0xrZ3u6rS456NvbCLWdqWKUZTC1FRlqEZtw4P7h5fHsGAxIB0Ss2SGKMrs4cdz5ITSEbjihQt9TiRRuXwMNhOWIpt5pAn7QeSgpAqd+Pk8UJaE0TrhDe90qghBjM5wfuI0qWRbgSr1HUwck8Dts9DDZwpQ5/NunzlNBGc07BPSS+NiJabGdlDaeYlCOIuMn/ZUcdikj4RtMdk41VsfzOvOe6uRJdpyVYZnl3rz9KSSIj2Pi9qh3eItDRfe0HNbJI0g2iPpEwkwYNNA1JaB1S2xh+ELEa6ScuDjChHaeUvWyKl2HGVFKj64IFQANdSehQTlCCajp8ogFDuBMSK5RxIN+pQc=',
    'bm_sz': 'BAE36CFE292B68C412D8AACF62EEA433~YAAQRiTDF7dFeO6TAQAAcDRhQxp+gLkRAA1Cx51DGqphoKiJcfCW7miy8kyZAh6ntHJJIUhSUeVealmbMuCbjsMwii3YGibMIKYZJ2CeAo9Dn8x9UQvtv7EvWN+jenofmYFP2QGsOp047sPXU7HyDnHhw+o4vCXnXoWJtWlTU/2Myn8anb24UMgKndur8npiOMH1Ouv2dYy0AVNlw3gC0pZ/IJLaoFScMBUR0hwNU4oUYNM6tzOwym6tvqvLw7YMXfk2+1/wQ6UFZvjnQ8bfEiI856DSkmrlro+svkp8gUgpJ9B9CgaxU5taF++UlMhbrVRj98NAO7vltV2OZ79zwlObYFSzZbdhNp1c7b8vBeb4fXgJiU5Vxcn2+ycV/cRlKfFLtLXjAd5DkaLUGZ0yDcUhPoV5Tg646FWnqZGTdf0EK6K4DIZr42TpvnA4~3225923~3748919',
    'RT': '"z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5n6irpv&sl=0&tt=0&bcn=%2F%2F173bf10c.akstat.io%2F&ld=3m6or&hd=qlo"',
    '_ga_4DGGV4HV95': 'GS1.1.1736297202.17.1.1736297231.31.0.0',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736297232135__UDF43_17ck_KJ05AZbSKkU%3D-7565-v2',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736297232135__UDF43_17ck_KJ05AZbSKkU%3D-7565-v2',
    '_abck': '55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQRiTDF5lGeO6TAQAAdzdhQw2WMIlVRkQdGkyKDxmiSGt1hw94km4/KW0BUG0I/mB1r3YgqVjl1Q8kTXeSXlPw6qqHSTvHtx7dNo2U6F5aiducV6GbvTuKErqK0EKPsHWxYEw8XFWJlk/ew8y67tX7StAwuZkHR2czst2AXth6dalCx/Bs+eiXmYmlK7cqakSQVSaIfIkMOwA2OQqRtBJKbMV5w0l7gmo1cVeJ31AFySrQGYPqDrzKMrs5+lTCb9oNkod17YqgfrvACkfH0CX5ByWQi4+Ibm6Qyt70CVSTYL4PKGvaUaJFXkFpBPDlBW4vRtoVxODp5s08oJxoyREjC/PqtL25S1ESe+torVzqKg7sJmhtxDDa2L0WUAdvWRhvmFRweMv8jO6LgRPzwfJiP0UOd6pzADdgwDC/WOt29TLze/8lCAKDIGy6KS2WCyjyTeJev+5AkLbiPwoEERU1VJRYHxny75s4ZVDtXLSxiCu5O7bTD4Ow3JYRV86M/bsxxgnTa2SELchQA7ip1ui9GQ9YDMivONar+WEfFkU9+6hBlQ==~-1~-1~1736294478',
    'UserSignUpAndSave': '49',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'mt.v=5.023471563.1735173098104; channelcloser=nonpaid; x-browser-id=ef39a6f2-8314-4f82-a0fa-363e49a57267; ab_qm=b; wishlist=%5B%5D; notice_preferences=%5B0%2C1%2C2%5D; _gcl_au=1.1.745756955.1735173104; _ga=GA1.1.417081306.1735173100; _scid=zniVhzQxtikyP_ORqzNgOBONUQNB32mF; _pin_unauth=dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA; QuantumMetricUserID=ce9e74e6acbef12e0916dd37bb958505; newsletterShownOnVisit=true; __olapicU=194fc6145839464cb3a8a92f2b8bb16e; _ScCbts=%5B%5D; x-commerce-next-id=17a7b974-4e70-4f46-bba0-c6138f386218; gl-feat-enable=CHECKOUT_PAGES_ENABLED; geo_ip=2a02:908:952:ae0:7981:9e6:a06f:3bad; onesite_country=DE; akacd_generic_prod_grayling_adidas=3913732872~rv=94~id=3336b890b330edab770b061a66e958c6; akacd_plp_prod_adidas_grayling=3913732872~rv=68~id=a9762bc9929f43752474b06e398d7c91; x-session-id=6844e51b-229e-4575-a00c-e8eb3845c5c8; wishlist=%5B%5D; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; s_cc=true; QSI_SI_0evq2NrkQkQaBb7_intercept=true; x-site-locale=de_DE; x-original-host=www.adidas.de; x-environment=production; akacd_pdp_prod_adidas_grayling=3913733001~rv=86~id=097dffb1c40917fdb98c4bccd5d7220d; checkedIfOnlineRecentlyViewed=true; persistentBasketCount=0; userBasketCount=0; pagecontext_cookies=; pagecontext_secure_cookies=; s_sess=%5B%5BB%5D%5D; QuantumMetricSessionID=e1f7ee138d2291cd3f0b1eea95ab0e66; bm_ss=ab8e18ef4e; ak_bmsc=D8D4484297FD7D117252EC73A04910AC~000000000000000000000000000000~YAAQRiTDF0YjeO6TAQAAzNFgQxr4viKE0UaSwbo/ClyjXpkpouFolcrO7nnvnXoKcYxZXfuHcAi7xptF0PC3DtHCyAMFBXn7jk741ISnsg9QQnAOGWg7isunzK1hhg4I35o3I7CMrEW4apFkphJU0VEY5VKwzJ0JQzqHNkd/Ck1h+WaFev1xU9ETx6tXaeXrbyZt7AY77aunU/eNuHQYPLM7Agodzhzg5i2yocBoNiAxOTREGcBb+3Fo9UD6u1AUfHhuk08HoWLQPfEfXbzfsQQztXem4Ixm5sACkg2/J7NcRRNJiGFwaBYLyoKAVxXBfxEz8pXXh6Gv7Tt1Y3sintVxuRWX/cNtMPe7A3DaIIlAlKTuXckdiOGc3QsHtzQ6NhswhXIND0JBZQ==; s_pers=%20pn%3D4%7C1738872236699%3B%20s_vnum%3D1738368000852%2526vn%253D7%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736299012018%3B; utag_main=v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:15$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1736299011555%3Bexp-session$ses_id:1736297211555%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:108%3Bexp-session$ab_dc:TEST%3Bexp-1741481211564$_prevpage:PRODUCT%7CSAMBA%20OG%20SCHUH%20(JI2734)%3Bexp-1736300811969; bm_lso=9F00459A29C41905B2A3FC3C3FF1463FAEA4BBC3B6BAC1A4EC27261B6A4EF0FF~YAAQRiTDF/8ceO6TAQAAN8FgQwIn1mkCgIDOjHk2CZdi9sYQTG4Lz6laNO2Ot/eqkFMvjEJ2B2BIXPWYoJegHIpX6zSo9KpxDbH4M5NNV7Bh7Q3ManBnXBpJO6oaJYzcbpRrBbtswqqkiT5aAhEIhvU5q6AU6+AUEogBDAZrsGoQHpOVIBHikXoOJWEsk7Jz5hjRs+LHIfsF8iANzx5WB3d5vW3ZYJEcYymVuAhXkdpp6ed6cvRbLbA4f3Rxej+1q5TsuAwO6GQUc5ughA+CCFGrnP95ISv++m4SvIdNkMsvUtLZkcEQv93/OCohtzceaj62dBJEHgzAamzemO9VtB86sn4rS744FUxY+6F7p6cmPiq2mguGeiz7dLutIkO38zmjy4mt2s33vIKcLs/JMmjSj7cnpnsL4uEXBZiLewmlmFv07zhHym5uWD9U5cdk2lvjep4QC7f0evyNwjQ=^1736297212110; _uetsid=28722e60cd3211efb75e39c5dcecade1|1jp1rs4|2|fse|0|1833; _uetvid=c85e49c0c32011ef95a8e15267052ca8|9yjkhb|1736297213055|3|1|bat.bing.com/p/insights/c/o; _rdt_uuid=1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20097%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736902014%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736304414s%7CNONE%7CMCAID%7CNONE; _scid_r=0fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9zA; geo_country=DE; geo_coordinates=lat=51.22, long=6.77; bm_s=YAAQRiTDF7VFeO6TAQAAcDRhQwIg6bkQKlQ44m59H2E13ItEAxRkhh6+TIWnZS/JHI4/Qah99S9AQt5AE8wM0PSC0pDu4Q76zB/oOuSp5J0090etNCLhQfRDITaRKOUci5JNoYAgsDV02AAmKVPHSBWIaAoxY5pkC6spMn6w2RoIzmPgAFiRyWkt7PX57NEzNqsHVofPjyHv3DRviTWGTmkrSqZnrJoI5/W5Pw4+xYv95GMK90sXbtw3ry0Xb8sZmQndAdu8AQfubzyxKF0ovXUrA6ukt3PVtE0S2Z2R9M26rRX+6AUO2mkWtfPoCL5EFUozdeiF1vq2ip8nqnOeRO1F4NI+; bm_so=8AB6CBF265CCBE3661E3CFF449388802AAE15F1C252D7F3BFFCBB5B2D52E5615~YAAQRiTDF7ZFeO6TAQAAcDRhQwK5ViEVBqkdC3J+xCOvMYiWMPqptvwu0e6MklvYodc69gO8ZtDvlWXr+R/iDX/dDcxwiuP8nTn/BuKpal1BwuS9BXQgXloQH0xrZ3u6rS456NvbCLWdqWKUZTC1FRlqEZtw4P7h5fHsGAxIB0Ss2SGKMrs4cdz5ITSEbjihQt9TiRRuXwMNhOWIpt5pAn7QeSgpAqd+Pk8UJaE0TrhDe90qghBjM5wfuI0qWRbgSr1HUwck8Dts9DDZwpQ5/NunzlNBGc07BPSS+NiJabGdlDaeYlCOIuMn/ZUcdikj4RtMdk41VsfzOvOe6uRJdpyVYZnl3rz9KSSIj2Pi9qh3eItDRfe0HNbJI0g2iPpEwkwYNNA1JaB1S2xh+ELEa6ScuDjChHaeUvWyKl2HGVFKj64IFQANdSehQTlCCajp8ogFDuBMSK5RxIN+pQc=; bm_sz=BAE36CFE292B68C412D8AACF62EEA433~YAAQRiTDF7dFeO6TAQAAcDRhQxp+gLkRAA1Cx51DGqphoKiJcfCW7miy8kyZAh6ntHJJIUhSUeVealmbMuCbjsMwii3YGibMIKYZJ2CeAo9Dn8x9UQvtv7EvWN+jenofmYFP2QGsOp047sPXU7HyDnHhw+o4vCXnXoWJtWlTU/2Myn8anb24UMgKndur8npiOMH1Ouv2dYy0AVNlw3gC0pZ/IJLaoFScMBUR0hwNU4oUYNM6tzOwym6tvqvLw7YMXfk2+1/wQ6UFZvjnQ8bfEiI856DSkmrlro+svkp8gUgpJ9B9CgaxU5taF++UlMhbrVRj98NAO7vltV2OZ79zwlObYFSzZbdhNp1c7b8vBeb4fXgJiU5Vxcn2+ycV/cRlKfFLtLXjAd5DkaLUGZ0yDcUhPoV5Tg646FWnqZGTdf0EK6K4DIZr42TpvnA4~3225923~3748919; RT="z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5n6irpv&sl=0&tt=0&bcn=%2F%2F173bf10c.akstat.io%2F&ld=3m6or&hd=qlo"; _ga_4DGGV4HV95=GS1.1.1736297202.17.1.1736297231.31.0.0; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736297232135__UDF43_17ck_KJ05AZbSKkU%3D-7565-v2; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736297232135__UDF43_17ck_KJ05AZbSKkU%3D-7565-v2; _abck=55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQRiTDF5lGeO6TAQAAdzdhQw2WMIlVRkQdGkyKDxmiSGt1hw94km4/KW0BUG0I/mB1r3YgqVjl1Q8kTXeSXlPw6qqHSTvHtx7dNo2U6F5aiducV6GbvTuKErqK0EKPsHWxYEw8XFWJlk/ew8y67tX7StAwuZkHR2czst2AXth6dalCx/Bs+eiXmYmlK7cqakSQVSaIfIkMOwA2OQqRtBJKbMV5w0l7gmo1cVeJ31AFySrQGYPqDrzKMrs5+lTCb9oNkod17YqgfrvACkfH0CX5ByWQi4+Ibm6Qyt70CVSTYL4PKGvaUaJFXkFpBPDlBW4vRtoVxODp5s08oJxoyREjC/PqtL25S1ESe+torVzqKg7sJmhtxDDa2L0WUAdvWRhvmFRweMv8jO6LgRPzwfJiP0UOd6pzADdgwDC/WOt29TLze/8lCAKDIGy6KS2WCyjyTeJev+5AkLbiPwoEERU1VJRYHxny75s4ZVDtXLSxiCu5O7bTD4Ow3JYRV86M/bsxxgnTa2SELchQA7ip1ui9GQ9YDMivONar+WEfFkU9+6hBlQ==~-1~-1~1736294478; UserSignUpAndSave=49',
    'origin': 'https://www.adidas.de',
    'priority': 'u=1, i',
    'referer': 'https://www.adidas.de/samba-og-schuh/JI2734.html',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-instana-l': '1,correlationType=web;correlationId=560070afafc52f2',
    'x-instana-s': '560070afafc52f2',
    'x-instana-t': '560070afafc52f2',
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

    #Saving out just the codes to iterate through it later on. It will recreate the file for the ongoing cycle.
    df.to_csv('raw_codes.csv', index=False)
    print('raw_code_list generated')
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


#url = f'https://www.adidas.de/api/products/IF9427/availability'
#response = requests.get(url, cookies=cookies, headers=headers, impersonate="chrome120")
#soup = BeautifulSoup(response.text, "html.parser")
#print(soup.prettify)

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

        #if i%500==0:
            #time.sleep(randint(100, 150))


        #Enable when find a solution for proxy rotation
        #if response.status_code == 403:
            #rotate_VPN(settings)


        if response.status_code == 200:
            print(i)
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

def get_last_successful_item():
    try:
        with open(memory, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                item, status = line.strip().split(',')
                if status == "success":
                    return item
    except FileNotFoundError:
        return None
    return None

def update_memory(category_name, status):
    with open(memory, "a") as file:
        file.write(f"{category_name},{status}\n")

def memory_decision(block_occured, category_name):

    status = "403_error" if block_occured else "success"
    update_memory(category_name, status)

    if block_occured:
        print(f"403 error encountered for {category_name}. Stopping execution.")
        

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





