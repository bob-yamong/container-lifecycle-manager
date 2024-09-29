from abc import ABC, abstractmethod

class ContainerRuntime(ABC):
    @abstractmethod
    def get_cgroup(self, container_id):
        pass

    @abstractmethod
    def get_namespace_id(self, container_id):
        pass

    @abstractmethod
    def monitor_events(self):
        pass




