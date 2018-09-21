function findssh(port, service, timeout, baseip)
%% FINDSSH  find SSH or other servers on an IPv4 subnet
%
% must first do one-time install in Python 3.6 from Terminal:
%   pip install -e .
%
% example (find all SSH servers on IPv4 subnet on Port 22):
%   findssh()

assert(~verLessThan('matlab', '8.4'), 'Matlab >= R2014b required')

if nargin < 1, port=22; end
if nargin < 2, service = ''; end
if nargin < 3, timeout = 0.1; end
if nargin < 4, baseip = ''; end


validateattributes(port, {'numeric'}, {'integer', 'nonnegative'})
validateattributes(service, {'string', 'char'}, {'scalartext'})
validateattributes(timeout, {'numeric'}, {'real', 'nonnegative'})
validateattributes(baseip, {'string', 'char'}, {'scalartext'})

% Matlab R2018b didn't like ThreadPoolExectutor
servers = py.findssh.run(uint16(port), service, timeout, baseip, true);

hosts = cellfun(@char, cell(servers), 'uniformoutput', false);
disp(hosts)
end