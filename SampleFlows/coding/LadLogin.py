from playwright.sync_api import sync_playwright
from Utilities.read_config import AppConfiguration
# from LadSportsPage import SportsListPage
# from Pages.base_page import BasePage
# from playwright.sync_api import Page
from datetime import datetime

class LadbrokesLogin():
    class _Selectors:
        USERNAME = "#userId"
        PASSWORD = "input[type='password']"  # or use "input[formcontrolname='password']" "#password"
        LOGIN_BUTTON = "button.login"  # or use "button.btn.btn-primary""#login-button"
        ERROR_MSG = "[data-test='error']"
        REMEMBER_ME = "#rememberMe"  # selector for the checkbox
    
    # def __init__(self, page: Page):
    #     super().__init__(page)
    #     self._selectors = self._Selectors()
    #     self.common_info = AppConfiguration.get_common_info()
    #     self.configuration = AppConfiguration.get_app_configuration()

    def __init__(self):
        self.common_info = AppConfiguration.get_common_info()
        self.configuration = AppConfiguration.get_app_configuration()
        self._selectors = self._Selectors()
        # self._selectors = {
        #     'USERNAME': "input[formcontrolname='username']",
        #     'PASSWORD': "input[formcontrolname='password']",
        #     'LOGIN_BUTTON': "button.login",
        #     'REMEMBER_ME': "#rememberMe"
        # }

    def get_user_credentials(self, user_type):
        return {
            "username": self.common_info[user_type + "UserName"],
            "password": self.common_info[user_type + "Password"]
        }

    def login(self, username: str, password: str, url: str, team1: str, team2: str, remember_me: bool = False):
        with sync_playwright() as playwright:
            # Browser options
            base_url = self.common_info["Url"]
            headless = eval(self.configuration["Headless"])  # convert to bool
            slow_mo = float(self.configuration["SlowMo"])
            launch_options = {"headless": headless, "slow_mo": slow_mo}


            # browser = playwright.chromium.launch(**launch_options, args=['--start-maximized'])
            browser = playwright.firefox.launch(**launch_options) #firefox
            context_options = {'base_url': base_url}
            browser_context = browser.new_context(**context_options, viewport={"width": 960, "height": 1080}) #firefox
            # browser_context = browser.new_context(**context_options, no_viewport=True)
            browser_context.set_default_navigation_timeout(float(self.configuration["DefaultNavigationTimeout"]))
            browser_context.set_default_timeout(float(self.configuration["DefaultTimeout"]))
            page = browser_context.new_page()
            
            page.goto(base_url)
            if remember_me:
                page.click(self._selectors.REMEMBER_ME)

            page.fill(self._selectors.USERNAME, username)
            page.fill(self._selectors.PASSWORD, password)
            page.click(self._selectors.LOGIN_BUTTON)
            #     page.click(self._selectors['REMEMBER_ME'])
            # page.fill(self._selectors['USERNAME'], username)
            # page.fill(self._selectors['PASSWORD'], password)
            
            # page.click(self._selectors['LOGIN_BUTTON'])
            # page.wait_for_load_state('networkidle')
            page.wait_for_timeout(4000) 
            # url =  "https://sports.ladbrokes.com/event/football/portuguese/portuguese-liga-portugal-2/fc-alverca-v-cd-tondela/248405163"
            # url = "https://sports.ladbrokes.com/event/football/costa-rican/costa-rican-primera-division-clausura/puntarenas-fc-v-cs-herediano/248457894/"
            page.goto(url)
            page.wait_for_timeout(1000)

            teams_segment = url.split('/')[-3]  # Gets 'real-madrid-v-fc-barcelona'
            print(teams_segment)
            # Now you can proceed with splitting team names
            # teams = teams_segment.split("-v-")
            # team1 = teams[0].replace("-", " ").title().upper()  # "Real Madrid"
            # team2 = teams[1].replace("-", " ").title().upper()  # "FC Barcelona"
            
            # Now we can use these variables in our selectors
            # page.click("xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'Draw')]/../..//button[@data-crlat='betButton']")
            # page.click("xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'Puntarenas FC')]/../..//button[@data-crlat='betButton']")
            # page.click("xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'CS Herediano')]/../..//button[@data-crlat='betButton']")
            # page.click("xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'Draw')]/../..//button[@data-crlat='betButton']")
            def convert_odds_to_decimal(odds_str):
                if '/' in odds_str:
                    num, den = map(int, odds_str.split('/'))
                    return num/den + 1
                return float(odds_str)
            
            # Get odds for team1 (first element only)
            team1_odds_element = page.locator(f"xpath=(//span[@data-crlat='outcomeEntity.name'][contains(text(),'{team1}')]/../..//span[@data-crlat='oddsPrice'])[1]")
            team1_odds = convert_odds_to_decimal(team1_odds_element.inner_text())

            # Get odds for team2 (first element only)
            team2_odds_element = page.locator(f"xpath=(//span[@data-crlat='outcomeEntity.name'][contains(text(),'{team2}')]/../..//span[@data-crlat='oddsPrice'])[1]")
            team2_odds = convert_odds_to_decimal(team2_odds_element.inner_text())

            # Check if odds are below 2.0 (equivalent to 1/1)
            if team1_odds < 2.0:
                print(f"Team {team1} odds too low: {team1_odds_element.inner_text()}")
                return

            if team2_odds < 2.0:
                print(f"Team {team2} odds too low: {team2_odds_element.inner_text()}")
                return

            # If odds are acceptable, proceed with clicking
            page.click(f"xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'{team1}')]/../..//button[@data-crlat='betButton']")
            page.click(f"xpath=//span[@data-crlat='outcomeEntity.name'][contains(text(),'{team2}')]/../..//button[@data-crlat='betButton']")

            # all_data = []
            page.wait_for_timeout(1000)

            # First click to focus on the input field
            page.click("#allSingleStakes")

            # Then fill in the stake amount
            page.fill("#allSingleStakes", "0.1")

            # Click the Place Bet button
            # page.click("button.base-btn.betnow-btn")
            print(f"place bet at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


            # # # Extract data from the current page
            # # elements = page.query_selector_all()
            # # for element in elements:
            # #     all_data.append(element.text_content().strip())

            # Save the complete page HTML
            # html_content = page.content()
            # with open('bet.html', 'w', encoding='utf-8') as f:
            #     f.write(html_content)

            # # # Add navigation to sports page here
            # # # self.navigate_to_sports()

            # page.pause()
            page.wait_for_timeout(20000)

    # def navigate_to_sports(self):
    #     # from Pages.Sports.sports_list_page import SportsListPage
    #     sports_page = SportsListPage(self.current_page)
    #     sports_page.navigate_to_sports()
    #     sports_page.wait_for_sports_page_load()
    #     return sports_page


# Usage example
# if __name__ == "__main__":
#     import time
    
#     login = LadbrokesLogin()
#     creds = login.get_user_credentials("Valid")
    
#     for i in range(4):
#         login.login(creds["username"], creds["password"], 
#                     "https://sports.ladbrokes.com/event/football/brazilian/carioca/fluminense-fc-rj-v-sampaio-correa-fe-rj/248319316/", 
#                     "Fluminense FC RJ", 
#                     "Sampaio Correa FE RJ", 
#                     remember_me=True)
#         if i < 3:  # Don't sleep after the last iteration
#             time.sleep(60*4)

if __name__ == "__main__":
    from datetime import datetime, timedelta
    import time

    login = LadbrokesLogin()
    creds = login.get_user_credentials("Valid")
    
    for i in range(4):
        print(f"\nExecution #{i+1} of 4")
        login.login(creds["username"], 
                   creds["password"],
                   "https://sports.ladbrokes.com/event/football/scottish/scottish-premiership/dundee-fc-v-celtic/248453178",
                   "Draw",
                   "Celtic",
                   remember_me=True)
        
        if i < 3:  # Don't countdown after the last iteration
            target_time = datetime.now() + timedelta(minutes=4)
            while datetime.now() < target_time:
                remaining = target_time - datetime.now()
                minutes, seconds = divmod(remaining.seconds, 60)
                print(f"\rNext bet in: {minutes:02d}:{seconds:02d}", end="", flush=True)
                time.sleep(1)
