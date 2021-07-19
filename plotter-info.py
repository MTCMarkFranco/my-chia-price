import PySimpleGUI as sg
import shutil as sh
import math
import sys
import os

# Help
if len(sys.argv) == 1:
    print("*********************************************************")
    print("Supply only your destination hard drive path to monitor\n")
    print("example #1: python run-plotter.py /mnt/WD-8TB-1")
    print("example #2: python run-plotter.py c:\\")
    print("*********************************************************")
    quit()

# Inputs
PLOT_DRIVE = sys.argv[1];

# Initialize DISK Variables
total, used, free = sh.disk_usage(PLOT_DRIVE)
DISK_TOTAL_GB = total // (2**30)
DISK_FREE_GB = free // (2**30)
DISK_FREE_GB_PERCENTAGE = (DISK_FREE_GB / DISK_TOTAL_GB) * 100
DISK_USED_GB = used // (2**30)
DISK_USED_GB_PERCENTAGE = (DISK_USED_GB / DISK_TOTAL_GB) * 100

# Initialize PLOT Variables
TOTAL_PLOTS = math.floor(DISK_TOTAL_GB / 110)
PLOTS_COMPLETED = 0

for base, dirs, files in os.walk(PLOT_DRIVE):
    for Files in files:
        if Files.lower().endswith(".plot"):
            PLOTS_COMPLETED += 1

PLOTS_LEFT = TOTAL_PLOTS - PLOTS_COMPLETED
PLOTS_LEFT_PERCENTAGE = (PLOTS_LEFT / TOTAL_PLOTS ) * 100
PLOTS_COMPLETED_PERCENTAGE = (PLOTS_COMPLETED / TOTAL_PLOTS) * 100

# Message Construction
MSG_PLOTS_LEFT = "[Plots] left: %d " % PLOTS_LEFT
MSG_PLOTS_COMPLETE = "[Plots] Completed: %d " % PLOTS_COMPLETED

MSG_DISK_FREE = "[Hard Drive] Free space: %dGB" % DISK_FREE_GB
MSG_DISK_USED = "[Hard Drive] Used space: %dGB" % DISK_USED_GB

# Constants
BAR_WIDTH = 300
GRAPH_DISKS_LEFT = BAR_WIDTH + 5
GRAPH_SIZE = (300,100)
PLOT_DATA_SIZE = (300,100)
DISK_DATA_SIZE = (300,100)

# Window & Graph Setup
graph_plots = sg.Graph(GRAPH_SIZE, (0,0), PLOT_DATA_SIZE)
graph_disk = sg.Graph(GRAPH_SIZE, (0,0), DISK_DATA_SIZE)
layout = [[graph_plots],[graph_disk]]
window = sg.Window('Plotting Metrics', layout)
window.Finalize()

# Setup Plots Graph
graph_plots.DrawRectangle(top_left=(0, PLOTS_COMPLETED_PERCENTAGE), bottom_right=(BAR_WIDTH, 0), fill_color='green')
graph_plots.DrawRectangle(top_left=(0, PLOTS_COMPLETED_PERCENTAGE + PLOTS_LEFT_PERCENTAGE), bottom_right=(BAR_WIDTH, PLOTS_COMPLETED_PERCENTAGE), fill_color='yellow')
if PLOTS_COMPLETED_PERCENTAGE < 100.0:
    graph_plots.DrawText(text=MSG_PLOTS_LEFT, location=(BAR_WIDTH /2, PLOTS_COMPLETED_PERCENTAGE + (PLOTS_LEFT_PERCENTAGE /2)))
graph_plots.DrawText(text=MSG_PLOTS_COMPLETE, location=(BAR_WIDTH / 2, PLOTS_COMPLETED_PERCENTAGE/2))

# Setup Disk Graph
graph_disk.DrawRectangle(top_left=(0, DISK_USED_GB_PERCENTAGE), bottom_right=(BAR_WIDTH, 0), fill_color='green')
graph_disk.DrawRectangle(top_left=(0, DISK_USED_GB_PERCENTAGE + DISK_FREE_GB_PERCENTAGE), bottom_right=(BAR_WIDTH, DISK_USED_GB_PERCENTAGE), fill_color='yellow')
if DISK_FREE_GB_PERCENTAGE != 0:
    graph_disk.DrawText(text=MSG_DISK_FREE, location=(BAR_WIDTH /2, DISK_USED_GB_PERCENTAGE + (DISK_FREE_GB_PERCENTAGE /2)))
graph_disk.DrawText(text=MSG_DISK_USED, location=(BAR_WIDTH / 2, DISK_USED_GB_PERCENTAGE/2))


while True:
    event, values = window.Read()
    graph_plots.Erase()
    graph_disk.Erase()
    if event is None:
        break

window.Close()