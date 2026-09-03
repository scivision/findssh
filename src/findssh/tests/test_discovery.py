import pytest
import ipaddress
import asyncio
import findssh
import findssh.coro

TIMEOUT = 0.5


@pytest.mark.asyncio
async def test_discover_services_validation():
    """Test discover_services parameter validation."""
    net = ipaddress.ip_network("127.0.0.1/32", strict=False)

    # Test max_concurrent validation
    with pytest.raises(ValueError):
        await findssh.coro.discover_services(
            net, {"ssh": 22}, TIMEOUT, max_concurrent=0
        )

    # Test invalid port type
    with pytest.raises(TypeError):
        await findssh.coro.discover_services(
            net,
            {"ssh": "invalid"},
            TIMEOUT,  # type: ignore
        )


@pytest.mark.asyncio
async def test_discover_services_port_list():
    """Test discover_services with port as list."""
    net = ipaddress.ip_network("127.0.0.1/32", strict=False)

    # Test with list of ports
    results = await findssh.coro.discover_services(
        net, {"http": [80, 443]}, TIMEOUT, max_concurrent=10
    )

    assert isinstance(results, dict)
    assert "http" in results
    assert isinstance(results["http"], list)


@pytest.mark.asyncio
async def test_discover_services_http_detection(mock_http_server):
    """Test HTTP service detection with working mock HTTP server."""
    port = mock_http_server

    net = ipaddress.ip_network("127.0.0.1/32", strict=False)
    results = await findssh.coro.discover_services(
        net, {"http": port}, timeout=1.0, max_concurrent=10
    )

    assert isinstance(results, dict)
    assert "http" in results
    assert isinstance(results["http"], list)

    # With the fixed HTTP detection (sending GET request), we should find the server
    assert len(results["http"]) > 0, "HTTP server should be detected"

    # Verify the response format
    host, banner = results["http"][0]
    assert isinstance(host, ipaddress.IPv4Address)
    assert isinstance(banner, str)
    assert "HTTP" in banner
    assert "200" in banner


@pytest.mark.asyncio
async def test_discover_services_http_detection_async(mock_http_server_async):
    """Test HTTP service detection with async mock HTTP server."""
    port = mock_http_server_async

    net = ipaddress.ip_network("127.0.0.1/32", strict=False)
    results = await findssh.coro.discover_services(
        net, {"http": port}, timeout=1.0, max_concurrent=10
    )

    assert isinstance(results, dict)
    assert "http" in results
    assert isinstance(results["http"], list)

    # Should detect the async HTTP server
    assert len(results["http"]) > 0, "Async HTTP server should be detected"

    host, banner = results["http"][0]
    assert isinstance(host, ipaddress.IPv4Address)
    assert "HTTP" in banner


def test_discover_services_multiple_services():
    """Test discover_services returns dict structure for multiple services."""
    net = ipaddress.ip_network("127.0.0.1/32", strict=False)

    results = asyncio.run(
        findssh.coro.discover_services(
            net, {"ssh": 22, "http": 80}, TIMEOUT, max_concurrent=10
        )
    )

    # Verify structure
    assert isinstance(results, dict)
    assert set(results.keys()) == {"ssh", "http"}
    assert isinstance(results["ssh"], list)
    assert isinstance(results["http"], list)

    # Verify each result in lists has correct structure
    for service_name, hosts in results.items():
        for host, banner in hosts:
            assert isinstance(host, ipaddress.IPv4Address)
            assert isinstance(banner, str)


def test_discover_services_structure():
    """Test that discover_services returns correct structure for empty results."""
    net = ipaddress.ip_network("127.0.0.1/32", strict=False)

    # Test multiple services on ports that likely have nothing
    results = asyncio.run(
        findssh.coro.discover_services(
            net,
            {"service1": 9999, "service2": 9998, "service3": 9997},
            timeout=0.1,
            max_concurrent=10,
        )
    )

    # Verify structure even with empty results
    assert isinstance(results, dict)
    assert "service1" in results
    assert "service2" in results
    assert "service3" in results
    assert all(isinstance(v, list) for v in results.values())
