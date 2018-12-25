import pygame
import random
import threading
import time
print "Enter Your Name"
player_name=raw_input()
#print player_name
pygame.init()
scr_size=(width,height)=(800,600)
FPS=60
Score=0
black=(0,0,0)
white=(255,255,255)
background_col = (125,125,125)
x=50
y=360
gx=0
gy=y+95-19
g=10
over=False
y_change=0
g1=200
count=0
up=False
down=False
cx=600
cy=y+18
cactus_speed=-5
fronttime=5
frontleg=0
stay=False
stay_time=5
ground_speed=-5
screen=pygame.display.set_mode(scr_size)
clock=pygame.time.Clock()
pygame.display.set_caption('T-Rex Runner')

dinoImg=pygame.image.load('dino1.png')
dinofrontlegImg=pygame.image.load('dino2.png')
dinobacklegImg=pygame.image.load('dino3.png')
groundImg=pygame.image.load('ground.png')
cactusImg=pygame.image.load('cacti-small.png')
tempImg=pygame.image.load('cacti-big.png')
cloudImg=pygame.image.load('cloud.png')
logoImg=pygame.image.load('logo.png')
need_for_change=False
temp_vars=cactusImg.get_size()
cactus_width=temp_vars[0]
cactus_height=temp_vars[1]
cactus_score_present=1
cactus_lock=threading.Lock()
cy=gy-cactus_height+7
# print random.randint(0,3)
# temp_vars=dinoImg.get_size()
# print temp_vars[1]
def reset():
	global up,down,y_change,count,g,g1,over,frontleg,fronttime,x,y,gx,gy,cx,cy,Score,cactus_speed,ground_speed
	global cactusImg,cactus_height,cactus_width,cy
	cactusImg=pygame.image.load('cacti-small.png')
	temp_vars=cactusImg.get_size()
	cactus_width=temp_vars[0]
	cactus_height=temp_vars[1] 
	cy=gy-cactus_height+7
	Score=0
	x=50
	y=360
	gx=0
	gy=y+95-19
	g=10
	over=False
	y_change=0
	g1=200
	count=0
	up=False
	down=False
	cx=600
	cy=y+18
	cactus_speed=-5
	fronttime=5
	frontleg=0
	ground_speed=-5

def dino(x,y):
	screen.blit(dinoImg,(x,y))

def dinofrontleg(x,y):
	screen.blit(dinofrontlegImg,(x,y))

def dinobackleg(x,y):
	screen.blit(dinobacklegImg,(x,y))

def T_Rex():
	#temp=dino.get_rect()
	global up,down,y_change,count,g,g1,over,frontleg,fronttime,x,y,stay,stay_time
	if up or down or stay:
		if stay and stay_time:
			stay_time-=1;
		if stay and (not stay_time):
			stay=False
			stay_time=5
			down=True
		if up and count<=g1:
			y_change=-g
			count+=g
		if count>=g1:
			up=False
			y_change=0
			stay=True
			#down=True
		if down and count>0:
			y_change=g
			count-=g
		if count==0:
			down=False
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_p:
					pause_game()
		pygame.event.clear()
	else:
		y_change=0
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				over=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					y_change=-g
					up=True
					count=0
				elif event.key==pygame.K_p:
					pause_game()
			if event.type==pygame.KEYUP:
				y_change=0
	y+=y_change
	if up or down:
		dino(x,y)
	elif frontleg<=fronttime:
		dinofrontleg(x,y)
		frontleg+=1
	elif frontleg>fronttime and frontleg<=2*fronttime:
		dinobackleg(x,y)
		frontleg+=1
	if frontleg==2*fronttime+1:
		frontleg=0

def ground():
	global gx,gy
	if gx>-1203:
		gx+=ground_speed
	else:
		gx=0
	screen.blit(groundImg,(gx,gy))
	screen.blit(groundImg,(gx+1203,gy))

cloud_x=1000
cloud_y=100
cloud_speed=-2
def cloud():
	global cloud_x,cloud_y
	if(cloud_x<-100):
		cloud_x=1000
	cloud_x+=cloud_speed
	screen.blit(cloudImg,(cloud_x,cloud_y))

def change_cactus_Img():
	global cactus_height,cactus_width,cactusImg,cactus_score_present,cx,cy,Score
	cactus_temp=random.randint(0,3)
	global cactus_lock
	cactus_lock.acquire()
	if(cactus_temp==0):
		cactusImg=pygame.image.load('cacti-small.png')
		cactus_score_present=1
	elif(cactus_temp==1):
		cactusImg=pygame.image.load('cacti-two.png')
		cactus_score_present=2
	elif(cactus_temp==2 or Score<20):
		cactusImg=pygame.image.load('cacti-three.png')
		cactus_score_present=3
	else:
		cactusImg=pygame.image.load('cacti-big.png')
		cactus_score_present=5
	temp_vars=cactusImg.get_size()
	cactus_width=temp_vars[0]
	cactus_height=temp_vars[1]
	cy=gy-cactus_height+7
	cactus_lock.release()

def cactus():
	global cx,cy
	if(cx<-1*cactus_width):
		change_cactus_Img()
		cx=800
	cx+=cactus_speed
	screen.blit(cactusImg,(cx,cy))

def collision(x1,y1,x2,y2):
	global cactus_height,cactus_width
	if x1+88-30<x2 or x1>x2+cactus_width-23 or y1+95-23<y2:
		return False
	else:
		return True	

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

