import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import scan_manager


def dummy_scan(duration: int) -> None:
    time.sleep(duration)


def test_start_scan_replaces_existing_process():
    scan_manager.scan_registry = {}
    p1 = scan_manager.start_scan("dummy", dummy_scan, 60)
    assert p1.is_alive()

    p2 = scan_manager.start_scan("dummy", dummy_scan, 60)

    assert not p1.is_alive()
    assert p2.is_alive()
    assert p1.pid != p2.pid

    scan_manager.stop_scan("dummy")


def test_stop_scan_terminates_process_and_handles_no_process():
    scan_manager.scan_registry = {}
    p = scan_manager.start_scan("dummy", dummy_scan, 60)
    assert p.is_alive()

    assert scan_manager.stop_scan("dummy") is True
    assert not p.is_alive()

    assert scan_manager.stop_scan("dummy") is False
