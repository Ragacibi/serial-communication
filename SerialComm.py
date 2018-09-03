"""This module is used to automate serial communication
"""
import serial, time

class SerialComm(object):
    """Class SerialComm
    """

    def __init__(self, **kwargs):
        """Used to initialize serial communication parameters and to open serial port
        """
        try:
            self.console = serial.Serial(**kwargs)
            self.console.write('\n')
        except OSError as msg:
            raise Exception(('Unable to open port {}: {}. ').format(port, msg))

    def read_out(self):
        """Used to read from serial, returns the output as raw string
        """
        size = self.console.inWaiting()
        if size:
            data = self.console.read(size)
            return data
        return ''

    def login_status(self):
        """Used to verify login status
        """
        self.console.write('\n')
        time.sleep(1)
        data = self.read_out()
        prompts = ('#', '$')
        return any((x in data for x in prompts))

    def login(self, username, passwd):
        """Used to login with credentials provided
        """
        username = username.encode()
        passwd = passwd.encode()
        status = self.login_status()
        if status:
            return True
        while True:
            self.console.write('\n')
            time.sleep(1)
            data = self.read_out()
            if 'login:' not in data:
                print 'no_login_prompt'
                continue
            self.console.write(username + '\n')
            time.sleep(2)
            data = self.read_out()
            if 'Password:' not in data:
                print 'no_passwd_prompt'
                continue
            self.console.write(passwd + '\n')
            time.sleep(2)
            status = self.login_status()
            if status:
                return True

    def sendline(self, cmd):
        """Used to send commands to the device which returns the output as string
        """
        cmd = cmd.encode()
        status = self.login_status()
        if status:
            self.console.write(cmd + '\n')
            time.sleep(1)
            data = self.read_out()
            return data
        raise Exception(('Unable to Execute command {}').format(cmd))

    def logout(self, out_cmd='exit'):
        """Used to log out
        """
        status = self.login_status()
        if status:
            self.console.write(out_cmd + '\r\n')
        else:
            raise Exception(('Unable to logout with command {}. Check login status').format(out_cmd))

    def __del__(self):
        try:
            self.console.close()
        except:
            pass
