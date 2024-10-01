from ip_address_format import is_valid_ip_address

def byte_to_bitstring(byte):
    bitstring=""
    if int(byte / 128) == 1:
        bitstring = bitstring+"1"
        byte= byte-128
    else:
        bitstring = bitstring+"0"
    if int(byte / 64) == 1:
        bitstring = bitstring+"1"
        byte= byte-64
    else:
        bitstring = bitstring+"0"
    if int(byte / 32) == 1:
        bitstring = bitstring+"1"
        byte= byte-32
    else:
        bitstring = bitstring+"0"
    if int(byte / 16) == 1:
        bitstring = bitstring+"1"
        byte= byte-16
    else:
        bitstring = bitstring+"0"
    if int(byte / 8) == 1:
        bitstring = bitstring+"1"
        byte= byte-8
    else:
        bitstring = bitstring+"0"
    if int(byte / 4) == 1:
        bitstring = bitstring+"1"
        byte= byte-4
    else:
        bitstring = bitstring+"0"
    if int(byte / 2) == 1:
        bitstring = bitstring+"1"
        byte= byte-2
    else:
        bitstring = bitstring+"0"
    if int(byte / 1) == 1:
        bitstring = bitstring+"1"
        byte= byte-1
    else:
        bitstring = bitstring+"0"
    
    return bitstring
    

def subnet_calculator(ip_address, mask):
    # Test the IP-address
    check_result = is_valid_ip_address(ip_address+"/"+ str(mask))
    if check_result[0]:
        # Remove the mask from check_result
        check_result[1].pop(4)
        
        #calculate the value of address
        address_value = 0;
        address_bit_string = ""
        for octet_no,octet in enumerate(check_result[1]):
            address_bit_string= address_bit_string + byte_to_bitstring(octet)
        
        mask_bit_string = ""
        for i in range(32,32-mask,-1):
            mask_bit_string = mask_bit_string + "1"
            
        for i in range(32-mask,0,-1):
            mask_bit_string = mask_bit_string + "0"
            
        
        print(address_bit_string)
        print(mask_bit_string)
            
        
        
        
        
    else:
        print("Please provide a proper IP-adress and mask")
        
    


def main():
    subnet_calculator('192.168.0.1', 24)
    


if __name__ == "__main__":
    main()