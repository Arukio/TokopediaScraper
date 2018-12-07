shop_id = 1759863

def harga_margin(harga):
    if int(harga) <= 10000 :
        rego = int(harga) + 10000
    elif int(harga) <= 50000 and int(harga) > 10000 :
        rego = int(harga) + 15000
    elif int(harga) <= 70000 and int(harga) > 50000 :
        rego = int(harga) + 20000
    elif int(harga) <= 100000 and int(harga) > 70000 :
        rego = int(harga) + 25000
    elif int(harga) <= 130000 and int(harga) > 100000 :
        rego = int(harga) + 30000
    elif int(harga) <= 150000 and int(harga) > 130000 :
        rego = int(harga) + 35000
    else :
        rego = int(harga) + 40000

    return rego