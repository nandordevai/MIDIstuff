import Live
from MPD16Component import MPD16Component

from consts import *

class MPD16MainController(MPD16Component):
	__module__ = __name__
	__doc__ = "Main controller (scene and track selection) for MPD16 remote control surface"
	__filter_funcs__ = ["update_display", "log"]

	def __init__(self, parent):
		MPD16Component.realinit(self, parent)

	def build_midi_map(self, script_handle, midi_map_handle):
		def forward_cc(chan, cc):
			Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)
		def forward_note(chan, note_no):
			Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, chan, note_no)

		for channel in MAIN_FUNCTIONS_CHANNELS:
			for note_no in MAIN_FUNCTIONS_NOTES:
				forward_note(channel, note_no)

		for channel in CLIP_TRIGGERS_CHANNELS:
			for note_no in CLIP_TRIGGERS_NAV_NOTES:
				forward_note(channel, note_no)


	def receive_midi_note(self, channel, status, note_no, note_vel):
		if (channel in MAIN_FUNCTIONS_CHANNELS and status == NOTEON_STATUS):
			if(note_no == SCENE_UP):
				self.select_up_scene()
			elif(note_no == SCENE_DOWN):
				self.select_down_scene()
			elif(note_no == TRACK_LEFT):
				self.select_left_track()
			elif(note_no == TRACK_RIGHT):
				self.select_right_track()
			elif(note_no == FIRE_SCENE):
				self.fire_selected_scene()
		if (channel in CLIP_TRIGGERS_CHANNELS and status == NOTEON_STATUS):
			if( note_no == SCENE_UP_BIS):
				self.select_up_scene()
			elif(note_no == SCENE_DOWN_BIS):
				self.select_down_scene()
			elif(note_no == FIRE_SCENE_BIS):
				self.fire_selected_scene()

	def receive_midi_cc(self, channel, cc_no, cc_value):
		pass


	def select_left_track(self):
		if(self.selected_track_idx() >0 ):
			self.parent.song().view.selected_track=self.song().tracks[self.selected_track_idx() - 1]

	def select_right_track(self):
		if(self.selected_track_idx() < len(self.parent.song().tracks)-1):
			self.parent.song().view.selected_track=self.song().tracks[self.selected_track_idx() + 1]

	def select_down_scene(self):
		if(self.selected_scene_idx() < len(self.parent.song().scenes)-1):
			self.parent.song().view.selected_scene=self.song().scenes[self.selected_scene_idx() + 1]

	def select_up_scene(self):
		if(self.selected_scene_idx() > 0 ):
			self.parent.song().view.selected_scene=self.song().scenes[self.selected_scene_idx() - 1]
	
	def fire_selected_scene(self):
		self.parent.song().view.selected_scene.fire()

		

	def disconnect(self):
		pass
	
"""
	if (channel == 0):
	   if (cc_no == SCENE_UP_CC):
		idx = self.selected_scene_idx() - 1
		new_idx = min(len(self.parent.song().scenes), max(0, idx))
		self.parent.song().view.selected_scene = self.parent.song().scenes[new_idx]
		elif (cc_no == SCENE_DOWN_NOTE):
		idx = self.selected_scene_idx() + 1
		new_idx = min(len(self.parent.song().scenes), max(0, idx))
	self.parent.song().view.selected_scene = self.parent.song().scenes[new_idx]
		elif (cc_no == SCENE_PLAY_NOTE):
		self.parent.song().view.selected_scene.fire()
		elif (cc_no in TRACK_TOGGLE_NOTE):
		clip_idx = cc_no
		scene = self.parent.song().view.selected_scene
		if (clip_idx < len(scene.clip_slots)):
			slot = scene.clip_slots[clip_idx]
			if (slot.has_clip):
			clip = slot.clip
			if (clip.is_playing):
				clip.stop()
			else:
				clip.fire()


"""

