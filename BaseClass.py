'''
Created on Jul 2, 2019

@author: HI TECH
'''
import argparse
import paramiko
import socket
from sys import stdin, stdout, stderr


class BaseClass():
    '''
    classdocs
    '''

    def __init__(self, id=None, name=None, category=None, salary=None):
        '''
        Constructor
        @param id: integer unique value 
        @param name : name of employee4
        @param Category:  the Category of employee4 (engineer or manger)
        @param salary: integer number , how much the employee4 Catching salary

        '''
        self.id = id
        self.name = name
        self.category = category
        self.salary = salary

    def argumentParser(self):

        # Instantiate the parser
        parser = argparse.ArgumentParser(description="The server IP")

        parser.add_argument(
            '-s', "--server", help="The server name", type=int, default=0)
        parser.add_argument(
            '-i', "--id", help="The id", type=int, default=0)
        parser.add_argument(
            '-n', "--name", help="The name of employee4", type=str, default="")
        parser.add_argument(
            '-sal', "--salary", help="The salary", type=int, default=0)

        # Parse the arguments
        arguments = parser.parse_args()
        return arguments

    # Connecting to the remote server using Paramiko
    def connect(self):
        '''
        @summary: connecting data with sever
        you need to add the IP of the sever and the password

        '''

        server_IP = "172.20.203.45"
        user = 'root'
        passwd = '3tango'

        # creating client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # connected with remote server
        ssh.connect(hostname=server_IP, username=user, password=passwd)
        return ssh

    def runCommand(self, cmd):
        '''
        @summary: run the commend in linux shell
        @param cmd: the commend 
        '''
        conn = self.connect()
        _, stdout, stderr = conn.exec_command(cmd)
        returncode = stdout.channel.recv_exit_status()
        result = stdout.read()
        return (returncode, result)

    def checkFile(self):
        '''
        @summary: check if the file in server
        '''
        try:
            rc, _ = self.runCommand("ls /tmp/employee4.txt")
            if rc == 0:
                print("the file here")

            else:
                self.runCommand(
                    'echo "id name CATEGORY salary" >> /tmp/employee4.txt')
                print("the file created")
        except Exception as e:
            print('Error: %s' % str(e))

    # insert the employee4 info to the file
    def addEmployee(self, id, name, category, salary):
        '''
        @summary: take the parametres and add it to the file
        @param id: integer unique value 
        @param name : name of employee
        @param Category:  the category of employee (engineer or manger)
        @param salary: integer number , how much the Employee Catching salary

        '''
        #
        try:

            rc, result = self.runCommand("cat /tmp/employee4.txt")
            results = result.split("\n")
        # check if the id in file
            # if the id in file
            for item in results:
                if str(id) in item:
                    print("this employee4 already added")
                    break

            else:
                new_line = str(id) + " " + name + " " + \
                    category + " " + str(salary)
                self.runCommand(
                    "echo {new_line} >> /tmp/employee4.txt".format(**locals()))
                print('done')

        except Exception as e:
            print('Error: %s' % str(e))

    # get all employee4 in the file

    def getAllEmployees(self, category=None):
        '''
        @summary: display the Employees which in file 
        @param category:  the category of employee (engineer or manger)
        '''

        try:
            if category is None:  # print all employee4
                _, result = self.runCommand("cat /tmp/employee4.txt")
                print(result)

            else:  # print specific employee4
                _, result = self.runCommand("cat /tmp/employee4.txt")
                results = result.split("\n")

                for item in results:
                    if category in item:
                        print(item)
                        break
                else:
                    print("Cannot find any {category}".format(**locals()))

        except Exception as e:
            print('Error: %s' % str(e))

    def getSalary(self, id):
        '''
        @summary: display the salary for specific id
        @param id: integer unique value 

        '''

        try:
            _, result = self.runCommand("cat /tmp/employee4.txt")
            results = result.split("\n")
            for item in results:
                if str(id) in item:
                    item = item.split(" ")
                    salaryis = int(item[3])
                    print("The salary is {salaryis}".format(**locals()))
                    break
            else:
                print("Cannot find any id = {id}".format(**locals()))

        except Exception as e:
            print('Error: %s' % str(e))

    # remove the manger with specific id
    def removeEmployee(self, id):
        '''
        @summary: remove specific id from the database
        @param id: integer unique value
        '''

        try:
            _, result = self.runCommand("cat /tmp/employee4.txt")
            results = result.split("\n")
            for item in results:
                if str(id) in item:
                    _, result_sel = self.runCommand(
                        "sed -i '/{item}/d' /tmp/employee4.txt".format(**locals()))
                    print("done")
                    break
            else:
                print("Cannot find any id = {id}".format(**locals()))

        except Exception as e:
            print('Error: %s' % str(e))
