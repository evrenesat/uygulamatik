import subprocess as sp


def sh(cmd):
    k=sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
    error=k.stderr.read()
    output=k.stdout.read().strip()
    if error:
        output= error + output
    k.wait()
    return not error, (output or 'OK')
