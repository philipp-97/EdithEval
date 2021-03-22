# Tool to evaluate csv-data from edith6
# (c) Philipp Dauer, 2021

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# parsing of arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "filename", help="e.g. Heimsprecher_in or Heimquintett", type=str)
parser.add_argument(
    "--maxvotes", help="maximum of votes per person", type=int, default=1)
parser.add_argument(
    "--name", help="name for column and for labels", type=str, default=" ")

args = parser.parse_args()

filename = args.filename
max_votes = args.maxvotes
name = args.name

# gender stuff
if name == " ":
    name = ""
    for char in filename:
        if char in ["_"]:
            name += "*"
        else:
            name += char

# load data
data = pd.read_csv(f"{filename}.csv", sep=";", encoding="latin_1")
raw_votes = pd.Series(data[name], dtype=str)
n_raw_votes = raw_votes.size

# select valid votes
votes = pd.Series(dtype=str)
for i, vote in enumerate(raw_votes):
    new_vote = vote.split(", ")
    if len(new_vote) > max_votes or new_vote == ["nan"]:
        new_vote = pd.Series(["Ungültig"], dtype=str)
    else:
        new_vote = pd.Series(new_vote, dtype=str)
    votes = votes.append(new_vote, ignore_index=True)
n_votes = votes.size

# evaluate canidates
canidates = votes.unique()
n_canidates = canidates.size


unsorted_votes = votes.copy()

# replace canidates by numers | unsorted canidates
# (-> correct this again in xticklabels) 
for i, canidate in enumerate(canidates):
    unsorted_votes.loc[unsorted_votes == canidate] = i

# sorting canidates
inv_sort = np.argsort(
    np.histogram(unsorted_votes.to_numpy(), bins=n_canidates)[0])
canidates = canidates[inv_sort[::-1]]

# replace canidates by numers | sorted canidates
# (-> correct this again in xticklabels)
for i, canidate in enumerate(canidates):
    votes.loc[votes == canidate] = i

# plot
fig = plt.figure(figsize=(n_canidates+1, 7))
ax = fig.gca()

votes.hist(
    ax=ax, align="mid", color="RoyalBlue", bins=3*n_canidates, xrot=90.0)

print((np.array([canidates, np.histogram(votes.to_numpy(), bins=n_canidates)[0]]).T))

ax.set_xticks(np.arange(n_canidates))
ax.set_xticklabels(canidates)
ax.set_xlim(-0.5, n_canidates-0.5)
ax.grid(ls=":", axis="y")
ax.grid(lw=0, axis="x")
ax.set_ylabel("Anzahl der Stimmen")
ax.set_title(f"{name}\nStimmen insgesamt {n_votes}, " \
    +f"Stimmzettel insgesamt {n_raw_votes}")
fig.tight_layout()

fig.savefig(f"{filename}.pdf")
