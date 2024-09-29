import docker
from .base import ContainerRuntime

class DockerRuntime(ContainerRuntime):
    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self):
        return self.client.containers.list(all=True)

    def get_cgroup(self, container_id):
        container = self.client.containers.get(container_id)
        return container.attrs['HostConfig']['CgroupParent']

    def get_namespace_id(self, container_id):
        container = self.client.containers.get(container_id)
        namespace_ids = {}
        for ns in ['IpcMode', 'NetworkMode', 'PidMode', 'UsernsMode', 'UtsMode']:
            namespace_ids[ns.lower().replace('mode', '')] = container.attrs['HostConfig'].get(ns, 'default')
        return namespace_ids

    def monitor_events(self):
        return self.client.events(decode=True)

    def close(self):
        self.client.close()