import json
import random
import sys
import os
import math

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import *
from direct.interval.IntervalGlobal import *

#function return coordinate quarter
def coordquart(angle):

	if angle >= 0.0 and angle < 90.0: quarter = 1
	elif angle >= 90.0 and angle < 180.0: quarter = 2
	elif angle >= -180.0 and angle < -90.0: quarter = 3
	elif angle >= -90.0 and angle < 0.0: quarter = 4

	return quarter

class Character(ShowBase):
	SCALE = 1
	POS = (0, 0, 0.4)
	HPR = (0)
	RATE = 1.5
	CAMDIST = 25

	def __init__(self, path):

		self.keyRead = True
		self.speed = 0

		self.keyMap = {
			'debug': False,
			'left': False, 'right': False, 'forward': False, 'back': False,
			'cam-left': False, 'cam-right': False, 'cam-up': False, 'cam-down': False,
			'cam-closer': False, 'cam-farther': False
			}

	# ======ANIMATION LIST=====================
		self.char = Actor(path + 'male.egg', {
			'walkcy_back': path + 'male-start_walk_stop_backward_l.egg',
			'walkcy_forw': path + 'male-start_walk_stop_forward_l.egg',
			'step_back': path + 'male-step_back_r.egg',
			'fists'	: path +'male-wrists_fist.egg',
			'hold_arms'	: path + 'male-wrists_hold_arms.egg',
			'swap_pocket_r': path + 'male-swap_pocket_r',
			'swap_pocket_l': path + 'male-swap_pocket_l',}
			)

		self.char.pose('walkcy_forw', 0)

		print(Actor.listJoints(self.char))

	# ======SCALE, POS, HPR, TASK PARAMS=======
		self.char.setScale(self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		self.floater = NodePath(PandaNode("floater"))
		self.floater.setPos(self.char.getPos())
		self.floater.setZ(self.floater.getZ() + 3.5)

		self.floater.reparentTo(render)
		self.char.reparentTo(self.floater)
		self.char.setZ(self.char.getZ() - 3.5)

		self.WALKSPEED = 10
		self.HSPEED = 500

	# ======MAKING SUBPARTS====================
		self.char.makeSubpart('torso', [
			'stomach',
			'chest'
			])
		self.char.makeSubpart('left_wrist', [
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
		self.char.makeSubpart('legs', [
			'upperleg_l',
			'lowerleg_l',
			'foot_l',
			'upperleg_r',
			'lowerleg_r',
			'foot_r',
			])

	# ======MAKING INTERVALS===================
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

	# ======SET CAMERA POS, HPR, TASK PARAMS===
		base.disableMouse()

		self.camSpeedPhi = 100
		self.camSpeedTheta = 100

		camera.setPos(
			self.floater.getX() + self.CAMDIST,
			self.floater.getY(),
			self.floater.getZ()
		)
		
		self.camdist = self.CAMDIST

		camera.lookAt(self.floater)
		self.camphi = camera.getH()
		self.camtheta = camera.getP()

	# ======TASKS LOAD=========================
		taskMgr.add(self.moveTask, 'MoveTask')
		taskMgr.add(self.cameraTask, 'CameraTask')
		#taskMgr.add(self.actionTask, 'ActionTask')

	# ======KEYS PRESS IVENTS==================
		self.accept('`', self.setKey,		['debug', True])
		self.accept('`-up', self.setKey,	['debug', False])

		self.accept('a', self.setKey,		['left', True])
		self.accept('d', self.setKey,		['right', True])
		self.accept('w', self.setKey,		['forward', True])
		self.accept('s', self.setKey,		['back', True])
		self.accept('a-up', self.setKey,	['left', False])
		self.accept('d-up', self.setKey,	['right', False])
		self.accept('w-up', self.setKey,	['forward', False])
		self.accept('s-up', self.setKey,	['back', False])

		self.accept('arrow_left', self.setKey,		['cam-left', True])
		self.accept('arrow_right', self.setKey,		['cam-right', True])
		self.accept('arrow_up', self.setKey,		['cam-up', True])
		self.accept('arrow_down', self.setKey,		['cam-down', True])
		self.accept('arrow_left-up', self.setKey,	['cam-left', False])
		self.accept('arrow_right-up', self.setKey,	['cam-right', False])
		self.accept('arrow_up-up', self.setKey,		['cam-up', False])
		self.accept('arrow_down-up', self.setKey,	['cam-down', False])

		self.accept('[', self.setKey,		['cam-closer', True])
		self.accept(']', self.setKey,		['cam-farther', True])
		self.accept('[-up', self.setKey,	['cam-closer', False])
		self.accept(']-up', self.setKey,	['cam-farther', False])

	def moveTask(self, task):
		dt = globalClock.getDt()
		km = self.keyMap
		camh = camera.getH()
		charh = self.char.getH()
		hspeed = self.HSPEED * dt
		dirmapON = km['left'] or km['right'] or km['forward'] or km['back']

		angleh = charh

		if   km['left'] and km['back']: 	angleh = camh - 45
		elif km['right'] and km['back']: 	angleh = camh + 45
		elif km['left'] and km['forward']: 	angleh = camh - 135
		elif km['right'] and km['forward']: angleh = camh + 135
		elif km['left']:	angleh = camh - 90
		elif km['forward']:	angleh = camh + 180
		elif km['right']:	angleh = camh + 90
		elif km['back']:	angleh = camh

		if angleh > 180:	angleh -= 360
		if angleh < -180:	angleh += 360
		anglehrad = angleh * math.pi / 180

		if charh > 180:		charh -= 360
		if charh < -180:	charh += 360

		resid = abs(angleh - charh)

		if angleh > charh: charhdir = 1
		elif angleh < charh: charhdir = -1
		if resid > 180: charhdir *= -1

		if hspeed > resid: hspeed = resid

		if dirmapON:
			self.floater.setX(self.floater.getX() + dt * self.WALKSPEED * math.sin(anglehrad))
			self.floater.setY(self.floater.getY() - dt * self.WALKSPEED * math.cos(anglehrad))

		if angleh != charh:
			self.char.setH(charh + hspeed * charhdir)

		#animations
		#if dirmapON: self.char.play('walkcy_forw')

		if self.keyMap['debug']:
			self.char.enableBlend()
			self.char.setControlEffect('swap_pocket_r', 1)
			self.char.setControlEffect('swap_pocket_l', 1)
			self.char.play('swap_pocket_r')
			self.char.play('swap_pocket_l')

		return task.cont

	def actionTask(self, task):
		if self.keyMap['debug']:
			self.char.play('right_arm_test_1')
			self.char.play('right_arm_test_2')

		return Task.cont

	def cameraTask2(self, task):
		dt = globalClock.getDt()

		if self.keyMap['cam-left']:
			camera.setX(camera, -self.camSpeedPhi * dt)
		if self.keyMap['cam-right']:
			camera.setX(camera, +self.camSpeedPhi * dt)

		if self.keyMap['cam-up']:
			camera.setY(camera, +self.camSpeedTheta * dt)
		if self.keyMap['cam-down']:
			camera.setY(camera, -self.camSpeedTheta * dt)

		camvec = self.floater.getPos() - camera.getPos()
		#camvec.setZ(0)
		camdist = camvec.length()
		camvec.normalize()
		if camdist > self.CAMDISTMAX:
			camera.setPos(camera.getPos() + camvec * (camdist - self.CAMDISTMAX))
			camdist = self.CAMDISTMIN
		if camdist < self.CAMDISTMIN:
			camera.setPos(camera.getPos() - camvec * (self.CAMDISTMIN - camdist))
			camdist = self.CAMDISTMAX

		if self.keyMap['debug']: print(camvec)

		camera.lookAt(self.floater)

		self.camTaskTime = task.time
		return Task.cont
	def cameraTask(self, task):

		dt = globalClock.getDt()
		floaterpos = list(self.floater.getPos())

		if self.keyMap['cam-left']:
			self.camphi += self.camSpeedPhi * dt
		if self.keyMap['cam-right']:
			self.camphi -= self.camSpeedPhi * dt			

		if self.keyMap['cam-up'] and self.camtheta < 179:
			self.camtheta += self.camSpeedTheta * dt
		if self.keyMap['cam-down'] and self.camtheta > 1:
			self.camtheta -= self.camSpeedTheta * dt

		if self.camphi > 180: self.camphi -= 360
		elif self.camphi < -180: self.camphi += 360

		if self.keyMap['cam-closer']: self.camdist -= self.camSpeedPhi * dt
		if self.keyMap['cam-farther']: self.camdist += self.camSpeedPhi * dt

		phi = self.camphi * math.pi/180
		theta = self.camtheta * math.pi/180

		sinphi = math.sin(phi)
		cosphi = math.cos(phi)
		sintheta = math.sin(theta)
		costheta = math.cos(theta)

		camera.setPos(
			floaterpos[0] + self.camdist * sintheta * cosphi,
			floaterpos[1] + self.camdist * sintheta * sinphi,
			floaterpos[2] + self.camdist * costheta
			)
		
		camera.lookAt(self.floater)

		#if self.keyMap['debug']:

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

			if light_param[0] == 'pl':
				self.typelight = PointLight('pl')
				self.lamp = render.attachNewNode(self.typelight)
				self.lamp.setPos(tuple(light_param[2]))
				print('point light loaded: ' + str(light_param))

			elif light_param[0] == 'dl':
				self.typelight = DirectionalLight('dl')
				self.lamp = render.attachNewNode(self.typelight)
				self.lamp.setHpr(tuple(light_param[2]))
				print('directional light loaded: ' + str(light_param))

			self.lights.append(self.typelight)

			self.typelight.setColor(VBase4(tuple(light_param[1])))
			render.setLight(self.lamp)


class Window(ShowBase):
	def __init__(self, arenapath, charpath):
		ShowBase.__init__(self)

		self.env = Environment(arenapath)

		self.char01 = Character(charpath)

		self.accept('escape', sys.exit)
		self.accept('q', self.char01.swapKeyRead)


arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()
