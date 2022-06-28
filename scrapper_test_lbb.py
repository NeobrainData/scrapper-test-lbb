from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time

path = "/Users/nathanredin/Documents/Git_neobrain/geckodriver"

class SeleniumTemplate:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=path)

    #Not used
    def get_trainings(self, code,cp,max_distance):
        base_url = "https://labonneboite.pole-emploi.fr/entreprises?j=" + str(code) +  "&l=" +str(cp)+ "&sort=score&h=1&tr=car&d="+str(max_distance) +"&tr=car"
        self.driver.get(base_url+ '&from=1&to=100')
        time.sleep(2)
        try:
            self.driver.find_element(By.ID,"footer_tc_privacy_button_2").click()
        except:
            None
        companies = self.driver.find_elements(By.CLASS_NAME,"lbb-bright-container")
        results = []

        for company in companies:
            try:
                h3 = company.find_element(By.TAG_NAME,'h3')
            except:
                h3 = None

            if h3 != None:
                try:
                    company_name = h3.text.split('-')[0].rstrip()
                except:
                    company_name = None
                try:
                    location = h3.text.split('-')[1].lstrip()
                except:
                    location = None

                try:
                    num_employees = company.find_element(By.CLASS_NAME,'grid-col-8').find_element(By.TAG_NAME,'p').text
                except:
                    num_employees = None

                try:
                    distance = str(company.find_element(By.CLASS_NAME,'travel-distance-duration').text.replace(' km de votre lieu de recherche', '').replace(' min en voiture', '').split(" ")[0])
                except:
                    distance = None

                try:
                    time_travel = str(company.find_element(By.CLASS_NAME,'travel-distance-duration').text.replace(' km de votre lieu de recherche', '').replace(' min en voiture', '').split(" ")[1])
                except:
                    time_travel = None

                try:
                    rating = company.find_element(By.CLASS_NAME,'rating-value').text
                except:
                    rating = None

                #mail adress:
                try:
                    hehe = company.find_element(By.CLASS_NAME,'break-word')
                    mail = hehe.get_attribute("href").split(":")[-1]
                except:
                    mail = "NaN"

                results.append(
                    {
                        #'jobs': get_value(rome_codes, 'Code ROME', 'Intitulé du poste', code),
                        'rome_code': code,
                        'company_name': company_name,
                        'location': location,
                        'num_employees': num_employees,
                        'distance': distance,
                        'time_travel':time_travel,
                        'rating': rating,
                        'code postal': cp,
                        'mail':mail
                    }
                )

        return results

code = "N1303"
name = "Intervention technique d'exploitation logistique "
cp = 93290 #zip code
max_distance=30 #MAX DISTANCES: 5, 10, 30, 50 OR 100 otherwise will bug the code