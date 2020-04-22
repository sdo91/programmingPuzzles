

# Tips
https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661

# Getting inputs
https://github.com/wimglenn/advent-of-code-data

steps:
* open new chrome tab
* open dev console
* click network tab
* go to: https://adventofcode.com/2016/day/1/input
* under "Name" click on one of the entries (might be called input)
* under "Cookies" look for "session"
* double click "Value", copy
* `echo <session value> > ~/.config/aocd/token`

# PyCharm setup
* (not needed anymore) mark `advent_of_code` dir as 'Sources Root'

# Other setup
* `sudo pip3 install advent-of-code-data`
    * `cookie=<aoc cookie>`
    * `mkdir -p ~/.config/aocd && echo $cookie > ~/.config/aocd/token && cat ~/.config/aocd/token`
* `sudo pip3 install parse`





