import pyodbc
import pandas as pd

#Using pyodbc to connect the NDI database from SQL SEVER
conn=pyodbc.connect('Driver= ODBC Driver 13 for SQL Server;'
					'Server=vasql.kdi.local,1433;'
					'Database=CDW_TIU;'
					'Trusted_connection=yes')
cursor=conn.cursor()

#Select the needed Deaths of Suicide from Database from X60-84,Y87,U03*

Query=""" SELECT * FROM VA_MVP011_CDWTIUNotes.va.NDI_VACohort_20201201 NDI
			WHERE ((NDI.rec_cond1 LIKE 'X6%') OR (NDI.rec_cond1 LIKE 'X7%')
			   OR (NDI.rec_cond1 LIKE 'X80%') OR (NDI.rec_cond1 LIKE 'X81%')
			   OR (NDI.rec_cond1 LIKE 'X82%') OR (NDI.rec_cond1 LIKE 'X83%')
			   OR (NDI.rec_cond1 LIKE 'X84%') OR (NDI.rec_cond1 LIKE 'X85%')
			   OR (NDI.rec_cond1 LIKE 'X86%') OR (NDI.rec_cond1 LIKE 'X87%'))
			   OR ((NDI.rec_cond2 LIKE 'X6%') OR (NDI.rec_cond2 LIKE 'X7%')
			   OR (NDI.rec_cond2 LIKE 'X80%') OR (NDI.rec_cond2 LIKE 'X81%')
			   OR (NDI.rec_cond2 LIKE 'X82%') OR (NDI.rec_cond2 LIKE 'X83%')
			   OR (NDI.rec_cond2 LIKE 'X84%') OR (NDI.rec_cond2 LIKE 'X85%')
			   OR (NDI.rec_cond2 LIKE 'X86%') OR (NDI.rec_cond2 LIKE 'X87%'))
			   OR ((NDI.UnderlyingCause_NDI LIKE 'X6%') OR (NDI.UnderlyingCause_NDI LIKE 'X7%'))
			   OR (NDI.UnderlyingCause_NDI LIKE 'X80%') OR (NDI.UnderlyingCause_NDI LIKE 'X81%')
			   OR (NDI.UnderlyingCause_NDI LIKE 'X82%') OR (NDI.UnderlyingCause_NDI LIKE 'X83%')
			   OR (NDI.UnderlyingCause_NDI LIKE 'X84%') OR (NDI.UnderlyingCause_NDI LIKE 'X85%')
			   OR (NDI.UnderlyingCause_NDI LIKE 'X86%') OR (NDI.UnderlyingCause_NDI LIKE 'X87%'));"""

#Get the corresponding VA SMR data
VA_SMR_raw_data=pd.read_sql_query(Query, conn)

#merge the SMR with total population to get suicide mortality patientICN's county/zip level
VA_SMR=pop.merge(VA_SMR_raw_data,how='inner',on=['PatientICN'])

#Get the corresponding county/zip level SMR data
#each patient has unique identifier called PatientICN 
Counties_SMR= VA_SMR.groupby('PatientFIPS')['PatientICN'].agg(lambda x:x.count()).reset_index()
ZIPS_SMR= VA_SMR.groupby('PatientZIP')['PatientICN'].agg(lambda x:x.count()).reset_index()


""" we can also get SA/SI data throughout the similar process """
