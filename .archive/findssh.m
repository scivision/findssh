function hosts = findssh(port, service, timeout)
%% FINDSSH  find SSH or other servers on an IPv4 subnet
%
% must first do one-time install in Python 3 from Terminal:
%   python3 -m pip install -e .
%
% example (find all SSH servers on IPv4 subnet on Port 22):
%   findssh()

arguments
    port (1,1) {mustBeInteger, mustBePositive} = 22
    service (1,1) string = ""
    timeout (1,1) {mustBeReal, mustBePositive} = 0.1
end

net = py.findssh.address2net(py.findssh.get_lan_ip());

hosts = cell(py.findssh.threadpool.get_hosts(net, uint8(port), service, timeout));

end
