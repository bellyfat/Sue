use framework "Foundation"
use scripting additions
-- the inputs
set buddyId to quoted form of "B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:sue@robertism.com"
set chatId to quoted form of "singleUser"
-- set textBody to quoted form of "!help"
set textBody to "hi"
set textBody to urlEncode(textBody)
set fileName to quoted form of "noFile"

-- build curl command


set command to "echo hi"

-- run in background
set runBackground to "> /dev/null 2>&1 &"

-- send inputs to server and return
-- do shell script pyBinary & " " & pyFile & " " & buddyId & " " & runBackground
-- do shell script pyBinary & " " & pyFile & " " & buddyId & " " & chatId & " " & textBody & " " & fileName & " " & runBackground
-- display dialog pyBinary & " " & pyFile & " " & buddyId & " " & chatId & " " & textBody & " " & fileName & " " & runBackground

set finalText to do shell script "echo hi"
-- display dialog finalText

on urlEncode(input)
	tell current application's NSString to set rawUrl to stringWithString_(input)
	set theEncodedURL to rawUrl's stringByAddingPercentEscapesUsingEncoding:4 -- 4 is NSUTF8StringEncoding
	return theEncodedURL as Unicode text
end urlEncode

on urlDecode(theText)
	set theString to stringWithString_(theText) of NSString of current application
	set theEncoding to NSUTF8StringEncoding of current application
	set theAdjustedString to stringByReplacingPercentEscapesUsingEncoding_(theEncoding) of theString
	return (theAdjustedString as string)
end urlDecode