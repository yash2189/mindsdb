import psutil
import time


def is_port_in_use(port_num):
    portsinuse = []
    conns = psutil.net_connections()
    portsinuse = [x.laddr[1] for x in conns if x.status == 'LISTEN']
    portsinuse.sort()
    return int(port_num) in portsinuse


def wait_port(port_num, timeout):
    start_time = time.time()

    in_use = is_port_in_use(port_num)
    while in_use is False and (time.time() - start_time) < timeout:
        time.sleep(2)
        in_use = is_port_in_use(port_num)

    return in_use


def get_listen_ports(pid):
    try:
        p = psutil.Process(pid)
        cons = p.connections()
        cons = [x.laddr.port for x in cons]
    except Exception:
        return []
    return cons


def is_pid_listen_port(pid, port):
    ports = get_listen_ports(pid)
    return int(port) in ports
