import sqlite3

class DataBaseService():
  def __init__(self, db_name):
    self.db_name = db_name
    self.conn = sqlite3.connect(db_name)
    self.cursor = self.conn.cursor()
  
  def insert(self, table:str, columns:list, values:list):
    """
    Add an element to the registry on a table in an SQLite database.
    Args:
      :param table: The table to query
      :param columns (list): The columns to include in the registry.
      :param values (list): The values to insert into the registry.
    Returns:
      None
    """
    self.cursor.execute(f"""
      INSERT INTO {table} ({', '.join(columns)})
      VALUES ({', '.join(['?' for _ in columns])});
    """, values)
    self.conn.commit()
  
  def select(self, table:str, conditions:dict=None):
    """
    Execute a SELECT query with conditions.
      :param table: The table to query
      :param conditions: A dictionary of conditions to execute the query
    :Returns: 
      A list of tuples containing the query results
    """
    query = f"SELECT * FROM {table}"
    params = ()
    if conditions:
      query += " WHERE "
      conditions_list = []
      for column, value in conditions.items():
        conditions_list.append(f"{column} = ?")
        params += (value,)
      query += " AND ".join(conditions_list)
    self.cursor.execute(query, params)
    
    column_names = [description[0] for description in self.cursor.description]
    results = self.cursor.fetchall()
    results_dict = []
    for row in results:
        row_dict = dict(zip(column_names, row))
        results_dict.append(row_dict)

    return results_dict


  def update(self, table:str, data:dict, conditions:dict):
    """
    Updates a registry in the specified table.
    Args:
      table (str): The name of the table to update.
      data (dict): A dictionary containing the columns to update and their new values.
      conditions (dict): A dictionary of conditions to execute the query
    Returns:
      None
    """
    columns = ", ".join([f"{key} = ?" for key in data.keys()])
    where_conditions = " AND ".join([f"{key} = ?" for key in conditions.keys()])
    query = f"UPDATE {table} SET {columns} WHERE {where_conditions}"
    values = list(data.values()) + list(conditions.values())
    self.cursor.execute(query, values)
    self.conn.commit()

  def close_connection(self):
    """
    Close the connection to the SQLite database.
    Returns:
      None
    """
    self.conn.close()
    