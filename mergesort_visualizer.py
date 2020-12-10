import pygame		# pip install pygame
import random
import time
import threading 


WHITE = (255,255,255)
BLACK = (0,0,0)
CRIMSON = (220,20,60)
GREEN = (0,255,0)
PURPLE = (255,0,255)
TEAL = (0,128,128)
SCRENN_SIZE = (700,500)
NO_OF_BARS = 113
WIDTH_OF_BARS = 5
TIME_DELAY = 0.015
TIME_DELAY_SMALL = 0.005

class Bar:
	def __init__(self,length):
		self.length = length
		self.color = TEAL

class App:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(SCRENN_SIZE)
		pygame.display.set_caption('Sorting Visualizer')
		self.clock = pygame.time.Clock()
		self.bars = []
		self.is_sorting = False
		self.createBars()

	def randomizeBars(self):
		self.bars = []
		self.createBars()

	def createBars(self):
		for i in range(NO_OF_BARS):
			temp = random.randint(10,450)
			bar_obj = Bar(temp)
			self.bars.append(bar_obj)

	def greenBars(self):
		for bar in self.bars:
			bar.color = GREEN
			time.sleep(0.005)

	def drawBars(self):
		for x,bar in enumerate(self.bars[::-1]):
			pygame.draw.rect(self.screen,bar.color,(x+(WIDTH_OF_BARS*x+10),0,WIDTH_OF_BARS,bar.length))

	def drawScreen(self):
		self.screen.fill(WHITE)
		self.drawBars()
		pygame.display.update()

	def colorChange(self,i,j,clr):
		self.bars[i].color = clr
		self.bars[j].color = clr

	def bubbleSort(self):
		for i in range(len(self.bars)):
			for j in range(0,len(self.bars)-1-i):
				self.colorChange(j,j+1,CRIMSON)
				# self.bars[j].color = CRIMSON
				# self.bars[j+1].color = CRIMSON
				time.sleep(TIME_DELAY_SMALL)
				if self.bars[j].length > self.bars[j+1].length:
					self.colorChange(j,j+1,PURPLE)
					# self.bars[j].color = PURPLE
					# self.bars[j+1].color = PURPLE
					time.sleep(TIME_DELAY)
					self.bars[j].length,self.bars[j+1].length = self.bars[j+1].length,self.bars[j].length
				self.colorChange(j,j+1,TEAL)
				# self.bars[j].color = TEAL
				# self.bars[j+1].color = TEAL
			self.bars[NO_OF_BARS-i-1].color = GREEN   # for the sorted bars

	def sorting(self,alg):
		self.is_sorting = True
		
		if alg == 'b':
			self.bubbleSort()
		elif alg == 'm':
			self.mergeSort(0,NO_OF_BARS-1)

		self.greenBars()
		self.is_sorting = False

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
			# self.bars[i].color = CRIMSON
			# self.bars[j].color = CRIMSON
			time.sleep(TIME_DELAY)
			if self.bars[i].length < self.bars[j].length:
				self.colorChange(i,j,PURPLE)
				# self.bars[i].color = PURPLE
				time.sleep(TIME_DELAY_SMALL)
				temp[k] = self.bars[i].length
				count = 1
			else:
				self.colorChange(i,j,PURPLE)
				# self.bars[j].color = PURPLE
				time.sleep(TIME_DELAY_SMALL)
				temp[k] = self.bars[j].length
				count = -1
			self.colorChange(i,j,TEAL)
			# self.bars[i].color = TEAL
			# self.bars[j].color = TEAL
			k+=1
			if count == 1:
				i+=1
			elif count ==-1:
				j+=1

		while i<=m:		
			self.bars[i].color = PURPLE
			time.sleep(TIME_DELAY_SMALL)
			temp[k] = self.bars[i].length
			self.bars[i].color = TEAL
			i+=1
			k+=1

		while j<=r:		
			self.bars[j].color = PURPLE
			time.sleep(TIME_DELAY_SMALL)
			temp[k] = self.bars[j].length
			self.bars[j].color = TEAL
			j+=1
			k+=1

		k = 0	
		for p in range(l,r+1):
			self.bars[p].color = PURPLE
			self.bars[p].length = temp[k]
			time.sleep(TIME_DELAY_SMALL)
			self.bars[p].color = TEAL
			k+=1

def main():	
	app = App()
	flag =True

	while flag:
		app.clock.tick(10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT and not app.is_sorting:
				flag = False
			elif event.type == pygame.KEYDOWN and not app.is_sorting:
				if event.key == pygame.K_b:
					t = threading.Thread(target=App.sorting,args=(app,'b'))
					t.start()
				elif event.key == pygame.K_m:
					t = threading.Thread(target=App.sorting,args=(app,'m'))
					t.start()
				elif event.key == pygame.K_r:
					app.randomizeBars()

		app.drawScreen()


if __name__ == '__main__':
	main()