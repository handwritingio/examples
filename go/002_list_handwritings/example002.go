package main

import (
	"fmt"

	"github.com/handwritingio/go-client/handwritingio"
)

var key = "<YOUR TOKEN>"
var secret = "<YOUR SECRET>"

func main() {
	// Initialize API client
	client, err := handwritingio.NewClient(key, secret)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Set up list params
	var params = handwritingio.DefaultHandwritingListParams
	params.OrderBy = "title"
	params.Limit = 50
	params.Offset = 0

	// Fetch first page
	handwritings, err := client.ListHandwritings(params)
	if err != nil {
		fmt.Println(err)
		return
	}

	for len(handwritings) > 0 {
		for _, handwriting := range handwritings {
			fmt.Printf("%s: %s\n", handwriting.ID, handwriting.Title)
		}

		// Fetch next page
		params.Offset += params.Limit
		handwritings, err = client.ListHandwritings(params)
		if err != nil {
			fmt.Println(err)
			return
		}

		fmt.Println("== Page ==")

	}

	return
}
