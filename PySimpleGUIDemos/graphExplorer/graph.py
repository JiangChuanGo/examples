import PySimpleGUI as sg
from collections import  namedtuple

XYCoord = namedtuple("XYCoord", ["x", "y"])

graph_size = XYCoord(500, 500)

layout = [
    [sg.Graph(canvas_size=graph_size, graph_bottom_left=(0, graph_size.y), graph_top_right=(graph_size.x, 0), background_color="white", key = "-GRAPH-", drag_submits=True, enable_events = True)],
    [sg.OK(), sg.Cancel()]
]


window = sg.Window("Graph", layout = layout, finalize=True)

graph = window["-GRAPH-"]

cat_figure = graph.draw_image(filename="./cat.png", location=(0,0))

on_drag = False

event_count = 0

while True:
    event, values = window.read(timeout = 500, timeout_key = "-TIMEOUT-")

    if event == "-TIMEOUT-":
        continue

    if event in (sg.WIN_CLOSED, "Cancel", "Quit"):
        break

    print(event, values)

    if event == "-GRAPH-":
        x, y = values[event]
        new_zero_point = XYCoord(x, y)
        
        if on_drag:
            print(f"movement: {x}, {y}")

            # sometimes, the movement sniffer erro, fix it
            if abs(x) + abs(y) > 200:
                continue
            graph.relocate_figure(cat_figure, x + cat_fix.x, y + cat_fix.y)

        else:
            on_drag = True

            new_zero_point = XYCoord(x, y)
            graph.change_coordinates((-new_zero_point.x, graph_size.y - new_zero_point.y), (graph_size.x - new_zero_point.x, -new_zero_point.y))
            cat_location = graph.get_bounding_box(cat_figure)
            cat_fix = XYCoord(*cat_location[0])

        continue

    if event == "-GRAPH-+UP":
        on_drag = False
            
        graph.change_coordinates((0, graph_size.y), (graph_size.x, 0))
        print("coordinate reset.")

window.close()
del window

