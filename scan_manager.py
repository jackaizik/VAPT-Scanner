from multiprocessing import Process, Manager

# Global manager for scan processes (by scanner type)
manager = Manager()
scan_registry = manager.dict()

def start_scan(scanner_type, func, *args):
    # Kill any previous scan
    stop_scan(scanner_type)
    proc = Process(target=func, args=args)
    proc.start()
    scan_registry[scanner_type] = proc
    return proc

def stop_scan(scanner_type):
    proc = scan_registry.get(scanner_type)
    if proc and proc.is_alive():
        proc.terminate()
        proc.join(timeout=1)
        scan_registry.pop(scanner_type, None)
        return True
    return False
