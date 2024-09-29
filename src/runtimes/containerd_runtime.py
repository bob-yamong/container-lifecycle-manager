from .base import ContainerRuntime

class ContainerdRuntime(ContainerRuntime):
    def __init__(self):
        # Containerd 클라이언트 초기화 (예시)
        # self.client = containerd.Client()
        pass

    def get_cgroup(self, container_id):
        # Containerd 특화 구현
        pass

    def get_namespace_id(self, container_id):
        # Containerd 특화 구현
        pass

    def monitor_events(self):
        # Containerd 이벤트 모니터링 구현
        pass