import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def _load_df():
    df = pd.read_csv("internet_speeds_dataset.csv", index_col="Date")
    return df

def _create_figure(df, col_name, fig_num, title=None):
    plt.figure(fig_num)
    if title is not None:
        plt.title(title)
    else:
        plt.title(f"{col_name} over Time")
    plt.ylabel(col_name)
    df[col_name].plot()
    plt.xticks(rotation=90)
    plt.show(block=False)


def draw_graphs():
    df = _load_df()
    print(df.columns)
    _create_figure(df, "Download (Mb/s)", 1)
    _create_figure(df, "Upload (Mb/s)", 2)
    plt.show(block=True)


if __name__ == "__main__":
    draw_graphs()