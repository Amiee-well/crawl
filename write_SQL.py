import re,pymysql
class write_sql(object):
    def __init__(self,Data_information,label,files):
        self.Data_information = Data_information
        self.label,self.files = label,files
        try:
            self.connection()
        except:
            self.create_db()
            self.connection()
        self.table = Data_information['table']
        self.cursor = self.conn.cursor()
        self.insert()
    def connection(self):
        try:
            self.conn = pymysql.connect(
                host=(lambda x: x['host'] if 'host' in self.Data_information.keys() else "localhost")(self.Data_information),
                port=int((lambda x: x['port'] if 'port' in self.Data_information.keys() else "3306")(self.Data_information)),
                user=(lambda x: x['user'] if 'user' in self.Data_information.keys() else "root")(self.Data_information),
                password=self.Data_information['password'],
                database=self.Data_information['db'],
                charset="utf8"
            )
        except ValueError:
            self.create_db()
    def create(self):
        self.cursor.execute("show tables")
        tables = self.cursor.fetchall()
        tables_list = re.findall('(\'.*?\')',str(tables))
        tables_list = [re.sub("'",'',each)for each in tables_list]
        if self.table not in tables_list:
            try:
                sql = self.Statement()
                self.cursor.execute(sql)
                self.conn.commit()
            except:
                self.conn.rollback()
    def insert(self):
        self.create()
        try:
            for one_file in self.files:
                Insert = 'insert into {} values('.format(self.table)
                for title in one_file.keys():
                    type_label = self.label[title][1]
                    if type_label == str:
                        label = one_file[title][0]
                        Insert += '"{}",'.format(label)
                    elif type_label == int:
                        label = one_file[title][0]
                        Insert += '{},'.format(label)
                Insert = Insert[:-1]
                Insert += ');'
                self.cursor.execute('alter table {} convert to character set utf8mb4;'.format(self.table))
                self.cursor.execute(Insert)
                self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()
    def Statement(self):
        Statement1 = 'CREATE TABLE IF NOT EXISTS {}('.format(self.table)
        for title in self.label.keys():
            label = self.label[title][1]
            if label == str:
                Statement1 += '{} VARCHAR(255) NOT NULL,'.format(title)
            if label == int:
                Statement1 += '{} INT NOT NULL,'.format(title)
        Statement1 = Statement1[:-1]
        Statement1 += ')'
        return Statement1
    def create_db(self):
        import mysql.connector
        mydb = mysql.connector.connect(
            host=(lambda x: x['host'] if 'host' in self.Data_information.keys() else "localhost")(self.Data_information),
            port=int((lambda x: x['port'] if 'port' in self.Data_information.keys() else "3306")(self.Data_information)),
            user=(lambda x: x['user'] if 'user' in self.Data_information.keys() else "root")(self.Data_information),
            password=self.Data_information['password']
            )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE {}".format(self.Data_information['db']))
        self.connection()