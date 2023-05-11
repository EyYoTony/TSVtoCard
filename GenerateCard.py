import cv2
import textwrap
import numpy as np
import pandas as pd

# -------------------- IMPORT DATA ----------------------
# pandas might be over engineering for this project lmao
# Read in tsv to dataframe
df = pd.read_csv('ActionCards.tsv', sep='\t', lineterminator='\n')
# for some reason windows likes at attach "\r" to the newline character, so we will sanitize some data
df = df.rename(columns=lambda x: x.replace('\r', ''))
df['Type'] = df['Type'].replace(r'\s+|\\r', '', regex=True)
#print(df.iloc[0]) return a row

# -------------------- GENERATE IMAGE ---------------------
# Generate Art with openAI if image not found in coresponding folder
# NO LONGER USING OPENAI
"""
openai.api_key = API_KEY
card_prompt = "a generally blue artwork for the card Frostbite in the style of a Magic The Gathering card from 2016"
response = openai.Image.create(prompt=card_prompt, n=1, size="1024x1024")
img_url = response['data'][0]['url']
"""

# Using local Stable Diffusion instead of openAI



# -------------------- GENERATE CARD ---------------------
# TODO
# Border Based on Elemental Type ? (split for 2 color?)
# Add Elemental Symbol?
# title_text = df.iloc[0].Title
def generateCard(df_row_in):
    # CARD ATTRIBUTES
    # will probably double card size to accomodate 512x512 images
    width = 250
    height = 350
    border = 12
    title_height = 40
    desc_height = 120
    border_color = (124, 124, 124)
    desc_color = (73, 121, 173)
    title_color = (108, 175, 211)
    text_color = (0,0,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    title_text = df_row_in.Title
    desc_text = df_row_in.Desc


    # generate card
    # (B, G, R) colors
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # -- add image to card --
    # TODO use stable diffusion generated img
    card_img = cv2.imread('C:\\Users\\aswan\PycharmProjects\TSVtoCard\ActionCardArt\\test_dk.png')
    img[0:width, 0:width] = card_img[0:width, 0:width]

    # -- add border to card --
    # border left -> right -> top -> bottom
    img[:, 0:border] = border_color
    img[:, width-border:width] = border_color
    img[0:border, :] = border_color
    img[height-border:height, :] = border_color

    # -- add text desc --
    # color in desc space
    img[height-(border+desc_height):height-border, border:width-border] = desc_color
    # add text
    textsize = cv2.getTextSize(desc_text, font, 0.5, 1)[0]
    txt_y = height-(border+desc_height) + 25
    txt_x = (width - textsize[0]) / 2
    ## text wrap to stop desc from overflowing off the side
    # used this as reference https://stackoverflow.com/questions/59390298/text-within-image-in-opencv
    wrapped_text = textwrap.wrap(desc_text, width=25, break_long_words=False)
    i = 0
    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, 0.5, 1)[0]

        gap = textsize[1] + 5
        y = txt_y + i * gap
        x = int((img.shape[1] - textsize[0]) / 2)
        cv2.putText(img, line, (x, y), font, 0.5, text_color, 1)
        i = i+1


    # -- add text title --
    # get values which will be used throughout the process (starting and end point of title)
    h1 = height-(border+(desc_height+title_height))
    h2 = height-(border+desc_height)
    # color in title space
    img[h1:h2, border:width-border] = title_color
    # add text
    # might need a conditional to reduce fontsize if text is too long (if textsize[0] > width-(border*2) then reduce fontsize double)
    textsize = cv2.getTextSize(title_text, font, 1, 2)[0]
    title_offset = (title_height - textsize[1])/2
    txt_y = (h2) - title_offset
    txt_x = (width - textsize[0]) / 2
    cv2.putText(img, title_text, (int(txt_x), int(txt_y)), font, 1, text_color, 2)

    cv2.imshow('a', img)
    #TODO change direct path to relative project path
    cv2.imwrite(f'C:\\Users\\aswan\PycharmProjects\TSVtoCard\ActionCardImgs\\{title_text}.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

generateCard(df.iloc[3])