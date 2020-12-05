# Points Within Radius 

This program identify the point's location by given latitude and longitude and find the other points within a radius. 
The center point of the radius is the targeting point and searching points are from the other groups.

Last column of output file is the list of points within the radius and its distance to the targeting point. The list is sorted by distance in ascending order.

Points in the figure are color grouped according to group and scattered by respective latitude and longitude.
![Points distribution form corresponding lat long](/image/plot_points.jpg)

### I/O files
Both input and output file support `xlsx`/`xls`(Microsoft Excel) and `csv` format.
The I/O files follow certain schema as showing below:

**Input file schema**
| | group | site | lat | long |
|:--|:----|:-----|:----|:-----|
|1|A|A1|3.165662|101.648677|
|2|A|A2|3.151360|101.615948|
|3|B|B1|3.166728|101.648859|
|4|B|B2|3.164158|101.647359|
|5|C|C1|3.16623|101.652126|
|6|C|C2|3.171291|101.663865|

**Output file schema**

| | group	| site	| lat |	long |	site_latlong |	radius_limit |	nearest |
|:--|:----|:-----|:----|:-----|:-----|:----|:-----|
| 1	| A	| A1 |	3.165662 |	101.648677 |	('A1', (3.165662, 101.648677)) |	10	| [('B3', 0.1200574336676934), ('B1', 0.12024377681503264), ...] |
| 2	| A	| A2 |	3.15136	| 101.615948 |	('A2', (3.15136, 101.615948))	| 10	| [('B2', 3.766613581343238), ('B3', 4.012220413375427), ...] |
| 3 |	B |	B1	| 3.166728 |	101.648859 |	('B1', (3.166728, 101.648859))	| 10	| [('A1', 0.12024377681503264), ('C1', 0.36692181064398766), ...] |
| 4	| B	| B2	| 3.164158	| 101.647359	| ('B2', (3.164158, 101.647359))	| 10	| [('A1', 0.2222186860319872), ('C1', 0.577231206875848), ...] |
| 5	| C	| C1	| 3.16623	| 101.652126	| ('C1', (3.16623, 101.652126))	| 10 |	[('B4', 0.06333608770282707), ('B1', 0.36692181064398766), ...] |
| 6	| C	| C2	| 3.171291	| 101.663865	| ('C2', (3.171291, 101.663865)) |	10	| [('B5', 0.536483252995675), ('B4', 1.3593291044942635), ...] |


### Execution
**Arguments**
- `--input` Input file. xlsx/xls or csv
- `--output` Output file. xlsx/xls or csv
- `--within_radius` Radius constraint. unit in km

**Example**
```
python3 latlong_km.py --input input_file/latlong_data.xlsx --output output/result.xlsx --within_radius 10

```
