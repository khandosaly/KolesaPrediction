import json

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'))

cars = []
global_counter = 0
for i in range(1, 10):
    driver.get(f"https://kolesa.kz/cars/?page={i}")
    car_boxes = driver.find_elements(by=By.CLASS_NAME, value="a-info-side.col-right-list")
    for car_box in car_boxes:
        print(f'\r Car: {global_counter}, Page: {i}', end='')
        car_dict = {'id': global_counter}
        try:
            #info_top = car_box.find_element(by=By.CLASS_NAME, value='a-info-top')
            #title = info_top.find_element(by=By.CLASS_NAME, value='list-link').text
            title = car_box.find_element(by=By.CLASS_NAME, value='list-link').text

            man_word_count = 1
            for man_two_word in [
                'Alfa Romeo', 'Aston Martin', 'Great Wall', 'Iran Khodro', 'Land Rover', 'ВАЗ (Lada)'
            ]:
                if man_two_word in title:
                    man_word_count = 2

            car_dict['manufacturer'] = ' '.join(title.split()[0:man_word_count]).strip()
            car_dict['model'] = ' '.join(title.split()[man_word_count:]).strip()
            #car_dict['price'] = info_top.find_element(by=By.CLASS_NAME, value='price').text.strip()
            car_dict['price'] = car_box.find_element(by=By.CLASS_NAME, value='price').text.strip()
        except Exception as e:
            print(e)

        try:
            #info_mid = car_box.find_element(by=By.CLASS_NAME, value='a-info-mid')
            #description = info_mid.find_element(by=By.CLASS_NAME, value='a-search-description').text
            description = car_box.find_element(by=By.CLASS_NAME, value='a-search-description').text
            description_tokens = description.split(',')
            car_dict['year'] = description_tokens[0].split()[0].strip()
            car_dict['body'] = description_tokens[1].split()[-1].strip()
            car_dict['engine_volume'] = description_tokens[2].split()[0].strip()
            car_dict['fuel_type'] = description_tokens[3].strip()
            car_dict['transmission'] = ' '.join(description_tokens[4].split()[1:]).strip()
        except Exception as e:
            print(e)

        try:
            #info_bot = car_box.find_element(by=By.CLASS_NAME, value='a-info-bot')
            #car_dict['city'] = info_bot.find_element(by=By.CLASS_NAME, value='list-region').text.strip()
            #car_dict['date'] = info_bot.find_element(by=By.CLASS_NAME, value='date').text.strip()
            #car_dict['views_count'] = info_bot.find_element(by=By.CLASS_NAME, value='nb-views-int').text.strip()
            car_dict['city'] = car_box.find_element(by=By.CLASS_NAME, value='list-region').text.strip()
            car_dict['date'] = car_box.find_element(by=By.CLASS_NAME, value='date').text.strip()
            car_dict['views_count'] = car_box.find_element(by=By.CLASS_NAME, value='nb-views-int').text.strip()
        except Exception as e:
            print(e)

        cars.append(car_dict)
        global_counter += 1

with open('json_data.json', 'w') as outfile:
    json.dump(cars, outfile, ensure_ascii=False)


