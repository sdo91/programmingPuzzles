

# Tips
https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661

# Getting inputs
https://github.com/wimglenn/advent-of-code-data

steps:
- copy this:
    - https://adventofcode.com/2018/day/22/input
- open new chrome tab (ctrl T)
- open dev console (ctrl shift J)
- click network tab
- nav to aoc input page (Ctrl L, Ctrl V, Enter)
    - see above
- under "Name" click on input
    - other entries might work?
- under "Cookies" look for "session"
- double click "Value", copy
- `echo <session value> > ~/.config/aocd/token`

# PyCharm setup
- (not needed anymore) mark `advent_of_code` dir as 'Sources Root'

# Other setup
- `sudo pip3 install advent-of-code-data`
    - `cookie=<aoc cookie>`
    - `mkdir -p ~/.config/aocd && echo $cookie > ~/.config/aocd/token && cat ~/.config/aocd/token`
- `sudo pip3 install parse`





