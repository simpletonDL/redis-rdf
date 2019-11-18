import paramiko


class SSH:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.kwargs = kwargs

    def __enter__(self):
        '''Как написать код для подключения к удаленному хосту с импрортируемым модулем paramiko'''
        kw = self.kwargs
        self.client.connect(hostname=kw.get('hostname'), username=kw.get('username'),
                            password=kw.get('password'), port=int(kw.get('port', 22)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def exec_cmd(self, cmd):
        ''' Необходимо выполнить команду с помощью скрипта (к прим. ls -al)'''
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        if stderr:
            raise stderr
        return data.decode()


if __name__ == '__main__':
    with SSH(hostname='vs-...', username='lo...', password='l...', port=22) as ssh:  # noob@10.0.1.**
        out = ssh.exec_cmd('ls -l')
        print(out)
        print(out, file=open('log.log', 'a'))  # и записью вывода в лог