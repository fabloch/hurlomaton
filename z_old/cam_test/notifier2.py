# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Modified:", event.pathname)

    def process_IN_CLOSE_NOWRITE(self, event):
        print("Has written: ", event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        print("Has written: ", event.pathname)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home/pi/dev/huuurlomaton/cam_test/images', mask, rec=True)

print("Watching images/button folder...")
print("(press CTRL + C to quit)")

notifier.loop()
