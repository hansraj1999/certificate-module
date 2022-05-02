city_table = {405040: "MUMBAI", 405060: "MUMBAI", 405062: "MUMBAI", 503040: "BANGALORE", 513011: "BANGALORE", 541030 : "BANGALORE", 113011: "DELHI"}

tat_table = [[405040, 113011, 2], [405060, 113011, 5], [405062, 113011, 3], [503040, 113011, 5], [513011, 113011, 3], [541030, 113011, 8]]


def route(from_city, to_city):
    a = city_table.values()
    if from_city not in a or to_city not in a:
        return 'enter valid city names'

    def get_pincode(city_name):
        list_of_pin = []
        for i in city_table:
            if city_table[i] == city_name:
                list_of_pin.append(i)
        return list_of_pin
    
    from_pin = get_pincode(from_city)
    to_city_pin = get_pincode(to_city)
    time = []

    for i in range(len(from_pin)):
        for j in range(len(tat_table)):
            if from_pin[i] == tat_table[j][0] and to_city_pin[0] == tat_table[j][1]:
                time.append(tat_table[j][2])
    return f"{min(time)}-{max(time)} days"


print(route("BANGALORE", "DELHI"))

