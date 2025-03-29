#!/usr/bin/python3
import sys
import subprocess
import os
import os.path
import string
import time
import csv


# Number of iterations (+1) (set lower for CAV19-AE)
maxiterations = 3

logfile = "lit-log-file-benchmarks-corrupt.txt"

# OUTPUT FILE
prefname = "lit-benchmarks-corrupt"

# TIMEOUT (in seconds)
cmdtimeout = 5 #

fsmfiles = []
for filename in os.listdir("tests/corruptbenchmarks"):
    if filename.endswith(".txt"):
        fsmfiles.append("tests/corruptbenchmarks/" + filename)
    
"""fsmfiles = [  "tests/benchmarks/client-server-logger.txt" # (1) Client-Server-Logger
            #, "tests/benchmarks/gmc-runningexample" # (2) 4 Player Game
            , "tests/benchmarks/Bargain.txt" # (3) Bargain
            , "tests/benchmarks/FilterCollaboration.txt" # (4) Filter Collaboration
            , "tests/benchmarks/AlternatingBit.txt" # (5) Alternating Bit
            , "tests/benchmarks/TPMContract.txt" # (6) TPMContract v2
            , "tests/benchmarks/SanitaryAgency.txt" # (7) Sanitary Agency
            , "tests/benchmarks/Logistic.txt" # (8) Logistic
            , "tests/benchmarks/CloudSystemV4.txt" # (9) Cloud System v4
            , "tests/benchmarks/commit-protocol.txt"# (10) Commit Protocol
            , "tests/benchmarks/elevator-extra.txt" # (11) Elevator
            , "tests/benchmarks/elevator-extra-variant.txt" # (12) Elevator-dashed
            , "tests/benchmarks/elevator-csa.txt" # (13) Elevator-directed
            , "tests/benchmarks/devsystem-fsm.txt" # (14) Dev system
]"""


"""dotfiles = [  "tests/Protocols/Fibonacci/fibo.txt" # (15) Fibonacci
            , "tests/Protocols/SAP-Negotiation/negotiate.txt" # (16) SAP-Nego
            , "tests/Protocols/SH/sh.txt" # (17) SH
            , "tests/Protocols/TravelAgency/travelagency.txt" # (18) Travel agency
            , "tests/Protocols/SMTP/smtp.txt" # (19) SMTP
            , "tests/Protocols/HTTP/http.txt"  # (20) HTTP
]"""


def cleanup(): 
    subprocess.call(["killall","KMC"]
                    , stdout=subprocess.PIPE
                    , stderr=subprocess.PIPE)


def runOverRange(name, filelist, filetype):
    with open(name,"a") as out:    
        write = csv.writer(out)
        with open(name+logfile, "ab") as log_file:
            for ex in filelist:
                timings = []
                nstates = ""
                ntrans = ""
                for it in range(1,maxiterations):
                    print("Running k-MC: ",ex)
                    startt = time.time() # time in seconds
                    #
                    #
                    try:
                        kmccmd = subprocess.run(["cabal", "run", "KMC", "--",ex,str(it),filetype,], capture_output=True, text=True, check=True,timeout=cmdtimeout) #stdout=subprocess.PIPE
                        #kmccmd.wait(timeout=cmdtimeout)
                        endt = time.time()
                        txt = "Measured execution time: "+str(endt-startt)
                        print(txt)
                        #write.writerow([ex, kmccmd.stdout.strip()])
                        write.writerow([ex, ', '.join(kmccmd.stdout.strip().splitlines())])
                        print(f"Processed {ex}")

                    except subprocess.TimeoutExpired:
                    #    kmccmd.kill()
                    #    kmccmd.wait()
                        write.writerow([ex, ', '.join(kmccmd.stdout.strip().splitlines())])
                        write.writerow([ex, "Timeout"])
                        print("KMC timedout")
                        
                    except subprocess.CalledProcessError as e:
                        write.writerow([ex, e.stderr.strip()])
                        print(f"Error processing {ex}")

                        """for line in kmccmd.stdout:
                            print(line)
                            line = str(line)
                            #sp = line.decode("utf-8").split("*")
                            sp = line.split("*")
                            if len(sp) > 4:
                                nstates = sp[1]
                                ntrans = sp[3]
                                log_file.write(line)
                        log_file.write((txt+"\n").encode())
                        timings.append(endt-startt)
                    except subprocess.TimeoutExpired:
                        kmccmd.kill()
                        kmccmd.wait()
                        print("KMC timedout")
                        return
                avg = sum(timings)/float(len(timings))
                write.writerow([ex,nstates,ntrans,avg]+timings)
    print("Saved in: ", name)   """                     


outputfile = "benchmarks-fromlit-corrupt.csv"

runOverRange(outputfile, fsmfiles, "--fsm")
#runOverRange(outputfile, dotfiles, "--scm")
