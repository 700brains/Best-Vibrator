# -*- coding: utf-8 -*-
# Kivy based Android service

# Kivy imports

from kivy.clock import mainthread, Clock
from kivy.lib import osc
from kivy.utils import platform

# Plyer API imports

if platform=="android":
	from plyer import vibrator
	from jnius import autoclass
	
SERVICE_PORT=3000

class BestVibratorAppServiceVibratorController(object):

	def __init__(self):
		self._callback=None
		
	def run_vibrator(self, message, *args):
		self._stop_vibrator()
		self._run_vibrator(message[2])
		
	@mainthread
	def _run_vibrator(self, period):
		if platform=="android":
			if period==1:
				vibrator.vibrate(1)
			else:
				self._callback = lambda *x: self.stop_vibrator(0)
				Clock.schedule_once(self._callback, period)
				vibrator.pattern(pattern=[0, 1, 0], repeat=0)
	
	def run_vibrator_schema(self, message, *args):
		self._stop_vibrator()
		self._run_vibrator_schema(message[2], message[3])
		
	@mainthread
	def _run_vibrator_schema(self, period, gap):
		if platform=="android":
			vibrator.pattern(pattern=[0, period, gap], repeat=0)
		
	def stop_vibrator(self, message, *args):
		self._stop_vibrator()
		
	@mainthread
	def _stop_vibrator(self):
		if platform=="android":
			if self._callback:
				Clock.unschedule(self._callback)
				self._callback=None
			vibrator.cancel()

serviceVibratorController=BestVibratorAppServiceVibratorController()

if __name__=="__main__":

	osc.init()
	oscid=osc.listen(ipAddr="0.0.0.0", port=SERVICE_PORT)
	osc.bind(oscid, serviceVibratorController.run_vibrator, "/run_vibrator")
	osc.bind(oscid, serviceVibratorController.run_vibrator_schema, "/run_vibrator_schema")
	osc.bind(oscid, serviceVibratorController.stop_vibrator, "/stop_vibrator")
	
	while True:
		osc.readQueue(oscid)
		Clock.tick()
