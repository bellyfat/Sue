use framework "Foundation"

urlEncode("{:}")

on urlEncode(input)
    tell current application's NSString to set rawUrl to stringWithString_(input)
    set theEncodedURL to rawUrl's stringByAddingPercentEscapesUsingEncoding:4 -- 4 is NSUTF8StringEncoding
    return theEncodedURL as Unicode text
end urlEncode