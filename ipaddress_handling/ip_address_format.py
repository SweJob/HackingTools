import re

def is_valid_ip_address(ip_address):
    
    # Check to see if start of input string is aaa.bbb.ccc.ddd 
    # with the possibility of a mask at the end.
    # Split at each "."
    
    # default value of mask is 32, ie. a single host
    mask = 32
    ip_valid = True
    mask_valid = True
       
    # split input string at each "." and "/"
    ip_address = ip_address.replace(" ","")    
    octet_list = re.split('[\\./]',ip_address)
     
    for index, octet in enumerate(octet_list):
        # Are the first four parts digits?
        if index < 4:
            if not octet.isdigit():
                ip_valid = False
            # Are the first four parts within 0 and 255
            elif int(octet) not in range(0,255):
                ip_valid = False
            else:
                octet_list[index] = int(octet)
                
        # if a fifth part, it should be the mask
        elif index == 4:                        
            # check to see if mask-part is a valid mask
            # if not a number not valid
            if not octet.isdigit():
                mask_valid = False
            
            # if value is not between 0 and 255, not valid
            elif int(octet) < 0 or int(octet) > 32:
                mask_valid = False
            else:
                mask = int(octet)
                octet_list[4] = mask
        else: 
            print(f"Disregarding data : {octet}")
           
    if not(mask_valid):
        octet_list[4] = "Not a valid mask. Should be between 0 and 32 (or ommitted to assume 32)"
    else:
        if len(octet_list) == 4:
            octet_list.append(mask)
    
    if ip_valid:
        return_address = octet_list    
    else:
        return_address = "Not a valid IP address"
        
    return ip_valid and mask_valid, return_address 


# test of function
def main():
    VALID_IP_ADDRESS = "192.168.0.1"
    VALID_IP_ADDRESS_AND_MASK = "192.168.0.1/24"
    VALID_IP_ADDRESS_WITH_SPACES = " 192.168.0.1 / 24"
    INVALID_IP_ADDRESS1 = "256.0.3.12"
    INVALID_IP_ADDRESS2 = "192.a.3.12"
    INVALID_IP_ADDRESS3 = "192.0.3."
    INVALID_MASK = "192.168.0.1/33"
    
    # Test is valid ip address
    print(is_valid_ip_address(VALID_IP_ADDRESS))
    print(is_valid_ip_address(VALID_IP_ADDRESS_AND_MASK))
    print(is_valid_ip_address(VALID_IP_ADDRESS_WITH_SPACES))
    print(is_valid_ip_address(INVALID_IP_ADDRESS1))
    print(is_valid_ip_address(INVALID_IP_ADDRESS2))
    print(is_valid_ip_address(INVALID_IP_ADDRESS3))
    print(is_valid_ip_address(INVALID_MASK))
    
if __name__ == "__main__":
    main()