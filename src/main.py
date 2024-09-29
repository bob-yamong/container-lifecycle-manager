from container_lifecycle_manager import ContainerLifecycleManager
from threading import Thread
import json

def main():
    manager = ContainerLifecycleManager()
    
    if not manager.containers:
        print("No containers detected. Exiting.")
        return

    print(f"Detected {len(manager.containers)} containers.")
    
    # 런타임 이벤트 모니터링을 별도의 스레드로 실행
    thread = Thread(target=manager.monitor_runtime_events)
    thread.start()

    try:
        while True:
            command = input("Enter command (list/info/quit): ")
            if command == "list":
                print(json.dumps(manager.list_containers(), indent=2))
            elif command == "info":
                container_id = input("Enter container ID: ")
                print(json.dumps(manager.get_container_info(container_id), indent=2))
            elif command == "quit":
                break
    finally:
        # 프로그램 종료 시 정리 작업
        # 현재는 특별한 정리 작업이 필요 없습니다.
        pass

if __name__ == "__main__":
    main()