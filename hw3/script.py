#select distinct column vals
#open the thing
#for line in thing
#strip new line
#print the thing with line

f = open("output.txt", "r")
for line in f:
  line.rstrip()
  print 'IFNULL(COUNT(IF(value = "' + line.strip() + '", 1, NULL)), 0) AS "' + line.strip() + '",'