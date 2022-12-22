import subprocess

cpu_percent = subprocess.run(
    ['powershell', '-Command', 'Get-Process -Id ' + str(9272) + ' | Select-Object -Expand CPU'],
    capture_output=True
).stdout.decode().replace('\r\n', '')
print(cpu_percent)