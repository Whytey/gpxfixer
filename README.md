gpxfixer is a simple utility for fixing gpx files.

	usage: gpxfixer.py [-h] {strip,copy} ...

	optional arguments:
	  -h, --help    show this help message and exit

	commands:
	  available commands.

	  {strip,copy}  additional help

Currently, two commands are supported, 'strip':

	usage: gpxfixer.py strip [-h] [-s STARTTIME] [-e ENDTIME] [nodes]

	positional arguments:
	  nodes                 A list of nodes to be removed in a simple XPath format
		                (e.g. "trkpt" or "trkpt[@lat]"). Defaults to
		                ["trkpt[@lat]", "trkpt[@lon]"] to remove the location
		                data from a point.

	optional arguments:
	  -h, --help            show this help message and exit
	  -s STARTTIME		The timestamp to start stripping nodes from, in
		                ISO8601 format. Omit this argument to have no lower
		                bounds.
	  -e ENDTIME		The timestamp to finish stripping nodes from, in
		                ISO8601 format. Omit this argument to have no upper
		                bounds.

and 'copy':

	usage: gpxfixer.py copy [-h] [-s STARTTIME] [-e ENDTIME] file [node]

	positional arguments:
	  file                  The path to the GPX file to copy data from.
	  node                  The node to be copied in string format (e.g. "trkpt").
		                Note that all child elements will be copied also.

	optional arguments:
	  -h, --help            show this help message and exit
	  -s STARTTIME          The timestamp to start copying nodes from, in ISO8601
		                format. Omit this argument to have no lower bounds.
	  -e ENDTIME            The timestamp to finish copying nodes from, in ISO8601
		                format. Omit this argument to have no upper bounds.


Commands can be chained together to perform multiple actions on a file.

Examples:

1) To strip all location data from dirty.gpx:

	cat dirty.gpx | python gpxfixer.py strip 

2) To strip all elevation data from dirty.gpx:

	cat dirty.gpx | python gpxfixer.py strip "['ele']"

2) To strip location data from dirty.gpx from 'trkpt's recorded before 12:32.15pm on Jan 12, 2013:

	cat dirty.gpx | python gpxfixer.py strip -e 2013-01-12T12:30:15Z

3) To copy all 'trkpt' data from a clean GPX file named clean.gpx and merge it with dirty.gpx:

	cat dirty.gpx | python gpxfixer.py copy clean.gpx

4) To strip location data from dirty.gpx and copy 'trkpt' data from clean.gpx, all between 12:32.15pm and 12:45.00pm on Jan 12, 2013:

	cat dirty.gpx | python gpxfixer.py strip -s 2013-01-12T12:30:15Z -e 2013-01-12T12:45:00Z | python gpxfixer.py copy -s 2013-01-12T12:30:15Z -e 2013-01-12T12:45:00Z clean.gpx
