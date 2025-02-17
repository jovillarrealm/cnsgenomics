import csv
import pandas as pd
import os
import matplotlib.pyplot as plt

dir_script = os.path.dirname(__file__) + "/"



def build_continent_map():
    with open(dir_script + "continentxcountry.csv", mode="r") as csvf:
        country_continent_reader = csv.reader(
            csvf,
        )
        country2continent = dict()
        for row in country_continent_reader:
            country2continent[row[1]] = row[0]
    return country2continent

country2continent = build_continent_map()

def reduce_hosts(value):
    if isinstance(value, float):
        return "UNKNOWN"
    if "soil" in value:
        return "soil"
    elif "rhizo" in value:
        return "soil"
    elif "anthropogenic environment" in value:
        return "soil"
    elif "industry" in value:
        return "soil"
    elif "island" in value:
        return "soil"
    elif "garden" in value:
        return "soil"
    elif "forest" in value:
        return "soil"
    elif "mining" in value:
        return "soil"
    elif "coast" in value:
        return "soil"
    elif "animal" in value:
        return "animal"
    elif "phyllo" in value:
        return "plant"
    elif "plant" in value:
        return "plant"
    elif "crop" in value:
        return "plant"
    elif "human" in value:
        return "human"
    elif "lichen" in value:
        return "lichen"
    elif "mangrove" in value:
        return "waters"
    elif "marine" in value:
        return "waters"
    elif "freshwater" in value:
        return "waters"
    elif "lagoon" in value:
        return "waters"
    elif "air" in value:
        return "air"
    elif "insect" in value:
        return "insect"
    else:
        msg = f"UNKNOWN: {value}"
        print(msg)
        return msg


df = pd.read_excel(
    dir_script + "20241128 Informacion filogeografica.xlsx",
    sheet_name="DATOS",
).dropna(subset=["Hospedador", "País"], how="all")

df["Continent"] = df["País"].map(lambda i: country2continent[i], na_action="ignore")
df["Host"] = df["Hospedador"].map(reduce_hosts, na_action="ignore")
df.to_csv(dir_script + "simple_Informacion_filogeografica.csv", index=False)
df["GCA"].to_csv(dir_script + "preferred_list.csv", index=False)

def plot_figs():
    plt.figure(figsize=(8, 9))  # Increase the size of the figure (width=8, height=6)
    continent_counts = df["Continent"].fillna("No data").value_counts()
    bars = plt.bar(continent_counts.index, continent_counts.values, color="darkblue")
    plt.xlabel("Continent")
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Count")
    plt.yscale("log")  # Set the y-axis to log scale

    # Annotate each bar with its count
    for bar in bars:
        yval = bar.get_height()  # Height of the bar
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x-coordinate: center of the bar
            yval + 0.1,  # y-coordinate: slightly above the top of the bar
            int(yval),  # Text to display
            ha="center",  # Horizontal alignment
            va="bottom",  # Vertical alignment
            fontsize=10,  # Font size
        )
    plt.savefig("continent.png")

    plt.clf()

    host_counts = df["Host"].fillna("No data").value_counts()
    bars = plt.bar(host_counts.index, host_counts.values, color="darkblue")
    plt.xlabel("Hosts")
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Count")
    plt.yscale("log")  # Set the y-axis to log scale
    for bar in bars:
        yval = bar.get_height()  # Height of the bar
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x-coordinate: center of the bar
            yval + 0.1,  # y-coordinate: slightly above the top of the bar
            int(yval),  # Text to display
            ha="center",  # Horizontal alignment
            va="bottom",  # Vertical alignment
            fontsize=10,  # Font size
        )
    plt.savefig("host.png")
    plt.clf()
