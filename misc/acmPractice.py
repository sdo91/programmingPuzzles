

uInput = input('cmd: ')

if uInput == 'send':
    
    print('git add -A')
    print('git commit -m "Some changes"')
    print('git pull')
    print('git push')
    
if uInput == 'receive':
    
    print('git add -A')
    print('git stash')
    print('git pull')
    print('git stash pop')
    
if uInput == 'info':
    
    print('git status -s')
    
