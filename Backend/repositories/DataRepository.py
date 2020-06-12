from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lichten():
        sql = "SELECT * from tbllocatie"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_licht_by_id(id):
        sql = "SELECT verkeerslichtid from tbllocatie WHERE straatid = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_metingen_snelheid():
        sql = "SELECT * from tblmeting where sensorid = 1 or sensorid = 2 order by metingid DESC LIMIT 20"
        return Database.get_rows(sql)

    @staticmethod
    def read_overtredingen():
        sql = "SELECT * from tblmeting where Waarde > 90 and sensorid = 1 or Waarde > 90 and sensorid = 2"
        return Database.get_rows(sql)

    @staticmethod
    def update_status_licht(id, status):
        sql = "UPDATE tbllocatie SET verkeerslichtid = %s WHERE straatid = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod 
    def create_meting(waarde, sensorid):
        sql = "INSERT INTO tblmeting(waarde, datum, sensorid) VALUES (%s,current_timestamp(),%s)"
        params = [waarde, sensorid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_status_straatverlichting(id):
        sql = "SELECT autostraatverlichting from tblkruispunt WHERE kruispuntid = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_straatverlichting(id, status):
        sql = "UPDATE tblkruispunt SET autostraatverlichting = %s WHERE kruispuntid = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_autoverkeerslichten(id):
        sql = "SELECT autoverkeerslichten from tblkruispunt WHERE kruispuntid = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_autoverkeerslichten(id, status):
        sql = "UPDATE tblkruispunt SET autoverkeerslichten = %s WHERE kruispuntid = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)