package main

import (
	"fmt"
	"io"
	"os"

	"github.com/handwritingio/go-client/handwritingio"
)

var key = "<YOUR TOKEN>"
var secret = "<YOUR SECRET>"

// this is the message we will turn into handwriting. It supports most
// white-space characters such as newline (\n) and tab (\t) as well as
// regular spaces
var message = "Hey man!\n\n\tI love handwriting!\n\nLove,\n\tSomeone"
var filename = "out.pdf"

func main() {
	// Initialize API client
	c, err := handwritingio.NewClient(key, secret)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Prepare params for rendering
	var params = handwritingio.DefaultRenderParamsPDF
	params.HandwritingID = "31SAZEF000DX" // found in our catalog or by listing handwritings
	params.HandwritingSize = "15pt"
	params.Text = message
	params.Height = "2in"
	params.Width = "4in"

	// Call API to render PDF
	r, err := c.RenderPDF(params)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer r.Close()

	// Create file
	f, err := os.Create(filename)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	// Write PDF to file
	_, err = io.Copy(f, r)
	if err != nil {
		fmt.Println(err)
	}

	return
}
