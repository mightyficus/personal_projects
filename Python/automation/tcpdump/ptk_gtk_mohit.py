import json
import logging
import argparse
import subprocess

IP = ''
USERNAME = ''
PASSWORD = ''

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    handler = logging.FileHandler('keys.log')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def get_args():
    global IP
    global USERNAME
    global PASSWORD

    parser = argparse.ArgumentParser(description=
                                        '''Get PTK for all clients and GTK for all VAPs''')

    parser.add_argument('-ip', '--ip',
        help="AP's IP address", required=True)
    parser.add_argument('-u', '--username', help="AP's SSH username", 
        required=True)
    parser.add_argument('-p', '--password', help="AP's SSH password", 
        required=True)        
                        
    args = parser.parse_args()
    
    IP = args.ip
    USERNAME = args.username
    PASSWORD = args.password
    
    return args

def run_cmd_on_AP(cmd):
    try:
        output = subprocess.run(f"sshpass -p {PASSWORD} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {USERNAME}@{IP} '{cmd}'", 
            shell=True, capture_output=True, text=True)

        return output.stdout
    except Exception as e:
        logging.warning(f"Failed to run {cmd} with error: {str(e)}")
        return ""

def get_inform():
    inform_str = run_cmd_on_AP('mca-dump')
    j = json.loads(inform_str)
    
    return j

def get_ptk_all_clients(inform):
    sta_ptk = {}
    vap_gtk = {}

    for vap in inform['vap_table']:
        interface = vap['name']
        gtk = run_cmd_on_AP(f"athkey -cfg80211 -i {interface} -g 2 ff:ff:ff:ff:ff:ff")
        vap_gtk[interface] = gtk
        logging.info(f"VAP {interface} (ESSID \'{vap['essid']}\', radio: {vap['radio']}) GTK:\n{gtk}")

        for sta in vap['sta_table']:
            sta_mac = sta['mac']
            ptk = run_cmd_on_AP(f"athkey -cfg80211 -i {interface} -g 1 {sta_mac}")
            logging.info(f"STA {sta_mac} PTK:\n{ptk}")
            sta_ptk[sta_mac] = ptk

    return sta_ptk, vap_gtk

if __name__ == '__main__':
    setup_logger()
    args = get_args()
    
    logging.info("Getting inform...")
    inform = get_inform()
    logging.debug(inform)

    logging.info("Getting GTK, PTK for all clients")
    sta_ptk, vap_gtk = get_ptk_all_clients(inform)