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

		self.speed = 0
		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {})
				
		#======SCALE POSITION ROTATE SET==========
		self.char.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======JOINTS CONTROLLERS=================
			#torso
		self.stomach = self.char.controlJoint(None,'modelRoot','stomach')
		self.chest = self.char.controlJoint(None,'modelRoot','chest')
		self.neck = self.char.controlJoint(None,'modelRoot','neck')
		self.head = self.char.controlJoint(None,'modelRoot','head')
		self.shoulder_l = self.char.controlJoint(None,'modelRoot','shoulder_l')
		self.shoulder_r = self.char.controlJoint(None,'modelRoot','shoulder_r')
			#legs
				#left
		self.upperleg_l = self.char.controlJoint(None,'modelRoot','upperleg_l')
		self.lowerleg_l = self.char.controlJoint(None,'modelRoot','upperleg_l')
		self.foot_l = self.char.controlJoint(None,'modelRoot','foot_l')
				#right
		self.upperleg_r = self.char.controlJoint(None,'modelRoot','upperleg_r')
		self.lowerleg_r = self.char.controlJoint(None,'modelRoot','lowerleg_r')
		self.foot_r = self.char.controlJoint(None,'modelRoot','foot_r')
			#arms
				#left
		self.upperarm_l = self.char.controlJoint(None,'modelRoot','upperarm_l')
		self.lowerarm_l = self.char.controlJoint(None,'modelRoot','lowerarm_l')
		self.palm_l = self.char.controlJoint(None,'modelRoot','palm_l')
		self.fingers_l = self.char.controlJoint(None,'modelRoot','fingers_l')
		self.bfinger_l = self.char.controlJoint(None,'modelRoot','bfinger_l')
				#right
		self.upperarm_r = self.char.controlJoint(None,'modelRoot','upperarm_r')
		self.lowerarm_r = self.char.controlJoint(None,'modelRoot','lowerarm_r')
		self.palm_r = self.char.controlJoint(None,'modelRoot','palm_r')
		self.fingers_r = self.char.controlJoint(None,'modelRoot','fingers_r')
		self.bfinger_r = self.char.controlJoint(None,'modelRoot','bfinger_r')

		#======MAKING INTERVALS===================
		

		#======RENDER ON==========================
		self.char.reparentTo(render)
		#print(Actor.listJoints(self.char))
	def jointHprTask(self, task, X, start, end, t=1)

		stask = task.time
		(xs, ys, zs) = start
		(xe, ye, ze) = end
		newx = (xe - xs)/t * task.time
		newy = (ye - ys)/t * task.time
		newz = (ze - zs)/t * task.time

		X.setHpr(newx, newy, newz)

		if task.time > (stask + t):
			return Task.end
		else:
			return Task.cont


	def startTask(self, task):
		print('start walk')
		print(task.time)
		ad = task.time*10
		self.lowerleg_l.setHpr(0, ad, 0)
		return Task.cont

	def start(self):
		self.jointHprTask(self.lowerleg_l, (0, 0, 0), (30, 30, 30), 2)

	def loopwalk(self):
		print('loop walk')
		
	def stopwalk(self):
		print('stop walk')
		
	def swap_left(self):
		print('swap left')

	def swap_right(self):
		print('swap right')

	def joints_test(self):
		self.foot_l.setHpr(0, 30, 0)
		self.upperleg_l.setHpr(0, 10, 0)

	def interval_test(self):
		print('interval_test')
		self.HprInterval1.start()
		
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

		self.accept('w', self.key_w)
		self.accept('w-up', self.char01.stopwalk)
		self.accept('z', self.char01.swap_left)
		self.accept('c', self.char01.swap_right)
		self.accept('j', self.char01.joints_test)
		self.accept('i', self.char01.interval_test)

	def key_w(self):
		self.char01.start()
		#self.taskMgr.add(self.char01.startTask, 'startwalk')

arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()