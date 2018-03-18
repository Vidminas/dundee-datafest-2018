import pygame
import wikidata
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Monument Game')

black = (0, 0, 0)
white = (255, 255, 255)

rightImg = pygame.image.load('goodPotato.jpg').convert()
wrongImg = pygame.image.load('badPotato.jpg').convert()

imageSize = (int((display_width * .49)), int((display_height * .8)))
rightImg = pygame.transform.scale(rightImg, imageSize)
wrongImg = pygame.transform.scale(wrongImg, imageSize)

rightImg_rect = rightImg.get_rect(topleft=(0, 0))
wrongImg_rect = wrongImg.get_rect(topright=(display_width, 0))

font = pygame.font.Font(None, 40)
text = font.render("Click on the good potatoe", True, white)
text_rect = text.get_rect(center = (display_width/2, display_height * .9))

clock = pygame.time.Clock()

finished = False
realSites = wikidata.getRealSites()
fakeSites = wikidata.getFakeSites()

print(realSites[1:3])
print(fakeSites[1:3])

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rightImg_rect.collidepoint(event.pos):
                text = font.render("Well done!", True, white)
                text_rect = text.get_rect(center = (display_width/2, display_height * .9))

            elif wrongImg_rect.collidepoint(event.pos):
                text = font.render("You stupid", True, white)
                text_rect = text.get_rect(center = (display_width/2, display_height * .9))

            else:
                text = font.render("Click on the good potatoe", True, white)
                text_rect = text.get_rect(center = (display_width/2, display_height * .9))

        #print(event)

    gameDisplay.fill(black)

    gameDisplay.blit(rightImg, rightImg_rect)
    gameDisplay.blit(wrongImg, wrongImg_rect)
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
