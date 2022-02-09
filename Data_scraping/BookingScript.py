import copy
import json
import logging
import traceback

import twint as twint
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import get_tiwint


class BookingScript:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        chrome_options.add_argument("--remote-debugging-port=8000")
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.driver = webdriver.Chrome(options=chrome_options,desired_capabilities=caps)
        wait = WebDriverWait(self.driver, 30)
        action = ActionChains(self.driver)
        self.domain = 'https://www.booking.com'
        self.driver.get('https://www.booking.com')
        self.driver.maximize_window()


    def fill_form(self, search_argument):
        '''Finds all the input tags in form and makes a POST requests.'''
        print(search_argument)

        search_field = self.driver.find_element_by_id('ss')
        search_field.send_keys(search_argument)
        print(search_field.text)
        # We look for the search button and click it
        self.driver.find_element_by_class_name('sb-searchbox__button') \
            .click()

        time.sleep(5)
        wait = WebDriverWait(self.driver, timeout=60).until(
            EC.presence_of_all_elements_located(
                (By.ID,
                 'ajaxsrwrap')))
        self.driver.find_elements(
            By.CSS_SELECTOR,
            'div.fde444d7ef._c445487e2')[0].click()

    def scrape_results(self, n_results):
        '''Returns the data from n_results amount of results.'''
        accommodations_urls = list()
        accommodations_data = list()

        for accomodation_title in self.driver.find_elements_by_class_name('sr-hotel__title'):
            accommodations_urls.append(accomodation_title.find_element_by_class_name(
                'hotel_name_link').get_attribute('href'))

        for url in range(0, n_results):
            if url == n_results:
                break
            url_data = self.scrape_accommodation_data(self.driver, accommodations_urls[url])
            accommodations_data.append(url_data)

        return accommodations_data

    def scrape_accommodation_data(self):
        '''Visits an accommodation page and extracts the data.'''
        accommodation_fields = dict()
        # Get the accommodation name
        self.driver.switch_to.active_element
        self.driver.switch_to.window(self.driver.window_handles[1])
        title = self.driver.find_element(By.CSS_SELECTOR,'h2#hp_hotel_name');
        accommodation_fields['name'] = title.text
        # Get the accommodation score
        accommodation_fields['score'] = self.driver.find_element_by_xpath(
            "//*[@id=\"js--hp-gallery-scorecard\"]/a/div/div/div/div/div[1]").text

        # Get the accommodation location
        accommodation_fields['location'] = self.driver.find_element_by_id('showMap2') \
            .find_element_by_class_name('hp_address_subtitle').text
        return accommodation_fields
        # Get the most popular facilities

    def Convert(lst:list()):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct
    def get_sous_category(self):
        self.driver.find_element_by_xpath('//*[@id="show_reviews_tab"]').click();
        self.driver.implicitly_wait(2);
        category_list = list();
        try:
            categories_list = self.driver.find_element_by_xpath("//*[@id=\"review_list_score\"]/div[4]/div/div/ul")
            for child in categories_list.find_elements_by_tag_name('span'):
                if not child.text: continue;
                category_list.append(child.text)
            res_dct = {category_list[i].replace(" ",''): category_list[i + 1] for i in range(0, len(category_list), 2)}
            print(res_dct)

            return res_dct
        except Exception as e:
            logging.error(traceback.format_exc())
            pass
    def get_popular_facility(self):
        facility_list=list()
        try:
            facilities = self.driver.find_element_by_class_name('hp_desc_important_facilities')

            for facility in facilities.find_elements_by_class_name('important_facility'):
                facility_list.append(facility.text)
            return facility_list
        except:
            print("------------no_facility")
            pass
    def get_comment(self):
            try:
                self.driver.find_element(By.CSS_SELECTOR,'a.pagenext').click();
            except:
                pass
            browser_log = self.driver.get_log('performance')
            print(type(browser_log))
            list_url_li=[]
            for log in browser_log:
                tmp=json.loads(log['message'])
                if tmp['message']['method']=='Network.requestWillBeSent':
                    if 'reviewlist.html' in tmp['message']['params']['request']['url']:
                        list_url_li.append(tmp['message']['params']['request']['url'])
            print(list_url_li)
       # nbr_page = self.driver.find_element(By.XPATH,
                                           # '//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[2]/div/div[7]/a/span[1]').text
        #nbr_page = int(nbr_page);
            comment_list = list()
            self.driver.get(list_url_li[0])
            self.driver.switch_to.active_element
            self.driver.switch_to.window(self.driver.window_handles[-1])
            try:
                numbers_of_pages=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/div/div[2]/div/div[7]/a/span[1]').text;
                numbers_of_pages=int(numbers_of_pages);
                print(numbers_of_pages)
                for i in range(numbers_of_pages):
                    print(i)
                    try:
                        WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.review_list_new_item_block')))
                        li_list = self.driver.find_elements(By.CSS_SELECTOR, 'li.review_list_new_item_block')
                    except TimeoutException:
                        continue;
                    time.sleep(2)
                    for li in li_list:
                        try:
                            name = li.find_element(By.CSS_SELECTOR, 'span.bui-avatar-block__title').text
                        except NoSuchElementException:
                            print(f"page {i} :--------------------name")

                            continue
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.bui-avatar-block__title')))
                            nationality = li.find_element(By.CLASS_NAME, 'bui-avatar-block__subtitle').text
                        except NoSuchElementException:
                            print(f"page {i} :--------------------nationality")

                            continue
                        try:
                            number_of_nights = li.find_element(By.CSS_SELECTOR, 'ul.c-review-block__stay-date').text
                        except NoSuchElementException:
                            print(f"page {i} :--------------------number_of_nights")
                            continue
                        try:
                            clinet_type = li.find_element(By.CSS_SELECTOR,
                                                      'ul.review-panel-wide__traveller_type').find_element(
                            By.CSS_SELECTOR, "div.bui-list__body").text
                        except NoSuchElementException:
                            print(f"page {i} =---------------------clinet_type")
                            continue
                        try:
                            room_type = li.find_element(By.CSS_SELECTOR,
                                                    'ul.bui-list.bui-list--text.bui-list--icon.bui_font_caption').text
                            review_date = li.find_elements(By.CSS_SELECTOR, 'span.c-review-block__date')[1].text
                            visite_date = li.find_element(By.CSS_SELECTOR, 'span.c-review-block__date').text
                            text = li.find_element(By.CSS_SELECTOR, 'span.c-review__body').text
                            score = li.find_element(By.CSS_SELECTOR, 'div.bui-review-score__badge').text
                        except NoSuchElementException:
                            print(f"page {i} :--------------------review_date")
                            continue
                        comment_list.append({"name": copy.copy(name), "nationality": copy.copy(nationality),
                                         "number_of_nights": copy.copy(number_of_nights),
                                         "clinet_type": copy.copy(clinet_type), "room_type": copy.copy(room_type),
                                         "review_date": copy.copy(review_date),
                                         "visite_date": copy.copy(visite_date), "text": copy.copy(text),
                                         "score": copy.copy(score)});
                    if i < (numbers_of_pages - 1):
                        next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.pagenext')
                        next_button.click()

                return comment_list;
            except:
                print('---------------->ERROR');

    def twitterScrapper(self,h):
        return  get_tiwint.twitterScrapper(h);

    def run_all(self,hotel_name):
            path="D:\hotel_data\\"+hotel_name;
            self.fill_form(hotel_name);
            tw_comment=self.twitterScrapper(hotel_name)
            hotel_data = self.scrape_accommodation_data();
            sousCategory = self.get_sous_category()
            import os
            if not os.path.exists(path):
                os.makedirs(path)
            hotel_comment = self.get_comment();
            hotel_comment=hotel_comment+tw_comment;
            hotel_dict={};
            hotel_dict["name"]=hotel_data["name"];
            hotel_dict["location"]=hotel_data["location"];
            hotel_dict["Score"]=hotel_data["score"];
            hotel_dict["sous_Category"]=sousCategory;

            with open(path+"\\1_"+hotel_name+"_info.json","w") as f:
                json.dump(hotel_dict,f)
            with open(path +"\\2_"+hotel_name + "_comment.json", "w") as f:
                json.dump(hotel_comment, f)
            self.driver.quit()




if __name__ == '__main__':
    f = open('hotel_list.json')
    data=json.load(f)
    for h in data:
        try:
           scriptboocking = BookingScript();
           scriptboocking.run_all(h)
        except:
            print("------------>Error "+h)
            continue
        finally:
            scriptboocking.driver.quit()










