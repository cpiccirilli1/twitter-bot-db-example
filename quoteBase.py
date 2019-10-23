import sqlite3 as lite
from random import randint


class QuoteBase:

    def __init__(self, db):
        self.db = db

    def connection(self):
        """
        creates connection and cursor
        :return: connection, cursor
        """
        con = lite.connect(self.db)
        cur = con.cursor()
        return con, cur

    def create_tables(self):
        """
        Creates table necessary to store quotes
        :return: void
        """

        print("create table")
        con, cur = self.connection()
        sql = "Create table if not exists quotes (id integer PRIMARY KEY, author text, source text, quote text)"
        try:
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print(str(e), str(e).__class__())
        finally:
            con.close()

    def check_number_entries(self):
        """
        checks how many entries are in the db
        :return: total amount of entries.
        """

        rows = None
        print("Getting Quote Number for randint")
        con, cur = self.connection()
        sql = "SELECT COUNT(*) FROM quotes"
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return rows[0][0]
        except Exception as e:
            print(str(e), str(e).__class__())
        finally:
            con.close()

    def insert_new_quotes(self, tup_quote_list):
        """
        This inputs one or more quotes into the table
        :param tup_quote_list: [(id, author, source, quote)] is the format
        :return: void
        """

        con, cur = self.connection()
        sql = "INSERT INTO quotes values(?, ?, ?, ?)"
        try:
            cur.executemany(sql, tup_quote_list)
            con.commit()
        except Exception as e:
            print(str(e), str(e).__class__())
        finally:
            con.close()

    def get_random_quote(self):
        """
        Checks for the number of entries in the database, selects random number between 1 and high number
        :return: tuple
        """

        high = self.check_number_entries()
        rand = randint(1, high)
        con, cur = self.connection()
        print("getting quote")
        sql = "SELECT * FROM quotes WHERE id=?"
        try:
            cur.execute(sql, (rand,))
            result = cur.fetchall()
            return result[0]
        except Exception as e:
            print(str(e), str(e).__class__())
        finally:
            con.close()

    def initial_insert(self):
        qu = []

        with open("quotes.txt", "r") as quotes:
            t = ()
            for q in quotes:

                if q.startswith("id"):
                    temp = q.split(":", 1)[1].strip()
                    t += (int(temp),)
                    #print(temp)
                elif q.startswith("author"):
                    temp = q.split(":", 1)[1].strip()
                    t += (temp,)
                    #print(temp)
                elif q.startswith("source"):
                    temp = q.split(":", 1)[1].strip()
                    t += (temp,)
                    #print(temp)
                elif q.startswith("quote"):
                    temp = q.split(":", 1)[1].strip()
                    t += ("\"{}\"".format(temp),)
                    #print(temp)
                else:
                    if len(t) > 0:
                        qu.append(t)
                        #print(t)
                   #print(t)
                    t = ()
        print(qu)
        return qu

    def main(self):
        """
        setting up the database for initial use.
        :return:
        """
        self.get_random_quote()


if __name__ == "__main__":
    qb = QuoteBase("quote.db")
    qb.main()