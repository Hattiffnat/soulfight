from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
class Window(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.loadModels()
		self.loadActor()
		self.ActorPos()

		#self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

	def loadModels(self):

		self.scene = loader.loadModel("models/arenas/arena2.egg")
		self.scene.reparentTo(render)
		self.scene.setScale(2, 2, 2)
		self.scene.setPos(0, 0, 0)

	def loadActor(self):
		self.actor = Actor("models/human/male.egg",
			{"bend1" : "models/human/male-male_walk.egg",
			# "bend2" : "models/testworm-ArmatureAction.001.egg",
			 #"bend3" : "models/testworm-ArmatureAction.002.egg",
			 #"bend4" : "models/testworm-wormbend01.001.egg"
			 })
		self.actor.reparentTo(render)
		self.actor.loop("bend1")

	def ActorPos(self):
		PosInterval1 = self.actor.posInterval(13,
												Point3(0, -10, 0),
												startPos=Point3(0, 10, 0))
		PosInterval2 = self.actor.posInterval(13,
												Point3(0, 10, 0),
												startPos=Point3(0, 10, 0))
		HrpInterval1 = self.actor.hprInterval(3,
												Point3(180, 0, 0),
												startHpr=Point3(0, 0, 0))
		HrpInterval2 = self.actor.hprInterval(3,
												Point3(0, 0, 0),
												startHpr=Point3(180, 0, 0))	

		self.pandaPace = Sequence(PosInterval1,
									HrpInterval1,
									PosInterval2,
									HrpInterval2,
									name="wormPace")
		self.pandaPace.loop()

	def spinCameraTask(self, task):
		angleDeg = task.time * 6
		angleRad = angleDeg * (pi / 180.0)
		self.camera.setPos(20*sin(angleRad), -20*cos(angleRad), 10)

		self.camera.setHpr(angleDeg, -45, 0)
		return Task.cont


app = Window()
app.run()