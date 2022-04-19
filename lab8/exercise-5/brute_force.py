# https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
import subprocess

passlist = open("wordlists.txt","r").read().split("\n")[0:-1]
print(passlist[:6])

for passwd in passlist[:]:
    res = subprocess.run(["unrar",  "x",  "steg.rar", "-inul", f"-p{passwd}"])
    print(res)
    if(res.returncode != 3):
        print(res.returncode)
        print ("[+] Extracted Succesfully!")
        break