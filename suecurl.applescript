use framework "Foundation"
use scripting additions

on run argv
	-- the inputs
	set buddyId to "B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:sue@robertism.com"
	set chatId to "singleUser"
	set textBody to "`this is a test`"
	set textBody to replaceText(textBody, "$", "¬¬¬")
	set fileName to "noFile"
	
	-- build curl command
	set command to "curl --data " & curlify("buddyId", buddyId) & " "
	set command to command & "--data " & curlify("chatId", chatId) & " "
	set command to command & "--data " & curlify("fileName", fileName) & " "
	set command to command & "--data " & curlify("textBody", textBody) & " "
	set command to command & "http://localhost:5000"
	
	-- run in background
	set runBackground to "> /dev/null 2>&1 &"
	
	-- send inputs to server and return
	-- do shell script pyBinary & " " & pyFile & " " & buddyId & " " & runBackground
	-- do shell script pyBinary & " " & pyFile & " " & buddyId & " " & chatId & " " & textBody & " " & fileName & " " & runBackground
	-- display dialog pyBinary & " " & pyFile & " " & buddyId & " " & chatId & " " & textBody & " " & fileName & " " & runBackground
	
	set finalText to do shell script command
	-- set finalText to curlify("msg", "`echo $PATH`")
	-- set finalText to urlEncode("`")
	display dialog finalText
end run

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

on curlify(key, val)
	set curlString to "\"" & key & "=" & urlEncode(val) & "\""
	return curlString
end curlify

on replaceText(someText, oldItem, newItem)
	set {tempTID, AppleScript's text item delimiters} to {AppleScript's text item delimiters, oldItem}
	try
		set {itemList, AppleScript's text item delimiters} to {text items of someText, newItem}
		set {someText, AppleScript's text item delimiters} to {itemList as text, tempTID}
	on error errorMessage number errorNumber
		set AppleScript's text item delimiters to tempTID
		error errorMessage number errorNumber
	end try
	return someText
end replaceText