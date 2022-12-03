# from PIL import Image, ImageDraw, ImageFont
# import textwrap
#
# TalentList = [
# "Fracture",
# "Brutal",
# "Center Mass",
# "Adrenaline Rush",
# "Close Quarters",
# "Critical Hit",
# "Desperate Times",
# "Paintball",
# "Energizing",
# "Even",
# "Boston Basher",
# "Routine Shot",
# "Range Specialist",
# "Firefly",
# "trigger Finger",
# "Lightweight",
# "Speedcola",
# "Accurate",
# "Silenced",
# "Space Stone",
# "Soul Stone",
# "Armour Piercing",
# "Copycat",
# "Wild! - Tier 1",
# "Hush",
# "Explosive",
# "Snowball",
# "Ice Cream",
# "Prepared",
# "Strength in Numbers",
# "Double-Cross",
# "Click",
# "Medicality",
# "Sustained",
# "Predatory",
# "Vampiric",
# "Necromancy",
# "Speedforce",
# "Extended Mag",
# "Scavenger",
# "Meticulous",
# "Replenish",
# "Visionary",
# "Stability",
# "Assassin",
# "Fortified",
# "Dual",
# "Reality Stone",
# "Time Stone",
# "Shellshock",
# "Martyrdom",
# "Wild! - Tier 2",
# "Inferno",
# "Tesla",
# "Contagious",
# "Frost",
# "Cripple",
# "Dragonborn",
# "Tug of War",
# "Mind Stone",
# "Soften",
# "Power Stone",
# "Leech",
# "Mark",
# "Cleanse",
# "Infinity",
# "Wild! - Tier 3",
# "Wild But Tame",
# "Wildcard",
# "Exalt"]
# for talent in TalentList:
#     text = f'''{talent}'''
#     para = textwrap.wrap(text, width=11)
#
#     MAX_W, MAX_H = 200, 200
#     im = Image.new('RGB', (MAX_W, MAX_H), (30, 30, 30, 0))
#     draw = ImageDraw.Draw(im)
#     font = ImageFont.truetype(
#         r'C:\MAMP\bin\ruby\lib\ruby\2.3.0\rdoc\generator\template\darkfish\fonts\Lato-Regular.ttf', 24, )
#
#     current_h, pad = 60, 10
#     for line in para:
#         w, h = draw.textsize(line, font=font)
#         draw.text(((MAX_W - w) / 2, current_h), line, font=font, fill="#00fa9a")
#         current_h += h + pad
#     im.save(fr"C:\Users\Brandon\PycharmProjects\NaClBot\Talents\{talent}.png")


# rpinput = int(input("Number!"))
# rpmcaps = [3960, 1980, 1320, 990, 792, 660, 565, 495, 440, 396, 360, 264, 220, 198, 180, 165, 132, 120, 110, 99, 90, 88, 72]
# rpmcaps.reverse()
# actual = False
# lastrpm = 72
# if rpinput <= 72:
#     actual = rpinput
# else:
#     for rpm in rpmcaps:
#         if not actual:
#             if rpinput >= rpm:
#
#                 lastrpm = rpm
#             else:
#                 actual = lastrpm
#                 nextcap = rpm
# nextcapdiff = -(100*actual-100*nextcap)/nextcap
# print (f"{actual} | {nextcap}")
# print (f"{nextcapdiff}")
#
#
# nextcap = baserpm / (1-stat + statdiff) / (1-Talent)
# A = B / (1-C+D) / (1-X)
#
# D = (-A*C*X + A*C + A*X - A + B) / (-A*X + A)
# statDiff = (-nextcap*Stat*Talent + nextcap*Stat + nextcap*Talent - nextcap + B) / (-nextcap*Talent + nextcap)
# statdiff =

import requests
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
import configparser
import urllib.request
from PIL import Image
import os


config = configparser.ConfigParser()
config.read(r"C:\Users\Brandon\PycharmProjects\NaClBot\auth.ini")

client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')

client = ImgurClient(client_id, client_secret)

albumlinks = ["https://imgur.com/a/8pTlBv0"]

albumnames = []
images = []

for link in albumlinks:
    linkid = link.replace(r"https://imgur.com/a/", "")
    newalbum = (client.get_album(linkid))
    albumnames.append(client.get_album(linkid))
    images.append(client.get_image(newalbum.cover))

for album in albumlinks:
    # Get our album images
    try:
        images = client.get_album_images(album)
    except ImgurClientError as e:
        print('ERROR: {}'.format(e.error_message))
        print('Status code {}'.format(e.status_code))

    print("Downloading album {} ({!s} images)".format(album, len(images)))

    # Download each image
    for image in images:
        # Turn our link HTTPs
        link      = image.link.replace("http://","https://")
        # Get our file name that we'll save to disk
        file_name = link.replace("https://i.imgur.com/","")
        download_path = os.path.join("TempImages", file_name)
        if os.path.isfile(download_path):
            print("File exists for image {}, skipping...".format(file_name))
        else:
            download_image(link, download_path)

max_image = None
max_views = 0

for index, name in enumerate(albumnames):
    print(name.title)
    print(images[index].content)








