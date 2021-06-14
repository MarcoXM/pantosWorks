# -*- coding: utf-8 -*-

from datetime import datetime
import numpy as np
import time 
import requests
import json
import urllib
import os
import pandas as pd
from glob import glob
from collections import ChainMap
from tqdm.notebook import tqdm as tqdm_notebook
from datetime import datetime 


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import requests
import json
import urllib
import os
import pandas as pd
from glob import glob
from collections import ChainMap
from tqdm.notebook import tqdm as tqdm_notebook
from datetime import datetime 


# Google Chrome Driver Setup
def chromeSetup():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
 
    return options


def get_selected_cols_df(df, cols):
    '''
    cols : list of str 
    '''
    return df[cols]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def transform(text):
    try:
        data = pd.to_datetime(text)
        return data.day
    except:
        return text     


def get_Drivers(options, json_path = ".\\config.json",webdriver_path = "C:\\Users\\marco.wang\\Downloads\\chromedriver_win32\\chromedriver"):

    with open(json_path) as f:
        data = json.load(f)

    browers = webdriver.Chrome(webdriver_path,options=options)

    print("get browsers!!")
    log_in_url = 'http://tms.us.lge.com/tm/framework/Frame.jsp'
    browers.get(log_in_url)
    time.sleep(3)
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('resultFrame')


    user = browers.find_element_by_name("loginUser")
    user.send_keys(data['user'])
    password = browers.find_element_by_name("dspLoginPassword")
    password.send_keys(data['password'])
    print("log in !!")

    button = browers.find_element_by_id("buttonEmphasized")
    button.click()


    time.sleep(3)
    browers.switch_to.default_content()
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('nav')

    
    browers.switch_to.default_content()
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('nav')
    IOD = browers.find_element_by_xpath("//*[@id='TREECELL_navigation_18']/a")
    IOD.click()
    time.sleep(3)

    daily = browers.find_element_by_xpath("//*[@id='TREECELL_navigation_18_1']/a[2]")
    daily.click()

    browers.switch_to.default_content()
    time.sleep(0.3)
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(20)
    browers.switch_to.frame('resultFrame')
    time.sleep(0.3)
    row = 6
    while row < 20:
        total = browers.find_element_by_id(f"iodMonitoringDailyGrid_BODY_{row}_2")
        print(total.text)
        if total.text == "Total":
            print(total.text)
            break
        else: 
            row += 1
    total = browers.find_element_by_xpath(f"//*[@id='iodMonitoringDailyGrid_BODY_{row}_3']/span/a")
    time.sleep(3)
    total.click()
    print("Done!!")
    return browers



def encode_search_word(text):
    return ",".join(map(str,text))



def enter_sys_value():
    return datetime.now().strftime("%m/%d/%Y") + str(datetime.now())[10:16]



