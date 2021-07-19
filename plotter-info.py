import PySimpleGUI as sg

#inputs
TOTAL_PLOTS=100
PLOTS_COMPLETED = 60
PLOTS_LEFT = 40

BAR_WIDTH = 300
GRAPH_SIZE = (300,TOTAL_PLOTS)
DATA_SIZE = (300,TOTAL_PLOTS)

graph = sg.Graph(GRAPH_SIZE, (0,0), DATA_SIZE)
layout = [[graph]]
window = sg.Window('Plots Completed', layout)
window.Finalize()


graph.DrawRectangle(top_left=(0, PLOTS_COMPLETED), bottom_right=(BAR_WIDTH, 0), fill_color='green')
graph.DrawRectangle(top_left=(0, PLOTS_COMPLETED + PLOTS_LEFT), bottom_right=(BAR_WIDTH, PLOTS_COMPLETED), fill_color='red')
graph.DrawText(text=PLOTS_LEFT, location=(BAR_WIDTH /2, PLOTS_COMPLETED + (PLOTS_LEFT /2)))
graph.DrawText(text=PLOTS_COMPLETED, location=(BAR_WIDTH / 2, PLOTS_COMPLETED/2))


while True:
    event, values = window.Read()
    graph.Erase()
    if event is None:
        break

window.Close()