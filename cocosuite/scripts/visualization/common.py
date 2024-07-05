from typing import Dict, List, Optional, Tuple

from matplotlib import pyplot as plt


def plot_bar_chart(
    data: Dict,
    x_label: str,
    y_label: str,
    title: str,
    rotation: int = 45,
    figsize: Tuple = (20, 10),
) -> None:
    """Plot a bar chart.

    Args:
        data (Dict): Data to plot.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        title (str): Title of the plot.
        rotation (int, optional): Rotation of the x-axis labels. Defaults to 45.
        figsize (Tuple, optional): Size of the figure. Defaults to (20, 10).
    """
    plt.figure(figsize=figsize)
    plt.bar(data.keys(), data.values())
    plt.xticks(rotation=rotation)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_scatter_chart(
    x_data: List,
    y_data: List,
    labels: List,
    x_label: str,
    y_label: str,
    title: str,
    legend_title: Optional[str] = None,
    figsize: Tuple = (20, 10),
) -> None:
    """Plot a scatter chart.

    Args:
        x_data (List): Data for the x-axis.
        y_data (List): Data for the y-axis.
        labels (List): Labels for each data point.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        title (str): Title of the plot.
        legend_title (str, optional): Title of the legend. Defaults to None.
        figsize (Tuple, optional): Size of the figure. Defaults to (20, 10).
    """
    unique_categories = List(set(labels))
    plt.figure(figsize=figsize)

    for category in unique_categories:
        idx = [i for i, label in enumerate(labels) if label == category]
        x_values = [x_data[i] for i in idx]
        y_values = [y_data[i] for i in idx]
        plt.scatter(x_values, y_values, label=category)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if legend_title:
        plt.legend(title=legend_title, loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()
