# $Header: /root/src/python/casse.py,v 1.4 2023/10/15 07:47:36 delfosse Exp $
imporot pygame;
import random

pygame.init()

WIDTH,HEIGHT=800,600
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)

font=pygame.font.Font('freesansbold.ttf',15)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Casse-briques")

clock=pygame.time.Clock()
FPS=30

def collisionChecker(rect, balle):
	if pygame.Rect.colliderect(rect, balle):
		return True
	return False

def populateBlocs(blocWidth, blocHeight, horizontalGap, verticalGap):
	listOfBlocs = []
	for i in range(0, WIDTH, blocWidth+horizontalGap):
		for j in range(0, HEIGHT//2, blocHeight+verticalGap):
			listOfBlocs.append(Bloc(i,j, blocWidth, blocHeight, random.choice([WHITE,GREEN])))
	return listOfBlocs

def gameOver():
	gameOver = True
	while gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					return True

class Raquette:
	def __init__(self,posx,posy,width,height,speed,color):
		self.posx, self.posy = posx, posy
		self.width, self.height = width, height
		self.speed = speed
		self.color = color
		self.raquetteRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
		self.raquette = pygame.draw.rect(screen, self.color, self.raquetteRect)
	def display(self):
		self.raquette = pygame.draw.rect(screen, self.color, self.raquetteRect)
	def update(self,xFac):
		self.posx += self.speed*xFac
		if self.posx <= 0:
			self.posx=0
		elif self.posx+self.width >= WIDTH:
			self.posx = WIDTH-self.width
		self.raquetteRect = pygame.Rect(self.posx, self.posy,self.width, self.height)
	def getRect(self):
		return self.raquetteRect

class Bloc:
	def __init__(self, posx, posy, width, height, color):
		self.posx, self.posy = posx, posy
		self.width, self.height = width, height
		self.color = color
		self.damage = 100
		if color == WHITE:
			self.health=200
		else:
			self.health=100
		self.blocRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
		self.bloc = pygame.draw.rect(screen,self.color,self.blocRect)
		
	def display(self):
		if self.health > 0:
			self.bloc = pygame.draw.rect(screen,self.color,self.blocRect)
	def hit(self):
		self.health -= self.damage
	def getRect(self):
		return self.blocRect
	def getHealth(self):
		return self.health

class Balle:
	def __init__(self, posx, posy, radius,speed,color):
		self.posx, self.posy = posx, posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac, self.yFac = 1,1
		self.balle = pygame.draw.circle(screen,self.color, (self.posx,self.posy) , self.radius)

	def display(self):
		self.balle = pygame.draw.circle(screen,self.color, (self.posx,self.posy) , self.radius)
		
	def update(self):
		self.posx += self.xFac*self.speed
		self.posy += self.yFac*self.speed
		if self.posx <= 0 or self.posx >= WIDTH:
			self.xFac *= -1
		if self.posy <= 0:
			self.yFac *= -1
		if self.posy >= HEIGHT:
			return True
		return False
	def reset(self):
		self.posx = 0
		self.posy = HEIGHT
		self.xFac, self.yFac = 1, -1
	def hit(self):
		self.yFac *= -1
	def getRect(self):
		return self.balle

def main():
	running=True
	lives=3
	score=0

	scoreText=font.render("score",True,WHITE)
	scoreTextRect=scoreText.get_rect()
	scoreTextRect.center=(20,HEIGHT-10)

	livesText=font.render("Vies",True,WHITE)
	livesTextRect=livesText.get_rect()
	livesTextRect.center=(120,HEIGHT-10)

	raquette=Raquette(0,HEIGHT-50,100,20,10, WHITE)
	raquetteXFac=0

	balle=Balle(0,HEIGHT-150,7,5,WHITE)

	blocWidth,blocHeight=40,15
	horizontalGap,verticalGap=20,20

	listOfBlocs=populateBlocs(blocWidth,blocHeight,horizontalGap,verticalGap)

	while running:
		screen.fill(BLACK)
		screen.blit(scoreText, scoreTextRect)
		screen.blit(livesText, livesTextRect)
		scoreText = font.render("Score : " + str(score), True, WHITE)
		livesText = font.render("Lives : " + str(lives), True, WHITE)
		if not listOfBlocs:
			listOfBlocs = populateBlocs(blocWidth, blocHeight, horizontalGap, verticalGap)
		if lives <= 0:
			running = gameOver()
			while listOfBlocs:
				listOfBlocs.pop(0)
			lives = 3
			score = 0
			listOfBlocs = populateBlocs(blocWidth, blocHeight, horizontalGap, verticalGap)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					raquetteXFac = -1
				if event.key == pygame.K_RIGHT:
					raquetteXFac = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					raquetteXFac = 0
		if (collisionChecker(raquette.getRect(),balle.getRect())):
			balle.hit()
		for bloc in listOfBlocs:
			if (collisionChecker(bloc.getRect(), balle.getRect())):
				balle.hit()
				bloc.hit()
				if bloc.getHealth() <= 0:
					listOfBlocs.pop(listOfBlocs.index(bloc))
					score += 5
		raquette.update(raquetteXFac)
		lifeLost = balle.update()
		if lifeLost:
			lives -= 1
			balle.reset()
			print(lives)
		raquette.display()
		balle.display()
		for bloc in listOfBlocs:
			bloc.display()
		pygame.display.update()
		clock.tick(FPS)
main()
