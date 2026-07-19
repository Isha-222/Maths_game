import pygame

pygame.init()

screen = pygame.display.set_mode((640,640))

cat_img = pygame.image.load('cat.png').convert()
cat_img = pygame.transform.scale(cat_img, 
                                 (cat_img.get_width()/2,
                                 cat_img.get_height()/2))

cat_img.set_colorkey((0,0,0))

cats = pygame.Surface((64,64),pygame.SRCALPHA)
cats.blit(cat_img,(0,0))
cats.blit(cat_img,(20,0))
cats.blit(cat_img,(10,10))


running = True
x=0
clock = pygame.time.Clock()

delta_time = 0.1 

while running: 

    screen.fill((255,255,255))
    screen.blit(cat_img, (x,30))

    hitbox = pygame.Rect(x,30,cat_img.getwidth(),cat_img.get_height())

    target = pygame.Rect(300,0,160,280)
    
    x += 50 *delta_time

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

    pygame.display.flip()

    delta_time= clock.tick(60)/1000
    delta_time = max(0.001, min(0.1,delta_time))
pygame.quit