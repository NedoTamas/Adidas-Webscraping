from curl_cffi import requests
from bs4 import BeautifulSoup
import asyncio
import time
from random import randint
import re
import pandas as pd
import os
import json


root = os.getcwd()
bronze_path=os.path.join(root,"bronze")
silver_path=os.path.join(root,"silver")
gold_path=os.path.join(root,"gold")

product_data_path=os.path.join(bronze_path,'product_data.csv')
product_data_availability_path=os.path.join(bronze_path,'product_data_availability.csv')



#look for the "personalizationengine" POST request
#a cookie can survive circa 30 mins
#an ip can survive around 1000 requests for availability

cookies = {
    'mt.v': '5.023471563.1735173098104',
    'channelcloser': 'nonpaid',
    'x-browser-id': 'ef39a6f2-8314-4f82-a0fa-363e49a57267',
    'x-commerce-next-id': 'fd64b71c-e602-4579-ad92-380944173704',
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
    'geo_ip': '2a02:908:952:ae0:c806:7ee2:6437:64a1',
    'onesite_country': 'DE',
    'geo_coordinates': 'lat=51.22, long=6.77',
    'gl-feat-enable': 'CHECKOUT_PAGES_DISABLED',
    'akacd_plp_prod_adidas_grayling': '3913463669~rv=90~id=15a69613aa9c95400bee1301cf515642',
    'x-session-id': '1e39d2dd-b217-4c64-a137-161524662742',
    'wishlist': '%5B%5D',
    'AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg': '1',
    's_cc': 'true',
    '_ScCbts': '%5B%5D',
    'QSI_SI_0evq2NrkQkQaBb7_intercept': 'true',
    'akacd_pdp_prod_adidas_grayling': '3913464524~rv=61~id=b4cd11ec60df57f336f236e50f460d0b',
    'checkedIfOnlineRecentlyViewed': 'true',
    'pagecontext_cookies': '',
    'pagecontext_secure_cookies': '',
    'persistentBasketCount': '0',
    'userBasketCount': '0',
    'akacd_generic_prod_grayling_adidas': '3913465445~rv=99~id=fe76c8da60a5c7dcc762281e4736d268',
    'x-original-host': 'adidas.co.uk',
    'x-site-locale': 'en_GB',
    's_sess': '%5B%5BB%5D%5D',
    'AKA_A2': 'A',
    'bm_ss': 'ab8e18ef4e',
    'AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20093%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736624201%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736026601s%7CNONE%7CMCAID%7CNONE',
    'bm_lso': '57FEB4746E31E158694BCAC6833688A0D162A188D042A7FD891401F2826B78B2~YAAQP2ETAj/IZL2TAQAAgwvVMgKD4JmUMgBfFkOo+97TvzhU3dZNmcmFlbL98o2oQHlrSAsoj6z+RDx9EtWUMJ2zrUbh7ryHc5bCC37IRHbIp+oWQdPZqiLO6QRhu6Wj2xDAWswUzJlPkp8Ztnyn1SkEdR0LUQyhAtwv4ZKP7xMEngCmdNPnJahMBXSRre9NJ3sa2l0Htk2oY2FGF4VJCStEDT7tJFOHQAfBRFWmvq8l3GoO2Tl4vp7/8HSMa0gWGLjrLcqt13ofBMgu50P+0X3sw41BqQ0YM+2AoA4gY4hZYCAuAjS0dOyVFW0DzVTfREuBhRYv69yYCyqVSbIRJNy8E+hqVoVr4/44/z7CDKH0KhGR0M93uook/mQ8DezmMG39XwrQasXhk3dq2Pli/D3qHOJ04FIR5BS0NvYvWCZX4S749eGslsTvKd6VNat0sGpCiCT9rZ60hPTw+vrqYWG6W2QpE9KKAyqHU7eHSRWoDdmx^1736019615417',
    'geo_country': 'DE',
    'ak_bmsc': 'B678F1D83A33D5D1DA38BAF8D949D7AD~000000000000000000000000000000~YAAQP2ETAr/KZL2TAQAAwjHVMhoEMPp/2zrJngBnlJ994wwczHfvp5hI47Ym5gqAZBy7oCU7lLvRlU1rjkPu5fjUDAm2XKbhMjpj/YPDv7cg+/YYsOhe3fEDYxpJU6VnlemB37hYMZFzr+IfbXReSDONNQts47OrbmyqkUF1wiUWHINWkpQdHjFhp8+nhFq5g7XmA2CIaCtgdtlcVRcEhatteLEDFKE/KjpW5zW6p651tqR6D0bp1l31t5r1ot1EfKYsQTJl0eCJ4Gg+RJ3a7y3JdaFCC1cDcyF9pN+YbneoBAxs6+KWvFixhvkm8UiX4Ahbgy3VsgXtTwYLsHqbbP+ae8IPZl5ENiQBtpl0uiL/EFsgNexfgBZndkIXLxZjcza9DYcg5DOiA39VeVo6VVZoFjUukIsFWaz95jia6eM=',
    '_rdt_uuid': '1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7',
    '_scid_r': '1PiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9oQ',
    '_uetsid': '5b24d730cabf11efa6b3510e5981e55b|81jus|2|fsa|0|1830',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736019396618__UDF43-m4_17ck_6gHvoNfPOCk%3D-1481-v2',
    '_uetvid': 'c85e49c0c32011ef95a8e15267052ca8|zr11dq|1736020138229|6|1|bat.bing.com/p/insights/c/u',
    'QuantumMetricSessionID': 'ee1c216dee99bf30b0b82c155f762853',
    'utag_main': 'v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:10$_se:5%3Bexp-session$_ss:0%3Bexp-session$_st:1736021938953%3Bexp-session$ses_id:1736019400807%3Bexp-session$_pn:2%3Bexp-session$_vpn:2%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:79%3Bexp-session$ab_dc:TEST%3Bexp-1741203400815$_prevpage:PLP%7CG_MEN%7CPT_TRAINERS%3Bexp-1736023215814',
    's_pers': '%20pn%3D2%7C1737781118250%3B%20s_vnum%3D1738368000852%2526vn%253D2%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736021938969%3B',
    'bm_so': '539A6D6EF2C9ACB3791394C72530B79F9AC47A024492B970BAC8DC2F6EBB71B3~YAAQH7IPF5Id/ZqTAQAAYTvdMgLhQ0YHcMd6+TNBKlhVJqva82D9cWM+uTRZrnk6PuDrODiul+4ODG/7oZGVV7Ux83Mixk6D55Ey6J/PDDrTwQ39C5Ral3obedpIvgqGuMSuck0UOAlfM9W331mq85Zx4brPTe7u39CtbPuARlXcdQg+v+AnFyTlgK1n+YDk7edE6VziaiPQtwEGFgA4NdpSYa+T+h1PkVMTPCwE1EY0V1fePbV5KIBGpAzHpyYxuqkXQzB362SoWte4rhVuqK1d0RlEDsOjL01d9twchxoVkyfl/XZgxG1cqdr3wYT6BMCnqRbHNA0TfmublI5xqmhgHHCU/vHIv/gdlSOcAW9BxAkdTL4P+kaZSJN935rJFmiCaXt1mlXW53zELAFFYcgP/93QJTG9cpfuO+NGgvlhS9RquNLYiPSU4lAJP2dWAVWD7iSVJPQupFkhkMD0NSgSz9FXJZWkfbwfRxXavtduo432',
    'bm_s': 'YAAQH7IPF/wd/ZqTAQAAIVrdMgJzOD+z3BWWVP0qzURYN0PR/QICfm/ehNDWWoVWHMGDzXgnYpHYSf1BYov/FbV8EzkO0Nvf/griTrb0vD0rbyR8egF9BegW38gczjNB6ItBBXGqLs7YlXLYX+LYWb4KjEEc6PMmwLS7XzJPV+CGu67NSZ97QnF9dxRAxB+m37NRZ67gXkhLAKPme64ljl4iw7IU06q9Blm4APO1U4z6LyECHQlg6yvb05JOVzLzpHNPLnXK/oUx1WmunoMhcOqCLcSVhmvDAh3ZvQy2/ZTqn8WFtEyAGVV7VgkQNAiMIochPOsFgMaAbDCDy54dAJdLLW3u',
    'bm_sz': 'B94C8E03BCBE4059402F5EE5931A975E~YAAQH7IPF/0d/ZqTAQAAIVrdMhoeOBqcz0y+Xs+sOsLEI10oIfyiJTlRVGeVJk0bK6OQF60cetdAOpe5mAHPMwhQhqTNW2A757ZemqZtl9nJk9vBwg4FOqQtg00YVmsY4LbgGhz1McfQdB/SWO/GUJuv2tKDlLUp+jm4OR0KPazXYe1oDNLDK/gh4mvi2aCqBUobp5HdVkTVrX83PgPUEFKngsihNF3fflLq+fm+HVcCU8wFVg6LYyMGJN3OpTXt2/IgeAkf4RZbqy3TwAKHgYh2dgUQ3CP992b8r69YsvH7sBd2HJSt9kaGjWKGQGEKBAayu7soa2XsawH6eWmTZjdmyvgJeCLDZIIc8PASk5GdwDYSlJZK+dETsA/UJzx4KOoj703c88yHm6tVweoKVvrpeUzxIu4xp44VoFRoBuMSNhty0TcmWrwESP2mKjbjAOa/B8yAR6QXf4OYN2yMz+4HxczwY9CJmA3AZIT6z2ClKx37qXfi0FNBbwng+OOjQkXDo1wLDJs/lB1XrQdQurjMpfxtrJ8NhBQ6V15Lg8k9BMHFxxpC8Dp2Wo8u/RruGSn2rdSDBo25usq4W5JV5DdtjdiQmgLcH1AQ~3682630~4470597',
    'RT': '"z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5il4isw&sl=0&tt=0&bcn=%2F%2F684dd330.akstat.io%2F&hd=g6fh"',
    '_ga_4DGGV4HV95': 'GS1.1.1736019396.11.1.1736020150.60.0.0',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1736020151015__UDF4_17ck',
    '_abck': '55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQH7IPFwQe/ZqTAQAAcVzdMg2IOHTW+1oW01udkcYF8Ri7ZjO/be5sssLdpqbLR2yuLNLJfUSJeVX/wm+Wzb7R1WIT9vxThAbDEg0SOQCArXTINcnrypBbZ2eof3xiULN70kQ9aa2sHdkPF90G7NHSGjjskNWz7bqQ8+TqRaSHUIgCPmr+co7RjksjCan8PZ7X7fsNa2sM4wn4uYuZa0JGsGNR9mgi4vu//3tZWql8j0AmU06tc5gDWcBaq/l7eQaWIceF7O5mXkCMCweqsJYRxnUrMO+WstZFY/1ItPlR0ROUbNZFgmxnudydFep2IPmLOmRtgz1/ScAsZg6LkDprmGU0bcHxR8P2KaGxfwp7gHgtpUnc6GQaT73v+w2xH1aWIseuiZEgjPhr0h3JYgxq9ZNFZFjF+tn+dyAAM1T4Vhi2sV/Di4HsBU5sPcM3ou6V71YffGaV2Oa8LNZ8bJhtR9mPMiCRl4FybqlXdEXtuj2mtY8fW4vFqnfG1CavNneUBf0X6vd6bwNAPEpry+sERCYfXsxaINUn+JgrpmzOdcY=~-1~-1~1736022990',
    'UserSignUpAndSave': '40',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'mt.v=5.023471563.1735173098104; channelcloser=nonpaid; x-browser-id=ef39a6f2-8314-4f82-a0fa-363e49a57267; x-commerce-next-id=fd64b71c-e602-4579-ad92-380944173704; ab_qm=b; wishlist=%5B%5D; notice_preferences=%5B0%2C1%2C2%5D; _gcl_au=1.1.745756955.1735173104; _ga=GA1.1.417081306.1735173100; _scid=zniVhzQxtikyP_ORqzNgOBONUQNB32mF; _pin_unauth=dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA; QuantumMetricUserID=ce9e74e6acbef12e0916dd37bb958505; newsletterShownOnVisit=true; __olapicU=194fc6145839464cb3a8a92f2b8bb16e; geo_ip=2a02:908:952:ae0:c806:7ee2:6437:64a1; onesite_country=DE; geo_coordinates=lat=51.22, long=6.77; gl-feat-enable=CHECKOUT_PAGES_DISABLED; akacd_plp_prod_adidas_grayling=3913463669~rv=90~id=15a69613aa9c95400bee1301cf515642; x-session-id=1e39d2dd-b217-4c64-a137-161524662742; wishlist=%5B%5D; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; s_cc=true; _ScCbts=%5B%5D; QSI_SI_0evq2NrkQkQaBb7_intercept=true; akacd_pdp_prod_adidas_grayling=3913464524~rv=61~id=b4cd11ec60df57f336f236e50f460d0b; checkedIfOnlineRecentlyViewed=true; pagecontext_cookies=; pagecontext_secure_cookies=; persistentBasketCount=0; userBasketCount=0; akacd_generic_prod_grayling_adidas=3913465445~rv=99~id=fe76c8da60a5c7dcc762281e4736d268; x-original-host=adidas.co.uk; x-site-locale=en_GB; s_sess=%5B%5BB%5D%5D; AKA_A2=A; bm_ss=ab8e18ef4e; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20093%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1736615667%7C6%7CMCAAMB-1736624201%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1736026601s%7CNONE%7CMCAID%7CNONE; bm_lso=57FEB4746E31E158694BCAC6833688A0D162A188D042A7FD891401F2826B78B2~YAAQP2ETAj/IZL2TAQAAgwvVMgKD4JmUMgBfFkOo+97TvzhU3dZNmcmFlbL98o2oQHlrSAsoj6z+RDx9EtWUMJ2zrUbh7ryHc5bCC37IRHbIp+oWQdPZqiLO6QRhu6Wj2xDAWswUzJlPkp8Ztnyn1SkEdR0LUQyhAtwv4ZKP7xMEngCmdNPnJahMBXSRre9NJ3sa2l0Htk2oY2FGF4VJCStEDT7tJFOHQAfBRFWmvq8l3GoO2Tl4vp7/8HSMa0gWGLjrLcqt13ofBMgu50P+0X3sw41BqQ0YM+2AoA4gY4hZYCAuAjS0dOyVFW0DzVTfREuBhRYv69yYCyqVSbIRJNy8E+hqVoVr4/44/z7CDKH0KhGR0M93uook/mQ8DezmMG39XwrQasXhk3dq2Pli/D3qHOJ04FIR5BS0NvYvWCZX4S749eGslsTvKd6VNat0sGpCiCT9rZ60hPTw+vrqYWG6W2QpE9KKAyqHU7eHSRWoDdmx^1736019615417; geo_country=DE; ak_bmsc=B678F1D83A33D5D1DA38BAF8D949D7AD~000000000000000000000000000000~YAAQP2ETAr/KZL2TAQAAwjHVMhoEMPp/2zrJngBnlJ994wwczHfvp5hI47Ym5gqAZBy7oCU7lLvRlU1rjkPu5fjUDAm2XKbhMjpj/YPDv7cg+/YYsOhe3fEDYxpJU6VnlemB37hYMZFzr+IfbXReSDONNQts47OrbmyqkUF1wiUWHINWkpQdHjFhp8+nhFq5g7XmA2CIaCtgdtlcVRcEhatteLEDFKE/KjpW5zW6p651tqR6D0bp1l31t5r1ot1EfKYsQTJl0eCJ4Gg+RJ3a7y3JdaFCC1cDcyF9pN+YbneoBAxs6+KWvFixhvkm8UiX4Ahbgy3VsgXtTwYLsHqbbP+ae8IPZl5ENiQBtpl0uiL/EFsgNexfgBZndkIXLxZjcza9DYcg5DOiA39VeVo6VVZoFjUukIsFWaz95jia6eM=; _rdt_uuid=1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7; _scid_r=1PiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9oQ; _uetsid=5b24d730cabf11efa6b3510e5981e55b|81jus|2|fsa|0|1830; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736019396618__UDF43-m4_17ck_6gHvoNfPOCk%3D-1481-v2; _uetvid=c85e49c0c32011ef95a8e15267052ca8|zr11dq|1736020138229|6|1|bat.bing.com/p/insights/c/u; QuantumMetricSessionID=ee1c216dee99bf30b0b82c155f762853; utag_main=v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:10$_se:5%3Bexp-session$_ss:0%3Bexp-session$_st:1736021938953%3Bexp-session$ses_id:1736019400807%3Bexp-session$_pn:2%3Bexp-session$_vpn:2%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:79%3Bexp-session$ab_dc:TEST%3Bexp-1741203400815$_prevpage:PLP%7CG_MEN%7CPT_TRAINERS%3Bexp-1736023215814; s_pers=%20pn%3D2%7C1737781118250%3B%20s_vnum%3D1738368000852%2526vn%253D2%7C1738368000852%3B%20s_invisit%3Dtrue%7C1736021938969%3B; bm_so=539A6D6EF2C9ACB3791394C72530B79F9AC47A024492B970BAC8DC2F6EBB71B3~YAAQH7IPF5Id/ZqTAQAAYTvdMgLhQ0YHcMd6+TNBKlhVJqva82D9cWM+uTRZrnk6PuDrODiul+4ODG/7oZGVV7Ux83Mixk6D55Ey6J/PDDrTwQ39C5Ral3obedpIvgqGuMSuck0UOAlfM9W331mq85Zx4brPTe7u39CtbPuARlXcdQg+v+AnFyTlgK1n+YDk7edE6VziaiPQtwEGFgA4NdpSYa+T+h1PkVMTPCwE1EY0V1fePbV5KIBGpAzHpyYxuqkXQzB362SoWte4rhVuqK1d0RlEDsOjL01d9twchxoVkyfl/XZgxG1cqdr3wYT6BMCnqRbHNA0TfmublI5xqmhgHHCU/vHIv/gdlSOcAW9BxAkdTL4P+kaZSJN935rJFmiCaXt1mlXW53zELAFFYcgP/93QJTG9cpfuO+NGgvlhS9RquNLYiPSU4lAJP2dWAVWD7iSVJPQupFkhkMD0NSgSz9FXJZWkfbwfRxXavtduo432; bm_s=YAAQH7IPF/wd/ZqTAQAAIVrdMgJzOD+z3BWWVP0qzURYN0PR/QICfm/ehNDWWoVWHMGDzXgnYpHYSf1BYov/FbV8EzkO0Nvf/griTrb0vD0rbyR8egF9BegW38gczjNB6ItBBXGqLs7YlXLYX+LYWb4KjEEc6PMmwLS7XzJPV+CGu67NSZ97QnF9dxRAxB+m37NRZ67gXkhLAKPme64ljl4iw7IU06q9Blm4APO1U4z6LyECHQlg6yvb05JOVzLzpHNPLnXK/oUx1WmunoMhcOqCLcSVhmvDAh3ZvQy2/ZTqn8WFtEyAGVV7VgkQNAiMIochPOsFgMaAbDCDy54dAJdLLW3u; bm_sz=B94C8E03BCBE4059402F5EE5931A975E~YAAQH7IPF/0d/ZqTAQAAIVrdMhoeOBqcz0y+Xs+sOsLEI10oIfyiJTlRVGeVJk0bK6OQF60cetdAOpe5mAHPMwhQhqTNW2A757ZemqZtl9nJk9vBwg4FOqQtg00YVmsY4LbgGhz1McfQdB/SWO/GUJuv2tKDlLUp+jm4OR0KPazXYe1oDNLDK/gh4mvi2aCqBUobp5HdVkTVrX83PgPUEFKngsihNF3fflLq+fm+HVcCU8wFVg6LYyMGJN3OpTXt2/IgeAkf4RZbqy3TwAKHgYh2dgUQ3CP992b8r69YsvH7sBd2HJSt9kaGjWKGQGEKBAayu7soa2XsawH6eWmTZjdmyvgJeCLDZIIc8PASk5GdwDYSlJZK+dETsA/UJzx4KOoj703c88yHm6tVweoKVvrpeUzxIu4xp44VoFRoBuMSNhty0TcmWrwESP2mKjbjAOa/B8yAR6QXf4OYN2yMz+4HxczwY9CJmA3AZIT6z2ClKx37qXfi0FNBbwng+OOjQkXDo1wLDJs/lB1XrQdQurjMpfxtrJ8NhBQ6V15Lg8k9BMHFxxpC8Dp2Wo8u/RruGSn2rdSDBo25usq4W5JV5DdtjdiQmgLcH1AQ~3682630~4470597; RT="z=1&dm=www.adidas.de&si=4882354e-05d1-4396-80c3-461e58eaff22&ss=m5il4isw&sl=0&tt=0&bcn=%2F%2F684dd330.akstat.io%2F&hd=g6fh"; _ga_4DGGV4HV95=GS1.1.1736019396.11.1.1736020150.60.0.0; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1736020151015__UDF4_17ck; _abck=55A4C44F0D37C1B5517B23E960AB4638~-1~YAAQH7IPFwQe/ZqTAQAAcVzdMg2IOHTW+1oW01udkcYF8Ri7ZjO/be5sssLdpqbLR2yuLNLJfUSJeVX/wm+Wzb7R1WIT9vxThAbDEg0SOQCArXTINcnrypBbZ2eof3xiULN70kQ9aa2sHdkPF90G7NHSGjjskNWz7bqQ8+TqRaSHUIgCPmr+co7RjksjCan8PZ7X7fsNa2sM4wn4uYuZa0JGsGNR9mgi4vu//3tZWql8j0AmU06tc5gDWcBaq/l7eQaWIceF7O5mXkCMCweqsJYRxnUrMO+WstZFY/1ItPlR0ROUbNZFgmxnudydFep2IPmLOmRtgz1/ScAsZg6LkDprmGU0bcHxR8P2KaGxfwp7gHgtpUnc6GQaT73v+w2xH1aWIseuiZEgjPhr0h3JYgxq9ZNFZFjF+tn+dyAAM1T4Vhi2sV/Di4HsBU5sPcM3ou6V71YffGaV2Oa8LNZ8bJhtR9mPMiCRl4FybqlXdEXtuj2mtY8fW4vFqnfG1CavNneUBf0X6vd6bwNAPEpry+sERCYfXsxaINUn+JgrpmzOdcY=~-1~-1~1736022990; UserSignUpAndSave=40',
    'origin': 'https://www.adidas.de',
    'priority': 'u=1, i',
    'referer': 'https://www.adidas.de/samba-og-schuh/B75807.html',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-instana-l': '1,correlationType=web;correlationId=4c0faf327211822',
    'x-instana-s': '4c0faf327211822',
    'x-instana-t': '4c0faf327211822',
}

