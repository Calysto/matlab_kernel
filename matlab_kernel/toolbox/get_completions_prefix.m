function prefix = get_completions_prefix(substr)
%get_completions_prefix  shared prefix for completion results
%   prefix = get_completions_prefix(substr) will return the prefix that needs
%   to be prepended to the results of mtFindAllTabCompletions in order for
%   Python's MetaKernel to use those results correctly. For now, this simply
%   fixes a problem where MetaKernel framework expects
%   do_matlab_complete('some_struct.long') to return
%   `some_struct.long_fieldname`, but mtFindAllTabCompletions returns
%   `long_fieldname` instead in this case.
    prefix = '';
    period_ind = find(substr == '.');
    if isempty(period_ind)
        return;
    end
    needs_prefix = false;
    try
        needs_prefix = evalin('base', ['isstruct(' substr(1:period_ind(1)-1) ')']);
    catch
    end
    if needs_prefix
        prefix = substr(1:period_ind(1));
    end
end

