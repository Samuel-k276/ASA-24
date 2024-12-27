import subprocess

def generate_tests(n, m, l, b, path):
    with open(path, 'w') as outfile:
        subprocess.run(
            ['./gera', str(n), str(m), str(l), str(b)],  # Arguments for the executable
            stdout=outfile,  # Redirect the output to the file
            stderr=subprocess.PIPE,  # Capture errors (if necessary)
            text=True  # Treat the data as text
        )

x = 0
for i in range(0, 10):
    n = 150000+20000*i
    for j in range(0, 5):
        m = n*2 + 50000*j
        for k in range(0, 5):
            l = 100 + 30*(k+1)
            generate_tests(n, m, l, 1, f"tests/test_{x:03d}.in")
            x += 1
            print(x)





