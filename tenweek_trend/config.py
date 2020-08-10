class Marco:
    carriers_code = [
        'FDEN','FXFE','FCTI','MGXB',
            'TFFC',
            'PGAA',
            'AFXN',
            'DSRE',
            'CGFR',
            'HSXF',
            'MGZI',
            'IVGC',
            'AZNG',
            'CAIQ',
            'FDEN_EXP',
            'FDTB',
            'SIIH',
            'TTMS',
            'TXAP',
            'USXI',

            ## Update in 07/23
            'AFNW',
            'FRCI',

            ## this is temp update 
            # 'SXPL',
            # 'STJW',
            # 'STQC',
            # 'SXPR',

    ]
    colsSend2Carrier = ['Div','Load ID','Stop Seq','Carrier Code','Carrier Name','Service Type','Alert Type','Ship Date','ETA','To Address','GERP Order No','Pick Order No','Pro No']
    
    alertType = ['Overdue 4', 'Overdue 3','Overdue 1', 'Overdue 2', 'Today', 'Upcoming 1','Upcoming 2' ]
    
    carrier_email = dict(
        FDEN="'PremierGlobalSupport' <premierglobalsupport@fedex.com>",
        FXFE="'Mrs. Pat R' <freightpremier2@fedex.com>",
        FCTI=" Dispatch@firstchoicetransport.com; 'Sonny White' <sonny@firstchoicetransport.com>; 'Albert Aportela' <aaportela@firstchoicetransport.com>",
        MGXB="Brett Bozeman' <bbozeman@magellanlogistics.com>; 'Lucas Arendt' <larendt@magellanlogistics.com>; 'lgcns' <lgcns@magellanlogistics.com>",
        TFFC="Dyane Gomez' <DGomez@traffictech.com>; 'Tanner Abel' <TAbel@traffictech.com>; 'Yiseli Gallinal' <YGallinal@traffictech.com> ;'TeamHawaii' <TeamHawaii@traffictech.com>; 'TeamGuam' <TeamGuam@traffictech.com>; 'TeamPuertoRico' <TeamPuertoRico@traffictech.com>",
        PGAA="'Tristan Carmichael' <tcarmichael@pegasuslogistics.com>",
        AFXN="'Annie' <pateanmo@amazon.com>; 'Connor' mccarcon@amazon.com; 'Alicia' <alicinel@amazon.com>; 'Connor' <mccarcon@amazon.com>; stceyw@amazon.com; carsamel@amazon.com; ingmicha@amazon.com; lgelectronics@amazon.com",
        DSRE="'Trisha Ballesteros' <trishab@dsrhawaii.com>, 'DSR Customer Service' <customerservice_trucking@dsrhawaii.com>",
        CGFR="'Clay Lewis' <clewis@challengerfreight.com>; 'Derek Goodnight' <Dgoodnight@cfslogisticsgroup.com>; 'Varanza Gonzales' <vgonzales@cfslogisticsgroup.com>; 'Kimberly Kindred' <kkindred@challengerfreight.com>; 'Erik Berry' <eberry@challengerfreight.com>; 'ops' <ops@challengerfreight.com>",
        HSXF="'Leimomi-Rose Bachiller' <lbachiller@hawaiianexpress.com>; 'Ruby Paiva' <rpaiva@hawaiianexpress.com>",
        MGZI="'Brett Bozeman' <bbozeman@magellanlogistics.com>; 'lgcns' <lgcns@magellanlogistics.com>",
        IVGC="robert.mize@invictusglobe.com; adam.hughes@invictusglobe.com; lisa.kim@invictusglobe.com",
        FDEN_EXP="'PremierGlobalSupport' <premierglobalsupport@fedex.com>",

        ## Update 07/23/2020 
        AFNW = "'AFN LG Electronics' <lg@afnww.com>; 'Henry Klobukowski' <Henry.Klobukowski@globaltranz.com>; 'AFN Ops 13' <afnops13@globaltranz.com>",
        FRCI = "'Eric Emswiler' <eric.emswiler@fcc-inc.com>; 'Russ Powell' <russ.powell@fcc-inc.com>; 'LG Electronics' <LG_Electronics@fcc-inc.com>; fcclge@fcc-inc.com",
        
    )