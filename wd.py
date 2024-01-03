from modules.Workday_Automation import LogHours

CHROME_DRIVER_PATH = "C:\\Applications\\chromedriver.exe"
WORKDAY_URL = "https://wd5.myworkday.com/schwab/d/home.htmld"

wd = LogHours (CHROME_DRIVER_PATH, WORKDAY_URL)
wd.navigateTo_timeClockHistory()
wd.end_session()
#wd.log_today()
wd.log_thisWeek()

#wd.log_date(10,12,2023)
#wd.log_date(10,13,2023)

