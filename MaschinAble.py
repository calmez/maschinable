from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

class MaschinAble(ControlSurface):
	__module__ = __name__
	__doc__ = '''Midi Remote Script for Clip launch control on the\n
Native Instruments Maschine Controller'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		self.log_message("====================== MaschineAble Log opened ======================")
		self.set_suppress_rebuild_requests(True)
		self._setup_session_control()
		self.set_suppress_rebuild_requests(False)
		
	def _setup_session_control(self):
		is_momentary = True
		num_tracks = 4
		num_scenes = 4
		
		global session
		session = SessionComponent(num_tracks, num_scenes)
		
		session.set_offsets(0, 0)
		
		launch_notes = range(60,76)
		current_scene = list(
			self.song().scenes).index(self.song().view.selected_scene)
		current_track = list(
			self.song().tracks).index(self.song().view.selected_track)
		for scene_index in range(num_scenes):
			for track_index in range(num_tracks):
				session.scene(num_scenes - 1 - scene_index + current_scene).clip_slot(track_index + current_track).set_launch_button(
					ButtonElement(
						is_momentary, 
						0, 
						1, 
						launch_notes[track_index+(4*scene_index)]))
					
	def _on_selected_track_changed(self):
		ControlSurface._on_selected_track_changed(self)
		selected_track = self.song().view.selected_track
		all_tracks = ((self.song().tracks + self.song().return_tracks) + (self.song().master_track,))
		index = list(all_tracks).index(selected_track)
		session.set_offsets(index, session._scene_offset)
		
	def _on_selected_scene_changed(self):
		ControlSurface._on_selected_scene_changed(self)
		selected_scene = self.song().view.selected_scene
		all_scenes = self.song().scenes
		index = list(all_scenes).index(selected_scene)
		session.set_offsets(session._track_offset, index)