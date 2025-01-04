from curl_cffi import requests
from bs4 import BeautifulSoup
import asyncio
import time
from random import randint
import re
import pandas as pd
import os
import json

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
    '_ScCbts': '%5B%5D',
    'QSI_SI_0evq2NrkQkQaBb7_intercept': 'true',
    'QuantumMetricUserID': 'ce9e74e6acbef12e0916dd37bb958505',
    'newsletterShownOnVisit': 'true',
    '__olapicU': '194fc6145839464cb3a8a92f2b8bb16e',
    'geo_ip': '2a02:908:952:ae0:a066:d33a:3770:253',
    'onesite_country': 'DE',
    'akacd_plp_prod_adidas_grayling': '3912679834~rv=38~id=26b1da392e32e1657b448f03e216fa35',
    'gl-feat-enable': 'CHECKOUT_PAGES_ENABLED',
    'akacd_generic_prod_grayling_adidas': '3912679837~rv=7~id=bcf3f37afa6bfb42186033ff932c85e8',
    'x-session-id': 'd5f4d62c-92db-46d6-9dc8-a7a16bd5be9f',
    'wishlist': '%5B%5D',
    'AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg': '1',
    's_cc': 'true',
    's_sess': '%5B%5BB%5D%5D',
    'akacd_pdp_prod_adidas_grayling': '3912679854~rv=99~id=f366d5e8786a4b5c1a8abb8747300930',
    'checkedIfOnlineRecentlyViewed': 'true',
    'persistentBasketCount': '0',
    'userBasketCount': '0',
    'pagecontext_cookies': '',
    'pagecontext_secure_cookies': '',
    'x-site-locale': 'de_DE',
    'x-original-host': 'www.adidas.de',
    'x-environment': 'production',
    'geo_country': 'DE',
    'geo_coordinates': 'lat=51.22, long=6.77',
    'bm_sz': '03D5AF072C870E6A581BACB236E2BA5E~YAAQP2ETAkvpvrqTAQAAAq3lBBqHZzg0P1lkkhqluZndKJEKCW4OMhp34xyInBgA0xi+CtaQn4JS6YtryyKNbjgXvmqoSDu4Q3C1OQcCAMNZtaG1dDnzj1HYeW//WIwD2iXZ4S1rc06jx4lQBq+iqWtP7Joyt5R8FbaG3ZOO8FuB3CVm6dQSeoGPn2NgUV7HqIyN4D/MLN+EgObwnjJSx/n5wyLuYDWT5LAF451EowRCH1fRfjLS6puQltXIvAZKJ9kV5SwkGUZqFrO9dBBzgOBOKYWIysvqHwo4vEUxiLzI1NagZjAN4UmXaerwrkjYSUDgbIfYnJgVuzXtJMGxcFnrIupawxb42tNMyFu/8qto2pfmod+5XTNiSQRnzKfP9pEFrr6yefq+TqfrU6qReu3qPVW0U8qDbS79UKvaNgM069nyPP2iJVqyjw7R7f/jqglfDWgYHqcuX3eOgwOsIlvCfmKpoNqs2ViEYXp8fI3UPsLEpAzjtk5molxaH18G3FxZu8iBHoM7cAZ5cbbwq6nwF28AuUkh8bT6jAk+0PR+5SUgugt1yHgpfTSCpSeRdj+tFbeimf+aly2Qzg/2IcOXmYcw+P6KwIa08wiN2To6A+Wt~4471108~4403248',
    'QuantumMetricSessionID': 'd01a5efa5adfe76b2f35d6f596e9a84c',
    'AKA_A2': 'A',
    'bm_ss': 'ab8e18ef4e',
    'bm_so': '5A51BE12935130ADF051A596AE0D5EEF7D05E29C44691B796D96D249B0A50689~YAAQP2ETAu/pvrqTAQAAjLLlBAIYKjg+pcZYtT+JATVnscdpkSTD5XcZqcoPkoRZFWdcIqKiMurBye6Pe3o7pyWEE26M/XF0KV6ufad8/qnAXm/gXEGbKILI6hUqSK91ohB5fey1iXkym1VshiPfPOG1T8bABmj6vUxaDFMbIMYs7uj+rGojJ6dqfchS3xtqmiJBNGnftvrQcO08lkKh5a7B+JxLetcXR5qmeVnjzwNUx17vL0WtBUFYFT4S1yLuRY2xhItzbmYcK/IdqiDg/TZCtpeiJpIZgO+Ajv0Xn9OTs4DEyQN8ZZcc8luTgJrDa6NB3xgqrFh0JJIbaciEM5SJzT5mtNZrmau+h9d9HFH7nEpKkZ7RDHR/Z1/77iFWG6dMnz3LeayGMKqKm9B15MVHLYaAmAMr33/jYx5xYK1Q/oT1bLw6S03Z0cUGoOAct1grQm94ZuO5DY9b2k5uV1laG8Q1DrFTavlsA7VxDcoM3Uw9',
    'ak_bmsc': '4F346EA845FC82C93A41317431DAAAED~000000000000000000000000000000~YAAQP2ETAqPqvrqTAQAAWbnlBBqrrhMPpCMTECSV7Gp95tCof5wP2hy720ZJrWHWNx5o9BnEdz07wZrhq1KIkkqke0HVCpGHrN+mdKkJsKziv7xX9+Aj4De1YhV6jWXNo90KAOkJyB4pqXnCGXSawdYrokn5Dnb0/Qr8ajS9r30+6inku00QVHJFkiW3UHQy9ZrDMruelUh75KZe8HgCix7sKxE/ok7rESsBUn6orbnaVIPauMb3qjp6PeGSRGxtJCiSteE6hjwnyJhma8g7vp0F7elsi3r8t0iR+auc9YqGEgB48DPmtbuGXr/o98vkzkCb8JMjXidV4T01eIzmXX+sIsS16+SNjodzvCeF9+AtF+Y+CU4/cQJ4PNEUAD/Rszk7MK7Oei4XV3b7cEF5dXNLAE/4/Q7Qwq/Tnro7qXY=',
    'bm_lso': '5A51BE12935130ADF051A596AE0D5EEF7D05E29C44691B796D96D249B0A50689~YAAQP2ETAu/pvrqTAQAAjLLlBAIYKjg+pcZYtT+JATVnscdpkSTD5XcZqcoPkoRZFWdcIqKiMurBye6Pe3o7pyWEE26M/XF0KV6ufad8/qnAXm/gXEGbKILI6hUqSK91ohB5fey1iXkym1VshiPfPOG1T8bABmj6vUxaDFMbIMYs7uj+rGojJ6dqfchS3xtqmiJBNGnftvrQcO08lkKh5a7B+JxLetcXR5qmeVnjzwNUx17vL0WtBUFYFT4S1yLuRY2xhItzbmYcK/IdqiDg/TZCtpeiJpIZgO+Ajv0Xn9OTs4DEyQN8ZZcc8luTgJrDa6NB3xgqrFh0JJIbaciEM5SJzT5mtNZrmau+h9d9HFH7nEpKkZ7RDHR/Z1/77iFWG6dMnz3LeayGMKqKm9B15MVHLYaAmAMr33/jYx5xYK1Q/oT1bLw6S03Z0cUGoOAct1grQm94ZuO5DY9b2k5uV1laG8Q1DrFTavlsA7VxDcoM3Uw9^1735248952203',
    's_pers': '%20pn%3D2%7C1737781118250%3B%20s_vnum%3D1735689600510%2526vn%253D8%7C1735689600510%3B%20s_invisit%3Dtrue%7C1735250753988%3B',
    'utag_main': 'v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:8$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1735250753730%3Bexp-session$ses_id:1735248953730%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:54%3Bexp-session$ab_dc:TEST%3Bexp-1740432953738$_prevpage:PRODUCT%7CGAZELLE%20INDOOR%20SCHUH%20(IH5484)%3Bexp-1735252553881',
    '_rdt_uuid': '1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7',
    '_scid_r': '0fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9nw',
    'AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20084%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1735777898%7C6%7CMCAAMB-1735853754%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1735256154s%7CNONE%7CMCAID%7CNONE',
    '_uetsid': 'c85e43f0c32011ef9458f1ea7a15764b|xwy2vv|2|fs1|0|1821',
    '_ga_4DGGV4HV95': 'GS1.1.1735248948.9.1.1735248954.54.0.0',
    '_uetvid': 'c85e49c0c32011ef95a8e15267052ca8|1ipwf1g|1735248955585|2|1|bat.bing.com/p/insights/c/p',
    'bm_s': 'YAAQP2ETAkbtvrqTAQAAXNPlBAK03h62fNJKRc+3/vml0zzvnH38Iu1arGZUvAjGJUCnT0Wl+OeTOMDw6ZDXys5vnChg8xz0PY3PnsJTqVB8xDeWhHxNow3lWF4kIoWTFoCCDgdQmol2sq2iTN0sYz1ZVwMzcxMR87ZP7Cc9vEX15I36rXJpJfO76tkFWqN1Vh3RFdDPhVbQjs3k2GEigQysqyXiqo17+GDCOx9c5GwZKWqU8Rb/ey0H7hbDqoJjD2IlVMePTFwg6i7bZn5bxXpA6pHRWBZR6h1KHx7FFBbv+tnxZ7qs1iUU+VOSH4pAByWPE8EgMGT/OM95p0tMtU1p0/Iu',
    'RT': '"z=1&dm=www.adidas.de&si=b178b27f-3d10-4794-b6eb-5e5df9c4f724&ss=m55lprl1&sl=0&tt=0&bcn=%2F%2F684dd313.akstat.io%2F&hd=8pkzl"',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1735248957618__UDF43_17ck_zX9ACce+y9E%3D-292-v2',
    'forterToken': 'db8f5bb12e0e4125b006fedf5185a2d0_1735248957618__UDF43_17ck_zX9ACce+y9E%3D-292-v2',
    '_abck': '9D87CCA4C1798CFA6013BAB51EB5B4AE~-1~YAAQP2ETAqbtvrqTAQAAfNblBA1mBa04C026Eg1BF0E6KK0XpD4310OUrLWsAW3kyc4AYKfSo7u9yI3F1AdXHXwDTh0FXM4uxOradZfp58+JlELWFARMMLzhZs/wOR9V/LP/6LiDCzRupF2vyA6AD9ONV06LSjZKPtsmZWzBjVe4QEc/KsVsNYQ0kmREyLcv42Ffk8VFqk6rga29PpGLHx4KscsSXjzHFF1Yq+LtXia1B10S7+3uwxDHTONAT3WjvXWLPADA1/Xq2Bn86arcnZ06hkQeEG6IMoJ1zsckBrnlANZHq4+OX/9/yAY2vdZnTvgWnaveDCbEBvqOMVfQOzPv5zk/OePPAESsC8VGtpBa0sd22wrRwu07ZwXiVjuVa6nqYJun29Td1G66hDIuC2y1ItAd4dzs7xlwa6VmuSUptNvwx1YRgaH6iuukQwEUklyFRAXqkfTsxdNqiS9jOSkz7U5LfM8rySD3+jYN0SWiIF0QUAYFrjXqrZSUIkVu4+yXZBKKPdQOxdU5TnOz+VSWnE6kAVU=~-1~||0||~1735252550',
    'UserSignUpAndSave': '22',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'mt.v=5.023471563.1735173098104; channelcloser=nonpaid; x-browser-id=ef39a6f2-8314-4f82-a0fa-363e49a57267; x-commerce-next-id=fd64b71c-e602-4579-ad92-380944173704; ab_qm=b; wishlist=%5B%5D; notice_preferences=%5B0%2C1%2C2%5D; _gcl_au=1.1.745756955.1735173104; _ga=GA1.1.417081306.1735173100; _scid=zniVhzQxtikyP_ORqzNgOBONUQNB32mF; _pin_unauth=dWlkPU56ZG1ZbVJpTTJJdFl6QXhaaTAwTldZNUxUazNOMll0WlRKbU9XWmlOakprWWpVNA; _ScCbts=%5B%5D; QSI_SI_0evq2NrkQkQaBb7_intercept=true; QuantumMetricUserID=ce9e74e6acbef12e0916dd37bb958505; newsletterShownOnVisit=true; __olapicU=194fc6145839464cb3a8a92f2b8bb16e; geo_ip=2a02:908:952:ae0:a066:d33a:3770:253; onesite_country=DE; akacd_plp_prod_adidas_grayling=3912679834~rv=38~id=26b1da392e32e1657b448f03e216fa35; gl-feat-enable=CHECKOUT_PAGES_ENABLED; akacd_generic_prod_grayling_adidas=3912679837~rv=7~id=bcf3f37afa6bfb42186033ff932c85e8; x-session-id=d5f4d62c-92db-46d6-9dc8-a7a16bd5be9f; wishlist=%5B%5D; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; s_cc=true; s_sess=%5B%5BB%5D%5D; akacd_pdp_prod_adidas_grayling=3912679854~rv=99~id=f366d5e8786a4b5c1a8abb8747300930; checkedIfOnlineRecentlyViewed=true; persistentBasketCount=0; userBasketCount=0; pagecontext_cookies=; pagecontext_secure_cookies=; x-site-locale=de_DE; x-original-host=www.adidas.de; x-environment=production; geo_country=DE; geo_coordinates=lat=51.22, long=6.77; bm_sz=03D5AF072C870E6A581BACB236E2BA5E~YAAQP2ETAkvpvrqTAQAAAq3lBBqHZzg0P1lkkhqluZndKJEKCW4OMhp34xyInBgA0xi+CtaQn4JS6YtryyKNbjgXvmqoSDu4Q3C1OQcCAMNZtaG1dDnzj1HYeW//WIwD2iXZ4S1rc06jx4lQBq+iqWtP7Joyt5R8FbaG3ZOO8FuB3CVm6dQSeoGPn2NgUV7HqIyN4D/MLN+EgObwnjJSx/n5wyLuYDWT5LAF451EowRCH1fRfjLS6puQltXIvAZKJ9kV5SwkGUZqFrO9dBBzgOBOKYWIysvqHwo4vEUxiLzI1NagZjAN4UmXaerwrkjYSUDgbIfYnJgVuzXtJMGxcFnrIupawxb42tNMyFu/8qto2pfmod+5XTNiSQRnzKfP9pEFrr6yefq+TqfrU6qReu3qPVW0U8qDbS79UKvaNgM069nyPP2iJVqyjw7R7f/jqglfDWgYHqcuX3eOgwOsIlvCfmKpoNqs2ViEYXp8fI3UPsLEpAzjtk5molxaH18G3FxZu8iBHoM7cAZ5cbbwq6nwF28AuUkh8bT6jAk+0PR+5SUgugt1yHgpfTSCpSeRdj+tFbeimf+aly2Qzg/2IcOXmYcw+P6KwIa08wiN2To6A+Wt~4471108~4403248; QuantumMetricSessionID=d01a5efa5adfe76b2f35d6f596e9a84c; AKA_A2=A; bm_ss=ab8e18ef4e; bm_so=5A51BE12935130ADF051A596AE0D5EEF7D05E29C44691B796D96D249B0A50689~YAAQP2ETAu/pvrqTAQAAjLLlBAIYKjg+pcZYtT+JATVnscdpkSTD5XcZqcoPkoRZFWdcIqKiMurBye6Pe3o7pyWEE26M/XF0KV6ufad8/qnAXm/gXEGbKILI6hUqSK91ohB5fey1iXkym1VshiPfPOG1T8bABmj6vUxaDFMbIMYs7uj+rGojJ6dqfchS3xtqmiJBNGnftvrQcO08lkKh5a7B+JxLetcXR5qmeVnjzwNUx17vL0WtBUFYFT4S1yLuRY2xhItzbmYcK/IdqiDg/TZCtpeiJpIZgO+Ajv0Xn9OTs4DEyQN8ZZcc8luTgJrDa6NB3xgqrFh0JJIbaciEM5SJzT5mtNZrmau+h9d9HFH7nEpKkZ7RDHR/Z1/77iFWG6dMnz3LeayGMKqKm9B15MVHLYaAmAMr33/jYx5xYK1Q/oT1bLw6S03Z0cUGoOAct1grQm94ZuO5DY9b2k5uV1laG8Q1DrFTavlsA7VxDcoM3Uw9; ak_bmsc=4F346EA845FC82C93A41317431DAAAED~000000000000000000000000000000~YAAQP2ETAqPqvrqTAQAAWbnlBBqrrhMPpCMTECSV7Gp95tCof5wP2hy720ZJrWHWNx5o9BnEdz07wZrhq1KIkkqke0HVCpGHrN+mdKkJsKziv7xX9+Aj4De1YhV6jWXNo90KAOkJyB4pqXnCGXSawdYrokn5Dnb0/Qr8ajS9r30+6inku00QVHJFkiW3UHQy9ZrDMruelUh75KZe8HgCix7sKxE/ok7rESsBUn6orbnaVIPauMb3qjp6PeGSRGxtJCiSteE6hjwnyJhma8g7vp0F7elsi3r8t0iR+auc9YqGEgB48DPmtbuGXr/o98vkzkCb8JMjXidV4T01eIzmXX+sIsS16+SNjodzvCeF9+AtF+Y+CU4/cQJ4PNEUAD/Rszk7MK7Oei4XV3b7cEF5dXNLAE/4/Q7Qwq/Tnro7qXY=; bm_lso=5A51BE12935130ADF051A596AE0D5EEF7D05E29C44691B796D96D249B0A50689~YAAQP2ETAu/pvrqTAQAAjLLlBAIYKjg+pcZYtT+JATVnscdpkSTD5XcZqcoPkoRZFWdcIqKiMurBye6Pe3o7pyWEE26M/XF0KV6ufad8/qnAXm/gXEGbKILI6hUqSK91ohB5fey1iXkym1VshiPfPOG1T8bABmj6vUxaDFMbIMYs7uj+rGojJ6dqfchS3xtqmiJBNGnftvrQcO08lkKh5a7B+JxLetcXR5qmeVnjzwNUx17vL0WtBUFYFT4S1yLuRY2xhItzbmYcK/IdqiDg/TZCtpeiJpIZgO+Ajv0Xn9OTs4DEyQN8ZZcc8luTgJrDa6NB3xgqrFh0JJIbaciEM5SJzT5mtNZrmau+h9d9HFH7nEpKkZ7RDHR/Z1/77iFWG6dMnz3LeayGMKqKm9B15MVHLYaAmAMr33/jYx5xYK1Q/oT1bLw6S03Z0cUGoOAct1grQm94ZuO5DY9b2k5uV1laG8Q1DrFTavlsA7VxDcoM3Uw9^1735248952203; s_pers=%20pn%3D2%7C1737781118250%3B%20s_vnum%3D1735689600510%2526vn%253D8%7C1735689600510%3B%20s_invisit%3Dtrue%7C1735250753988%3B; utag_main=v_id:019400604aac00391324492474cc0506f001606700bd0$_sn:8$_se:1%3Bexp-session$_ss:1%3Bexp-session$_st:1735250753730%3Bexp-session$ses_id:1735248953730%3Bexp-session$_pn:1%3Bexp-session$_vpn:1%3Bexp-session$ttdsyncran:1%3Bexp-session$dcsyncran:1%3Bexp-session$dc_visit:1$dc_event:54%3Bexp-session$ab_dc:TEST%3Bexp-1740432953738$_prevpage:PRODUCT%7CGAZELLE%20INDOOR%20SCHUH%20(IH5484)%3Bexp-1735252553881; _rdt_uuid=1735173103699.99afae56-e721-436b-b16f-2b2b59fa94c7; _scid_r=0fiVhzQxtikyP_ORqzNgOBONUQNB32mFZit9nw; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20084%7CMCMID%7C15790907160741417814272843183976764876%7CMCAAMLH-1735777898%7C6%7CMCAAMB-1735853754%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1735256154s%7CNONE%7CMCAID%7CNONE; _uetsid=c85e43f0c32011ef9458f1ea7a15764b|xwy2vv|2|fs1|0|1821; _ga_4DGGV4HV95=GS1.1.1735248948.9.1.1735248954.54.0.0; _uetvid=c85e49c0c32011ef95a8e15267052ca8|1ipwf1g|1735248955585|2|1|bat.bing.com/p/insights/c/p; bm_s=YAAQP2ETAkbtvrqTAQAAXNPlBAK03h62fNJKRc+3/vml0zzvnH38Iu1arGZUvAjGJUCnT0Wl+OeTOMDw6ZDXys5vnChg8xz0PY3PnsJTqVB8xDeWhHxNow3lWF4kIoWTFoCCDgdQmol2sq2iTN0sYz1ZVwMzcxMR87ZP7Cc9vEX15I36rXJpJfO76tkFWqN1Vh3RFdDPhVbQjs3k2GEigQysqyXiqo17+GDCOx9c5GwZKWqU8Rb/ey0H7hbDqoJjD2IlVMePTFwg6i7bZn5bxXpA6pHRWBZR6h1KHx7FFBbv+tnxZ7qs1iUU+VOSH4pAByWPE8EgMGT/OM95p0tMtU1p0/Iu; RT="z=1&dm=www.adidas.de&si=b178b27f-3d10-4794-b6eb-5e5df9c4f724&ss=m55lprl1&sl=0&tt=0&bcn=%2F%2F684dd313.akstat.io%2F&hd=8pkzl"; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1735248957618__UDF43_17ck_zX9ACce+y9E%3D-292-v2; forterToken=db8f5bb12e0e4125b006fedf5185a2d0_1735248957618__UDF43_17ck_zX9ACce+y9E%3D-292-v2; _abck=9D87CCA4C1798CFA6013BAB51EB5B4AE~-1~YAAQP2ETAqbtvrqTAQAAfNblBA1mBa04C026Eg1BF0E6KK0XpD4310OUrLWsAW3kyc4AYKfSo7u9yI3F1AdXHXwDTh0FXM4uxOradZfp58+JlELWFARMMLzhZs/wOR9V/LP/6LiDCzRupF2vyA6AD9ONV06LSjZKPtsmZWzBjVe4QEc/KsVsNYQ0kmREyLcv42Ffk8VFqk6rga29PpGLHx4KscsSXjzHFF1Yq+LtXia1B10S7+3uwxDHTONAT3WjvXWLPADA1/Xq2Bn86arcnZ06hkQeEG6IMoJ1zsckBrnlANZHq4+OX/9/yAY2vdZnTvgWnaveDCbEBvqOMVfQOzPv5zk/OePPAESsC8VGtpBa0sd22wrRwu07ZwXiVjuVa6nqYJun29Td1G66hDIuC2y1ItAd4dzs7xlwa6VmuSUptNvwx1YRgaH6iuukQwEUklyFRAXqkfTsxdNqiS9jOSkz7U5LfM8rySD3+jYN0SWiIF0QUAYFrjXqrZSUIkVu4+yXZBKKPdQOxdU5TnOz+VSWnE6kAVU=~-1~||0||~1735252550; UserSignUpAndSave=22',
    'origin': 'https://www.adidas.de',
    'priority': 'u=1, i',
    'referer': 'https://www.adidas.de/gazelle-indoor-schuh/IH5484.html',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-instana-l': '1,correlationType=web;correlationId=213170e8c4f230ae',
    'x-instana-s': '213170e8c4f230ae',
    'x-instana-t': '213170e8c4f230ae',
}


