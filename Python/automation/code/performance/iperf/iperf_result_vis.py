# Script to parse output from iperf3
# Command is "iperf3 -J -t 60 -O 10 -p <port> -c <IP Address>"
#   TODO: Decide if I should use subprocess and call commands from
#       Python or wrap this script in a bash script and do system 
#       calls from there

#imports
import json
import datetime
import matplotlib.pyplot as plt


def main(): 
    # Load json data from latest iperf test
    with open('iperf_test.json', 'r') as f:
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
    plt.xlabel("Seconds")
    plt.ylabel("Speed (Mbps)")
    plt.title(title)
    plt.savefig(f'iperf-results_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.png')
        
if __name__ == '__main__':
    # TODO: Command line arguments
    main()