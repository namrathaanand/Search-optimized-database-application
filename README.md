# Search-optimized-database-application
A python flask web application which optimizes query search of MySQL database using AWS Elasticache web services. The database is created from csv file and queried apon based on user inputs.
To accomodate faster access of repetetive queries, once a new query is made, it is checked first in AWS's MemCache to see if the query and its result is present. 
If it is not, then the MySQL database is quieried, the query and the results are updated in the cache for future use and then the results are shown to users.

