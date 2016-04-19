Example 2
===============

This example demonstrates listing all handwritings
It requires a valid API token pair, which can be created for free at
https://handwriting.io

After you have your token pair simply find the following two lines in
 `example002.go`


```golang
var key = "<YOUR TOKEN>"
var secret = "<YOUR SECRET>"
```

And change them to your token and secret. Be sure to keep the quotes, and don't include
any spaces.

Then, to run this script, simply invoke it...

```sh
go run example002.go
```

The list of handwritings will be printed to standard output.
