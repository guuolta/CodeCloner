import matplotlib.pyplot as plt
import Visualization.BoxPlot.BoxPlotData as BoxPlotData
import Visualization.CommonVisualization as CommonVisualization

def create_all_project_clone_rate_box_plot(engine_name, project_names, clone_rates):
    '''  プロジェクトごとのファイル内クローン率の箱ひげ図を作成 '''

    figure = _get_box_plot(BoxPlotData.ALL_PROJECT_CLONE_RATE_TITLE, clone_rates, project_names)

    # 箱ひげ図を保存
    CommonVisualization.save_figure(BoxPlotData.get_save_path(engine_name), BoxPlotData.ALL_PROJECT_CLONE_RATE_FILE_NAME, figure)

def create_total_project_clone_rate_box_plot(engine_name, line_clone_rate_datasets, file_clone_rate_datasets):
    '''  全プロジェクトのクローン率の箱ひげ図を作成 '''

    figure = _get_box_plot(BoxPlotData.TOTAL_CLONE_RATE_TITLE,
        [line_clone_rate_datasets, file_clone_rate_datasets],
        [BoxPlotData.TOTAL_LINE_CLONE_RATE_LABEL, BoxPlotData.TOTAL_FILE_CLONE_RATE_LABEL])

    # 箱ひげ図を保存
    CommonVisualization.save_figure(BoxPlotData.get_save_path(engine_name), BoxPlotData.TOTAL_CLONE_RATE_FILE_NAME, figure)

def _get_box_plot(title, datasets, x_labels):
    '''  箱ひげ図を取得 '''

    plt.figure(figsize=(BoxPlotData.FIGURE_WIDTH, BoxPlotData.FIGURE_HEIGHT))
    plt.title(title)
    plt.grid()

    plt.boxplot(datasets, labels=x_labels)
    plt.xticks(rotation=90)
    plt.ylabel(BoxPlotData.Y_LABEL)

    plt.tight_layout()
    return plt.gcf()