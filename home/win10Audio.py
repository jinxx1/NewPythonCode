#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   需要修改 /etc/pulse/default.pa以下部分
   加载PulseAudio 对DBus的支持模块

    ### Load DBus protocol
    .ifexists module-dbus-protocol.so
    load-module module-dbus-protocol
    .endif

   sink与port的名字可以用 pacmd list-sinks 找到
   根据名字修改 honey_sink_pattern 以及 honey_portpattern

   default_signal_receiver
   默认情况是有线耳机（前置接口）与USB声卡/耳机的切换
   1.调节音量就会切换到调节的设备，
   2.插入有线耳机就会切换到有线耳机
   3.拔出其中一个设备切换到另外一个设备

   通过 AudioLogic/add_signal_receiver
   添加额外功能

   前置接口检测:
   https://wiki.ubuntu.com/Audio/PreciseJackDetectionTesting

   PulseAudio 前置接口接口路径适配
   /usr/share/pulseaudio/alsa-mixer/paths/analog-output-headphones.conf
   [Jack Front Headphone]
   required-any = any

"""

import sys
import dbus
import os
import subprocess
import re
from functools import partial

if sys.version_info >= (3,):
	from gi.repository import GObject
if sys.version_info < (3,):
	import gobject

from dbus.mainloop.glib import DBusGMainLoop


class AudioLogic(object):
	_conn = None

	def __new__(cls):
		assert AudioLogic._conn == None, "too many AudioLogic instance"
		return super(AudioLogic, cls).__new__(cls)

	def __init__(self, honey_port_pattern=r"headphones", honey_sink_pattern=r"Usb|usb|USB"):
		"""
			honey_port_pattern 喜欢使用的port的名字含有的字符
			honey_sink_pattern 喜欢使用的的sink的名字含有的字符

		"""
		DBusGMainLoop(set_as_default=True)

		self.pacore = None
		self.nulldevice = None
		self.honey_port_pattern = honey_port_pattern
		self.honey_sink_pattern = honey_sink_pattern
		self.fallback_sink = None
		self.nulldevice = open(os.devnull, 'w')

		AudioLogic._conn = AudioLogic.connect()
		self.conn = AudioLogic._conn

		self.pacore = self.conn.get_object(object_path="/org/pulseaudio/core1", introspect=False)
		self.pacore.ListenForSignal("", dbus.Array(signature='o'))

		if self.fallback_sink == None:
			self.fallback_sink = self.pacore.Get("org.PulseAudio.Core1", "FallbackSink")

		assert self.fallback_sink != None, "There must have a fallback_sink"

	def default_signal_receiver(self):
		self.conn.add_signal_receiver(self.on_active_port_updated, signal_name="ActivePortUpdated")
		self.conn.add_signal_receiver(self.on_volume_updated, signal_name="VolumeUpdated", path_keyword="path")

	def add_signal_receiver(self, *args, **kargs):
		self.conn.add_signal_receiver(*args, **kargs)

	@staticmethod
	def connect():
		if 'PULSE_DBUS_SERVER' in os.environ:
			address = os.environ['PULSE_DBUS_SERVER']
		else:
			bus = dbus.SessionBus()
			server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
			address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address")

		return dbus.connection.Connection(address)

	def get_playback_streams_index(self):
		"""
			get all curent playback_streams
		"""
		streams = self.pacore.Get("org.PulseAudio.Core1", "PlaybackStreams")
		index = []
		for i in streams:
			tmp = self.conn.get_object("org.PulseAudio.Core1.Stream", i, introspect=False)
			index.append(tmp.Get("org.PulseAudio.Core1.Stream", "Index"))
		return index

	@property
	def honey_sink_names(self):
		"""
			return a honey_sink list if no honey_sink retuen fallback_sink list
		"""
		sinks = self.pacore.Get("org.PulseAudio.Core1", "Sinks")
		names = []
		for i in sinks:
			tmp = self.conn.get_object("org.PulseAudio.Core1.Device", i, introspect=False)
			sinkname = tmp.Get("org.PulseAudio.Core1.Device", "Name")
			if re.search(self.honey_sink_pattern, sinkname):
				names.append(sinkname)
		if len(names) == 0:
			return self.fallback_sink
		return names

	def on_volume_updated(self, _, path=None):
		"""
			when VolumnUpdated, move all playbackstream to
			the singnal emmiter (the sink)
		"""
		sourceindex = self.get_playback_streams_index()
		tmp = self.conn.get_object("org.PulseAudio.Core1.Device", path)
		sinkname = tmp.Get("org.PulseAudio.Core1.Device", "Name")
		for i in sourceindex:
			subprocess.call(["pacmd", "move-sink-input", str(i), sinkname], stdout=self.nulldevice)

	def on_active_port_updated(self, port):

		"""
			when ActivePortUpdated, check port name
			if it's honey_port, move all playbackstreams to it
			and set that sink as default.
			if not, and no fallback_sink move all playbackstreams to honey_sink
			otherwise will move to fallback_sink
		"""
		sourceindex = self.get_playback_streams_index()
		sink_tmp = self.conn.get_object("org.PulseAudio.Core1.Device", os.path.dirname(port), introspect=False)
		sinkname = sink_tmp.Get("org.PulseAudio.Core1.Device", "Name")
		port_tmp = self.conn.get_object("org.PulseAudio.Core1.DevicePort", port, introspect=False)
		portname = port_tmp.Get("org.PulseAudio.Core1.DevicePort", "Name")
		if re.search(self.honey_port_pattern, portname):
			for i in sourceindex:
				subprocess.call(["pacmd", "set-default-sink", sinkname], stdout=self.nulldevice)
				subprocess.call(["pacmd", "move-sink-input", str(i), sinkname], stdout=self.nulldevice)
		else:
			print(portname)
			for i in sourceindex:
				subprocess.call(["pacmd", "set-default-sink", self.honey_sink_names[0]], stdout=self.nulldevice)
				subprocess.call(["pacmd", "move-sink-input", str(i), self.honey_sink_names[0]], stdout=self.nulldevice)


def on_new_sink(obj, sink):
	"""
		when get a newsink, move all playbackstream to the new sink
		and set that sink as default
		print "Catch NewSink ",sink
	"""

	sourceindex = obj.get_playback_streams_index()
	sink_tmp = obj.conn.get_object("org.PulseAudio.Core1.Device", sink, introspect=False)
	sinkname = sink_tmp.Get("org.PulseAudio.Core1.Device", "Name")
	for i in sourceindex:
		subprocess.call(["pacmd", "set-default-sink", sinkname], stdout=obj.nulldevice)
		subprocess.call(["pacmd", "move-sink-input", str(i), sinkname], stdout=obj.nulldevice)


if __name__ == "__main__":

	if sys.version_info >= (3,):
		loop = GObject.MainLoop()
	if sys.version_info < (3,):
		loop = gobject.MainLoop()

	al = AudioLogic()
	al.default_signal_receiver()
	al.add_signal_receiver(partial(on_new_sink, al), signal_name="NewSink")
	loop.run()
