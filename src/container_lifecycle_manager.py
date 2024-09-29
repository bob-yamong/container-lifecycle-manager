import docker
from utils.container_info_collector import ContainerInfoCollector
from utils.cgroup_monitor import setup_cgroup_monitoring

class ContainerLifecycleManager:
    def __init__(self):
        self.containers = {}
        self.load_container_info()
        self.cgroup_notifier = setup_cgroup_monitoring(self)
        self.cgroup_notifier.start()

    def load_container_info(self):
        self.containers = ContainerInfoCollector.collect_container_info()

    def handle_container_event(self, runtime, event, container_id):
        if event in ['start', 'create']:
            container_info = ContainerInfoCollector.collect_container_info().get(container_id)
            if container_info:
                self.containers[container_id] = container_info
        elif event in ['stop', 'destroy']:
            if container_id in self.containers:
                self.containers[container_id]['status'] = event
        elif event == 'die':
            if container_id in self.containers:
                del self.containers[container_id]

    def monitor_runtime_events(self):
        # 이 메서드는 각 런타임의 이벤트를 모니터링하도록 구현해야 합니다.
        # 예를 들어, Docker의 경우:
        client = docker.from_env()
        for event in client.events(decode=True):
            if 'status' in event and 'id' in event:
                self.handle_container_event('docker', event['status'], event['id'])

    def get_container_info(self, container_id):
        return self.containers.get(container_id, None)

    def list_containers(self):
        return self.containers