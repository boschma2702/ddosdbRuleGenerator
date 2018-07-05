with open('results-attacker.txt') as f:
    s = f.read()
    s = s.split("\n")
    new_s = ""
    for i in range(1, len(s)):
        if s[i].startswith("Times for: "):
            print(new_s)
            new_s = s[i].split("Times for: ")[1]
        else:
            new_s += " " + s[i]