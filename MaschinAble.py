from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement 

class MaschinAble(ControlSurface):
	__module__ = __name__
	__doc__ = '''Midi Remote Script for Clip launch control on the\n
Native Instruments Maschine Controller'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		self.log_message("====================== MaschineAble Log opened ======================")
		self.set_suppress_rebuild_requests(True)
		self._suggested_input_port = 'Maschine Controller In'
		self._suggested_output_port = 'Maschine Controller Out'
		self.session = None
		self._setup_session_control()
		self.set_suppress_rebuild_requests(False)
		
	def _setup_session_control(self):
		is_momentary = True
		num_tracks = 4
		num_scenes = 4
		
		self.session = SessionComponent(num_tracks, num_scenes)
		self.session.name = 'MaschinAble_session_control'
		matrix = ButtonMatrixElement()
		
		self.session.set_offsets(0, 0)
		
		up_button = ButtonElement(is_momentary, 1, 1, 108)
		down_button = ButtonElement(is_momentary, 1, 1, 109)
		left_button = ButtonElement(is_momentary, 1, 1, 110)
		right_button = ButtonElement(is_momentary, 1, 1, 111)
		
		self.session.set_track_bank_buttons(right_button, left_button)
		self.session.set_scene_bank_buttons(down_button, up_button)
		
		launch_notes_start_from = 112
		launch_notes = range(launch_notes_start_from, launch_notes_start_from + 16)
		current_scene = list(
			self.song().scenes).index(self.song().view.selected_scene)
		current_track = list(
			self.song().tracks).index(self.song().view.selected_track)
		for scene_index in range(num_scenes):
			button_row = []
			for track_index in range(num_tracks):
				clip_slot = self.session.scene(num_scenes - 1 - scene_index + current_scene).clip_slot(track_index + current_track)
				button = ButtonElement(is_momentary, 0, 1, launch_notes[track_index+(4*scene_index)])
				button_row.append(button)
				if clip_slot.has_clip:
					clip_slot.set_stopped_value(1)
				else:
					clip_slot.set_stopped_value(0)
				clip_slot.set_triggered_to_play_value(2)
				clip_slot.set_triggered_to_record_value(2)
				clip_slot.set_launch_button(button)
			matrix.add_row(tuple(button_row))
			
	def disconnect(self):
		ControlSurface.disconnect(self)
		self.log_message("====================== MaschineAble Log closed ======================")