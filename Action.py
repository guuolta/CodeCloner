import sys
from Analyzer import Analyzer as Analyzer
from Visualization.BoxPlot import BoxPloter as BoxPloter
import os

def main():
    engine_name = sys.argv[1]

    Analyzer.create_db(engine_name)

    project_names = Analyzer.get_project_names(engine_name)
    project_clone_rates = Analyzer.get_project_clone_rates(engine_name)

    BoxPloter.create_all_project_clone_rate_box_plot(engine_name, project_names, project_clone_rates)

    line_clone_rates = Analyzer.get_line_clone_rates(engine_name)
    file_clone_rates = Analyzer.get_file_clone_rates(engine_name)

    BoxPloter.create_total_project_clone_rate_box_plot(engine_name, line_clone_rates, file_clone_rates)

    print(Analyzer.calculate_line_clone_rate(engine_name))
    print(Analyzer.calculate_file_clone_rate(engine_name))

main()