def update_iod_tms_with_now(browers):
    i = 0 
    while browers.find_element_by_id(f"iodMonitoringDetailGrid_BODY_{i}_CHECKBOX"):
        checkButton = browers.find_element_by_id(f"iodMonitoringDetailGrid_BODY_{i}_CHECKBOX")
        time.sleep(0.1)
        checkButton.click()
        time.sleep(0.2)
        enter = browers.find_element_by_id(f'iodMonitoringDetailGrid_BODY_{i}_20_INPUT')
        enter.click()
        time.sleep(0.1)
        enter.send_keys(enter_sys_value())
        remark = browers.find_element_by_id(f'iodMonitoringDetailGrid_BODY_{i}_21_INPUT')
        remark.send_keys(datetime.now().strftime("%m/%d/%Y") + "Marco")
        i += 1
        if i > 30:
            browers.find_element_by_tag_name('body').send_keys(Keys.END)


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class Marco:
    carriers_code = [
        'RDWY',
        "BTVP",
        "TQLI_FW",
        "HMES",
        "RETL",
        "HRCF",
        "UTP2",
#         "NFIL",
        "AFXN",
#         "AFNW",
#         "ISCO",
        "CVYI",
        "PGAA",
        "AERG",
        "TFFC",
        "HUBG",
        "HSXF",
#         "CGFR",
        "DSRE",
#         "WSXI",
        "PASC",
        "MGZI",
        "WXLO",
        "UTPA",
        "DDXI",
        "CAIQ",
        "IVGC",
#         "RLIL",
        "SIIH",
        "TQLI_OR",
        "TTMS",
        "TXAP",
        "USXI",
        "CIAN",
        "TQLL",
        "VLLL",
        'RDWY_CRA',
             'RDWY_FON',
             'RDWY_FTW',
             'RDWY_POR',
             'RDWY_ROM',
        "AMZX",
        
        
        "SWFC",
        "SWFT",
        'AVRT_FTW', 'AVRT', 'AVRT_ATL','AVRT_ROM','AVRT_ORL',
        "HJBI","CNWY","WENP","KNIG",
#             'SLCY',
#            'GLBL',
#             'SNZW',
#             'SCDS',
#            'GLPC',
#             'ARVY',
        "JFYL","FRCI","UXLL"

        
        ## 
#         "TQYL",
#         "AACT",
#         "STJW",
#         "PGLI",
#        "ADSJ",
#         "SXPR",
#         "ARVY",
# "GLPC",
# "GLBL",
# "NPME",
# "PLCY",
# "SLCY",
# "SNZW",
# "SCDS",
    ]
    colsSend2Carrier = ['Sales','Load ID','Stop Seq','Carrier Code','Carrier Name','Service Type','Alert Type','Ship Date','ETA','From Address','To Address', 'Customer Name','GERP Order No','Pick Order No','Pro No']
    
    alertType = ['Overdue 4', 'Overdue 3','Overdue 1', 'Overdue 2', 'Today', 'Upcoming 1','Upcoming 2' ]
    
    carrier_email = dict(
        FDEN="'PremierGlobalSupport' <premierglobalsupport@fedex.com>",
        FXFE="'Mrs. Pat R' <freightpremier2@fedex.com>",
        FCTI=" Dispatch@firstchoicetransport.com; 'Sonny White' <sonny@firstchoicetransport.com>; 'Albert Aportela' <aaportela@firstchoicetransport.com>",
        MGXB="Brett Bozeman' <bbozeman@magellanlogistics.com>; 'Lucas Arendt' <larendt@magellanlogistics.com>; 'lgcns' <lgcns@magellanlogistics.com> ; 'Stephen Kelly' <skelly@magellanlogistics.com>; ",
        TFFC=" 'Maria Flores' <MFlores@traffictech.com>; 'Tanner Abel' <TAbel@traffictech.com>; 'Yiseli Gallinal' <YGallinal@traffictech.com> ;'TeamHawaii' <TeamHawaii@traffictech.com>; 'TeamGuam' <TeamGuam@traffictech.com>;TeamLG <TeamLG@traffictech.com>; Tania Bergamin <TBergamin@traffictech.com>; Tara Diggle <TDiggle@traffictech.com>; 'TeamPuertoRico' <TeamPuertoRico@traffictech.com>",
        PGAA="'Tristan Carmichael' <tcarmichael@pegasuslogistics.com>;'Joey Gabel' <JGabel@pegasuslogistics.com>; 'LG Team' <lg@pegasuslogistics.com>; 'Brian May' <bmay@pegasuslogistics.com>; 'Tara Howard' thoward@pegasuslogistics.com ",
        AFXN="'Annie' <pateanmo@amazon.com>; 'Connor' mccarcon@amazon.com; 'Alicia' <alicinel@amazon.com>; 'Connor' <mccarcon@amazon.com>; stceyw@amazon.com; carsamel@amazon.com; ingmicha@amazon.com; lgelectronics@amazon.com",
        DSRE="'Trisha Ballesteros' <trishab@dsrhawaii.com>, 'DSR Customer Service' <customerservice_trucking@dsrhawaii.com>",
        CGFR="'Clay Lewis' <clewis@challengerfreight.com>; 'Derek Goodnight' <Dgoodnight@cfslogisticsgroup.com>; 'Varanza Gonzales' <vgonzales@cfslogisticsgroup.com>; 'Kimberly Kindred' <kkindred@challengerfreight.com>; 'Erik Berry' <eberry@challengerfreight.com>; 'ops' <ops@challengerfreight.com>",
        HSXF="'Leimomi-Rose Bachiller' <lbachiller@hawaiianexpress.com>; 'Ruby Paiva' <rpaiva@hawaiianexpress.com>",
        MGZI="'Brett Bozeman' <bbozeman@magellanlogistics.com>; 'lgcns' <lgcns@magellanlogistics.com>",
        IVGC="robert.mize@invictusglobe.com; adam.hughes@invictusglobe.com; lisa.kim@invictusglobe.com",
        FDEN_EXP="'PremierGlobalSupport' <premierglobalsupport@fedex.com>",
        PASC="PTL LG <lg@ptl-inc.com>",

        ## Update 07/23/2020 
        AFNW = "'AFN LG Electronics' <lg@afnww.com>; 'Henry Klobukowski' <Henry.Klobukowski@globaltranz.com>; 'AFN Ops 13' <afnops13@globaltranz.com>",
        FRCI = "'Eric Emswiler' <eric.emswiler@fcc-inc.com>; 'Russ Powell' <russ.powell@fcc-inc.com>; 'LG Electronics' <LG_Electronics@fcc-inc.com>; fcclge@fcc-inc.com",
        
        ## Update 09/03/2020 
        AXRO = "Greg Harrison <greg.harrison@agxfreight.com>; Greig Mare <greig.mare@agxfreight.com>; Kelly Rowe <kelly.rowe@agxfreight.com>; LG <lg@agxfreight.com>",
        KWII = "'Leslie Jeong' <leslie.jeong@kwinternational.com>; 'DISPATCH' <dispatch@kwtransportation.com>; 'lgthdreturn' <lgthdreturn@kwinternational.com>",
        TQLI_FW = "Loren.Williams@tqlogistics.com; Bob.Sorrell@tqlogistics.com; Greg.Nichols@tqlogistics.com",
        TQLI_OR = "Loren.Williams@tqlogistics.com; Bob.Sorrell@tqlogistics.com; Greg.Nichols@tqlogistics.com",
        
        ## DDXI
        DDXI = "'Don Price' <Don.P@shipddl.com>; 'Jay Lorino' <Jay.L@shipddl.com>; 'Adam Kirchner' <Adam.K@shipddl.com> ;'Amy Raciti' <Amy.R@ddex.us>; 'Steve Tutkowski' <steve.t@shipddl.com>",
        HUBG = "DG2@hubgroup.com; dskenderovic@hubgroup.com",
        RLIL = "'Melissa Tolbert' <mborders@roarlogistics.com>",
        ROAR = "lg@roarlogistics.com; ltourville@roarlogistics.com",
        WXSI = "jstephens@westernexp.com",
        WXLO = "lg@westernexp.com ;cfraley@westernexp.com",
        RWDY = "Katherine.McPherson@yrcw.com",
        RETL = "CustomerService@Reddaway.com ;customer.service@yrcfreight.com",
        AERG = "'Laura McGee' <LMcGee@aeronet.com>; 'NCT' <nct@aeronet.com>",
        AVRT = "customerservice@averittexpress.com",
        AVRT_FTW = "customerservice@averittexpress.com",
        AVRT_ATL = "customerservice@averittexpress.com",
        UTP2 = "holly.lynch@unisco.com; april.camarillo@unisco.com",
        BTVP = "Stephanie Gonzales <stephanie@bestovernite.com>; 'Eric Lamadrid' <eric.lamadrid@pantosusa.com>; Janiese Martinez <janiese@bestovernite.com>; customer service <customerservice@bestovernite.com>",
        CVYI = "Convoy Ops <lge@convoymail.com>; Convoy Ops <lge@convoy.com>",
        HMES = "sysHolland - Tracing <Holland.Tracing@usfc.com>",
        NFIL = "'Stoy Jan' <Jan.Stoy@nfiindustries.com>; 'Palomino Jonathan' <jonathan.palomino@nfiindustries.com>; 'Garrison Brooke' <brooke.cecil@nfiindustries.com>; exthrs <EXTHRS@nfiindustries.com>; LGNFI <lg@nfiindustries.com>"

        
        
        ### Sophia's 08/13/2020
        # ARV2 = 'lgops@arrivelogistics.com;  acasperson@arrivelogistics.com; dbecerra@arrivelogistics.com',     
        # ARVT = 'lgops@arrivelogistics.com;  acasperson@arrivelogistics.com; dbecerra@arrivelogistics.com',
        # ARVY = 'lgops@arrivelogistics.com;  acasperson@arrivelogistics.com; dbecerra@arrivelogistics.com',
        # AXRO = 'jason.grumling@agxfreight.com; lg@agxfreight.com',
        # BNLS = 'ryan.meyer@bnsflogistics.com',
        # BTYT = 'pablo@bestyetexpress.com',
        # CEEG = 'lg@circle8logistics.com',
        # CLLQ = 'sarah.weir@coyote.com;reva.myers@coyote.com; LG@Coyote.com',
        # COYY = 'sarah.weir@coyote.com;reva.myers@coyote.com; LG@Coyote.com',
        # COZT = 'dispatch@cottrucking.com',
        # CRPS = 'csolem@crst.com',
        # CVEN = 'SLathrop@covenanttransport.com' ,
        # FHII = 'Justin.Dahl@fairchildfreight.com; LGE@fairchildfreight.com',
        # GLPC = 'jvanorden@fusiontransport.com; Tracing@fusiontransport.com',
        # GLTW = 'jvanorden@fusiontransport.com; Tracing@fusiontransport.com',
        # JTLC = 'ray.lee@jeffreyfreight.com;arnold.martinez@jeffreyfreight.com',
        # KWII = 'leslie.jeong@kwinternational.com;  dispatch@kwtransportation.com; lgthdreturn@kwinternational.com',
        # RYXV = 'lg@royaltransportationservices.com',
        # SCDS = 'STMLG@schneider.com',
        # SCNN = 'TLCSEast@schneider.com',
        # SLCL = 'STMLG@schneider.com',
        # SLCY = 'STMLG@schneider.com',
        # SNZW = 'STMLG@schneider.com',
        # SUNO = 'Dispatch@shipsun.com; brianjr@shipsun.com',
        # SUXE = 'Dispatch@shipsun.com; brianjr@shipsun.com',
        # TQLI_FW = 'Loren.Williams@tqlogistics.com;  Bob.Sorrell@tqlogistics.com;  Greg.Nichols@tqlogistics.com',
        # TQLI_OR = 'Loren.Williams@tqlogistics.com;  Bob.Sorrell@tqlogistics.com;  Greg.Nichols@tqlogistics.com',
        # TQLL = 'Loren.Williams@tqlogistics.com;  Bob.Sorrell@tqlogistics.com;  Greg.Nichols@tqlogistics.com',
        # UTPA = 'angel.hernandez@unisco.com',
        # VLLL = 'miguel.gentolizo@unisco.com',
        # VSSI = 'hallj@vsslg.com',
        # XPOL = 'LGEUS@xpo.com;  Kevin.Cote@xpo.com; Stephanie.l.Jones@xpo.com',
        # XPOX = 'LGEUS@xpo.com;  Kevin.Cote@xpo.com; Stephanie.l.Jones@xpo.com',


    )
    