score_time=60
total_time=0
def score():
	global Score,score_time,total_time,cactus_speed,ground_speed,cactus_score_present,x,cx,cactus_width
	global cactus_lock
	cactus_lock.acquire()
	if(cx+cactus_width<x):
		Score+=cactus_score_present
		cactus_score_present=0
	total_time+=1
	if(total_time%600==0):
		cactus_speed-=1
		ground_speed-=1
	cactus_lock.release()
	# if score_time:
	# 	score_time-=1
	# else:
	# 	Score+=1
	# 	score_time=60
	largeText=pygame.font.Font('freesansbold.ttf',25)
	TextSurf, TextRect = text_objects(str(Score), largeText)
	TextRect.center = (width-100,100)
	screen.blit(TextSurf, TextRect)

def collision_message():
	global Score,over
	largeText=pygame.font.Font('freesansbold.ttf',50)
	TextSurf,TextRect= text_objects('Game over:Score Is '+str(Score),largeText)
	#print "collision_message has been called"
	leaderboards_update()
	TextRect.center=(width/2,height/4)
	screen.blit(TextSurf,TextRect)
	pygame.display.update()
	while(1):
		flag=False
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				over=True
				flag=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					flag=True
				elif event.key==pygame.K_l:
					#print 'l has been pressed'
					leaderboards()
			#if event.type==pygame.KEYUP:
			#	y_change=0
		if(flag):
			break
	# time.sleep(2)
lines=[]

def leaderboards_file_initial():
	global lines
	filename="leaderboards.txt"
	file=open(filename,'r')
	linenumber=0
	for line in file:
		lines.append(line)

def leaderboards_file_closing():
	global lines
	filename="leaderboards.txt"
	file=open(filename,'w')
	for i in 0,1,2:
		file.write(lines[i])

def leaderboards_update():
	global Score,player_name,lines
	# filename="leaderboards.txt"
	# file=open(filename,'r')
	# linenumber=0
	# for line in file:
	# 	lines.append(line)
	#print lines
	# file.seek(0,0)
	linenumber=0
	for line in lines:
		i=0
		while line[i]!=' ':
		 	i+=1
		temp=int(line[i+1:len(line)-1],10)
		if Score<temp:
			linenumber+=1
		else:
			break
	lines.insert(linenumber,player_name+' '+str(Score)+'\n')
	# file.seek(0,0)
	# file=open(filename,'w')
	# for i in 0,1,2:
	# 	file.write(lines[i])



def leaderboards():
	global lines
	# filename="leaderboards.txt"
	# file=open(filename,'r')
	temp="Leaderboards:"
	i=0
	for line in lines:
		if i==3:
			break
		temp+=line[0:len(line)-1]+"     "
		i+=1
	print temp
	#file.close()
	largeText=pygame.font.Font('freesansbold.ttf',25)
	TextSurf,TextRect= text_objects(temp,largeText)
	TextRect.center=(width/2,height-100)
	screen.blit(TextSurf,TextRect)
	pygame.display.update()

def start_game():
	global over
	pygame.display.update()
	clock.tick(FPS)
	# largeText=pygame.font.Font('freesansbold.ttf',50)
	# TextSurf,TextRect= text_objects('Start Game',largeText)
	# TextRect.center=(width/2,height/4)
	# screen.blit(TextSurf,TextRect)
	screen.fill(white)
	screen.blit(logoImg,(160,200))
	pygame.display.update()
	clock.tick(FPS)
	while 1:
		flag=False
		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					over=True
					flag=True
					break
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_SPACE:
						flag=True
						break
		if flag:
			break

def pause_game():
	global over,x,y
	pygame.display.update()
	clock.tick(FPS)
	largeText=pygame.font.Font('freesansbold.ttf',50)
	TextSurf,TextRect= text_objects('Paused',largeText)
	TextRect.center=(width/2,height/4)
	screen.blit(TextSurf,TextRect)
	dino(x,y)
	pygame.display.update()
	clock.tick(FPS)
	while 1:
		flag=False
		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					over=True
					flag=True
					break
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_SPACE:
						flag=True
						break
		if flag:
			break


def gameplay():
	global over
	screen.fill(background_col)
	start_game()
	while not over:
		screen.fill(background_col)
		t1=threading.Thread(target=T_Rex,args=())
		t2=threading.Thread(target=ground,args=())
		t3=threading.Thread(target=cactus,args=())
		t4=threading.Thread(target=score,args=())
		t5=threading.Thread(target=cloud,args=())
		t2.start()
		t1.start()
		t3.start()
		t4.start()
		t5.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		t5.join()
		sprite_list=["dinoImg","dinobacklegImg","dinofrontlegImg"]
	#	temp_list=pygame.sprite.spritecollide(cactusImg,sprite_list,False)
	#	print dinoImg.sprite.colliderect(cactusImg.rect);
		col=collision(x,y,cx,cy)
		if col:
			collision_message()
			temp_over=over
			reset()
			over=temp_over
		pygame.display.update()
		clock.tick(FPS)
leaderboards_file_initial()
gameplay()
leaderboards_file_closing()
pygame.quit()
quit()

# Cactus Small: width=34 height=70
# dino images: width=88 height=95
# ground: width=1203 height=19
# cloud: width=90 height=42