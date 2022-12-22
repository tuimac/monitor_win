import psutil
import datetime
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def get_metricts(data, proc):
    pinfo = dict()
    pinfo.update(proc.as_dict(attrs=["name", "pid"]))
    cpu_percent = subprocess.run(
        ['powershell', '-Command', 'Get-Process -Id ' + str(pinfo['pid']) + ' | Select-Object -Expand CPU'],
        capture_output=True
    ).stdout.decode().replace('\r\n', '')
    if cpu_percent == '':
        pinfo['cpu_ps'] = 0.0
    else:
        pinfo['cpu_ps'] = float(cpu_percent)

    pinfo['cpu_psutil'] = round(proc.cpu_percent(interval=1) / psutil.cpu_percent(interval=1) * 100, 5)
    data.append(pinfo)

def monitor():
    data = []

    with ThreadPoolExecutor(max_workers=50) as e:
        for proc in psutil.process_iter():
            e.submit(get_metricts, data, proc)

    '''
    for proc in psutil.process_iter():
        process = multiprocessing.Process(target=get_metricts, args=(data, proc, ))
        process.start()
    '''

    for metrics in data:
        print(metrics)

if __name__ == '__main__':
    monitor()