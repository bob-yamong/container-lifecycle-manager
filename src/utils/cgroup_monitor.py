import pyinotify

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, manager):
        self.manager = manager

    def process_IN_CREATE(self, event):
        if event.dir:
            print(f"New cgroup created: {event.pathname}")
            # 여기에 cgroup 생성에 대한 추가 로직을 구현할 수 있습니다.
            # 예: self.manager.handle_cgroup_created(event.pathname)

    def process_IN_DELETE(self, event):
        if event.dir:
            print(f"Cgroup deleted: {event.pathname}")
            # 여기에 cgroup 삭제에 대한 추가 로직을 구현할 수 있습니다.
            # 예: self.manager.handle_cgroup_deleted(event.pathname)

def setup_cgroup_monitoring(manager):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE
    handler = EventHandler(manager)
    notifier = pyinotify.ThreadedNotifier(wm, handler)
    wm.add_watch('/sys/fs/cgroup', mask, rec=True, auto_add=True)
    return notifier

# 필요한 경우 추가 유틸리티 함수들을 여기에 구현할 수 있습니다.