import Live
from FCB1010Component import FCB1010Component

from consts import *

class FCB1010TrackController(FCB1010Component):
    __module__ = __name__
    __doc__ = "Track controller for FCB1010 remote control surface"
    __filter_funcs__ = ["update_display", "log"]

    def __init__(self, parent):
	FCB1010Component.realinit(self, parent)

    def clip_is_recording(self, clip):
	return (clip.looping and clip.is_playing and (clip.loop_end == 63072000.0))
	
    def receive_midi_cc(self, channel, cc_no, cc_value):
	def index_of(list, elt):
	    for i in range(0,len(list)):
		if (list[i] == elt):
		    return i

	if (channel == FCB1010_CHANNEL):
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

    def find_similar_tracks(self, track):
	def first_word(string):
	    end = string.find(" ")
	    if (end == -1):
		return string
	    else:
		return string[0:end]

	name = first_word(track.name)
	return [ t for t in self.song().tracks if ((first_word(t.name) == name) and (t != track))]

    def arm_track(self, track):
	tracks = self.find_similar_tracks(track)
	for t in tracks:
	    if t.can_be_armed and t.arm:
		t.arm = 0
	track.arm = 1
    
    def record_empty_clip(self, track):
	def index_of(list, elt):
	    for i in range(0,len(list)):
		if (list[i] == elt):
		    return i
	
	if track.can_be_armed:
	    self.arm_track(track)
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
	
    def receive_midi_note(self, channel, status, note_no, note_vel):
	pass

    def find_first_rack_device(self, track):
	for dev in track.devices:
	    if dev.class_name in ["AudioEffectGroupDevice",
				  "InstrumentGroupDevice",
				  "MidiEffectGroupDevice"]:
		return dev
	return None
    
    def build_midi_map(self, script_handle, midi_map_handle):
	def forward_cc(chan, cc):
	    Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)

	def map(channel, cc, parameter, mode):
	    Live.MidiMap.map_midi_cc(midi_map_handle,
				     parameter, channel, cc,
				     mode)
	    
	for cc in RECORD_CLIP_CCS:
	    forward_cc(FCB1010_CHANNEL, cc)
	for cc in TOGGLE_CLIP_CCS:
	    forward_cc(FCB1010_CHANNEL, cc)
	for cc in RECORD_EMPTY_CLIP_CCS:
	    forward_cc(FCB1010_CHANNEL, cc)

	for idx in range(0,9):
	    if (idx < len(self.song().tracks)):
		track = self.song().tracks[idx]
		rack = self.find_first_rack_device(track)
		if rack:
		    # macro 1 param
		    map(FCB1010_CHANNEL, PEDAL_A_CCS[idx], rack.parameters[1],
			Live.MidiMap.MapMode.absolute)
		    # macro 2 param
		    map(FCB1010_CHANNEL, PEDAL_B_CCS[idx], rack.parameters[2],
			Live.MidiMap.MapMode.absolute)
		    # feedback?? XXX
		    map(FCB1010_CHANNEL, CHAIN_SELECT_CCS[idx], rack.parameters[9],
			Live.MidiMap.MapMode.absolute)

	rack = self.find_first_rack_device(self.song().master_track)
	if rack:
		    # macro 1 param
		    map(FCB1010_CHANNEL, MASTER_PEDALA_CC, rack.parameters[1],
			Live.MidiMap.MapMode.absolute)
		    # macro 2 param
		    map(FCB1010_CHANNEL, MASTER_PEDALB_CC, rack.parameters[2],
			Live.MidiMap.MapMode.absolute)
		

    def disconnect(self):
	pass
    
