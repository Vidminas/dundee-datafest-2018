import pygame
pygame.init()

display_width = 800
display_height = 600



gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Monument Game')

black = (0, 0, 0)
white = (255, 255, 255)

rightImg = pygame.image.load('goodPotato.jpg')
rightImg = pygame.transform.scale(rightImg, (int((display_width * .49)), int((display_height * .8))))
wrongImg = pygame.image.load('badPotato.jpg')
wrongImg = pygame.transform.scale(wrongImg, (int((display_width * .49)), int((display_height * .8))))
font = pygame.font.Font(None, 40)
text = font.render("Click on the good potatoe", True, white)

clock = pygame.time.Clock()

finished = False

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if rightImg.get_rect().collidepoint(x, y):
                text = font.render("Well done!", True, white)

            if wrongImg.get_rect().collidepoint(x, y):
                text = font.render("You stupid", True, white)

        print(event)

    gameDisplay.fill(black)

    gameDisplay.blit(rightImg, (0, 0))
    gameDisplay.blit(wrongImg, ((display_width - wrongImg.get_width()), 0))
    gameDisplay.blit(text, text.get_rect(center = (display_width/2, display_height * .9)))



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
