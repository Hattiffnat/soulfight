import json
import random
import sys
import os
import math

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
	HPR = (0, 0, 0)
	RATE = 1.5

	def __init__(self, path):

		self.keyRead = True
		self.speed = 0

		self.keyMap = {
            'left': False, 'right': False, 'forward': False, 'back': False,
            'cam-left': False, 'cam-right': False, 'cam-up': False, 'cam-down': False}

		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {
			'walkcy_back'	: path+'male-start_walk_stop_backward_l.egg',
			'walkcy_forw'	: path+'male-start_walk_stop_forward_l.egg',
			'step_back'		: path+'male-step_back_r.egg',
			'fists'			: path+'male-wrists_fist.egg',
			'hold_arms'		: path+'male-wrists_hold_arms.egg'})

		self.char.pose('walkcy_forw', 0)

		print(Actor.listJoints(self.char))
				
		#======SCALE POSITION ROTATE SET==========
		self.char.setScale(self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======MAKING SUBPARTS====================
		self.char.makeSubpart('left_wrist', 
			[
			'f_finger_1_l',
			'f_finger_2_l',
			'f_finger_3_l',
			'lit_finger_1_l',
			'lit_finger_2_l',
			'lit_finger_3_l',
			'm_finger_1_l',
			'm_finger_2_l',
			'm_finger_3_l',
			'ring_finger_1_l',
			'ring_finger_2_l',
			'ring_finger_3_l',
			'thumb_1_l',
			'thumb_2_l',
			])

		#======MAKING INTERVALS===================
		self.startI = self.char.actorInterval(
			'walkcy_forw',
			loop=0,
			constrainedLoop=0,
			startFrame=0,
			endFrame=10,
			playRate=1,
			)
		self.fistI = self.char.actorInterval(
			'fists',
			loop=0,
			constrainedLoop=0,
			startFrame=0,
			endFrame=4,
			playRate=1,
			partName='left_wrist')

		#======SET CAMERA POS, HPR================
		base.disableMouse()

		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(self.char)
		self.floater.setPos(self.char.getPos())
		self.floater.setZ(self.floater.getZ() + 3.5)

		camera.setPos(
			self.char.getX(),
			self.char.getY() + 20,
			self.char.getZ() + 10
			)


		self.camvec = ()

		#======RENDER ON==========================
		self.char.reparentTo(render)

		#======TASKS LOAD=========================
		taskMgr.add(self.moveTask, 'MoveTask')
		taskMgr.add(self.cameraTask, 'CameraTask')

		#======KEYS PRESS IVENTS==================

		self.accept('a', self.setKey, ['left', True])
		self.accept('d', self.setKey, ['right', True])
		self.accept('w', self.setKey, ['forward', True])
		self.accept('s', self.setKey, ['back', True])
		self.accept('arrow_left', self.setKey, ['cam-left', True])
		self.accept('arrow_right', self.setKey, ['cam-right', True])
		self.accept('arrow_up', self.setKey, ['cam-up', True])
		self.accept('arrow_down', self.setKey, ['cam-down', True])
		self.accept('a-up', self.setKey, ['left', False])
		self.accept('d-up', self.setKey, ['right', False])
		self.accept('w-up', self.setKey, ['forward', False])
		self.accept('s-up', self.setKey, ['back', False])
		self.accept('arrow_left-up', self.setKey, ['cam-left', False])
		self.accept('arrow_right-up', self.setKey, ['cam-right', False])
		self.accept('arrow_up-up', self.setKey, ['cam-up', False])
		self.accept('arrow_down-up', self.setKey, ['cam-down', False])

	def moveTask(self, task):
		hpr_speed = 5
		charHpr = newHpr = list(self.char.getHpr())

		self.char.setHpr(tuple(newHpr))

		return task.cont

	def actionTask(self, task):



		return Task.cont

	def cameraTask(self, task):

		if self.keyMap['cam-left']:

			print(1)


		camera.lookAt(self.floater)
		return Task.cont

	def setKey(self, key, value):
		self.keyMap[key] = value

	def swapKeyRead(self):
		if self.keyRead:
			taskMgr.remove('MoveTask')
			self.keyRead = False
		else:
			taskMgr.add(self.moveTask, 'MoveTask')
			self.keyRead = True

	def fisttest(self):
		self.fistI.start()

	def swap_left(self):
		print('swap left')

	def swap_right(self):
		print('swap right')
		
class Environment(ShowBase):

	def __init__(self, path):
		
		self.loadmodel(path)

		self.lights = []
		self.loadlights(path)

		print('Envirement loaded')

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

		self.accept('q', self.char01.swapKeyRead)


	

arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()