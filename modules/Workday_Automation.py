from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import time as Time
from datetime import date
from modules.Selenium_Helper import Selenium_Helper 
from calendar import monthrange

class LogHours (Selenium_Helper):
    PATH_TYPE = By.XPATH
    PATH_MYTIME_BUTTON = ".//button[@aria-label-'MyTime']"
    PATH_TIMECLOCKHISTORY_BUTTON = ".//a[@title='Time Clock History']" 
    PATH_ADDCLOCKEVENT_BUTTON = ".//button[@title='Add Clock Event']"
    PATH_CLOCKEVENT_TIME_FIELD = ".//label[text()-'Time']/../../div[2]/div/div/input"
    PATH_CLOCKEVENT_EVENTTYPE_FIELD = ".//label[text()='Event Type']/../../div[2]/div/div/div/div/div" 
    PATH_CLOCKEVENT_EVENTTYPE_CHECKIN = ".//div[@aria-label='Check-in radio button unselected']"
    PATH_CLOCKEVENT_EVENTTYPE_CHECKOUT = ".//div[@aria-label='Check-out radio button unselected']" 
    PATH_CLOCKEVENT_EVENTTYPE_MEALOUT=".//div[@aria-label='Check-out (meal) radio button unselected']" 
    PATH_CLOCKEVENT_TIMETYPE_FIELD = ".//label[text()='Time Type']/../../div[2]/div/div/div/div/div" 
    PATH_CLOCKEVENT_TIMETYPE_TELECOMMUTE = ".//div[@aria-label='Telecommute radio button unselected']" 
    PATH_CLOCKEVENT_TIMETYPE_ONCALL = ".//div[@aria-label='On Call Pay radio button unselected']" 
    PATH_CLOCKEVENT_DATE_DAY = ".//input[@data-automation-id='dateSectionDay-input']"
    PATH_CLOCKEVENT_DATE_MONTH=".//input[@data-automation-id='dateSectionMonth-input']" 
    PATH_CLOCKEVENT_DATE_YEAR=".//input[@data-automation-id='dateSectionYear-input']"
    PATH_CLOCKEVENT_OK_BUTTON = ".//button[@title='OK']"
    PATH_CLOCKEVENT_DONE_BUTTON = ".//button[@title='Done']"

    TIMETYPE_TELECOMMUTE= "telecommute"
    TIMETYPE_ONCALL = "oncall"

    EVENTTYPE_CHECKIN = "checkin" 
    EVENTTYPE_CHECKOUT = "checkout" 
    EVENTTYPE_MEALOUT="mealout"

    TIME_DAY = "day" 
    TIME_MONTH = "month" 
    TIME_YEAR = "year"

    def __init__(self, driverPath, url):
        self.seleniumHelper=super(LogHours, self)
        self.seleniumHelper.__init__(driverPath, url)
        self.startTime = "08:00 AM" 
        self.startLunch = "12:00 PM"
        self.endLunch = "01:00 PM"
        self.endTime = "05:00 PM"

    def log_thisWeek(self):
        # Mon-0 Sun-7
        today = date.today()
        for ind in range(5):
            dayOffset = today.weekday()-ind
            monthOffset = 0
            yearOffset = 0
            if today.day-dayOffset < 1:
                monthOffset = 1
                if today.month == 1:
                    yearOffset = 1
            elif today.day-dayOffset > monthrange(today.year, today.month)[1]:
                monthOffset = -1
                if today.month == 12:
                    yearOffset = -1
            self.log_day(dayOffset, monthOffset, yearOffset) 
            self.seleniumHelper.wait(500)
            Time.sleep(1)

    def log_date(self, month, day, year): 
        monthOffset = date.today().month - month
        dayOffset = date.today().day - day
        yearOffset = date.today().year - year
        self.log_day(dayOffset, monthOffset, yearOffset)

    def log_today(self):
        self.log_day(0, 0, 0)

    def log_day(self, dayOffset, monthOffset, yearOffset):
        self.add_clockEvent(self.startTime, self.EVENTTYPE_CHECKIN, dayOffset, monthOffset, yearOffset) 
        self.add_clockEvent(self.startLunch, self.EVENTTYPE_MEALOUT, dayOffset, monthOffset, yearOffset) 
        self.add_clockEvent(self.endLunch, self.EVENTTYPE_CHECKIN, dayOffset, monthOffset, yearOffset) 
        self.add_clockEvent(self.endTime, self.EVENTTYPE_CHECKOUT, dayOffset, monthOffset, yearOffset)

    def add_clockEvent(self, time, eventType, dayOffset, monthOffset, yearOffset):
        self.seleniumHelper.wait(100)
        Time.sleep(5)
        self.select_addClockEvent()
        self.set_clockEvent_date(self.TIME_MONTH, monthOffset)
        self.set_clockEvent_eventType(eventType)
        if eventType == self.EVENTTYPE_CHECKIN:
            self.set_clockEvent_timeType(self.TIMETYPE_TELECOMMUTE)
            self.set_clockEvent_date(self.TIME_YEAR, yearOffset)
            self.set_clockEvent_time(time)
            self.set_clockEvent_date(self.TIME_DAY, dayOffset)
            self.submit_clockEvent()

    def navigateTo_timeClockHistory(self):
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_MYTIME_BUTTON) 
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_TIMECLOCKHISTORY_BUTTON)

    def end_session(self):
        self.seleniumHelper.end()

    def select_addClockEvent(self):
        # Should happen after navigating to timeClockHistory
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_ADDCLOCKEVENT_BUTTON)  

    def set_clockEvent_eventType(self, eventType):
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_EVENTTYPE_FIELD)
        if eventType == self.EVENTTYPE_CHECKIN:
            self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_EVENTTYPE_CHECKIN)
        elif eventType == self.EVENTTYPE_MEALOUT:
            self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_EVENTTYPE_MEALOUT) 
        elif eventType == self.EVENTTYPE_CHECKOUT:
            self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_EVENTTYPE_CHECKOUT)
        else:
            print("Did not recognize event type") 
            exit(1)

    def set_clockEvent_timeType(self, timeType): 
        # Must happen after EventType is set
        # Defaults to regular
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_TIMETYPE_FIELD)
        if timeType == self.TIMETYPE_TELECOMMUTE:
            self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_TIMETYPE_TELECOMMUTE)
        elif timeType == self.TIMETYPE_ONCALL:
            self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_TIMETYPE_ONCALL)
        else:
            print("Did not recognize time type")
            exit(1)

    def set_clockEvent_time(self, time):
        self.seleniumHelper.clear_fill_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_TIME_FIELD, time)

    def set_clockEvent_date(self, type, offset):
        key = Keys.ARROW_DOWN if offset >= 0 else Keys.ARROW_UP
        times = abs(offset) 
        if type == self.TIME_DAY:
            self.seleniumHelper.sendKeyTo_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_DATE_DAY, key, times)
        elif type == self.TIME_MONTH:
            self.seleniumHelper.sendKeyTo_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_DATE_MONTH, key, times)
        elif type == self.TIME_YEAR:
            self.seleniumHelper.sendKeyTo_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_DATE_YEAR, key, times)
        else:
            print("Did not recognize time as month, day or year")
            exit(1)
            
    def submit_clockEvent(self):
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_OK_BUTTON) 
        self.seleniumHelper.click_element(self.PATH_TYPE, self.PATH_CLOCKEVENT_DONE_BUTTON)