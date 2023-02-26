function hosts = findssh(port, service, timeout)
%% FINDSSH  find SSH or other servers on an IPv4 subnet
%
% must first do one-time install in Python 3 from Terminal:
%   python3 -m pip install -e .
%
% example (find all SSH servers on IPv4 subnet on Port 22):
%   findssh()

assert(~verLessThan('matlab', '8.4'), 'Matlab >= R2014b required')

if nargin < 1, port=22; end
if nargin < 2, service = ''; end
if nargin < 3, timeout = 0.1; end

validateattributes(port, {'numeric'}, {'integer', 'nonnegative'})
validateattributes(service, {'string', 'char'}, {'scalartext'})
validateattributes(timeout, {'numeric'}, {'real', 'nonnegative'})

net = py.findssh.address2net(py.findssh.get_lan_ip());

hosts = cell(py.findssh.threadpool.get_hosts(net, uint8(port), service, timeout));

end
