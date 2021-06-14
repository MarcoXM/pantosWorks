from config import Marco,content_generator
import pandas as pd
import os 
from utils import get_selected_cols_df,get_selected_values_df,joinStr,ensure_dir,get_daily_report_df,getDate_in_month,get_selected_values_over_df
from datetime import datetime 
from glob import glob


data_path = 'daily_route_data'

df = pd.read_csv(glob(f".\{data_path}\*.csv")[-1])
print(glob(f".\{data_path}\*.csv")[-1])



class DailySheet:
    def __init__(self, df, user, need_over_due = False):
        self.mode = ['end_of_month','regular'][ getDate_in_month() <= 22]
        self.alertType = ['Overdue 4', 'Overdue 3','Overdue 1', 'Overdue 2', 'Today', 'Upcoming 1','Upcoming 2' ]
        self.need_over_due = 
        self.df = df
        self.user = user
        self.week_day = datetime.now().weekday()
    
    
    def filter_by_carriers(self,df):
        return get_selected_values_df(df,self.user.carriers_code,col_name = 'Carrier Code')
    
    
    def filter_by_allert(self,df):
        self.all_allert_df = get_selected_values_df(df,self.alertType, col_name = 'Alert Type')
        if self.mode == 'regular':
            return get_selected_values_df(df,self.alertType[:5], col_name = 'Alert Type')
        elif self.mode == 'end_of_month':
            return get_selected_values_df(df,self.alertType, col_name = 'Alert Type')
    
    
    def get_each_carriers_iod_email_content(self , cols_send2carrier):
        user_carrier_df = self.filter_by_carriers(self.df)
        past_alert_user_carrier_df = self.filter_by_allert(user_carrier_df)
        
        ## dont show too much information to the carriers
        self.cleaned_df = past_alert_user_carrier_df
        return get_selected_cols_df(past_alert_user_carrier_df, cols_send2carrier)
    
    
    def get_high_value_loads(self):
        high_values_df = get_selected_values_over_df(self.cleaned_df, 10000.00, col_name = 'Sales')
        return high_values_df        
    
    
    def get_overdue(self,df):
        return get_selected_values_df(self.filter_by_carriers(df),['Overdue 4', 'Overdue 3', 'Overdue 2'],col_name = 'Alert Type')
    

    def save_daily_content2carriers(self, df, date_path):
        unique_files = sorted(df['Carrier Code'].unique())
        timestamp = str(datetime.now())[0:10]
        date_path = os.path.join(joinStr('Carrier Code'),str(datetime.now())[0:10])
        ensure_dir(date_path)
        
        ## unique identifier
        order = glob(f".\{data_path}\*.csv")[-1][-12:-4]
        final_folder = os.path.join(date_path, str(order))
        ensure_dir(final_folder)

        for col_value in unique_files:
            emails = Marco.carrier_email.get(col_value)
            carrier_df = df[df['Carrier Code'] == col_value]
            carrier_df.loc[0,'E-mail to'] = emails
            carrier_df.loc[0,'Subject'] = f"{col_value} Pending IOD {timestamp}"
            carrier_df.loc[0,'Content'] = content_generator(col_value)
            carrier_df.to_csv(os.path.join(final_folder,f"{col_value}_{timestamp}.csv"),index = False)
            print(f" Finished {col_value} content !!")
            
        ## all carriers 
        df.to_excel(os.path.join(final_folder,f"all_{timestamp}.xlsx"),index = False)
        print(f" Finished ALL carriers content !!")
        
        self.cleaned_df.to_excel(os.path.join(final_folder,f"all_cols_{timestamp}.xlsx"),index = False)
        print(f" Finished ALL cols and carriers content !!")
        
        if self.mode == 'end_of_month':
            self.get_high_value_loads().to_csv(os.path.join(final_folder,f"high_values_{timestamp}.csv"))
            print(f" Oh high values !! Finished high content !!")
            
        if self.week_day == 0 or self.need_over_due:
            over_due_df = self.get_overdue(df)
            over_due_df.to_excel(os.path.join(date_path,f"Over_due_Marco_{timestamp}.xlsx"))
            print(f" Oh Monday overdue !! Please send to Jinwoo !!")
            
                                               
                
        
                                               
                
def daily_route(df,Marco):
    print(f" Today is {str(datetime.now())[0:10]}")
    dailysheet = DailySheet(df,Marco)
    
    ## prepare for the data to e-mail
    dailysheet.save_daily_content2carriers(dailysheet.get_each_carriers_iod_email_content(Marco.colsSend2Carrier),data_path)





if __name__ == "__main__":
    daily_route(df,Marco)