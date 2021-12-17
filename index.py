# For the Process and Time
import psutil;
import datetime;

# For the pop-up
import tkinter as tk;
from tkinter import ttk;


# List Processes what you want watch
# P.S.: Only watch one process by time
PROCESSNAME = ['LeagueClient', 'Discord'];
ACTIVEPROCESS = None;

# Times for limit
HOURS = 2;
MINUTES = 30;
SECONDS = 0;

# Warning popup in minutes before the time limit
WARNINGTIME = 1;
# Auto close the pop after the time (in milliseconds)
CLOSETIME = 180000;

# Fonts for pop-up
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


#  Check if a process is running
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True;
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

# Find PID (Process ID) of a running process by Name
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = [];
    # Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;

# Find PIDs od all the running instances of process that contains one of the process in array in it's name
def findPid():
    listOfProcessIds = findProcessIdByName(ACTIVEPROCESS);
    if len(listOfProcessIds) > 0:
        return listOfProcessIds;

# Finish the process
def killProcess():
    for proc in psutil.process_iter():
        # Check whether the process name matches
        if proc.name().lower() == ACTIVEPROCESS.lower():
            proc.kill();

# Check if any process was running or not.
def isRunning():
    for process in PROCESSNAME:
        if checkIfProcessRunning(process):
            global ACTIVEPROCESS;
            ACTIVEPROCESS = process;
            return True;

    return False;


def popUpMsg():
    popup = tk.Tk();
    popup.wm_title('Warning');

    label = ttk.Label(popup, text='No máximo mais ' + str(WARNINGTIME) + 'min. de gameplay.', font=LARGE_FONT);
    label.pack(side="top", fill="x", pady=15, padx=10);
    B1 = tk.Button(popup, text="Okay", bg='#FF8C1A', activebackground='#FF8C1A', command = popup.destroy, pady=5);
    B1.pack();

    popup.after(CLOSETIME, lambda: popup.destroy());
    popup.mainloop();
    

def main():
    timeLimit = datetime.timedelta(hours=HOURS, minutes=MINUTES, seconds=SECONDS);
    timeWarning = datetime.timedelta(minutes=WARNINGTIME);
    
    warned = False;

    while(isRunning()):
        currentTime = datetime.datetime.now();
        
        processes = findPid(); 
        for elem in processes:
            processCreateTime = datetime.datetime.fromtimestamp(elem['create_time']);
            timeInterval = currentTime - processCreateTime;

        if not warned and (timeInterval + timeWarning) >= timeLimit:
            popUpMsg();
            warned = True;

        if timeInterval >= timeLimit:
            timeFinished = datetime.datetime.strftime(currentTime, '%Y-%m-%d %H:%M:%S');
            killProcess();
            print(timeFinished + ' - ' + ACTIVEPROCESS.upper() + ' KILLED');
            print('Time the process was active: ' + str(timeInterval) + '\n');
            main();

    main();

if __name__ == '__main__':
    main()