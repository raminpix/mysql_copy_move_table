import sys
import pymysql
import configparser

print("MySQL Copy Move Table Tool - v1.0.0 - 2019-02-06.r1")

try:
    config = configparser.ConfigParser()
    config_file_name = "config.ini"
    config.read(config_file_name)
    src_schema_name=config["DB"]["src_schema"]
    dest_schema_name=config["DB"]["dest_schema"]

    src_table_name = "`" + config["DB"]["src_table"] + "`"
    src_table_full_name = "`" + config["DB"]["src_schema"] + "`.`" + config["DB"]["src_table"] + "`"

    dest_table_name = "`" + config["DB"]["dest_table"] + "`"
    dest_table_full_name = "`" + config["DB"]["dest_schema"] + "`.`" + config["DB"]["dest_table"] + "`"
except:
    print("Error reading file " + config_file_name)    
    sys.exit(1)
    
try:
    mydb = pymysql.connect(host=config["DB"]["host"], user=config["DB"]["user"], passwd=config["DB"]["passwd"])    
    mycursor = mydb.cursor()
except:
    print("Error connecting database")
    sys.exit(1)
    
print("Connected to " + config["DB"]["host"])    

operation = "Copying"
import_data_msg = ""
if config["DB"]["move_table"] == "True":
    operation = "Moving"
if config["DB"]["import_data"] == "True":
    import_data_msg = "with data"
print(operation + " " + src_table_full_name + " to " + dest_table_full_name + " " + import_data_msg)

try:
    mycursor.execute("SHOW CREATE TABLE " + src_table_full_name)

    myresult = mycursor.fetchone()
    create_table_sql = myresult[1].replace(src_table_name, dest_table_name,1)
    mydb.select_db(dest_schema_name)
    dest_table_remove = "DROP TABLE IF EXISTS "+ dest_table_full_name +";"
    mycursor.execute(dest_table_remove)
    mycursor.execute(create_table_sql)

    if config["DB"]["import_data"] == "True":
        sql = "insert into "+ dest_table_full_name +" select * from "+ src_table_full_name + ";"
        mycursor.execute(sql)    

    if config["DB"]["move_table"] == "True":
        sql = "DROP TABLE IF EXISTS "+ src_table_full_name +";"
        mycursor.execute(sql)

    mydb.commit()
except:
    print("Error moving tables")
    sys.exit(1)

sys.exit(0)
