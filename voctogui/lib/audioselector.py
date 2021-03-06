import logging
from gi.repository import Gst, Gdk, GLib

class AudioSelectorController(object):
	""" Displays a Level-Meter of another VideoDisplay into a GtkWidget """

	def __init__(self, drawing_area, win, uibuilder):
		self.log = logging.getLogger('AudioSelectorController')

		self.drawing_area = drawing_area
		self.win = win

		combo = uibuilder.find_widget_recursive(win, 'combo_audio')
		combo.connect('changed', self.on_changed)
		#combo.set_sensitive(True)
		self.combo = combo

		eventbox = uibuilder.find_widget_recursive(win, 'combo_audio_events')
		eventbox.connect('button_press_event', self.on_button_press_event)
		eventbox.set_property('above_child', True)
		self.eventbox = eventbox

		combo.remove_all()
		combo.append('moobar', 'Moo Bar')
		combo.append('moofar', 'Moo Far')

		combo.set_active_id('moobar')

		self.timer_iteration = 0

	def on_button_press_event(self, combo, event):
		if event.type != Gdk.EventType.DOUBLE_BUTTON_PRESS:
			return

		self.log.debug('double-clicked, unlocking')
		self.set_enabled(True)
		GLib.timeout_add_seconds(5, self.on_disabled_timer, self.timer_iteration)

	def on_disabled_timer(self, timer_iteration):
		if timer_iteration != self.timer_iteration:
			self.log.debug('lock-timer fired late, ignoring')
			return

		self.log.debug('lock-timer fired, locking')
		self.set_enabled(False)
		return False

	def set_enabled(self, enable):
		self.combo.set_sensitive(enable)
		self.eventbox.set_property('above_child', not enable)

	def is_enabled(self):
		return self.combo.get_sensitive()

	def on_changed(self, combo):
		if not self.is_enabled():
			return

		self.timer_iteration += 1

		value = combo.get_active_text()
		self.log.debug('changed to %s', value)
		self.set_enabled(False)
