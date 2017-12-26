## Get Encoded Email, Decode in string & append to same list
def binary_to_str(bin_list):
    for val in bin_list[1:]:
        email = (val[3])
        email = email.replace(" ", "")
        hex_str = (hex(int(email, 2)))
        email_id = (bytes.fromhex(hex_str[2:]).decode('utf-8'))
        val.append(email_id)