#response = requests.get('https://www.adidas.de/api/product-list/GW1706',  cookies=cookies, headers=headers)

category=['manner-sneakers','frauen-sneakers','jungen-sneakers','manner-fitness_training-schuhe','manner-fussball-schuhe','manner-running-schuhe']
#https://www.adidas.de/manner-sneakers

def raw_codes(category_name):
    base_url=f'https://www.adidas.de/{category_name}'
    all_item_code=[]
    a=-48
    next_page=True
    while next_page:
        try:
            a=a+48
            url=f'{base_url}?start={a}'
            response =  requests.get(url,  cookies=cookies, headers=headers)
            
            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.find_all("article", {"class": "product-card_product-card__a9BIh product-grid_product-card__8ufJk"})
            
            if not items:
                next_page = False
                print(a/48+1)
                break

            for item in items:
                all_item_code.append(item.find("a").attrs["href"])
                print(item.find("a").attrs["href"])

        except Exception as e:
            print(f"An error occurred: {e}")
            next_page=False

    return all_item_code

def codes(all_item_code):
    item_codes=[]
    for item in all_item_code:
        item_codes.append(item[-11:-5])
    df = pd.DataFrame(all_item_code)
    df.to_csv('raw_codes.csv', index=False)
    print('raw_code_list generated')
    return item_codes


def details(item_codes, category_name):
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
                    "weight": {product_data.get('attribute_list', {}).get('weight', None)},
                    "best_for_wear": next(iter(product_data.get("attribute_list", {}).get("best_for_ids", [])), None)
                }
                print(product_info)
                product_list.append(product_info)
            else:
                print(f"No data found for item {item}")
        else:
            print(f"Failed to retrieve data for item {item}: {response.status_code}")
    
    return product_list

def export(product_list):

    
    df = pd.DataFrame(product_list)
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
        if i%100==0:
            time.sleep(randint(5, 20))
        if response.status_code == 403:
            rotate_VPN(settings)
        if response.status_code == 200:
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
    for category_name in category:
        all_item_code = raw_codes(category_name)
        item_codes = codes(all_item_code)
        product_list = details(item_codes, category_name)
        export(product_list)


#main()
availability()

