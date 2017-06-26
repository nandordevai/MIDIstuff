import Live
from FCB1010Component import FCB1010Component

from consts import *

class FCB1010MainController(FCB1010Component):
    __module__ = __name__
    __doc__ = "Main controller for FCB1010 remote control surface"
    __filter_funcs__ = ["update_display", "log"]

    def __init__(self, parent):
	FCB1010Component.realinit(self, parent)

    def selected_scene_idx(self):
	def tuple_idx(tuple, obj):
	    for i in xrange(0,len(tuple)):
		if (tuple[i] == obj):
		    return i
	return tuple_idx(self.parent.song().scenes, self.parent.song().view.selected_scene)
	
    def receive_midi_cc(self, channel, cc_no, cc_value):
	if (channel == 0):
	    if (cc_no == SCENE_UP_CC):
		idx = self.selected_scene_idx() - 1
		new_idx = min(len(self.parent.song().scenes), max(0, idx))
		self.parent.song().view.selected_scene = self.parent.song().scenes[new_idx]
	    elif (cc_no == SCENE_DOWN_CC):
		idx = self.selected_scene_idx() + 1
		new_idx = min(len(self.parent.song().scenes), max(0, idx))
		self.parent.song().view.selected_scene = self.parent.song().scenes[new_idx]
	    elif (cc_no == SCENE_PLAY_CC):
		self.parent.song().view.selected_scene.fire()
	    elif (cc_no in TRACK_TOGGLE_CCS):
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

    def receive_midi_note(self, channel, status, note_no, note_vel):
	pass

    def build_midi_map(self, script_handle, midi_map_handle):
	def forward_cc(chan, cc):
	    Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)

	for cc in [0,1,2,3,4,5,6,7,8,9]:
	    forward_cc(0, cc)

    def disconnect(self):
	pass
    
