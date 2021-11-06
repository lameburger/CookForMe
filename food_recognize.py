from google.cloud import vision
import os
from google.cloud.vision_v1 import types
from google.cloud.vision_v1.services.image_annotator import client
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

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

# Calls the scrape function
scrape_google("recipies for" + )
    
# Main function
def main():
    uri_image = 'https://previews.123rf.com/images/lenm/lenm1206/lenm120600121/14039151-text-illustration-featuring-the-word-apple.jpg'        
    detect_labels_uri(uri_image)

main()
