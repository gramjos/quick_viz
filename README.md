## Quick Viz 


### Which counties in Illinois have a population greater than 60,000

| Files              | Purpose                            | Lines of Code  |
| -------------   |:-------------:                       | -----:         |
| `getData.sh `   | contrust API call, raw *curl* call   | 8              |
| `Cleaning.py `  | change data types, *join* databases  |   25           |
| `viz.py`        |  interactive choropleth population   |    59          |
| `conda_list_export.txt`        |  environment set up   |    200          |

```shell
$ ./driver.sh
./getData.sh  0.02s user 0.01s system 3% cpu 0.955 total
./Cleaning.py  1.04s user 0.17s system 172% cpu 0.698 total
./viz.py  2.26s user 0.40s system 89% cpu 2.977 total
```
# TODO 
    - Remove top 1..n outliers for a given range. Get user input to specify n. As of now the viz not meaningful (for index.html)
    - for the outlier exlcuded map show a floating histogram and a bar chart of the excluded top N as well bar chart columns for the max, mean, median, and min of the chorepleth data (in the top N bar chart as well)
    - data more data fields

