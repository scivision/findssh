"""
Example: Discovering both SSH and HTTP servers on a subnet using discover_services()
"""

import asyncio
import findssh


async def discover_servers_example():
    """
    Discover SSH (port 22) and HTTP (ports 80, 443) servers on the local subnet
    in a single efficient pass using asyncio.TaskGroup.
    """

    # Get the local LAN IP and convert to network
    local_ip = findssh.get_lan_ip()
    network = findssh.address2net(local_ip)
    print(f"Scanning network: {network}")

    # Define services to discover
    # Can specify single port (int) or multiple ports (list)
    services = {
        "ssh": 22,
        "http": [80, 443],
    }

    # Discover all services in one pass
    results = await findssh.discover_services(
        network,
        service_ports=services,
        timeout=1.0,
        max_concurrent=100,
    )

    # Display results
    print(f"\n{'Service':<10} {'Host':<20} {'Banner':<50}")
    print("-" * 80)

    for service_name, hosts in results.items():
        if hosts:
            for ip_addr, banner in hosts:
                print(f"{service_name:<10} {str(ip_addr):<20} {banner[:50]}")
        else:
            print(f"{service_name:<10} {'(none found)':<20}")

    # Example of using results programmatically
    print("\nDiscovery Summary:")
    print(f"  SSH servers found: {len(results.get('ssh', []))}")
    print(f"  HTTP servers found: {len(results.get('http', []))}")

    # Access specific results
    if ssh_servers := results.get("ssh"):
        print("\n  SSH Server Hosts:")
        for ip_addr, banner in ssh_servers:
            print(f"    - {ip_addr}: {banner}")

    if http_servers := results.get("http"):
        print("\n  HTTP Server Hosts:")
        for ip_addr, banner in http_servers:
            print(f"    - {ip_addr}: {banner}")


async def discover_single_service_example():
    """
    Alternative: Discover just HTTP servers (simpler case).
    """

    local_ip = findssh.get_lan_ip()
    network = findssh.address2net(local_ip, mask="24")  # /24 subnet

    results = await findssh.discover_services(
        network,
        service_ports={"http": 80},
        timeout=1.0,
        max_concurrent=50,
    )

    http_hosts = results["http"]
    print(f"Found {len(http_hosts)} HTTP servers")
    for ip_addr, status_line in http_hosts:
        print(f"  {ip_addr}: {status_line}")


async def discover_custom_ports_example():
    """
    Example: Use custom ports for services.
    """

    import ipaddress

    # Scan a specific subnet
    network = ipaddress.ip_network("192.168.1.0/24")

    # Define custom ports
    services = {
        "ssh": 22,
        "web": [80, 443, 8080, 8443],  # Multiple web server ports
        "dns": 53,
    }

    results = await findssh.discover_services(
        network,
        service_ports=services,
        timeout=2.0,
        max_concurrent=200,  # Higher concurrency for larger networks
    )

    for service, hosts in results.items():
        print(f"{service}: {len(hosts)} discovered")


if __name__ == "__main__":
    # Run the example
    print("=== SSH and HTTP Server Discovery Example ===\n")
    asyncio.run(discover_servers_example())

    # Uncomment to run other examples:
    # asyncio.run(discover_single_service_example())
    # asyncio.run(discover_custom_ports_example())
