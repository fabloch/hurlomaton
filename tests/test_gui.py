import unittest
from gui.controller import GUIController

class TestGUIController(unittest.TestCase):
    def setUp(self):
        self.controller = GUIController()

    def test_is_fullscreen_true(self):
        """
        Starts with is_fullscreen True
        """
        self.assertTrue(self.controller.is_fullscreen)

    def test_toggle_fullscreen(self):
        """
        Sets is_fullscreen to !is_fullscreen
        """
        self.assertTrue(self.controller.is_fullscreen)
        self.controller.toggle_fullscreen()
        self.assertFalse(self.controller.is_fullscreen)
