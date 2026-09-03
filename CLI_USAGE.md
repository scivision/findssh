"""
CLI Usage Examples for findssh - Multi-Service Discovery
=========================================================

The findssh package can now be used from the command line to discover multiple
services (SSH, HTTP, etc.) on a network in a single efficient scan.
"""

# === ORIGINAL SINGLE-PORT SCANNING (unchanged)

# Scan local subnet for SSH servers (port 22):
#   python -m findssh
#
# Output:
#   own address 192.168.1.100
#   searching 192.168.1.0/24
#   (IPv4Address('192.168.1.1'), 'OpenSSH_8.0...')
#   (IPv4Address('192.168.1.15'), 'OpenSSH_7.4...')


# Scan for a specific port:
#   python -m findssh -p 8080
#
# With service matching:
#   python -m findssh -p 8080 -s "nginx"
#
# Custom timeout:
#   python -m findssh -p 22 -t 0.5


# Scan a specific network:
#   python -m findssh -b 192.168.0.1


# === NEW: MULTI-SERVICE DISCOVERY

# Discover SSH servers (default port 22):
#   python -m findssh --services ssh
#
# Output:
#   own address 192.168.1.100
#   searching 192.168.1.0/24
#   discovering services: ssh
#
#   ssh:
#     192.168.1.1: SSH-2.0-OpenSSH_8.0
#     192.168.1.15: SSH-2.0-OpenSSH_7.4


# Discover HTTP servers (default port 80):
#   python -m findssh --services http
#
# Output:
#   http:
#     192.168.1.2: HTTP/1.1 200 OK


# Discover both SSH and HTTP in a single pass:
#   python -m findssh --services ssh http
#
# Output:
#   discovering services: ssh, http
#
#   http:
#     192.168.1.2: HTTP/1.1 200 OK
#   ssh:
#     192.168.1.1: SSH-2.0-OpenSSH_8.0
#     192.168.1.15: SSH-2.0-OpenSSH_7.4


# Discover HTTP on custom ports (80 and 443):
#   python -m findssh --services "http:80,443"
#
# Output:
#   discovering services: http
#
#   http:
#     192.168.1.2: HTTP/1.1 200 OK
#     192.168.1.5: HTTP/1.1 301 Moved Permanently


# Mix services with custom and default ports:
#   python -m findssh --services "ssh:2222 http:80,443 https"
#
# Output:
#   discovering services: ssh, http, https
#
#   http:
#     192.168.1.2: HTTP/1.1 200 OK
#   https:
#     192.168.1.5: HTTP/1.1 301 Moved Permanently
#   ssh:
#     192.168.1.3: SSH-2.0-OpenSSH_8.0


# Scan a specific network with multi-service discovery:
#   python -m findssh -b 10.0.0.1 --services "ssh http:8080"
#
# With custom timeout (for slower networks):
#   python -m findssh --services ssh http -t 2.0


# With verbose logging (shows connection attempts):
#   python -m findssh --services ssh http -v


# === KNOWN SERVICES (auto-detected defaults)

# If you use a bare service name without specifying a port, the following
# defaults are used:
#   - ssh → 22
#   - http → 80
#   - https → 443
#   - dns → 53
#
# Example:
#   python -m findssh --services ssh https dns
#
# Equivalent to:
#   python -m findssh --services "ssh:22 https:443 dns:53"


# === COMMON PATTERNS

# Quick scan for web servers on common ports:
#   python -m findssh --services "http:80,8080,8443 https:443"

# Scan for SSH on non-standard port and HTTP:
#   python -m findssh --services "ssh:2222 http"

# Comprehensive server discovery (all known services):
#   python -m findssh --services ssh http https dns

# Ultra-fast scan on a small subnet:
#   python -m findssh -b 192.168.1.0 --services ssh http -t 0.1

# Thorough scan on a large network with longer timeout:
#   python -m findssh -b 10.0.0.0 --services ssh http https -t 2.0 -v


# === SERVICE PARSING FORMAT

# The --services argument uses this format:
#   service[:port[,port,...]]
#
# Components:
#   - service: name of the service (required)
#   - port: TCP port number (optional, uses default if omitted)
#   - Multiple ports: comma-separated, no spaces
#   - Multiple services: space-separated
#
# Examples:
#   ssh                          → SSH on port 22 (default)
#   ssh:2222                     → SSH on port 2222
#   http                         → HTTP on port 80 (default)
#   http:80,443                  → HTTP on ports 80 and 443
#   ssh:22 http:80,443           → SSH on 22, HTTP on 80 and 443
#   ssh:2222 http:8080,8443 dns  → SSH on 2222, HTTP on 8080/8443, DNS on 53


# === NOTES

# - Multi-service discovery uses asyncio for concurrent scanning
#   (much faster than single-port mode with threadpool)
# - The --threadpool flag is ignored when using --services
# - Results are grouped by service type in the output
# - Empty service results show "(none found)"
# - Use -t/--timeout appropriately for your network:
#   * LAN: 0.5-1.0 seconds (default)
#   * WiFi: 1.0-2.0 seconds
#   * WAN/VPN: 2.0-5.0 seconds
# - Verbose mode (-v) shows connection attempts and timing info
