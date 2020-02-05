import sys
import os.path
import ipaddress
from jinja2 import Environment, FileSystemLoader

##This script builds a router template based on Jinja2 Templates and user inputs from the CLI##
##This is specifically for SROS/TiMOS 7210-SAS-T auto-init pre-provisioining stored in a remote server, this would be the bof and cfg file.##





## User Inputted Arguments ##
def input_variables_hostname():
    hostname = input("What is the Hostname of the Device?:")
    print("\n\n\n")
    print(hostname)
    print("\n\n\n")
    return hostname

def input_variables_hostip():
    ip = input("What is your Host IP Address?:")
    while True:
        if(ipaddress.ip_address(ip)==False):
            print("\n\n")
            print("This is an invalid address.")
            print("\n\n")
            quit()
        else:
            print("\n\n")
            print("\nIP address {} is valid\n".format(ip))
            print("\n\n")
            return ip
            break

def input_variables_systemip():
    systemip = input("What is your System IP Address?:")
    while True:
        if(ipaddress.ip_address(systemip)==False):
            print("\n\n")
            print("This is an invalid address.")
            print("\n\n")
            quit()
        else:
            print("\n\n")
            print("\nIP address {} is valid\n".format(systemip))
            print("\n\n")
            return systemip
            break

def input_variables_mask():
    mask = input("What is your Mask?:")
    while True:
        if(ipaddress.ip_address(mask)==False):
            print("\n\n")
            print("This is an invalid address.")
            print("\n\n")
            quit()
        else:
            print("\n\n")
            print("\n IP address {} is valid\n".format(mask))
            print("\n\n")
            return mask
            break



##Checks if files already exists, if file exists it will only overwrite based on yes input from user##
##If file doesnt exist builds as normal in else statement##


## Checks if BOF files exists or not, allows users to overwrite or backout ###
## Requires Arguments based on the file function ##
def bof(file_bof, bof_output, hostname, ip, systemip):
    while True:
        if os.path.isfile(file_bof):
            overwrite = input("This BOF file already exists." "Overwrite? Y = yes, N = no\n")
            if overwrite.lower() == "y":
              with open(file_bof, "w") as outfile_bof:
                    outfile_bof.write(bof_output)
                    outfile_bof.close()
                    break
            elif overwrite == "n":
                    print("\n\n")
                    print('You have selected No, check whatever you need to check and try again!!\n')
                    print("\n\n")
                    break
            else:
                    print("\n\n")
                    print('You have entered invalid input, please run script again, Thank You!\n')
                    print("\n\n")
                    break
        else:
          with open(file_bof, "w") as outfile_bof:
              outfile_bof.write(bof_output)
              outfile_bof.close()
              break

## Checks if Config files exists or not, allows users to overwrite or backout ###

def conf(file_conf, conf_output, hostname, ip, systemip):
    while True:
        if os.path.isfile(file_conf):
            overwrite = input("This Config file already exists." "Overwrite? Y = yes, N = no\n")
            if overwrite.lower() == "y":
              with open(file_conf, "w") as outfile_conf:
                  outfile_conf.write(conf_output)
                  outfile_conf.close()
                  print("\n\n")
                  print("\n*** Check /user/home/tftp directory for SAS Boot Files ***\n", "\n Host Name:", hostname, "\n", "\n Address:", ip, "\n", "\n System Address:", systemip, "\n", "\n*** You Are Ready To CBAD ***\n")
                  print("\n\n")
                  break
            elif overwrite == "n":
                    print("\n\n")
                    print('You have selected No, check whatever you need to check and try again!!\n')
                    print("\n\n")
                    break
            else:
                    print("\n\n")
                    print('You have entered invalid input, please run script again, Thank You!\n')
                    print("\n\n")
                    break
        else:
          with open(file_conf, "w") as outfile_conf:
              outfile_conf.write(conf_output)
              outfile_conf.close()
              print("\n\n")
              print("\n*** Check /user/home/tftp directory for SAS Boot Files ***\n", "\n Host Name:", hostname, "\n", "\n Address:", ip, "\n", "\n System Address:", systemip, "\n", "\n *** You Are Ready To CBAD ***\n")
              print("\n\n")
              break





def main():
    hostname = input_variables_hostname()
    ip = input_variables_hostip()
    systemip = input_variables_systemip()
    mask = input_variables_mask()
    ### Directory for bof and conf files ###
    ##file_path= '/usr/home/tftp/' ###Prod Directory
    file_path = '/XXXX/XXXX/XXXX/XXXX/'  ###This is the directory of the remote server to get the cfg/bof file, this is where the files will be placed.

    ## Define  Location of Jinja2 Templates ##
    env = Environment(loader=FileSystemLoader(file_path))

    ##Reference Templates## 
    bof_template = env.get_template("./template.bof.j2")
    conf_template = env.get_template("./template.conf.j2")


    ## Static Variables ##
    masklen = ("24")
    gateway = ("10.255.255.1")

    ###Jinja2 Templating Information##
    ###Determines what objects replace what jinja2 variables in the j2 template##
    bof_output = bof_template.render(hostname=hostname, ip=ip, mask=mask, masklen=masklen, gateway=gateway)
    conf_output = conf_template.render(hostname=hostname, ip=ip, systemip=systemip, mask=mask,masklen=masklen, gateway=gateway)
    ## Define file names for bof and conf ##
    ## Defines location where said files will be saved ##
    file_bof = os.path.join(file_path, hostname+'.bof')
    file_conf = os.path.join(file_path, hostname+'.conf')

    bof(file_bof,bof_output,hostname,ip,systemip)
    conf(file_conf,conf_output,hostname,ip,systemip)


if __name__ == '__main__':
    main()