#response = requests.get('https://www.adidas.de/api/product-list/GW1706',  cookies=cookies, headers=headers)

category=['manner-sneakers','frauen-sneakers','jungen-sneakers','manner-fitness_training-schuhe','manner-fussball-schuhe','manner-running-schuhe']


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
                    "name": product_data.get("name"),
                    "id": product_data.get("id"),
                    "price": product_data.get("pricing_information", {}).get("currentPrice"),
                    "sizes": [size.get("size") for size in product_data.get("variation_list", [])],
                    "category": category_name
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
    file_exists = os.path.isfile('product_data.csv')
    df.to_csv('product_data.csv', mode='a', header=not file_exists, index=False)
    print("product_data.csv generated")





def main():
    for category_name in category:
        all_item_code = raw_codes(category_name)
        item_codes = codes(all_item_code)
        product_list = details(item_codes, category_name)
        export(product_list)

#main()


#url = f'https://www.adidas.de/api/products/IF9427/availability'
#response = requests.get(url, cookies=cookies, headers=headers, impersonate="chrome120")
#soup = BeautifulSoup(response.text, "html.parser")
#print(soup.prettify)

def availability():
    i=0
    df = pd.read_csv('product_data_availability.csv')

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
            print(f"Failed to retrieve data for item {id}: {response.status_code}")
            print("The script is quiting.")
            break
    print(f"Total data collected: {i-1}")
    df.to_csv("product_data_availability.csv", index=False)
    print("Updated the availability.")

availability()






