#!/usr/bin/python3
"""This module features functions and classes to manipulate data for the
collaborative filtering algorithm.
"""

# Importing necessary modules
from pathlib import Path
import scipy
import pandas as pd


def load_user_artists(user_artists_file: Path) -> scipy.sparse.csr_matrix:
    """Load the user artists file and return a user-artists matrix in csr
    fromat

     Args:
        user_artists_file (Path): The file path to the user-artists data file.

    Returns:
        scipy.sparse.csr_matrix: A sparse matrix representation (CSR) of the
        user-artist data.
    """
    # Load the user-artist interaction data into a Pandas DataFrame
    user_artists = pd.read_csv(user_artists_file, sep="\t")

    # Set the DataFrame's index to a multi-index with userID and artistID
    user_artists.set_index(["userID", "artistID"], inplace=True)

    # Create a sparse matrix
    coo = scipy.sparse.coo_matrix(
        (
            user_artists.weight.astype(float),
            (
                user_artists.index.get_level_values(0),
                user_artists.index.get_level_values(1),
            ),
        )
    )
    return coo.tocsr()


class ArtistRetriever:
    """The ArtistRetriever class gets the artist name from the artist ID."""

    def __init__(self):
        self._artists_df = None

    def get_artist_name_from_id(self, artist_id: int) -> str:
        """Return the artist name from the artist ID."""
        return self._artists_df.loc[artist_id, "name"]

    def load_artists(self, artists_file: Path) -> None:
        """Load the artists file and stores it as a Pandas dataframe in a
        private attribute.
        """

        # Load the artist data from the provided file into a Pandas DataFrame
        artists_df = pd.read_csv(artists_file, sep="\t")
        artists_df = artists_df.set_index("id")
        self._artists_df = artists_df

# Main block to test the functionality of the ArtistRetriever class
if __name__ == "__main__":
    # user_artists_matrix = load_user_artists(
    #     Path("lastfmdata/user_artists.dat")
    # )
    # print(user_artists_matrix)

    artist_retriever = ArtistRetriever()
    artist_retriever.load_artists(Path("lastfmdata/artists.dat"))
    artist = artist_retriever.get_artist_name_from_id(1)
    print(artist)   # This should print the artist's name corresponding to ID 1
