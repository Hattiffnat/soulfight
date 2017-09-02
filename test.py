from math import pi, sin, cos
import json

#import direct.directbase.DirectStart

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import *
from direct.interval.IntervalGlobal import *
#from direct.interval.IntervalGlobal import Sequence

class Character(ShowBase):

	SCALE = 1
	POS = (0, 0, 0.4)
	HPR = (-90, 0, 0)
	RATE = 1.5

	def __init__(self, path):

		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {
			'walk_loop' : path+'male-male_walk.egg',
			'walk_start_l' : path+'male-start_walk_l.egg',
			'walk_start_r' : path+'male-start_walk_r.egg',
			'swap' : path+'male-swap_wearpon.egg'
			})

		#======ANIMATION PLAY RATE SET============
		self.char.setPlayRate(self.RATE, [
			'walk_loop',
			'walk_start_l',
			'walk_start_r',
			'swap',
			])
		
		#======SCALE POSITION ROTATE SET==========
		self.char.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======MAKING SUBPARTS====================
		self.char.makeSubpart('legs', 
			[
			'upperleg_l',
			'upperleg_r',
			'lowerleg_l',
			'lowerleg_r',
			'legk_l',
			'legk_r',
			'foot_l',
			'foot_r',
			'knee_l',
			'knee_r'
			])
		#self.char.makeSubpart('tors', 
		#	[
		#	'stomach',
		#	'chest',
		#	])
		self.char.makeSubpart('left_hand', 
			[
			'shoulder_l',
			'elbow_l',
			'armk_l'
			])
		self.char.makeSubpart('right_hand', 
			[
			'shoulder_r',
			'elbow_r',
			'armk_r'
			])
		self.char.makeSubpart('head', 
			[
			'head',
			])

		#======INPUT ANIMATIONS INTERVALS=========
		self.start_l = self.char.actorInterval(
			'walk_start_l',
			loop=0,
			constrainedLoop=0,
			duration=0.54,
			startTime=0,
			endTime=0.54,
			playRate=1,
			partName='legs',
			)
		self.start_r = self.char.actorInterval(
			'walk_start_r',
			loop=0,
			constrainedLoop=0,
			duration=0.54,
			startTime=0,
			endTime=0.54,
			playRate=1,
			partName='legs',
			)
		self.walk_step_r = self.char.actorInterval(
			'walk_loop',
			loop=0,
			constrainedLoop=1,
			duration=1.02,
			startTime=0,
			endTime=1.02,
			playRate=1,
			partName='legs',
			)
		self.walk_step_l = self.char.actorInterval(
			'walk_loop',
			loop=0,
			constrainedLoop=1,
			duration=1.02,
			startTime=1.02,
			endTime=2.04,
			playRate=1,
			partName='legs',
			)
		self.laststep = None
		self.swap_l = self.char.actorInterval(
			'swap',
			loop=0,
			constrainedLoop=0,
			duration=0.54,
			startTime=0,
			endTime=0.54,
			playRate=1,
			partName='left_hand'
			)
		self.swap_r = self.char.actorInterval(
			'swap',
			loop=0,
			constrainedLoop=0,
			duration=0.54,
			startTime=0,
			endTime=0.54,
			playRate=1,
			partName='right_hand'
			)

		#======RENDER ON==========================
		self.char.reparentTo(render)
		print(Actor.listJoints(self.char))

	def startwalk(self):
		self.start_l.start()
		self.laststep = 'l'

	def loopwalk(self):
		if all(
			self.start_l.isStopped(),
			self.start_r.isStopped(),
			self.walk_step_l.isStopped(),
			self.walk_step_r.isStopped(),) == True :

			if self.laststep == 'l':
				self.walk_step_r.start()
				self.laststep = 'r'

			elif self.laststep == 'r':
				self.walk_step_l.start()
				self.laststep = 'l'
		
	def stopwalk(self):
		print('that pretty good')
		
	def swap_left(self):
		self.swap_l.start()

	def swap_right(self):
		self.swap_r.start()
		
class Environment(ShowBase):

	def __init__(self, path):
		
		self.loadmodel(path)

		self.lights = []
		self.loadlights(path)

		print("Envirement loaded")

	def loadmodel(sefl, path):

		solid = loader.loadModel(path + 'solid.egg')

		with open(path + 'data.txt', 'r') as datafile:
			data = json.loads(datafile.read())

		scale = data[0]
		pos = data[1]
		hpr = data[2]	

		solid.setScale(tuple(scale))
		solid.setPos(tuple(pos))
		solid.setHpr(tuple(hpr))

		solid.reparentTo(render)

	def loadlights(self, path):

		lights_params = []
		with open(path + 'lights.txt', 'r') as lights_file:
			for line in lights_file:
				if line[0] == '#': continue
				lights_params.append(tuple(json.loads(line)))

		for light_param in lights_params:

			if   light_param[0] == 'pl':		
				 self.typelight = PointLight('pl')
				 self.lamp = render.attachNewNode(self.typelight)
				 self.lamp.setPos(tuple(light_param[2]))
				 print('point light loaded: '+str(light_param))

			elif light_param[0] == 'dl':
				 self.typelight = DirectionalLight('dl')
				 self.lamp = render.attachNewNode(self.typelight)
				 self.lamp.setHpr(tuple(light_param[2]))
				 print('directional light loaded: '+str(light_param))

			self.lights.append(self.typelight)

			self.typelight.setColor(VBase4(tuple(light_param[1])))
			render.setLight(self.lamp)

class Window(ShowBase):

	def __init__(self, arenapath, charpath):

		ShowBase.__init__(self)

		self.env = Environment(arenapath)

		self.char01 = Character(charpath)

		self.accept('w', self.char01.startwalk)
		self.accept('w-repeat', self.char01.loopwalk)
		self.accept('w-up', self.char01.stopwalk)
		self.accept('z', self.char01.swap_left)
		self.accept('c', self.char01.swap_right)

arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()