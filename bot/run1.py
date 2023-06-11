my_dict = {
    "a": "a",
    "b": "b"
}
for count, (key, value) in enumerate(my_dict.items(), 1):
    print(key, value, count)