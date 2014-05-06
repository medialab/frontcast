##observer management commands
###how to guide

The observer management commands perform insert and update queries on the database.
CSV import is the standard python csv import from utf8 files.

To save the file into the right format, please `export as csv for windows`, then specify `utf8` as encoding.

For each management commands __two command line options__ must be in place:

options | value | sample
---|          
`--owner` | _django user username_ | daniele.guido
`--csv` | _relative path_ | contents/observator_xxx.csv.sample 

####fill_lessons.py
Please check the csv file provided as sample: `frontcast/contents/observator_fill_lessons.csv.sample `

	$ cd ~/Sites/frontcast
	$ workon frontcast
	$ python manage.py fill_lessons --owner=daniele.guido --csv=contents/observator_fill_lessons.csv.sample 