contents = dict(
    delay = "Please provide the current status of below loads.\nEspecially for the overdue loads, please advise the reason they delayed.",
    normal = "Please see below for today's loads IOD pending.\nPlease update accordingly in TMS and let me know if there are any issues.",
    generals = '''
                Please see below for today's loads IOD pending.
                Please update accordingly and let me know if there are any issues.
                * If delivered, please update IOD
                *	If still in transit, please provide ETA
                '''
)

def content_generator(carrier, carrier_df, contents = contents):
    ans = ""
    t = datetime.now()
    hour = int(t.hour)
    if hour < 12:
        ans += "Good Morning! "
    elif hour <= 16 :
        ans += "Good Afternoon "
    else:
        ans += "Good Evening "

    ans += carrier + " TEAM" + '\n' 
    sisuation = email_sisuation(carrier_df)
    r = np.random.randint(len(contents))
    wday = datetime.today().strftime('%A')
    end = f"\nHave a great {wday} !"

    return ans + contents[sisuation] + end


def email_sisuation(df):
    sisuation_list = set(df['Alert Type'])
    for o in ['Overdue 4', 'Overdue 3','Overdue 1', 'Overdue 2']:
        if o in sisuation_list:
            return "delay"

    for o in ['Upcoming 1','Upcoming 2']:
        if o in sisuation_list:
            return "normal"

    return "generals"




if __name__ == "__main__":
    print(Marco)



