#!/usr/bin/env python3
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows),
  and device does not have Avahi server.
I wanted to make it as cross-platform as possible,
  where the user would have only basic Python installed (Windows)

Note:
timeout value bare minimum is 0.15 seconds for LAN,
suggest using higher values say 0.25 or 0.35 to allow for network / CPU delays
Wifi timeout should be 1 second or more
"""

import asyncio
import logging
import ipaddress as ip
from argparse import ArgumentParser

from . import get_lan_ip, address2net, discover_services
from . import coro
from . import threadpool

PORT = 22
TIMEOUT = 1.0

# Default ports for known services
DEFAULT_SERVICE_PORTS = {
    "ssh": 22,
    "http": 80,
    "https": 443,
    "dns": 53,
}


def parse_services(services_str: str) -> dict[str, int | list[int]]:
    """
    Parse service specification string.

    Format: "service[:port[,port,...]]" (space-separated)
    Examples:
        "ssh" → {"ssh": 22}
        "ssh:22" → {"ssh": 22}
        "http:80,443" → {"http": [80, 443]}
        "ssh http:80,443" → {"ssh": 22, "http": [80, 443]}
        "ssh:2222 http:8080,8443" → {"ssh": 2222, "http": [8080, 8443]}
    """
    result: dict[str, int | list[int]] = {}

    for spec in services_str.split():
        if ":" in spec:
            service_name, ports_str = spec.split(":", 1)
            ports_list = [int(p.strip()) for p in ports_str.split(",")]
            if len(ports_list) == 1:
                result[service_name] = ports_list[0]
            else:
                result[service_name] = ports_list
        else:
            # Use default port for service
            service_name = spec
            if service_name in DEFAULT_SERVICE_PORTS:
                result[service_name] = DEFAULT_SERVICE_PORTS[service_name]
            else:
                raise ValueError(
                    f"Unknown service: {service_name}. Use service:port format."
                )

    if not result:
        raise ValueError("No services specified")

    return result


def main():
    p = ArgumentParser("scan for hosts with open port, without NMAP")

    # Single port mode (original behavior)
    p.add_argument("-p", "--port", help="single port to try", default=PORT, type=int)
    p.add_argument(
        "-s", "--service", default="", help="string to match to qualify detections"
    )

    # Multi-service mode (new feature)
    p.add_argument(
        "--services",
        help=(
            "discover multiple services. Format: 'service[:port[,port,...]]' (space-separated). "
            "Examples: 'ssh', 'ssh http:80,443', 'ssh:2222 http:8080'. "
            "Defaults: ssh=22, http=80, https=443, dns=53"
        ),
        type=str,
        default="",
    )

    p.add_argument(
        "-t",
        "--timeout",
        help="timeout to wait for server. Must be finite or will hang.",
        type=float,
        default=TIMEOUT,
    )
    p.add_argument("-b", "--baseip", help="set a specific subnet to scan")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument(
        "-threadpool", help="use threadpool instead of asyncio", action="store_true"
    )
    P = p.parse_args()

    ll = logging.DEBUG if P.verbose else logging.INFO
    logging.basicConfig(level=ll)

    if not P.baseip:
        ownip = get_lan_ip()
        print("own address", ownip)
    else:
        ownip = ip.ip_address(P.baseip)

    net = address2net(ownip)
    print("searching", net)

    # Multi-service discovery mode
    if P.services:
        if P.threadpool:
            print(
                "Warning: threadpool not supported for multi-service discovery, using asyncio"
            )

        try:
            service_ports = parse_services(P.services)
        except ValueError as e:
            print(f"Error parsing services: {e}")
            return

        print(f"discovering services: {', '.join(service_ports.keys())}")
        results = asyncio.run(discover_services(net, service_ports, P.timeout))

        # Display results
        print()
        for service_name in sorted(results.keys()):
            hosts = results[service_name]
            print(f"{service_name}:")
            if hosts:
                for host, banner in hosts:
                    print(f"  {host}: {banner}")
            else:
                print("  (none found)")

    # Original single-port mode
    else:
        if P.threadpool:
            for host in threadpool.get_hosts(
                net,
                P.port,
                P.timeout,
                P.service,
            ):
                print(host)
        else:
            asyncio.run(coro.get_hosts(net, P.port, P.timeout, P.service))


if __name__ == "__main__":
    main()
