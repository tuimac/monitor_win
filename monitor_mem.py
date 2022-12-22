import openpyxl
import datetime
import psutil
import traceback
import sys
import os
import json
import subprocess
import logging.config
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger

def load_config():
    global logger
    global config
    try:
        if len(sys.argv) != 2:
            print('Please set config.json path to the argument.', file=sys.stderr)
            os._exit(1)
        else:
            config_path = sys.argv[1]
            if os.path.exists(config_path) is False:
                print('config.json path is invalid.', file=sys.stderr)
                os._exit(1)
            else:
                with open(config_path, 'r', encoding='utf-8_sig') as f:
                    config = json.load(f)
    except:
        print(traceback.print_exc(), file=sys.stderr)
        os._exit(1)

    logging.config.dictConfig(config['log_config'])
    logger = getLogger('main')

def get_metricts(proc, data, timestamp):
    pinfo = { "timestamp":  timestamp}
    pinfo.update(proc.as_dict(attrs=config['metrics']))
    pinfo['memory'] = proc.memory_info().vms
    cpu_percent = subprocess.run(
        ['powershell', '-Command', 'Get-Process -Id ' + str(pinfo['pid']) + ' | Select-Object -Expand CPU'],
        capture_output=True
    ).stdout.decode().replace('\r\n', '')
    if cpu_percent == '':
        pinfo['cpu_percent'] = 0.0
    else:
        pinfo['cpu_percent'] = float(cpu_percent)
    data.append(pinfo)

def monitor_metrics():
    data = []
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with ThreadPoolExecutor(max_workers=config['max_thread']) as e:
        for proc in psutil.process_iter():
            e.submit(get_metricts, data, proc, timestamp)

    return data

def save_metrics(data):
    file_path = config['export_dir'] + '\\' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
    if os.path.exists(config['export_dir']) is False:
        os.mkdir(config['export_dir'])
    for metrics in data:
        with open(file_path, 'a') as f:
            json.dump(metrics, f)
            f.write('\n')

if __name__ == '__main__':
    load_config()
    try:
        data = monitor_metrics()
        save_metrics(data)
    except:
        traceback.print_exc()
        logger.error(traceback.print_exc())