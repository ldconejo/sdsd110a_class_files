import subprocess

p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "py"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()

output, _ = p2.communicate()
print(output.decode())