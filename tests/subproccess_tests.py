import subprocess


# if __name__ == '__main__':
proc = subprocess.Popen(['/bin/sh', '-l'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            bufsize=0)

proc.stdin.write('ls -la /\n')
output = proc.stdout.read(1000)
#while output and output.find('total') <> -1:
#    print output
print output

proc.stdin.write('help\n')
output = proc.stdout.read()
print output