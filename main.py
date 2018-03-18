import io
import pygame
import wikidata
from urllib.request import urlopen
from random         import randrange

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
stages = 5

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

def loading_text(font, percent, old_rect, screen):
    global display_width, display_height, black, white
    text = font.render("Loading... ({}%)".format(percent), True, white)
    new_rect = text.get_rect(center=(display_width * .5, display_height * .5))

    if old_rect is not None:
        screen.fill(black, old_rect)

    screen.blit(text, new_rect)
    return new_rect

def game_text(font, text, old_rect, screen):
    global display_width, display_height, black, white
    rendertext = font.render(text, True, white)
    new_rect = rendertext.get_rect(center=(display_width * .5, display_height * .9))

    if old_rect is not None:
        screen.fill(black, old_rect)

    screen.blit(rendertext, new_rect)
    return new_rect

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(window_title)
    font = pygame.font.Font(None, 40)
    screen.fill(black)
    pygame.display.update()

    # Gets Category A listed sites (most protected buildings in Scotland)
    # Only those which have images
    realSitesData = wikidata.getRealSites()
    fakeSitesData = wikidata.getFakeSites()
    realSites = []
    fakeSites = []

    # Randomly pick 5 real and 5 fake sites
    close = False
    i = 0

    while i <= stages and not close:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            close = True

        else:
            if i == 0:
                rect = loading_text(font, 0.0, None, screen)
                pygame.display.update(rect)

            else:
                randomIndex1 = randrange(0, len(realSitesData))
                randomIndex2 = randrange(0, len(fakeSitesData))
                name1, url1 = realSitesData[randomIndex1]
                name2, url2 = fakeSitesData[randomIndex2]
                image1 = pygame.transform.scale(load_image(url1), imageSize)
                image2 = pygame.transform.scale(load_image(url2), imageSize)
                realSites.append((name1, image1))
                fakeSites.append((name2, image2))
                old_rect = rect
                rect = loading_text(font, i / stages * 100, old_rect, screen)
                pygame.display.update([old_rect, rect])

            i += 1

    print("Done reading images")
    text_rect = game_text(font, "Which site is in Dundee?", rect, screen)

    # Not really necessary but should improve performance
    realSites = optimise_images(realSites)
    fakeSites = optimise_images(fakeSites)

    # Generate Rects with image sizes and positioning
    leftImageRect = pygame.Rect((0,0), imageSize)
    rightImageRect = pygame.Rect((display_width-imageSize[0], 0), imageSize)

    stage, correct, leftImage, rightImage = next_stage(stage, realSites, fakeSites)
    screen.blit(leftImage[1], leftImageRect)
    screen.blit(rightImage[1], rightImageRect)

    pygame.display.update()

    while not close:
        to_update = []
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            close = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if answered and stage == stages:
                close = True

            elif answered:
                stage, correct, leftImage, rightImage = next_stage(stage, realSites, fakeSites)
                screen.blit(leftImage[1], leftImageRect)
                screen.blit(rightImage[1], rightImageRect)
                to_update.append(leftImageRect)
                to_update.append(rightImageRect)
                old_text_rect = text_rect
                text_rect = game_text(font, "Which site is in Dundee?", old_text_rect, screen)
                to_update.append(old_text_rect)
                to_update.append(text_rect)
                answered = False

            elif leftImageRect.collidepoint(event.pos) and correct == "left" or \
                 rightImageRect.collidepoint(event.pos) and correct == "right":
                old_text_rect = text_rect
                text_rect = game_text(font, "Correct, well done! Click again to try the next stage", old_text_rect, screen)
                to_update.append(old_text_rect)
                to_update.append(text_rect)
                answered = True

            elif leftImageRect.collidepoint(event.pos) and correct == "right" or \
                 rightImageRect.collidepoint(event.pos) and correct == "left":
                old_text_rect = text_rect
                text_rect = game_text(font, "That was not correct! Click again to try the next stage", old_text_rect, screen)
                to_update.append(old_text_rect)
                to_update.append(text_rect)
                answered = True

            else:
                old_text_rect = text_rect
                text_rect = game_text(font, "Which site is in Dundee?", old_text_rect, screen)
                to_update.append(old_text_rect)
                to_update.append(text_rect)

        pygame.display.update(to_update)
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
