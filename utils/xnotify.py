__author__ = 'Evren Esat Ozkan'
import AppKit

if hasattr(AppKit, 'NSUserNotificationCenter'):

    appDelegate = AppKit.NSApplication.sharedApplication().delegate()
    notifCenter = AppKit.NSUserNotificationCenter.defaultUserNotificationCenter()
    notifCenter.setDelegate_(appDelegate)


    class Pynotify:
        def init(self, title):
            self.title = title
        def Notification(self, title=None, msg=None):
            return Notification(title or self.title , msg)
        EXPIRES_DEFAULT = 1500


    class Notification:
        def __init__(self,title,msg):
            self.notif = AppKit.NSUserNotification.alloc().init()
            self.notif.setTitle_(title)
            self.notif.setInformativeText_(msg)

        def update(self, title, msg):
    #        self.notif = AppKit.NSUserNotification.alloc().init()
            self.notif.setInformativeText_(msg)
            notifCenter.deliverNotification_(self.notif)

        def set_timeout(self, timeout):
            pass

        def show(self):
    #        notifCenter.deliverNotification_(self.notif)
            pass

    pynotify = Pynotify()
else: #osx lion or lower
    class Pynotify:
        def init(self, title):
            pass
        def Notification(self, title=None, msg=None):
            return Notification(title or self.title , msg)
        EXPIRES_DEFAULT = 1500


    class Notification:
        def __init__(self,title,msg):
            print title, msg

        def update(self, title, msg):
    #        self.notif = AppKit.NSUserNotification.alloc().init()
            print title, msg

        def set_timeout(self, timeout):
            pass

        def show(self):
    #        notifCenter.deliverNotification_(self.notif)
            pass

    pynotify = Pynotify()
