from flask import Blueprint, render_template, request, make_response


from selenium import webdriver
import pandas as pd
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods = ['GET', 'POST'])
def crawler():
    
    website = "https://www.aqi.in/ca/dashboard/india#:~:text=The%20current%20PM2.,hrs%20air%20quality%20guidelines%20value."

    driver = webdriver.Chrome()
    driver.get(website)

    # Output the overall PM2.5 concentration
    India_overall = driver.find_element("xpath", '//span[@class="Pollutants_sensor_text pm25"]').text

    # Scrape the data
    rows = driver.find_elements("xpath", '//*[@id="state-table"]/tbody/tr')
    states = []
    status = []
    aqi_us = []
    pm25 = []
    pm10 = []
    temp = []
    humid = []

    for row in rows:
        states.append(row.find_element("xpath", './th').text)
        status.append(row.find_element("xpath", './td[1]').text)
        aqi_us.append(row.find_element("xpath", './td[3]').text)
        pm25.append(row.find_element("xpath", './td[5]').text)
        pm10.append(row.find_element("xpath", './td[6]').text)
        temp.append(row.find_element("xpath", './td[7]').text)
        humid.append(row.find_element("xpath", './td[8]').text)

    # Save data in csv
    df = pd.DataFrame({'States': states, 'Status': status, 'AQI-US': aqi_us, 'PM2.5': pm25, 'PM10': pm10, 'Temperature': temp, 'Humidity': humid})
    df.to_csv("website\static\IndianAQI.csv", index=False)

    instate = ""
    instatus = ""
    p_output = ""
    s_output = ""

    
    driver.quit()

    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # Get input from user
    if request.method == 'POST':
        instate = request.form.get('instate', '')
        instatus = request.form.get('instatus', '')

        # Output filtered with states
        if instate != '':
            for state in states:
                if state == instate:
                    p_df = df.loc[df['States'] == state].reset_index(drop=True)
                    p_output = p_df.to_html(index=False).replace('<tr style="text-align: right;">', '<tr style="text-align: center; background-color: #FFFFFF; color: #551E19">').replace('<th>', '<th style="padding-right: 15px; padding-left: 15px">').replace('<tr>', '<tr style="background-color: rgba(255,255,255,.2)">')

        # Output filtered with status
        if instatus != '':
            for value in status:
                if value == instatus:
                    s_df = df.loc[df['Status'] == value].reset_index(drop=True)
                    s_output = s_df.to_html(index=False).replace('<tr style="text-align: right;">', '<tr style="text-align: center; background-color: #FFFFFF; color: #551E19">').replace('<th>', '<th style="padding-right: 15px; padding-left: 15px">').replace('<tr>', '<tr style="background-color: rgba(255,255,255,.2)">')
                    break


    return render_template("index.html", overall = India_overall, p = instate, s = instatus, output1 = p_output, output2 = s_output, t = time)


