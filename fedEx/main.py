from bs4 import BeautifulSoup
import requests
import json
import urllib
import time 

def get_selected_cols_df(df, cols):
    '''
    cols : list of str 
    '''
    return df[cols]


class FedExShipmentTracking:
    def __init__(self, df, col_name = 'Pro No', verbose = True):
        self.df = df
        self.shipment_ids = self.df[col_name].values
        self.verbose = verbose
        self.url = 'https://www.fedex.com/trackingCal/track'
        self.headers = {
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    "Accept" : "application/json, text/javascript, */*; q=0.01",
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'Host': 'www.fedex.com',
                    'Origin': 'https://www.fedex.com',

                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With' : "XMLHttpRequest",
                    'Cookie': 'fdx_cbid=30036807161594754925222750021081; fdx_locale=en_US; fdx_redirect=en-us; cc_path=us; s_ecid=MCMID%7C91240026263101807612795946297234918876; _abck=E6BF6C129F738D2B9D1C7477355EE277~0~YAAQL5EvFwBtVC1zAQAAAwvNTgSEKQJaNIT46+OyW/Rl1EiG2zsHB8tUiwjmoECJgd2c5DwAVVZJqwRE1WyaZUW6CBEIrzjTPlAfDtIA0eWI1PZx8cmmPMA8K043L/XtLVvra0HYHOpMsVBS/T9heRtUPhD61LP9fCtzlX8ASW2c/LueOQF0WnVI6fhEBpzT7lxVey3V7rIXOIdQx785tSS1+3g9TOPU74tgm0TvJyIpOTjLhX27RoU7wo+mzSD5HKwhzKC3pckP0hjKF1EGAXRyh7NQTD4m08aQDFxo0f0BS7BbSbLuVXHDuKdgHLRb5nJkiLs4~-1~-1~-1; _gcl_au=1.1.494437621.1594754928; tracking_locale=en_US; wdpl_id=30036807161594754925222750021081_1594754941226; optimizelyEndUserId=oeu1594842710172r0.13632731098668605; s_vi=[CS]v1|2F8820BB8515E1A5-6000073AEC279C6F[CE]; siteDC=edc; mbox=PC#1595273312475-908373.35_0#1596830577|session#1595620934343-546912#1595622837; Rbt=f0; AMCVS_1E22171B520E93BF0A490D44%40AdobeOrg=1; Nina-nina-fedex-session=%7B%22loginStatus%22%3A%22loggedOut%22%2C%22locale%22%3A%22en_us%22%2C%22lcstat%22%3Afalse%7D; s_sq=%5B%5BB%5D%5D; xacc=US; bm_sz=4537EBE6509A5D440AD47ED3F80C79BE~YAAQr3lGaOb59X9zAQAAPkn1iwjilFEKU/Hxbvqfeprv1pCh3PT2Me3bTAJQ12QgCNOtfHlxS+XK5Fa+X0LlfEm6kIgpH+Dlm9NQ0ypUeJ9BwqNwBuXI2IP6RGDvdEnsLnYg9JbJni8A/iP8YVPtGzSLZtucUOOqxj45znRIaMvvfQ7HLxOikNDq/2LQ4us=; ak_bmsc=CD81CB8828BE3D10205B58F77A78AF9F684679AF5C7D00006EAF1D5F61860971~plb5JNNd4MRJ+ZVIxorPq7NA1gFLL5TFJ/LEr5c2hx86FWjsmi7lF08BdqCL5Ee7PLBqfubVT/xzkPj+sl4riDqFyHe68mlzdT8V7t3XgyUTkNeg/eFURmr63IljjawrpW2KEswRN4XDAt1fnGzl3jEGV6PFsD+M6ECn5Cswi/rXsj0+axDVvBsXBdmloZeogYOnwKaYvTpNtxtPyYwrEzrRckCOGkkjzC/xtoyE1o6lID6AbzuMtxQvUEGAiqoQg5; AMCV_1E22171B520E93BF0A490D44%40AdobeOrg=1075005958%7CMCIDTS%7C18470%7CMCMID%7C91240026263101807612795946297234918876%7CMCAAMLH-1596385774%7C7%7CMCAAMB-1596385774%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1595788174s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.1; isTablet=false; isMobile=false; isWireless=false; level=test; aemserver=Prod-c0015884.prod.cloud.fedex.com; s_pers=%20s_vnum%3D1595822400191%2526vn%253D1%7C1595822400191%3B%20gpv_pageName%3Dus%252Fen%252Ffedex%252Funified%252Fsummarypage%7C1595782777780%3B%20s_nr%3D1595780977791-Repeat%7C1627316977791%3B%20s_invisit%3Dtrue%7C1595782777802%3B%20s_dfa%3Dfedexglbl%252Cfedexus%7C1595782797031%3B; s_sess=%20s_visit%3D1%3B%20SC_LINKS%3D%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dus%252Fen%252Ffedex%252Funified%252Fsummarypage%252C89%252C89%252C1461%3B%20setLink%3D%3B; bm_sv=4EFB739A657166D148018747EECAE444~EEeDC8RhatPCxiJEcuvlyKw8uW9YjuNB0LsSrvXfL/4RUZTVIwcQhJSOOddouq0QvxUkB0laCZWErSpRDgmVOcGGbYaEHeDEh/JdTumXJZ3ol/DQnfjjhX6/zG1XHpRXTeqIIk+l98DMBDWQKTaMT4fzKmyVbors5C8i0jX6GsA='
                    } 

    def track(self, max_amount_track = 30):
        print(" start !!!!")
        print("we have {} fedex tracking number".format(len(self.df)))
        final_data = []
        for idx in range(0, len(self.df),max_amount_track):
            if idx + 30 <= len(self.df):
                data = self.encode(self.shipment_ids[idx:idx+30])
                response = self.crawl(data)
            else:
                data = self.encode(self.shipment_ids[idx:])
                response = self.crawl(data)
            
            bt_result = self.parse(response)
            final_data.extend(bt_result)
            time.sleep(5)
        return final_data
  
    def encode(self,ids):
        form_data = {"data":{"TrackPackagesRequest":{
                    "appType":"WTRK",
                    "appDeviceType":"DESKTOP",
                    "supportHTML":True,
                    "supportCurrentLocation":True,
                    "uniqueKey":"",
                    "processingParameters":{},
                    "trackingInfoList":[{"trackNumberInfo":{"trackingNumber":str(i),"trackingQualifier":"","trackingCarrier":""}} for i in ids]}
                            },
                    "action":"trackpackages",
                    "locale":"en_US",
                    "version":"1",
                    "format":"json",
                    }

        data = 'data='+ json.dumps(form_data['data'],separators=(',',':')) + '&action=trackpackages&locale=en_US&version=1&format=json'
        return data
        
    def crawl(self,data):
        res_id= requests.post(self.url,data=data,headers = self.headers)
        respond = res_id.json()
        return respond
    
    def parse(self, respond): ## list of dict 
        packages  = respond['TrackPackagesResponse'].get('packageList',[])
        if self.verbose:
            print(f"{len(packages)} loads tracked !!!")
        batch_result = []
        for p in packages:
            data = [p['displayTrackingNbr'],
                    p['scanEventList'][0]['status'],
                    p['displayEstDeliveryDateTime'] if p['displayActDeliveryDateTime'] == "" else p['displayActDeliveryDateTime'],
                    p['scanEventList'][0]['scanDetails']]
            if self.verbose:
                print(data)
                
            batch_result.append(
                {data[0]:{
                    "Action":data[1],
                    "Status" : data[2],
                    "Details":data[3]
                }}
            )
            
        return batch_result


if __name__ == "__main__":
    FEDEX_CARRIER_CODE = ['FDEN','FDEN_EXP','FXFE']
    FILE_PATH = ".\data\IOD_MONITORING_DETAIL_US_202061515948415074903147.csv"
    df_origin = pd.read_csv(FILE_PATH)
    df = df_origin[df_origin['Carrier Code'].isin(FEDEX_CARRIER_CODE)]
    test = FedExShipmentTracking(df)    
    result = test.track()
    result = dict(ChainMap(*result))
    