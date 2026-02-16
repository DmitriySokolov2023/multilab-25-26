text = "яблоко груша яблоко банан груша яблоко"
count_dict = {}

for el in text.split(" "):
	if el in count_dict:
		count_dict[el] = count_dict[el] + 1
	else: count_dict[el] = 1

print(count_dict)
