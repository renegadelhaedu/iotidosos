import psutil
import socket


def list_connections():
    """List all active network connections with IP addresses and ports"""
    print("Active Network Connections:")
    print("-" * 60)
    print(f"{'Protocol':<8} {'Local IP':<15} {'Local Port':<10} {'Status':<12}")
    print("-" * 60)

    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr:  # Local address exists
            protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
            local_ip = conn.laddr.ip
            local_port = conn.laddr.port
            status = conn.status if conn.status else 'N/A'

            print(f"{protocol:<8} {local_ip:<15} {local_port:<10} {status:<12}")


if __name__ == "__main__":
    list_connections()