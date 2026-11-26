import time
import networkx as nx
import GraphBuilder as gb
from problems.none import No_reds_shortespath as nr

def GetTime():
    return time.perf_counter_ns()

def PrintFormattedTime(problem, input, algorithm, elapsed_time):
    print(
        f"Problem: {problem} | Input file: {input}" 
        f" | Algorithm: {algorithm} | Time: {elapsed_time}ns"
    )
        
