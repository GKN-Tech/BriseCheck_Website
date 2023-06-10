# Project Overview

“BriseCheck” is a website that scrapes AQI (Air Quality Monitoring) data from India’s official website and presents it in an easy-to-understand format, allowing individuals to make informed decisions about their health and provides a downloadable file with formatted data, empowering the ability to perform analysis on Air Quality Data. India’s website was chosen for this project because air quality is a significant problem in India and the data fluctuates more frequently compared to other countries, thus monitoring such data is more comprehensible. Further, an example of analysis that can be performed using the CSV formatted file is logging all data from file into a database after certain intervals of time and calculating averages of pollution concentration for each day. Then any kind of visualization such as a line chart can be plotted from these averages to track the improvement in reducing the pollution levels. 

**Listed below are the primary functionalities of this website:**

* Real time AQI data in a concise format of tables. 

* Filters to facilitate data search. 

* Choropleth map and scatter plot for data visualization. 

* Downloadable CSV file for performing data analysis. 

* Engaging game communicating a message to save the trees. 

_Note: India’s website provides AQI-US and AQI-IN, the data is different for these two standards. “BriseCheck” shows the data based on AQI-US._




**Resources Used**

The Flask, which is a python web framework and Jinja2 which is a python web template engine are used for this project. The frontend templates are coded using HTML, CSS and JavaScript languages. The backend functions are programmed using various python libraries and modules. Selenium is primarily used to run the chrome web driver and scrape the information inside HTML elements using their xpath. For all data processing and data conversion, the Pandas library is utilized. The Express module from python’s Plotly library is used in coding the visualizations. For writing the Eco-Game, Pygame is used. Pyrebase, which is a python interface to the REST API of Firebase helps in setting up the form on contact page and send the POST requests to the realtime database in Firebase. The website is coded in Visual Studio Code however, the WebCrawler and other functions were written in PyCharm and later integrated into one workspace. Unit tests were performed on the localhost with the help of Werkzueg that provides a development server. 

**Below are the references to resources from the internet.**

>India’s AQI website: https://www.aqi.in/   
>
>Website logo: https://logo.com/  
>
>Text Fonts: https://fonts.google.com/  
>
>The GeoJSON file for India’s choropleth map:  https://un-mapped.carto.com/tables/states_india/public/map  
>
>The keyframe ideas for animations on the website: https://codepen.io/  




**Limitation**

The Eco-Game icon has to be manually clicked by the player in taskbar for showing the window up on screen. 



 

 
