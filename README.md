# Container Lifecycle Manager

This project provides a flexible and extensible system for managing container lifecycles across different runtime environments.

> [!CAUTION]
> This project looks at the namespace and cgroup areas in the sys folder. Root privileges are required to run the project.

## execution
```bash
git clone https://github.com/bob-yamong/container_lifecycle_manager.git
cd container_lifecycle_manager
pip install -r ./requirements.txt
cd src && sudo python main.py
```

## File Structure
```
Container Lifecycle Manager
├── README.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── container_lifecycle_manager.py
    ├── main.py
    ├── runtimes
    │   ├── __init__.py
    │   ├── base.py
    │   ├── containerd_runtime.py
    │   └── docker_runtime.py
    └── utils
        ├── __init__.py
        ├── cgroup_monitor.py
        └── container_info_collector.py
```