function do_matlab_complete(substring)
%DO_MATLAB_COMPLETE   list tab completion options for string
%   do_matlab_complete(substring) prints out the tab completion options for the
%   string `substring`, one per line. This required evaluating some undocumented
%   internal matlab code in the "base" workspace.
% 
%	Only MATLAB versions R2013a, R2014b, and R2015a were available for testing.
%	This function is probably incompatible with some or many other releases, as
%	the undocumented features it relies on are subject to change without notice.

% grep'ing MATLAB R2014b for "tabcomplet" and dumping the symbols of the ELF
% files that match suggests that the internal tab completion is implemented in
% bin/glnxa64/libmwtabcompletion.so and called from
% /bin/glnxa64/libnativejmi.so, which contains the function
% mtFindAllTabCompletions. We can infer from MATLAB's undocumented naming
% conventions that this function can be accessed as a method of
% com.matlab.jmi.MatlabMCR objects.

% Trial and error reveals likely function signatures for certain MATLAB versions
% R2014b and R2015a:
% 	mtFindAllTabCompletions(String substring, int len, int offset)
%	where `substring` is the string to be completed, `len` is the length of the
%	string, and the first `offset` values returned by the engine are ignored.
% R2013a:
%	mtFindAllTabCompletions(String substring, int offset [optional])

len = length(substring);
offset = 0;

if verLessThan('MATLAB','8.4')
    % verified for R2013a
    args = sprintf('''%s'', %g', substring, offset);
else
    % verified for R2014b, 2015a
	args = sprintf('''%s'', %g, %g', substring, len, offset);
end


get_completions = [ ...
    'matlabMCRinstance_avoid_name_collisions = com.mathworks.jmi.MatlabMCR;' ...
    'completions_output = matlabMCRinstance_avoid_name_collisions.mtFindAllTabCompletions(' ...
    args ');' ...
    'for i=1:length(completions_output);' ...
    '    fprintf(1, ''%s\n'', char(completions_output(i)));' ...
    'end;' ...
    'clear(''matlabMCRinstance_avoid_name_collisions'', ''completions_output'');' ];

try
    evalin('base', get_completions);
end
