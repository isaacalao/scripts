#!/bin/python3

# CONSTANTS
OCTET_DELIM = "."
COLOR = tuple(f"\x1b[3{clr}m" for clr in range(1, 6))
STYLE = tuple(f"\x1b[{stl}m" for stl in range(6))

# FUNCTIONS

# A simple mask generator
def gen_mask(sublen):
    mask = [ 0, 0, 0, 0 ]
    for i in range(sublen):
        mask[i//8] += 2**(7-(i%8))
    return mask

# This function thoroughly examines the given cidr value and yields and exception if the value is not proper
def examine_cidr(cidr):
    ip,baseip,mask,sublen = None,None,None,None
    try:
        if len(cidr) != 2:
            raise Exception(f"Error parsing CIDR value {cidr}")
        else:
            ip = list(map(lambda var : int(var), cidr[0].split(OCTET_DELIM)))
            sublen = int(cidr[1])
            if sublen < 0 or sublen > 32:
                raise Exception(f"Subnet length out of bounds {sublen}")
            if len(ip) == 4:
                for bits in ip:
                    if 0 > bits or bits > 255:
                        raise Exception("Value is not in octet range")
            else:
                raise Exception(f"Failed to parse {cidr[0]}")
            mask = gen_mask(sublen)
    except Exception as err:
        raise Exception(f"{COLOR[0]}{err}{STYLE[0]}")

    return { "IP" : ip, "SUBLEN" : sublen, "HOST_BITS" : 32-sublen, "HOST_AVAIL" : (2**(32-sublen))-2 }

# Helper for the function below, utilizes bitwsize operations to increase the ip addr
def inc_ip(ip, val):
    ip = (ip[0] << 24) | (ip[1] << 16) | (ip[2] << 8) | ip[3]
    ip = ip + val
    return [ (ip >> 24) & 255, (ip >> 16) & 255, (ip >> 8) & 255, (ip & 255) ]


# This function helps to enumerate the given subnet and forge a new cidr value
def get_new_cidr(subnet, cidr, wan):
    if subnet["HOST"] < cidr["HOST_AVAIL"] or wan:
      if not wan:
        bit_pos,hosts_needed=cidr["HOST_BITS"],0
        possible = [ 2**i for i in range(cidr["HOST_BITS"]) ]
        for i in range(cidr["HOST_BITS"]):
            if subnet["HOST"] <= possible[i]:
                hosts_needed=possible[i]
                bit_pos=i
                break
        if hosts_needed == 0 or cidr["HOST_AVAIL"] < hosts_needed:
            raise Exception(f"{COLOR[0]}Not enough hosts in addr space.{STYLE[0]}")
      else:
        hosts_needed=4
        bit_pos=2

      subnet["DEPT_HOST"]["NETID"] = cidr["IP"]
      subnet["DEPT_HOST"]["FIRST_HOST"] = inc_ip(cidr["IP"], 1)
      subnet["DEPT_HOST"]["LAST_HOST"] = inc_ip(cidr["IP"], (hosts_needed-2))
      subnet["DEPT_HOST"]["BROAD_ID"] = inc_ip(cidr["IP"], (hosts_needed-1))
      subnet["SUBLEN"]= 32-bit_pos
      subnet["MASK"]=gen_mask(subnet["SUBLEN"])

      cidr["IP"] = inc_ip(cidr["IP"], hosts_needed)
      cidr["SUBLEN"] = subnet["SUBLEN"]
      #cidr["HOST_BITS"] = bit_pos
      cidr["HOST_AVAIL"] -= hosts_needed 
      return 0
    else:
        print(f"{COLOR[0]}Not enough hosts in this block!{STYLE[0]}")
        return 1

# This function builds subnets
def build_subnets(cidr):
    status = 0
# Create cidr
    CIDR=cidr

# Each each subnet # is represented by its subscript
    SUBNET = [{ "SEGMENT" : None, "HOST" : 2, # For net and broad
                "DEPT_HOST" : {
                    "NETID" : None, "FIRST_HOST" : None,
                    "LAST_HOST" : None, "BROAD_ID" : None
                    }, "SUBLEN" : None, "MASK" : None
              } for i in range(6)
             ]

    for i in range(len(SUBNET)):
        if i < 3:
            print(f"There are [{COLOR[1]}{CIDR['HOST_AVAIL']}{STYLE[0]}] addressable IP addresses available!")
            SUBNET[i]["SEGMENT"] = input("Enter the name of the segment: ")
            SUBNET[i]["HOST"] += int(input(f"Enter the number of hosts for {SUBNET[i]['SEGMENT']}: "))
            status = get_new_cidr(SUBNET[i], CIDR, False)
        else:
            SUBNET[i]["SEGMENT"] = f"WAN link {COLOR[1]}{STYLE[1]}{i-2}{STYLE[0]}"
            SUBNET[i]["HOST"] += 2
            print(f"{SUBNET[i]['SEGMENT']} requires [{COLOR[1]}{SUBNET[i]['HOST']-2}{STYLE[0]}] addressable IPs.")
            status = get_new_cidr(SUBNET[i], CIDR, True)
        if status:
            return status


# First table
    print(f"{STYLE[4]}Subnet\tSegment\tHost{STYLE[0]}")
    for i in range(len(SUBNET)):
        print(f"{i+1}\t{SUBNET[i]['SEGMENT']}\t{SUBNET[i]['HOST']-2}")

# Second table
    for i in range(len(SUBNET)):
        print(
               f"Segment\t\t{SUBNET[i]['SEGMENT']}\n"
               f"Requirement\t\t{SUBNET[i]['HOST']-2}\n"
               f"CIDR\t\t/{SUBNET[i]['SUBLEN']}\n"
               f"Subnet Mask\t\t{OCTET_DELIM.join(list(map(lambda var : str(var), SUBNET[i]['MASK'])))}\n"
               f"Network ID\t\t{OCTET_DELIM.join(list(map(lambda var : str(var), SUBNET[i]['DEPT_HOST']['NETID'])))}\n"
               f"First hosts\t\t{OCTET_DELIM.join(list(map(lambda var : str(var), SUBNET[i]['DEPT_HOST']['FIRST_HOST'])))}\n"
               f"Last hosts\t\t{OCTET_DELIM.join(list(map(lambda var : str(var), SUBNET[i]['DEPT_HOST']['LAST_HOST'])))}\n"
               f"Broadcast ID\t\t{OCTET_DELIM.join(list(map(lambda var : str(var), SUBNET[i]['DEPT_HOST']['BROAD_ID'])))}\n"
              )
    return status

# Main driver
cidr=examine_cidr(input("Enter CIDR value: ").split("/"))
build_subnets(cidr)
