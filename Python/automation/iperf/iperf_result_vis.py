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
    parser.add_argument('-f', '--file', help='Json file to save to. This will overwrite an existing file with the same name', required=True)
    
    # Optional arguments
    parser.add_argument('-P', '--parallel', help='Number of parallel client streams to run (Default=1)', default=1, required=False)
    parser.add_argument('-t', '--time', help='Duration of iperf3 speed test (Will automatically skip first 10 seconds) (Default=10s)', default=10, required=False)
    parser.add_argument('-m', '--minimum', help='Throughput speed in Mbps which will trigger the command (Default=100)', default=100, required=False)
    parser.add_argument('-c', '--command', help='''Command that will be run when throughput speed falls below the given minimum speed
                                                    Note: This will run any command without checks! Use with caution!''', default=None, required=False)
    parser.add_argument('--stop-on-error', help='Do not run command or visualize results if an error occurs with iperf3, usually early interrupt (Default=False)', default=False, required=False)
    
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
        print(f'Something went wrong: {str(e)}')

def main(args): 
    # Load json data from latest iperf test
    with open(args['file'], 'r') as f:
        data = json.load(f)
        
    # If error occured, json file will have an "error" key
    # Generate warning if continuing on error, else stop execution
    if 'error' in data:
        if not args['stop-on-error']:
            print(f"An error occured during iperf3 execution: {data['error']}\nContinuing...")
        else:
            raise Exception(f"An error occured during iperf3 execution: {data['error']}\nExiting...")

    # Start gathering data for line graph
    title = f'{data["start"]["connected"][0]["local_host"]} <-> {data["start"]["connected"][0]["remote_host"]}'

    # Gather speed @ each interval
    intervals = [i for i in range(1, len(speeds)+1)] # x-axis
    speeds = [] # y-axis
    speed_flag = False
    # speeds = [float(test["sum"]["bits_per_second"])/1000000 for test in data["intervals"]]
    for test in data["intervals"]:
        speed = float(test["sum"]["bits_per_second"]) / 1000000
        speeds.append(speed)
        # When this flag is true, we will run the given command after speed data is gathered 
        # and visualization graph is generated
        if args['command'] and speed < args['minimum']:
            speed_flag = True
    
    # Do this before running a command so that if command causes error, the graph will still generate
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