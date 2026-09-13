import re

from sea import Sea
text = input("Введите описание моря: ")

parts = re.findall(r'"[^"]*"|\S+', text)

object_type = parts[0]
name = parts[1].strip('"')
depth = float(parts[2])
salinity = float(parts[3]) 

sea = Sea(name, depth, salinity)

print("\nСоздан объект:")
sea.print_info()