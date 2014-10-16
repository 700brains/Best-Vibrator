# -*- coding: utf-8 -*-

# Kivy imports

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.utils import platform
from kivy.lib import osc
from kivy.base import EventLoop

# pyjnius imports

from jnius import autoclass

# Android-specific actions

if platform=="android":
	PythonActivity=autoclass("org.renpy.android.PythonActivity")
	Build=autoclass("android.os.Build$VERSION")
	ANDROID_VERSION=Build.RELEASE

# Check Kivy required version

kivy.require("1.8.0")
		
class BestVibratorAppVibratorController(object):

	SERVICE_PORT=3000
	
	def __init__(self, **kwargs):
		super(BestVibratorAppVibratorController, self).__init__(**kwargs)
		if platform=="android":
			from plyer import vibrator
			self.vibrator=vibrator
			self.check_vibrator()
		else:
			self.HAS_VIBRATOR=False
			
	def custom_vibrations_time(self, period):
		if period <=59:
			return str(int(period))+"s"
		elif period >=60 and period <=3599:
			return str(int(period/60))+"min"
		elif period >=3600:
			return str(int(period/3600))+"h"
			
	def check_vibrator(self):
		if platform=="android":
			if not ANDROID_VERSION.startswith("2"):
				if self.vibrator.exists():
					return "Your device supports vibrations!"
				else:
					return "Your device doesn't support vibrations!"
			else:
				return "Your device should support vibrations!"
		else:
			return "It is not a mobile device!"
	
	def run_vibrator(self, period):
		path="/run_vibrator"
		osc.sendMsg(path, [period, ], port=self.SERVICE_PORT)
			
	def run_vibrator_schema(self, period, gap):
		path="/run_vibrator_schema"
		osc.sendMsg(path, [period, gap, ], port=self.SERVICE_PORT)
			
	def stop_vibrator(self):
		path="/stop_vibrator"
		stop=1
		osc.sendMsg(path, [stop, ], port=self.SERVICE_PORT)
		
class BestVibratorAppServiceController(object):

	def __init__(self, **kwargs):
		super(BestVibratorAppServiceController, self).__init__(**kwargs)
		self.SERVICE_ACTIVE=False
		if platform=="android":
			from android import AndroidService
			self.service=AndroidService("Best Vibrator Service", "running")
			self.service.start("Best Vibrator Service started")
			self.SERVICE_ACTIVE=True
		osc.init()
	
	def service_stop(self):
		self.service.stop()
		self.SERVICE_ACTIVE=False
		
class BestVibratorAppWebController(object):
	
	def __init__(self, **kwargs):
		super(BestVibratorAppWebController, self).__init__(**kwargs)
		import webbrowser
		self.webbrowser=webbrowser
		if platform=="android":
			from plyer import email
			self.email=email
	
	def open_website(self, text):
		self.webbrowser.open(text)
	
	def send_email_to_dev(self):
		if platform=="android":
			recipient="rafal.kaczor.1993@gmail.com"
			subject="BEST VIBRATOR QUESTION"
			text=""
			create_chooser=False
			self.email.send(recipient,subject,text,create_chooser)

class BestVibratorAppAdsController(object):
	
	def __init__(self, **kwargs):
		super(BestVibratorAppAdsController, self).__init__(**kwargs)
		if platform=="android":
			import random
			self.random=random
			self.AdBuddiz=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")
			#~ self.AdBuddizLogLevel=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddizLogLevel")
			self.AdBuddiz.setPublisherKey("82ed36f7-f673-4cb0-b225-2689286f2754")
			#~ self.AdBuddiz.setTestModeActive()
			#~ self.AdBuddiz.setLogLevel(self.AdBuddizLogLevel.Error)
			self.AdBuddiz.cacheAds(PythonActivity.mActivity)
			self.WAS_AD_SHOWN=False
	
	def show_ads(self):
		if platform=="android":
			if not self.WAS_AD_SHOWN:
				tick=self.random.randint(1, 4)
				if tick==1:
					self.AdBuddiz.showAd(PythonActivity.mActivity)
					self.WAS_AD_SHOWN=True
					return True
				else:
					return False
	
class BestVibratorApp(App):

	def __init__(self, **kwargs):	
		super(BestVibratorApp, self).__init__(**kwargs)
		self.serviceController=BestVibratorAppServiceController()
		self.vibratorController=BestVibratorAppVibratorController()
		self.webController=BestVibratorAppWebController()
		self.adsController=BestVibratorAppAdsController()
	
	def on_start(self):
		use_kivy_settings=False
		EventLoop.window.bind(on_keyboard=self.hook_keyboard)
		self.adsController.show_ads()
		
	def open_settings(self, *largs):
		pass
		
	def hook_keyboard(self, window, key, *largs):
		if key in [27, 1001]:
			if not self.adsController.show_ads():
				self.close_app()
			return True
		return False
	
	def on_pause(self):
		return True
	
	def close_app(self):
		if self.serviceController.SERVICE_ACTIVE:
			self.vibratorController.stop_vibrator()
			self.serviceController.service_stop()
		self.stop()
	
class BestVibratorAppMain(BoxLayout):
	pass

class BestVibratorButton(Button):
	pass

class BestVibratorLabel(Label):
	pass
	
class BestVibratorSlider(Slider):
	pass

class BestVibratorAppMainView(TabbedPanel):
	pass
	
class BestVibratorAppBottomBar(BoxLayout):
	pass
	
class BestVibratorAppTimeView(BoxLayout):
	pass

class BestVibratorAppCustomTimeView(BoxLayout):
	pass

class BestVibratorAppSchemaView(BoxLayout):
	pass

class BestVibratorAppAboutView(BoxLayout):
	pass
	
if __name__=="__main__":
	BestVibratorApp().run()
