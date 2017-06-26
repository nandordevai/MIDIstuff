import Live
from MPD16Component import MPD16Component

from consts import *

class MPD16ClipController(MPD16Component):
	__module__ = __name__
	__doc__ = "Clip controller for MPD16 remote control surface"
	__filter_funcs__ = ["update_display", "log"]

	def __init__(self, parent):
		MPD16Component.realinit(self, parent)


	def build_midi_map(self, script_handle, midi_map_handle):
		def forward_cc(chan, cc):
			Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)
		def forward_note(chan, note_no):
			Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, chan, note_no)

		for channel in CLIP_FUNCTIONS_CHANNELS:
			for note_no in CLIP_FUNCTIONS_NOTES:
				forward_note(channel, note_no)

		for channel in CLIP_TRIGGERS_CHANNELS:
			for note_no in CLIP_TRIGGERS_NOTES:
				forward_note(channel, note_no)
	

	def receive_midi_note(self, channel, status, note_no, note_vel):
		def index_of(list, elt):
			for i in range(0,len(list)):
				if (list[i] == elt):
					return i

		if (channel in CLIP_FUNCTIONS_CHANNELS and status == NOTEON_STATUS):
			if(note_no == TOGGLE_CLIP):
				self.toggle_current_clip()
			elif(note_no == RECORD_EMPTY_CLIP):
				self.record_empty_clip_on_current_track()
			elif(note_no == REMOVE_CLIP):
				self.remove_current_clip()

		if (channel in CLIP_TRIGGERS_CHANNELS and status == NOTEON_STATUS):
			if(note_no in CLIP_TRIGGERS_NOTES):
				self.toggle_clip_by_note(index_of(CLIP_TRIGGERS_NOTES,note_no))

	def receive_midi_cc(self, channel, cc_no, cc_value):
		pass



	def toggle_current_clip(self):
		slot = self.selected_scene().clip_slots[self.selected_track_idx()]
		if (slot.has_clip):
			clip = slot.clip
			if (clip.is_playing and not self.clip_is_recording(clip)):
				clip.stop()
			else:
				clip.fire()
		else:
			slot.fire()

	def toggle_clip_by_note(self,note_no):
		slot = self.selected_scene().clip_slots[note_no]
		if (slot.has_clip):
			clip = slot.clip
			if (clip.is_playing and not self.clip_is_recording(clip)):
				clip.stop()
			else:
				clip.fire()
		else:
			slot.fire()


	def remove_current_clip(self):
		pass
#		slot = self.selected_scene().clip_slots[self.selected_track_idx()]
#		slot.has_clip=0


	def record_empty_clip_on_current_track(self):
		self.record_empty_clip(self.selected_track())

	def record_empty_clip(self, track):
		def index_of(list, elt):
			for i in range(0,len(list)):
				if (list[i] == elt):
					return i
		if track.can_be_armed:
			self.parent.track_controller.arm_track(track)
		else:
			return
		start_idx = index_of(self.song().scenes, self.song().view.selected_scene)
		if not start_idx:
			start_idx = 0
		for idx in range(start_idx, len(track.clip_slots)):
			if not track.clip_slots[idx].has_clip:
				self.song().view.selected_scene = self.song().scenes[idx]
				track.clip_slots[idx].fire()
				return


	def clip_is_recording(self, clip):
		return (clip.looping and clip.is_playing and (clip.loop_end == 63072000.0))


	def disconnect(self):
		pass
	




