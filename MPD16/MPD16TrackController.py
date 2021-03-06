import Live
from MPD16Component import MPD16Component

from consts import *

class MPD16TrackController(MPD16Component):
	__module__ = __name__
	__doc__ = "Track controller for MPD16 remote control surface"
	__filter_funcs__ = ["update_display", "log"]

	def __init__(self, parent):
		MPD16Component.realinit(self, parent)


	def build_midi_map(self, script_handle, midi_map_handle):
		def forward_cc(chan, cc):
			Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)
		def forward_note(chan, note_no):
			Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, chan, note_no)

		for channel_no in TRACK_FUNCTIONS_CHANNELS:
				forward_cc(channel_no, TRACK_VOL_CC)
				for note_no in TRACK_FUNCTIONS_NOTES:
					forward_note(channel_no, note_no)
		

	def receive_midi_note(self, channel, status, note_no, note_vel):
		if ( channel in TRACK_FUNCTIONS_CHANNELS and status == NOTEON_STATUS):
			if(note_no == TRACK_TOGGLE_ARM):
				self.toggle_arm_selected_track()
			elif(note_no == TRACK_TOGGLE_SOLO):
				self.toggle_solo_selected_track()
			elif(note_no == TRACK_TOGGLE_MUTE):
				self.toggle_mute_selected_track()
			elif(note_no == TRACK_ARM):
				self.arm_selected_track()
			elif(note_no == TRACK_UNARM):
				self.unarm_selected_track()
			elif(note_no == TRACK_VOL_INC):
				self.inc_volume_selected_track()
			elif(note_no == TRACK_VOL_DEC):	
				self.dec_volume_selected_track()

	def receive_midi_cc(self, channel, cc_no, cc_value):
		if (channel in TRACK_FUNCTIONS_CHANNELS):
			if (cc_no == TRACK_VOL_CC):
				self.set_volume_selected_track(cc_value)

	
	def set_volume_selected_track(self,cc_value):
		self.selected_track().mixer_device.volume.value=(self.selected_track().mixer_device.volume.max - self.selected_track().mixer_device.volume.min)	* cc_value / 127 + self.selected_track().mixer_device.volume.min
		
	def inc_volume_selected_track(self):
		pass

	def dec_volume_selected_track(self):
		pass


	def toggle_solo_selected_track(self):
		self.toggle_solo_track(self.selected_track())

	def toggle_solo_track(self,track):
		if(track.solo):
			track.solo=0
		else:
			track.solo=1


	def toggle_mute_selected_track(self):
		self.toggle_mute_track(self.selected_track())

	def toggle_mute_track(self,track):
		if(track.mute):
			track.mute=0
		else:
			track.mute=1


	def toggle_arm_selected_track(self):
		self.toggle_arm_track(self.selected_track())

	def unarm_selected_track(self):
		self.unarm_track(self.selected_track())

	def arm_selected_track(self):
		self.arm_track(self.selected_track())

	def toggle_arm_track(self, track):
		if(track.arm):
			self.unarm_track(track)
		else:
			self.arm_track(track)

	def unarm_track(self, track):
		track.arm = 0

	def arm_track(self, track):
		tracks = self.song().tracks #self.find_similar_tracks(track)
		for t in tracks:
			if t.can_be_armed and t.arm:
				t.arm = 0
		track.arm = 1


	def disconnect(self):
		pass
	

"""




    def find_similar_tracks(self, track):
	def first_word(string):
		end = string.find(" ")
		if (end == -1):
		return string
		else:
		return string[0:end]
	name = first_word(track.name)
	return [ t for t in self.song().tracks if ((first_word(t.name) == name) and (t != track))]

			
	def index_of(list, elt):
		for i in range(0,len(list)):
		if (list[i] == elt):
			return i

	if (channel == MPD16_CHANNEL):
		if (cc_no in RECORD_CLIP_CCS):
		idx = index_of(RECORD_CLIP_CCS, cc_no)
		if (idx < len(self.song().tracks)):
			track = self.song().tracks[idx]
			scene = self.parent.song().view.selected_scene
			if track.can_be_armed:
			if track.arm:
				track.arm = 0
			else:
				self.arm_track(track)

		elif (cc_no in TOGGLE_CLIP_CCS):
		idx = index_of(TOGGLE_CLIP_CCS, cc_no)
		scene = self.parent.song().view.selected_scene
		if (idx < len(scene.clip_slots)):
			slot = scene.clip_slots[idx]
			if (slot.has_clip):
			clip = slot.clip
			if (clip.is_playing and not self.clip_is_recording(clip)):
				clip.stop()
			else:
				clip.fire()
			else:
			slot.fire()

		elif (cc_no in RECORD_EMPTY_CLIP_CCS):
		idx = index_of(RECORD_EMPTY_CLIP_CCS, cc_no)
		if (idx < len(self.song().tracks)):
			self.record_empty_clip(self.song().tracks[idx])



   def find_first_rack_device(self, track):
for dev in track.devices:
		if dev.class_name in ["AudioEffectGroupDevice",
				  "InstrumentGroupDevice",
				  "MidiEffectGroupDevice"]:
		return dev
	return None



	def map(channel, cc, parameter, mode):
		Live.MidiMap.map_midi_cc(midi_map_handle,
					 parameter, channel, cc,
					 mode)
		
	for cc in RECORD_CLIP_CCS:
		forward_cc(MPD16_CHANNEL, cc)
	for cc in TOGGLE_CLIP_CCS:
		forward_cc(MPD16_CHANNEL, cc)
	for cc in RECORD_EMPTY_CLIP_CCS:
		forward_cc(MPD16_CHANNEL, cc)

	for idx in range(0,9):
		if (idx < len(self.song().tracks)):
		track = self.song().tracks[idx]
		rack = self.find_first_rack_device(track)
		if rack:
			# macro 1 param
			map(MPD16_CHANNEL, PEDAL_A_CCS[idx], rack.parameters[1],
			Live.MidiMap.MapMode.absolute)
			# macro 2 param
			map(MPD16_CHANNEL, PEDAL_B_CCS[idx], rack.parameters[2],
			Live.MidiMap.MapMode.absolute)
			# feedback?? XXX
			map(MPD16_CHANNEL, CHAIN_SELECT_CCS[idx], rack.parameters[9],
			Live.MidiMap.MapMode.absolute)

	rack = self.find_first_rack_device(self.song().master_track)
	if rack:
			# macro 1 param
			map(MPD16_CHANNEL, MASTER_PEDALA_CC, rack.parameters[1],
			Live.MidiMap.MapMode.absolute)
			# macro 2 param
			map(MPD16_CHANNEL, MASTER_PEDALB_CC, rack.parameters[2],
			Live.MidiMap.MapMode.absolute)
"""	

