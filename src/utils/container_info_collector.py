import shutil
import docker
import subprocess
import os

class ContainerInfoCollector:
    @staticmethod
    def collect_container_info():
        container_info = {}
        runtimes = ContainerInfoCollector.detect_runtimes()

        for runtime in runtimes:
            if runtime == 'docker':
                container_info.update(ContainerInfoCollector.get_docker_info())
            elif runtime == 'containerd':
                container_info.update(ContainerInfoCollector.get_containerd_info())
            # 여기에 다른 런타임에 대한 처리를 추가할 수 있습니다.

        return container_info

    @staticmethod
    def detect_runtimes():
        available_runtimes = []

        if shutil.which('docker'):
            try:
                docker.from_env().ping()
                available_runtimes.append('docker')
            except:
                pass

        if shutil.which('ctr'):
            try:
                subprocess.run(['ctr', 'version'], check=True, capture_output=True)
                available_runtimes.append('containerd')
            except:
                pass

        return available_runtimes

    @staticmethod
    def get_docker_info():
        client = docker.from_env()
        containers = client.containers.list(all=True)
        container_info = {}

        for container in containers:
            info = {
                'id': container.id,
                'name': container.name,
                'status': container.status,
            }
            
            if container.status == 'running':
                info['cgroup'] = ContainerInfoCollector.get_cgroup(container)
                info['namespaces'] = ContainerInfoCollector.get_namespaces(container)
            
            container_info[container.id] = info

        return container_info

    @staticmethod
    def get_containerd_info():
        # containerd 정보를 가져오는 로직을 구현해야 합니다.
        # 이는 containerd의 API나 명령줄 도구를 사용해야 할 수 있습니다.
        return {}

    @staticmethod
    def get_cgroup(container):
        try:
            # cgroup v2를 사용하는 경우
            cgroup_path = container.attrs['HostConfig']['CgroupParent']
            if not cgroup_path:
                # cgroup v1을 사용하는 경우
                pid = container.attrs['State']['Pid']
                with open(f'/proc/{pid}/cgroup', 'r') as f:
                    for line in f:
                        if 'memory' in line:  # memory subsystem을 기준으로 함
                            return line.split(':')[-1].strip()
            return cgroup_path
        except Exception as e:
            return f"Error getting cgroup: {str(e)}"

    @staticmethod
    def get_namespaces(container):
        try:
            pid = container.attrs['State']['Pid']
            namespaces = {}
            ns_types = ['ipc', 'mnt', 'net', 'pid', 'user', 'uts']
            
            for ns in ns_types:
                try:
                    path = f'/proc/{pid}/ns/{ns}'
                    if os.path.exists(path):
                        namespaces[ns] = os.readlink(path)
                    else:
                        namespaces[ns] = f"Namespace not available"
                except (IOError, OSError) as e:
                    namespaces[ns] = f"Error reading namespace: {str(e)}"

            return namespaces
        except Exception as e:
            return {ns: f"Error getting namespaces: {str(e)}" for ns in ['ipc', 'mnt', 'net', 'pid', 'user', 'uts']}