# WikiLinks

This program finds the list of jumps(or paths) to take inorder to reach from a given start page of wikipedia to a given destination page on wikipedia.

The program uses PriorityQueue datastructure to choose the next page to visit and HTMLParser to scrape data from wikipedia page.

The program assumes that when a page has more links in common with target page than other pages, then the chances of reaching the destination is more if one chooses that page.
