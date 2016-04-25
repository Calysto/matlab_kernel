function do_complete(substring)
% Ask for completions of SUBSTRING from MATLAB.
%
% This hides the differences between versions
% for the calls needed to do completions.
%
% Copied nearly verbatim from matlab-emacs.

    v = ver('MATLAB');


    if str2double(v.Version) < 8.4

        % Pre R2014b: partial_string
        extracmd = '';

    else

        % Post R2014b: partial_string, caret, num
        extracmd = [ ', ' num2str(length(substring)) ',0' ];

        % DEV NOTE: If you find a test failure, contact Eric Ludlam
        % to also update matlab-emacs SF repository.

    end

    command = [ 'matlabMCRprocess_emacs = com.mathworks.jmi.MatlabMCR;' ...
                'completions_output = matlabMCRprocess_emacs.mtFindAllTabCompletions(''' ...
                substring '''' extracmd ');' ...
                'for i=1:length(completions_output); fprintf(1, ''%s\n'', char(completions_output(i))); end']; ...
         %       'clear(''matlabMCRprocess_emacs'',''completions_output'');' ];

    % Completion engine needs to run in the base workspace to know
    % what the variables you have to work with are.
    evalin('base',command);

end
