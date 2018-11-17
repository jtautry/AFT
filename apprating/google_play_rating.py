from bs4 import BeautifulSoup
import requests


def get_package_name(app_friendly_name):
    r = requests.get('https://play.google.com/store/search?q=' + app_friendly_name + '&c=apps')
    soup = BeautifulSoup(r.text, features='lxml')
    search_results = soup.findAll("div", {"class": "card no-rationale square-cover apps small"})
    first_result = search_results[0]
    package_name_of_first_result = first_result['data-docid']
    return package_name_of_first_result


def get_rating_by_app_package_name(app_package_name):
    r = requests.get('https://play.google.com/store/apps/details?id=' + app_package_name)
    soup = BeautifulSoup(r.text, features='lxml')
    average_rating = soup.select_one('div.BHMmbe').text
    return average_rating


def get_rating_by_simple_name(simple_app_name):
    package_name = get_package_name(simple_app_name)
    rating = get_rating_by_app_package_name(package_name)
    return package_name, rating

# package_name, rating = get_rating_by_simple_name('facebook')

app_names = ['Dark GoldSteel Go Launcher Ex', 'Sweets Mania Matching Game', 'Venice Manual', 'Tourist  Info Laag Holland', 'AIK Innebandy', 'ScratchDown: Custom', 'Keep Distance', 'IPM - Head and Neck', 'Wonders Seafood Trading', 'Shout It ! lite', 'List Minder', 'videogame2all pro version', 'Spread Image', 'Les Paradis Artificiels 2014', 'Gerbera Wallpapers', 'NetLube Tectaloy Australia', 'Canto Canario', 'Butterfly Live Wallpaper', 'drive safe road safety sos', 'Decidable', 'Left-Handed Clock', 'Amrealm', 'Ira is cool', 'Test Application w11 - rc3', 'BubblePoc', 'Anjena Hair Spa', 'Spanish to Punjabi Phrasebook','Teneo Wordgame', 'Zorro Dial', 'Thai Driving License Practice', 'i-WALL', '[Shake]Spacewalk wallpaper', 'Red Rock Canyon Wallpapers','Family Budget Estimator', 'Mobil 1 Lube Express - Laurel', 'PEL', 'Veggie Bottoms Lite', 'City Street Runner: Dog Jump', 'Rocket Blast : UFO Attack', 'The Queen Mary', 'LeftRoom', 'Plan a Trip', 'BDO International Events', 'Habitat for Humanity Mobile', 'Pull the finger', 'PAO FC Fans', 'Shrimad Bhagwat Gita Marathi', 'Talking Pierre the Parrot Free', 'GPS Map Locations', 'Hair Regrowth Tips', 'Sexy Puzzle - Matt Bomer Edit.', 'Seckey', 'Tennessee Vols Football Trivia', 'Breakout Charts', 'Wine Judge',   'Compass Two', 'Valpolicella', 'MySchoolSquared Mobile Q&A', 'Christmas Ringtones', 'Know Your Savaari', 'SEND', 'Restaurant Picker', 'AfricanSchedules', 'Today in history calendar', 'Interactor', 'Call of Shame', 'Exotic Hawaii Live Wallpaper', 'Matstreif', 'Hudson Valley Bank Mobile', 'Pick-up The Trash', 'Crystals Russisch Black Jack', 'Edupress', 'Juicy Ladies - Order Online', 'Ethiopian TV and Radio Live', 'iBouncer', 'Yen Yoga & Fitness', 'Dynamic Warm Up Trainer', 'Front battle zombie shooter']
package_names = []
total_apps = len(app_names)

count = 0
for app in app_names:
    count += 1
    name = get_package_name(app)
    print(str(count) + "/" + str(total_apps) + ': Searched ' + app + ', got' + name)
    package_names.append(name)

print(package_names)
