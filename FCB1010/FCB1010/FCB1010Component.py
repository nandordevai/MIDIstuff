#import Live
from consts import *
from Tracing import Traced

class FCB1010Component(Traced):
#class FCB1010Component:
    __module__ = __name__
    __doc__ = 'Baseclass for a subcomponent for FCB1010 controllers.'
    __filter_funcs__ = ["update_display", "log"]

    def __init__(self, parent):
	FCB1010Component.realinit(self, parent)

    def realinit(self, parent):
	self.parent = parent

    def log(self, string):
	self.parent.log(string)
	
    def application(self):
	return self.parent.application()

    def song(self):
	return self.parent.song()

    def send_midi(self, midi_event_bytes):
	self.parent.send_midi(midi_event_bytes)

    def request_rebuild_midi_map(self):
	self.parent.request_rebuild_midi_map()

    def disconnect(self):
	pass

    def build_midi_map(self, script_handle, midi_map_handle):
	pass

    def receive_midi_cc(channel, cc_no, cc_value):
	pass

    def receive_midi_note(channel, status, note, velocity):
	pass

    def refresh_state(self):
	pass

    def update_display(self):
	pass

