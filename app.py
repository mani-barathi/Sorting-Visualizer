import pygame		# pip install pygame
import random
import time
import threading 


WHITE = (245,245,245)
BLACK = (0,0,0)
CRIMSON = (220,20,60)
GREEN = (0,255,0)
DARK_GREEN = (29, 131,72)
GREENISH = ( 46, 204, 113)
PURPLE = (255,0,255)
YELLOW = (241, 196, 15)
BLUE =  (52, 152, 219) 
SCREEN_SIZE = (700,500)
NO_OF_BARS = 113
WIDTH_OF_BARS = 5
TIME_DELAY = 0.015
TIME_DELAY_SMALL = 0.005

class Bar:
	def __init__(self,length):
		self.length = length
		self.color = BLUE

class App:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption('Sorting Visualizer')
		self.clock = pygame.time.Clock()
		self.bars = []
		self.is_sorting = False
		self.info_text = '1. Bubble Sort         2 . Merge Sort           3. Quick Sort'
		self.is_sorted = False
		self.createBars()

	def randomizeBars(self):
		self.bars = []
		self.createBars()
		self.is_sorted = False

	def createBars(self):
		for i in range(NO_OF_BARS):
			temp = random.randint(10,450)
			bar_obj = Bar(temp)
			self.bars.append(bar_obj)

	def greenBars(self):
		for bar in self.bars:
			bar.color = GREENISH
			time.sleep(0.005)

	def drawBars(self):
		for x,bar in enumerate(self.bars):
			pygame.draw.rect(self.screen,bar.color,(x+(WIDTH_OF_BARS*x+10),0,WIDTH_OF_BARS,bar.length))

	def drawInfo(self):
		font = pygame.font.SysFont(None, 20)
		text = font.render(self.info_text, True, BLACK)
		text_2 = font.render(' 0. Shuffle Bars',True,BLACK)
		self.screen.blit(text, (20, 470))
		self.screen.blit(text_2, (570, 470))

	def drawScreen(self):
		self.screen.fill(WHITE)
		self.drawBars()
		self.drawInfo()
		pygame.display.update()

	def colorChange(self,i,j,clr):
		self.bars[i].color = clr
		self.bars[j].color = clr

	def bubbleSort(self):
		for i in range(len(self.bars)):
			for j in range(0,len(self.bars)-1-i):
				self.colorChange(j,j+1,CRIMSON)
				time.sleep(TIME_DELAY_SMALL)
				if self.bars[j].length > self.bars[j+1].length:
					self.colorChange(j,j+1,GREEN)
					time.sleep(TIME_DELAY)
					self.bars[j].length,self.bars[j+1].length = self.bars[j+1].length,self.bars[j].length
				self.colorChange(j,j+1,BLUE)
			self.bars[NO_OF_BARS-i-1].color = PURPLE   # for the sorted bars

	def sorting(self,alg):
		self.is_sorting = True
		
		if alg == 1:
			self.bubbleSort()
		elif alg == 2:
			self.mergeSort(0,NO_OF_BARS-1)
		elif alg ==3:
			self.quickSort(0,NO_OF_BARS-1)

		self.greenBars()
		self.is_sorting = False
		self.is_sorted = True

	def mergeSort(self,l,r):
		if l<r:
			m = (l+r) // 2
			self.mergeSort(l,m)
			self.mergeSort(m+1,r)
			self.merge(l,m,r)

	def merge(self,l,m,r):
		i = l
		j = m+1
		k = 0
		temp = ['' for i in range(l,r+1)]
		count = 0
		while i<=m and j<=r:
			self.colorChange(i,j,CRIMSON)
			time.sleep(TIME_DELAY)
			if self.bars[i].length < self.bars[j].length:
				self.colorChange(i,j,GREEN)
				time.sleep(TIME_DELAY_SMALL)
				temp[k] = self.bars[i].length
				count = 1
			else:
				self.colorChange(i,j,GREEN)
				time.sleep(TIME_DELAY_SMALL)
				temp[k] = self.bars[j].length
				count = -1
			self.colorChange(i,j,BLUE)
			k+=1
			if count == 1:
				i+=1
			elif count ==-1:
				j+=1

		while i<=m:		
			self.bars[i].color = GREEN
			time.sleep(TIME_DELAY_SMALL)
			temp[k] = self.bars[i].length
			self.bars[i].color = BLUE
			i+=1
			k+=1

		while j<=r:		
			self.bars[j].color = GREEN
			time.sleep(TIME_DELAY_SMALL)
			temp[k] = self.bars[j].length
			self.bars[j].color = BLUE
			j+=1
			k+=1

		k = 0	
		for p in range(l,r+1):
			self.bars[p].color = GREEN
			self.bars[p].length = temp[k]
			time.sleep(TIME_DELAY)
			self.bars[p].color = BLUE
			k+=1

	def partition(self,l,r):
		i = l-1
		j = l
		pivot = self.bars[r].length
		self.bars[r].color = YELLOW
		time.sleep(TIME_DELAY)
		for j in range(l,r):
			self.bars[j].color = CRIMSON
			time.sleep(TIME_DELAY)
			if self.bars[j].length < pivot:
				i+=1
				self.colorChange(i,j,GREEN)
				time.sleep(TIME_DELAY_SMALL)
				self.bars[i].length, self.bars[j].length = self.bars[j].length, self.bars[i].length

			self.colorChange(i,j,BLUE)
		i+=1
		self.colorChange(i,r,GREEN)
		time.sleep(TIME_DELAY_SMALL)
		self.bars[i].length, self.bars[r].length = self.bars[r].length, self.bars[i].length	
		self.colorChange(i,r,BLUE)	
		self.bars[i].color = PURPLE
		return i

	def quickSort(self,l,r):
		if l<r:
			new_index = self.partition(l,r)
			self.quickSort(l,new_index-1)
			self.quickSort(new_index+1,r)


def main():	
	app = App()
	flag =True

	while flag:
		app.clock.tick(10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT and not app.is_sorting:
				flag = False
			elif event.type == pygame.KEYDOWN and not app.is_sorting:
				if event.key == pygame.K_1 and not app.is_sorted:
					t = threading.Thread(target=App.sorting,args=(app,1))
					t.start()
				elif event.key == pygame.K_2 and not app.is_sorted:
					t = threading.Thread(target=App.sorting,args=(app,2))
					t.start()
				elif event.key == pygame.K_3 and not app.is_sorted:
					t = threading.Thread(target=App.sorting,args=(app,3))
					t.start()
				elif event.key == pygame.K_0:
					app.randomizeBars()

		app.drawScreen()


if __name__ == '__main__':
	main()
