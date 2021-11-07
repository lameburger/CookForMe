from google.cloud import vision
import os
import requests
import urllib
from requests_html import HTMLSession
from flask import Flask, flash, request, redirect, url_for, render_template

# API key for Google Vision API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'white-cedar-331312-e9f42f725c6d.json'

# Main ingredients List
ingredients = ["Apples","Apple", "Asparagus", "Banana", "Bananas", "Beans", "Beans", "Beef", "Beef", "Beets", "Beets", "Bell Peppers", "Bell Peppers", "Blueberries", "Blueberries", "Broccoli on wood", "Broccoli", "Brussel Sprouts", "Brussels Sprouts", "Cabbage", "Cabbage", "Cane Berries", "Cane Berries", "Carrot Bunch on Wood", "Carrots", "Cauliflower", "Cauliflower", "Celery", "Celery", "Cheese in Bowls", "Cheese", "Cherries on Wood", "Cherries", "Chicken", "Chicken", "Corn", "Corn", "Cranberries", "Cranberries", "Cucumbers", "Cucumber", "Eggplant Image", "Eggplant", "Eggs", "Eggs", "Garlic", "Garlic", "Grapes on Vine", "Grapes", "Green Beans", "Green Beans", "Fresh Herbs", "Herbs and Spices", "Hot Peppers", "Hot Peppers", "Kale", "Kale", "Kiwis", "Kiwi", "Greens", "Leafy Greens", "Leeks", "Leeks", "Lentils", "Lentils", "Mangos", "Mangos", "Microgreens", "Microgreens", "a Glass of Milk", "Milk", "Chopped Mushrooms", "Mushrooms", "Oats", "Oats", "Onions", "Onions", "Oranges", "Oranges", "Parsnips", "Parsnips", "Peaches", "Peaches", "Pears", "Pears", "Peas", "Peas", "Cut Pineapple on Wood", "Pineapple", "Pork", "Pork", "Potatoes", "Potatoes", "Pumpkin Puree", "Pumpkin", "Radishes", "Radishes", "Rhubarb", "Rhubarb", "Brown Rice", "Rice", "Salad", "Salad Greens", "Cooked Salmon", "Salmon", "Spinach", "Spinach", "Split Peas", "Split Peas", "Strawberries", "Strawberries", "Summer Squash", "Summer Squash", "Sweet Potatoes", "Sweet Potato", "Tofu", "Tofu", "Tomatoes", "Tomatoes", "Tuna", "Tuna", "Turkey Image", "Turkey", "Turnips", "Turnips", "Glass of Water", "Water", "Watermelon", "Watermelon", "Wheat", "Wheat", "Pasta in Bowl", "Whole Grains", "Winter Squash", "Winter Squash", "Yogurt on Wood", "Yogurt", "Abiu", "Açaí", "Acerola", "Ackee", "African cucumber", "Apple", "Apricot", "Avocado", "Banana", "Bilberry", "Blackberry", "Blackcurrant", "Black sapote", "Blueberry", "Boysenberry", "Breadfruit", "Buddha's hand (fingered citron)", "Cactus pear", "Canistel", "Cempedak", "Cherimoya (Custard Apple)", "Cherry", "Chico fruit", "Cloudberry", "Coco De Mer", "Coconut", "Crab apple", "Cranberry", "Currant", "Damson", "Date", "Dragonfruit (or Pitaya)", "Durian", "Egg Fruit", "Elderberry", "Feijoa", "Fig", "Finger Lime (or Caviar Lime)", "Goji berry", "Gooseberry", "Grape", "Raisin", "Grapefruit", "Grewia asiatica (phalsa or falsa)", "Guava", "Hala Fruit", "Honeyberry", "Huckleberry", "Jabuticaba", "Jackfruit", "Jambul", "Japanese plum", "Jostaberry", "Jujube", "Juniper berry", "Kaffir Lime", "Kiwano (horned melon)", "Kiwifruit", "Kumquat", "Lemon", "Lime", "Loganberry", "Longan", "Loquat", "Lulo", "Lychee", "Magellan Barberry", "Mamey Apple", "Mamey Sapote", "Mango", "Mangosteen", "Marionberry", "Melon", "Cantaloupe", "Galia melon", "Honeydew", "Mouse melon", "Musk melon", "Watermelon", "Miracle fruit", "Monstera deliciosa", "Mulberry", "Nance", "Nectarine", "Orange", "Blood orange", "Clementine", "Mandarine", "Tangerine", "Papaya", "Passionfruit", "Pawpaw", "Peach", "Pear", "Persimmon", "Plantain", "Plum", "Prune (dried plum)", "Pineapple", "Pineberry", "Plumcot (or Pluot)", "Pomegranate", "Pomelo", "Purple mangosteen", "Quince", "Raspberry", "Salmonberry", "Rambutan (or Mamin Chino)", "Redcurrant", "Rose apple", "Salal berry", "Salak", "Satsuma", "Shine Muscat or Vitis Vinifera", "Sloe or Hawthorn Berry", "Soursop", "Star apple", "Star fruit", "Strawberry", "Surinam cherry", "Tamarillo", "Tamarind", "Tangelo", "Tayberry", "Ugli fruit", "White currant", "White sapote", "Yuzu"]

# Function that finds objects that represent food ingredients
def detect_labels_uri(uri):
    
    global realIngredient
    
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    realIngredient = []
    
    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        label = label.description
        if label in ingredients:
            realIngredient.append(label)
    text_detection(uri, realIngredient)

# Finds textual data that enhance the liability of the ingredients list
def text_detection(uri, realIngredient):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response_text = client.text_detection(image=image)

    for r in response_text.text_annotations:
        d = r.description
        if d not in realIngredient:
            if d in ingredients:
                realIngredient.append(d)
    print(realIngredient)
    return(realIngredient)

# Source finder for google search
def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)
   
# Scrapes google search for links     
def scrape_google(query):
    global links
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    print("-------------------")
    print(links)
    return links

def scrape_google_vegan(query):
    global links_vegan
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links_vegan = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links_vegan[:]:
        if url.startswith(google_domains):
            links_vegan.remove(url)
    print("-------------------")
    print(links_vegan)
    return links_vegan

def scrape_google_vegetarian(query):
    global links_vegetarian 
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links_vegetarian = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links_vegetarian [:]:
        if url.startswith(google_domains):
            links_vegetarian .remove(url)
    print("-------------------")
    print(links_vegetarian )
    return links_vegetarian 
    
# Main function
def main(inputUri):
    
    global listToStr
    
    uri_image = inputUri
    detect_labels_uri(uri_image)
    
    listToStr = ' '.join([str(elem) for elem in realIngredient])
    print(listToStr)
    scrape_google("recipies for {}".format(listToStr))
    scrape_google_vegan("recipies for {} vegan".format(listToStr))
    scrape_google_vegetarian("recipies for {} vegetarian".format(listToStr))
    return(listToStr, links[:7], links_vegetarian[:7], links_vegan[:7])

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html')

x = "N/A"

@app.route('/')
def my_form():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
    variable = request.form['variable']
    
    main('{}'.format(variable))
    
    return render_template('model.html', variable=variable, links=links, links_vegan=links_vegan, links_vegetarian=links_vegetarian)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
