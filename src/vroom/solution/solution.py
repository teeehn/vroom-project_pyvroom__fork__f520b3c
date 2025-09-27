from typing import Any, Dict
import json

import numpy
import pandas

from .. import _vroom

NA_SUBSTITUTE = 4293967297


class Solution(_vroom.Solution):

    @property
    def routes(self) -> pandas.DataFrame:
        array = numpy.asarray(self._routes_numpy())
        frame = pandas.DataFrame({
            "vehicle_id": array["vehicle_id"],
            "type": pandas.Categorical(
                array["type"].astype("U9"),
                categories=["start", "end", "break", "job", "delivery", "pickup"],
            ),
            "arrival": array["arrival"],
            "duration": array["duration"],
            "setup": array["setup"],
            "service": array["service"],
            "waiting_time": array["waiting_time"],
            "location_index": array["location_index"],
            "longitude": pandas.array(array["longitude"], dtype="Int64"),
            "latitude": pandas.array(array["latitude"], dtype="Int64"),
            "id": pandas.array(array["id"], dtype="Int64"),
            "description": array["description"].astype("U40"),
        })
        for column in ["longitude", "latitude", "id"]:
            if (frame[column] == NA_SUBSTITUTE).all():
                del frame[column]
            else:
                frame.loc[frame[column] == NA_SUBSTITUTE, column] = pandas.NA
        return frame

    def to_dict(self, geometry: bool = False) -> Dict[str, Any]:
        """
        Returns the solution as a dictionary.

        Args:
            geometry: Flag whether to include route geometry in the dictionary.

        Returns:
            The solution as a dictionary.
        """
        return json.loads(self._to_json(geometry))

    def to_json(self, filename: str, geometry: bool = False):
        """
        Dumps the solution to a JSON file.

        Args:
            filename: Path to the output file.
            geometry: Flag whether to include route geometry in the file.
        """
        with open(filename, "w") as f:
            f.write(self._to_json(geometry))
