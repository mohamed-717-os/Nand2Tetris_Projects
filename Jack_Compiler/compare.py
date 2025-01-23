file1 = open('test.xml')
file2 = open('ArrayTest\Main.xml')

listfile1 = file1.readlines()
listfile2 = file2.readlines()

complete = True
for line in range(len(listfile1)):
    if listfile1[line] != listfile2[line]:
        complete = False
        print('Error in line:', line + 1)
        print('your line:', listfile1[line] ,end='')
        print('correct line:', listfile2[line])
        break

if complete:
    print('succesful')
