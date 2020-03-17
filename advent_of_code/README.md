

# Tips
https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661

# Getting inputs
https://github.com/wimglenn/advent-of-code-data

steps:
* open new chrome tab
* open dev console
* click network tab
* go to: https://adventofcode.com/2016/day/1/input
* under "Name" click 2nd
* look for "session" under "Cookies"
* double click, copy
* `echo <session> > ~/.config/aocd/token`

# PyCharm setup
* mark `advent_of_code` dir as 'Sources Root'

# Other setup
* `sudo pip3 install advent-of-code-data`
    * `cookie=<aoc cookie>`
    * `mkdir -p ~/.config/aocd && echo $cookie > ~/.config/aocd/token && cat ~/.config/aocd/token`
* `sudo pip3 install parse`





