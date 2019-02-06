# mysql_copy_move_table
A python script to copy or move a table between different schema in a MySQL database.

To use this tool set the following values in the config file(config.ini):

- database hostname
- username
- password
- source schema name
- destination schema name(You may want to have a different destination table name)
- source table name
- destination table name
Set move_table=True if you want to move tables between schema(with move_table=False you will have a copy of source table in destination)
And set import_data=True if you want to copy/move data as well
