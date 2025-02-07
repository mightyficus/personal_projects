# Script to parse output from iperf3

#imports
import json
import argparse
import datetime
import subprocess
import matplotlib.pyplot as plt

def getargs(): 
    parser = argparse.ArgumentParser(description='Visualize iperf3 performance and optionally run command if degradation found')
    
    parser.add_argument('-s','--server', help='IP of iperf3 server', required=True)
    parser.add_argument('-p', '--port', help='Port iperf3 is running on', required=True)
    parser.add_argument('-f', '--file', help='Json file to save to', required=True)
    
    # Optional arguments
    parser.add_argument('-P', '--parallel', help='Number of parallel client streams to run', default=1, required=False)
    parser.add_argument('-t', '--time', help='Duration of iperf3 speed test (Will automatically skip first 10 seconds). Default=10s', default=10, required=False)
    parser.add_argument('-m', '--minimum', help='Throughput speed which will trigger the command', default=100, required=False)
    parser.add_argument('-c', '--command', help='''Command that will be run when throughput speed falls below the given minimum speed
                                                    Note: This will run any command without checks! Use with caution!''', default=None, required=False)
    # There's no way this could go wrong...
    parser.add_argument('--privileged-mode', help='''Runs command in privileged mode
                                                    Note: DANGEROUS!! This will run any command with root privileges without checks!
                                                    Using this flag without care could result in serious damage to your system!''',
                                                    default=False, required=False)
    
    args = parser.parse_args()
    return args

def run_command(args):
    # Run iperf3
    # Command is "iperf3 -J -t 20 -O 10 -p <port> -c IP ADDRESS > OUTPUT FILE"
    try:
        subprocess.call('iperf3', '-J', '-t', str(int(args['time'])+10), '-O', '10', '-P', args['parallel'],'-p', args['port'], '-c', args['server'], '>', args['file'])
        
    except Exception as e:
        print('Something went wrong:')
        print(str(e))

def main(args): 
    # Load json data from latest iperf test
    with open('iperf_60s.json', 'r') as f:
        data = json.load(f)

    # Start gathering data for line graph
    title = f'{data["start"]["connected"][0]["local_host"]} <-> {data["start"]["connected"][0]["remote_host"]}'

    # Gather speed @ each interval
    speeds = [] # y-axis
    intervals = [] # x-axis
    i = 1
    for test in data["intervals"]:
        speeds.append(float(test["sum"]["bits_per_second"]) / 1000000)
        intervals.append(i)
        i += 1
    
    # Create the graph
    plt.plot(intervals, speeds)
    ax = plt.gca()
    ax.set_ylim(0,1200)
    plt.xlabel("Seconds")
    plt.ylabel("Speed (Mbps)")
    plt.title(title)
    plt.savefig(f'iperf-results_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.png')
        
if __name__ == '__main__':
    args = getargs()
    
    main(args)