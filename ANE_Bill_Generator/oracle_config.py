import cx_Oracle as oracle
#from oracle_config import *

ip = "172.20.100.121"

host = "emdb1-vip.kdahit.com"

port = 1521

service_name =  "EMRAC.kdahit.com"

instance_name = "EMRAC1"

dsn_tns = oracle.makedsn(ip,port,instance_name)

ora_db = oracle.connect("appluser","appluser",dsn_tns)

cursor = ora_db.cursor()


class Ora:

    def __init__(self):
        self.ora_db = oracle.connect("appluser","appluser",dsn_tns)
        self.cursor = ora_db.cursor()

    def status_update(self):

        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department" 
      


    def __del__(self):
        self.cursor.close()
        self.ora_db.close()
    
    def view_ane_bill(self,uhid):

      
        sql_qurey = ('''
        
        SELECT DISTINCT A.PATIENT_ID,B.PATIENT_NAME, A.EPISODE_TYPE,A.EPISODE_ID,A.ENCOUNTER_ID,A.SERV_ITEM_CODE,A.SERV_ITEM_DESC,A.BASE_RATE,A.SERV_QTY,A.ORG_NET_CHARGE_AMT  
        FROM BL_PATIENT_CHARGES_FOLIO A,MP_PATIENT B
        WHERE A.PATIENT_ID = B.PATIENT_ID AND  A.trx_status is null AND A.EPISODE_TYPE = 'E'
        AND A.TRX_DATE >=TO_DATE(SYSDATE-1) AND A.PATIENT_ID IN ( SELECT PATIENT_ID FROM AE_CURRENT_PATIENT WHERE QUEUE_DATE >= to_date(sysdate-1) AND FACILITY_ID = 'KH')
        AND A.PATIENT_ID = :uhid_get
        ORDER BY A.PATIENT_ID


        ''')

        self.cursor.execute(sql_qurey,{"uhid_get":uhid})
        ane_bill = self.cursor.fetchall()
        # for row in get:
        #     print(row)
        
       
        return ane_bill
        
    def current_ane_patient(self):
        self.cursor.execute('''
        
        SELECT A.PATIENT_ID,B.PATIENT_NAME,A.QUEUE_DATE,A.VISIT_TYPE_IND,A.EPISODE_ID,A.ENCOUNTER_ID 
        FROM AE_CURRENT_PATIENT A ,MP_PATIENT B
        WHERE A.PATIENT_ID = B.PATIENT_ID AND A.QUEUE_DATE >= to_date(sysdate-1)
        AND A.FACILITY_ID = 'KH'
        ORDER BY A.QUEUE_DATE

        
        
        ''')

        current_ane_data = self.cursor.fetchall()
               
        return current_ane_data
       



#dsn_tns = cx_Oracle.makedsn(ip,port,instance_name)

#db = cx_Oracle.connect("appluser","appluser",dsn_tns)


#172.20.100.121

