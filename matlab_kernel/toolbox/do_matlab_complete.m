function do_matlab_complete(substring)
%DO_MATLAB_COMPLETE   list tab completion options for string
%   do_matlab_complete(substring) prints out the tab completion options for the
%   string `substring`, one per line. This required evaluating some undocumented
%   internal matlab code in the "base" workspace.

% only tested on R2014b and R2015a
v = ver('MATLAB');
if str2num(v) < 8.4
    return
end

% grep'ing MATLAB R2014b for "tabcomplet" and dumping the symbols of the ELF
% files that match suggests that the internal tab completion is implemented in
% bin/glnxa64/libmwtabcompletion.so and called from
% /bin/glnxa64/libnativejmi.so, which contains the function
% mtFindAllTabCompletions. We can infer from MATLAB's undocumented naming
% conventions that this function can be accessed as a method of
% com.matlab.jmi.MatlabMCR objects.

% some trial and error reveals the likely function signature
% function mtFindAllTabCompletions(String substring, int len, int offset)
% where `substring` is the string to be completed, `len` is the length of the
% string, and the first `offset` values returned by the engine are ignored.
len = num2str(length(substring));
offset = num2str(0);

get_completions = [ ...
    'matlabMCRinstance_avoid_name_collisions = com.mathworks.jmi.MatlabMCR;' ...
    'completions_output = matlabMCRinstance_avoid_name_collisions.mtFindAllTabCompletions(''' ...
    substring ''', ' len ', ' offset ');' ...
    'for i=1:length(completions_output);' ...
    '    fprintf(1, ''%s\n'', char(completions_output(i)));' ...
    'end;' ...
    'clear(''matlabMCRinstance_avoid_name_collisions'', ''completions_output'');' ];
evalin('base', get_completions);
