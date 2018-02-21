on run argv
	-- set testOutput to do shell script "python server.py" as «class utf8» without altering line endings
    -- display dialog testOutput
    delay 3
    display dialog item 1 of argv
    -- do shell script "python server.py"
end run