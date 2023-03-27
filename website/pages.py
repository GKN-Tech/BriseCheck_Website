from flask import Blueprint, render_template, request

import pyrebase

import pygame
import random
import time


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
# import plotly.io as pio
# from dash import Dash, dcc, html
# from base64 import b64encode
# import io

pages = Blueprint('pages', __name__)

config = {
    "apiKey": "AIzaSyABJ10ymkdku0rAHTc2UNw-T0ibKiyTNps",
    "authDomain": "brisecheck.firebaseapp.com",
    "databaseURL": "https://brisecheck-default-rtdb.firebaseio.com",
    "projectId": "brisecheck",
    "storageBucket": "brisecheck.appspot.com",
    "messagingSenderId": "207142188678",
    "appId": "1:207142188678:web:8c216ac4d5e47a474cc307"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
@pages.route('/contact', methods = ['GET', 'POST'])
def contact():
    thank = ""
    if request.method == 'POST':
        Email = request.form["user-email"]
        db.child("Email").push(Email)
        Message = request.form["message"]
        db.child("Message").push(Message)
        thank = "Thanks for your valuable feedback!"
    return render_template("contact.html", thank = thank)



@pages.route('/game', methods  = ['GET', 'POST'])
def game():

    # Initialize Pygame
    pygame.init()
        
    WIDTH, HEIGHT = 900, 600 
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eco-Game")

    BG = pygame.transform.scale(pygame.image.load("website\static\images\\bg.jpg"), (WIDTH, HEIGHT))

    # Constants
    TREE_WIDTH = 90
    TREE_HEIGHT = 90

    TREE_VEL = 7
    STAR_VEL = 5

    TREE_X = 200
    TREE_Y = HEIGHT - TREE_HEIGHT

    STAR_WIDTH = 10
    START_HEIGHT = 15

    playername = ""

    pygame.font.init()
    FONT_TIME = pygame.font.SysFont("Times New Roman", 30)
    FONT_RESULT = pygame.font.SysFont("Verdana", 50)

    def draw(tree, tree_rect, elapsed_time, stars):
        WIN.blit(BG, (0,0))
        # WIN.fill((0,0,0))

        time_text = FONT_TIME.render(f"Time: {round(elapsed_time)}s", 1, "white")
        WIN.blit(time_text, (10, 10))

        name_text = FONT_TIME.render(f"Player: {playername}", 1, "white")
        WIN.blit(name_text, (890 - name_text.get_width(), 10))

        # Drawing Tree
        WIN.blit(tree, tree_rect)

        # Drawing the stars
        for star in stars:
            pygame.draw.rect(WIN, "white", star)

        pygame.display.update()

    def gmain():
        pygame.init()
        run = True

        # Creating Tree
        tree = pygame.transform.scale(pygame.image.load("website\static\images\\tree_c.png"), (TREE_WIDTH, TREE_HEIGHT))
        tree_rect = tree.get_rect()
        tree_rect.x = TREE_X
        tree_rect.y = TREE_Y

        clock = pygame.time.Clock()

        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False

        # Game loop
        while run:
            # To have same speed of loop on all computers (slower or faster)
            star_count += clock.tick(20) # Track number of milliseconds elapsed since last loop
            elapsed_time = time.time() - start_time

            # Play the loop for this much time
            if elapsed_time >= 60:
                won_text = FONT_RESULT.render(f"Congratulations {playername}! You WON", 1, (102, 204, 0), "white")
                WIN.blit(won_text, (WIDTH/2 - won_text.get_width()/2, HEIGHT/2 - won_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(5000)
                break

            if star_count > star_add_increment:
                for _ in range(2):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -START_HEIGHT, STAR_WIDTH, START_HEIGHT)
                    stars.append(star)

                    star_add_increment = max(200, star_add_increment - 20)
                    star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            
            # Moving the Tree
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and tree_rect.x - TREE_VEL >= 0:
                tree_rect.x -= TREE_VEL
            if keys[pygame.K_RIGHT] and tree_rect.x + tree_rect.width + TREE_VEL <= WIDTH:
                tree_rect.x += TREE_VEL

            # Moving the stars
            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                if star.y + star.height >= TREE_Y and star.colliderect(tree_rect):
                    stars.remove(star)
                    hit = True
                    break 

            if hit:
                lost_text = FONT_RESULT.render("Game Over!", 1, "white", "red")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(3000)
                break

            draw(tree, tree_rect, elapsed_time, stars)
        
        pygame.quit()
    
    
    if request.method == 'POST':
        playername = request.form.get('playername', '')
        gmain()

    return render_template("game.html")



@pages.route('/viz')
def viz():
    def colormap():
        # app = Dash(__name__)
        # buffer = io.StringIO()

        #pio.renderers.default = 'browser'

        # GeoJSON file for Indian states
        india_states = json.load(open('website\static\states_india.geojson', 'r'))

        # Read CSV data file
        df = pd.read_csv('website\static\IndianAQI.csv')

        # Changing state name spellings with geojson file spellings
        df.iloc[:, 0] = df.iloc[:, 0].replace('Arunachal Pradesh', 'Arunanchal Pradesh')
        df.iloc[:, 0] = df.iloc[:, 0].replace('Dadra And Nagar Haveli', 'Dadara & Nagar Havelli')
        df.iloc[:, 0] = df.iloc[:, 0].replace('Daman And Diu', 'Daman & Diu')
        df.iloc[:, 0] = df.iloc[:, 0].replace('Delhi', 'NCT of Delhi')
        df.iloc[:, 0] = df.iloc[:, 0].replace('Jammu And Kashmir', 'Jammu & Kashmir')

        # id for each state
        state_id_map = {}
        for feature in india_states['features']:
            feature['id'] = feature['properties']['state_code']
            state_id_map[feature['properties']['st_nm']] = feature['id']

        # Creating id column in df
        df['id'] = df['States'].apply(lambda x: state_id_map[x])

        # Choropleth graph
        fig = px.choropleth_mapbox(
            df,
            locations = 'id',
            geojson = india_states,
            color = 'PM2.5',
            hover_name = 'States',
            hover_data = ['Status', 'Temperature', 'PM10'],
            title="India Air Quality",
            center={"lat": 24, "lon": 78},
            mapbox_style="carto-positron",
            zoom=3,
            opacity=0.9,
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        #fig.show()
        fig.write_html("website\\templates\mapfile.html")

    def plot():
        # Read CSV data file
        df = pd.read_csv('website\static\IndianAQI.csv')

        fig = go.Figure(data=[go.Scatter(
        x = df['PM2.5'], y = df['Humidity'],
        mode='markers',
        marker_size = df['Temperature'])
        ])

        fig.update_layout(
        title='PM2.5 vs Humidity, Temperature',
        xaxis=dict(
            title='PM2.5 (µg/m3)',
            gridcolor='white',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Humidity (%)',
            gridcolor='white',
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        )

        fig.write_html("website\\templates\plotfile.html")


    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    colormap()
    plot()

    return render_template("visualize.html", t = time)
