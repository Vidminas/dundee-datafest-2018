import io
import pygame
import wikidata
from urllib.request import urlopen
from random         import randrange

def load_image(image_url):
    print("Reading image from " + image_url)
    image_stream = urlopen(image_url).read()
    image_file = io.BytesIO(image_stream)
    return pygame.image.load(image_file)

def optimise_images(site_data):
    return [(name, img.convert()) for (name, img) in site_data]

def next_stage(stage, realSites, fakeSites):
    leftImage = None
    rightImage = None
    correct = "error"

    if randrange(0, 1) == 0:
        leftImage = realSites[stage]
        rightImage = fakeSites[stage]
        correct = "left"

    else:
        leftImage = fakeSites[stage]
        rightImage = realSites[stage]
        correct = "right"

    return (stage + 1, correct, leftImage, rightImage)

if __name__ == "__main__":
    window_title = "The Monument Game"
    display_width = 800
    display_height = 600
    black = (0, 0, 0)
    white = (255, 255, 255)
    imageSize = (int((display_width * .49)), int((display_height * .8)))
    textCenter = (display_width * .5, display_height * .9)
    finished = False
    answered = False
    stage = 0
    stages = 10

    # Gets Category A listed sites (most protected buildings in Scotland)
    # Only those which have images
    realSitesData = wikidata.getRealSites()
    fakeSitesData = wikidata.getFakeSites()
    realSites = []
    fakeSites = []

    # Randomly pick 5 real and 5 fake sites
    for i in range(stages):
        randomIndex1 = randrange(0, len(realSitesData))
        randomIndex2 = randrange(0, len(fakeSitesData))
        name1, url1 = realSitesData[randomIndex1]
        name2, url2 = fakeSitesData[randomIndex2]
        image1 = pygame.transform.scale(load_image(url1), imageSize)
        image2 = pygame.transform.scale(load_image(url2), imageSize)
        realSites.append((name1, image1))
        fakeSites.append((name2, image2))

    # Generate Rects with image sizes and positioning
    leftImageRect = pygame.Rect((0,0), imageSize)
    rightImageRect = pygame.Rect((display_width-imageSize[0], 0), imageSize)

    stage, correct, leftImage, rightImage = next_stage(stage, realSites, fakeSites)

    pygame.init()
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(window_title)

    font = pygame.font.Font(None, 40)
    text = font.render("Which site is in Dundee?", True, white)
    text_rect = text.get_rect(center = textCenter)

    # Not really necessary but should improve performance
    realSites = optimise_images(realSites)
    fakeSites = optimise_images(fakeSites)

    clock = pygame.time.Clock()

    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if answered and stage == stages:
                    finished = True

                elif answered:
                    stage, correct, leftImage, rightImage = next_stage(stage, realSites, fakeSites)
                    text = font.render("Which site is in Dundee?", True, white)
                    text_rect = text.get_rect(center = textCenter)
                    answered = False

                elif leftImageRect.collidepoint(event.pos) and correct == "left" or \
                     rightImageRect.collidepoint(event.pos) and correct == "right":
                    text = font.render("Well done! Click again to try the next stage", True, white)
                    text_rect = text.get_rect(center = textCenter)
                    answered = True

                elif leftImageRect.collidepoint(event.pos) and correct == "right" or \
                     rightImageRect.collidepoint(event.pos) and correct == "left":
                    text = font.render("That was not correct :( Click again to try the next stage)", True, white)
                    text_rect = text.get_rect(center = textCenter)
                    answered = True

                else:
                    text = font.render("Which site is in Dundee?", True, white)
                    text_rect = text.get_rect(center = textCenter)

        gameDisplay.fill(black)

        gameDisplay.blit(leftImage[1], leftImageRect)
        gameDisplay.blit(rightImage[1], rightImageRect)
        gameDisplay.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

# Ask user to input a city name
# Ask user how many pictures
    # limit at available data
# Import two pictures
    # one right and one wrong
# display text: Click the image in <input city>
# display images: left one is right, right one is wrong
    # set up a score counter
# If click right one: you were right!
# If click wrong one: you were wrong! Try again...
