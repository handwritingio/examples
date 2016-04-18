Example 1
===============

This example demonstrates very simple API access to render a PDF of a message.
It requires a valid API token pair, which can be created for free at
https://handwriting.io

After you have your token pair simply find the following two lines in
 `example001.go`


```golang
var key = "<YOUR TOKEN>"
var secret = "<YOUR SECRET>"
```

And change them to your token and secret. Be sure to keep the quotes, and don't include
any spaces.

Then, to run this script, simply invoke it...

```sh
go run example001.go
```

After it runs look for a file called `out.pdf` in the working directory and open it
