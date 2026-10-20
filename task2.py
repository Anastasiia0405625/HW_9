list1 = ["potato", 123, 1.22, 5>2, "food", "vegetable"]
number_str = 0
for item in list1:
    if type(item) is str:
        number_str +=1
number_str