from pygame import *
font.init()
#музыка
mixer.init()
def musos():
    mixer.music.load('fnaf-ambiance-2.mp3')
    mixer.music.play(-1)
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
#создай окно игры
window = display.set_mode((1300,700))
display.set_caption('Лабиринт')

#задай фон сцены
backgroung = transform.scale(
    image.load('background1.jpg'),
    (1300,700)
)
background1 = transform.scale(
    image.load('images.jpg'),
    (1300,700)
)

#cсоздание спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x ,y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        #движение персонажа 1
        if keys_pressed[K_UP] and self.rect.y>=0:
            self.rect.y -= 5
        if keys_pressed[K_DOWN] and self.rect.y<=700:
            self.rect.y += 5
        if keys_pressed[K_LEFT] and self.rect.x>=0:
            self.rect.x -= 5
        if keys_pressed[K_RIGHT] and self.rect.x<=1300:
            self.rect.x += 5
class Enemy(GameSprite):
    direction = 'right'
    def update(self):
        if self.rect.x <= 640:
            self.direction = 'right'
        if self.rect.x >= 1050 - 85:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= 2
        else:
            self.rect.x += 2
class Area():
 #создание прямоугольника   
    def __init__(self, x, y, whide, heidht, color):
        self.fill_color = color
        self.rect = Rect(x, y, whide, heidht)
#Заданный цвет  прямоугольника
    def set_color(self,color):
        self.fill_color = color
#Рисует прямоугольник
    def fill(self):
        draw.rect(window, self.fill_color, self.rect)
        #проверка столкновения
    def collidepoint(self, x, y):
            return self.rect.collidepoint(x,y)
    #рамочка
    def draw_stroke(self,color,trikkes):
        draw.rect(window, color, self.rect, trikkes)
# создает прмоугольник с надписью
class Label(Area):
    def __init__ (self,x,y, whide, heidht, color):
        super().__init__(x, y , whide, heidht, color)

    def set_text(self,fsize, text, text_color):
        font1 = font.SysFont('verdana', fsize)
        self.image = font1.render(text, True, text_color)
# рисует карточку вместе с текстом
    def draw(self, shift_x, shift_y):
        self.fill()
        window.blit(self.image,(self.rect.x + shift_x, self.rect.y + shift_y))

class Wall(sprite.Sprite):
    def __init__(self,width,height,x,y):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill((213,42,52))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y ))

#персонажи
player = Player('hero.png', 65, 65, 10, 100, 100 )
zlodei = Enemy('cyborg.png', 65, 65, 10, 600, 500 )
golda = GameSprite('treasure.png', 65, 65, 10, 850, 600 )

font1 = font.Font(None, 70)
win = font1.render(
    '6 am', True, (255,255,255)
)
font2 = font.Font(None, 70)
dead = font2.render(
    'DEAD', True, (255,255,255)
)

card = Label(56,360,290,100,(0,0,0))
card.set_text(40, "New game",(255,255,255))
sten1 = Wall(320,20,100,50)
sten2 = Wall(200,20,100,180)
sten3 = Wall(20,470,400,50)
sten4 = Wall(20,470,290,180)
sten6 = Wall(20,600,600,100)
walls = sprite.Group()
walls.add(sten1, sten2, sten3, sten4, sten6)
game = True
menu = True
finish = True
while game:
    if menu:
        window.blit(background1, (0,0))
        card.draw(20,20)
            # событие нажатие мыщи
        for ev in event.get():
            if ev.type == QUIT:
                game = False
            if ev.type == MOUSEBUTTONDOWN:
                x,y = ev.pos
                if card.collidepoint(x,y):
                    menu = False
                    finish = False
                    
        
    if finish != True:
        if len(sprite.spritecollide(player, walls, False)) > 0:
            player.rect.x = 100
            player.rect.y = 100
        musos()
        window.blit(backgroung, (0,0))
        player.reset()
        zlodei.reset()
        golda.reset()
        player.update()
        zlodei.update()
        sten1.draw_wall()
        sten2.draw_wall()
        sten3.draw_wall()
        sten4.draw_wall()
        sten6.draw_wall()
        if sprite.collide_rect(player,golda):
            window.blit(win, (200,200))
            finish = True
            money.play()
        if sprite.collide_rect(player,zlodei):
            window.blit(dead,(200,200))
            finish = True
            kick.play()
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()