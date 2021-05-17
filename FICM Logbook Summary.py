#!/usr/bin/env python
# coding: utf-8

# FICM Logbook Summary Report 
# Creates a FICM Logbook Summary Report from an Anaesthetics LLP Logbook excel export

# User Defined Variables

name = 'Mark Jeffrey'
logbook = 'logbook_export.xlsx'
start_date = 'Aug 18'
end_date = 'Aug 21'


# Events Table

# Import Libraries
import pandas as pd

#Import each sheet into a DataFrame
#Set Case ID as Index
anaesthetic_log = pd.read_excel(logbook, sheet_name='LOGBOOK_CASE_ANAESTHETIC',index_col=0)
procedure_log = pd.read_excel(logbook, sheet_name='LOGBOOK_STAND_ALONE_PROCEDURE',index_col=0)
session_log = pd.read_excel(logbook, sheet_name='LOGBOOK_SESSION',index_col=0)
icu_log = pd.read_excel(logbook, sheet_name='LOGBOOK_CASE_INTENSIVE',index_col=0)

#Divide DataFrame by levels of supervision
#local = immediate and local
#distant = distant and solo
icu_log_local = icu_log[(icu_log['Supervision']=='Immediate') | (icu_log['Supervision']=='Local')]
icu_log_distant = icu_log[(icu_log['Supervision']=='Distant') | (icu_log['Supervision']=='Solo')]
icu_log_teaching = icu_log[icu_log['Supervision']=='Teaching']

#Data for event table columns
event_local = [
    len(icu_log_local[icu_log_local['Event'].str.contains('ward-review')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('admission')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('lead-ward-round')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('cardiac-arrest')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('trauma-team')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('intra-hospital-transfer')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('inter-hospital-transfer')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('discussion-with-relatives')]),
    len(icu_log_local[icu_log_local['Event'].str.contains('end-of-life-care')])
]

event_distant = [
    len(icu_log_distant[icu_log_distant['Event'].str.contains('ward-review')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('admission')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('lead-ward-round')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('cardiac-arrest')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('trauma-team')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('intra-hospital-transfer')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('inter-hospital-transfer')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('discussion-with-relatives')]),
    len(icu_log_distant[icu_log_distant['Event'].str.contains('end-of-life-care')])
]

event_total = [
    len(icu_log[icu_log['Event'].str.contains('ward-review')]),
    len(icu_log[icu_log['Event'].str.contains('admission')]),
    len(icu_log[icu_log['Event'].str.contains('lead-ward-round')]),
    len(icu_log[icu_log['Event'].str.contains('cardiac-arrest')]),
    len(icu_log[icu_log['Event'].str.contains('trauma-team')]),
    len(icu_log[icu_log['Event'].str.contains('intra-hospital-transfer')]),
    len(icu_log[icu_log['Event'].str.contains('inter-hospital-transfer')]),
    len(icu_log[icu_log['Event'].str.contains('discussion-with-relatives')]),
    len(icu_log[icu_log['Event'].str.contains('end-of-life-care')])
]

# Creates Events table
Events = pd.DataFrame(
    data=[event_local, event_distant, event_total],              #event_teaching,
    index= ['Local Supervision','Distant Supervision','Total'],  #'Teaching'
    columns=['Ward review','Admission','Lead ward round','Cardiac arrest','Trauma team','Intra-hospital transfer','Inter-hosptial transfer','Discussion with relatives','End of life care/donation']
)

#Transpose axes for correct layout
Events = Events.T
Events.index.names = ['Events']

# Procedures Table

#Procedures Multi-index
outside = [
    'Airways and Lungs', 'Airways and Lungs','Airways and Lungs','Airways and Lungs','Airways and Lungs','Airways and Lungs',
    'Cardiovascular','Cardiovascular','Cardiovascular','Cardiovascular','Cardiovascular','Cardiovascular','Cardiovascular',
    'Abdomen','Abdomen','Abdomen',
    'CNS','CNS'
]
inside = [
    'Emergency Intubation',
    'Percutaneous Tracheostomy',
    'Bronchoscopy',
    'Chest Drain - Seldinger',
    'Chest Drain - Surgical',
    'Lung Ultrasound',
    'Arterial cannulation',
    'Central venous access – IJ',
    'Central venous access – SC',
    'Central venous access – Femoral',
    'Pulmonary artery catheter',
    'Non-invasive CO monitoring',
    'Echocardiogram',
    'Ascitic drain/tap',
    'Sengstaken tube placement',
    'Abdominal ultrasound/FAST',
    'Lumbar puncture',
    'Brainstem death testing'
]
hier_index = list(zip(outside,inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)

#Creates table for each procedure column with supervision 
#Removes rows with missing entries
#Renames columns to "Procedure Type" and "Supervision"
anaesthetic_procedure_log = procedure_log[['Procedure Type (Anaesthesia)','Supervision']].dropna().rename(columns={"Procedure Type (Anaesthesia)":"Procedure Type"})
medicine_procedure_log = procedure_log[['Procedure Type (Medicine)','Supervision']].dropna().rename(columns={"Procedure Type (Medicine)":"Procedure Type"})
pain_procedure_log = procedure_log[['Procedure Type (Pain)','Supervision']].dropna().rename(columns={"Procedure Type (Pain)":"Procedure Type"})
anaesthetic_sheet_procedure_log = anaesthetic_log[['Procedure Type','Procedure Supervision']].dropna().rename(columns={"Procedure Supervision":"Supervision"})

#Contatencates above into a single table with 2 columns "Procedure Type" and "Supervision"
procedures_all = pd.concat([
    anaesthetic_procedure_log,
    medicine_procedure_log,
    pain_procedure_log,
    anaesthetic_sheet_procedure_log]
)

#Makes Supervision column all lower case to avoid duplication
procedures_all['Supervision'] = procedures_all['Supervision'].str.lower()

#Subdivides all procedures by level of supervision
procedures_all_local = procedures_all[(procedures_all['Supervision']=='supervised') | (procedures_all['Supervision']=='observed')]
procedures_all_distant = procedures_all[procedures_all['Supervision']=='solo']

#Data for procedure table columns
procedures_total = [
    len(procedures_all[(procedures_all['Procedure Type']=='rsi')|(procedures_all['Procedure Type']=='emergency-intubation')|(procedures_all['Procedure Type']=='airway-protection')]),
    len(procedures_all[procedures_all['Procedure Type']=='percutaneous-tracheostomy']),
    len(procedures_all[procedures_all['Procedure Type']=='bronchoscopy']),
    len(procedures_all[procedures_all['Procedure Type']=='intercostal-drain:seldinger']),
    len(procedures_all[procedures_all['Procedure Type']=='intercostal-drain:open']),
    len(procedures_all[procedures_all['Procedure Type']=='lung-ultrasound']),
    len(procedures_all[procedures_all['Procedure Type']=='arterial-cannulation']),
    len(procedures_all[procedures_all['Procedure Type']=='central-venous-access–internal-jugular']),
    len(procedures_all[procedures_all['Procedure Type']=='central-venous-access–subclavian']),
    len(procedures_all[procedures_all['Procedure Type']=='central-venous-access–femoral']),
    len(procedures_all[procedures_all['Procedure Type']=='pulmonary-artery-catheter']),
    len(procedures_all[procedures_all['Procedure Type']=='non-invasive-co-monitoring']),
    len(procedures_all[procedures_all['Procedure Type']=='echocardiogram']),
    len(procedures_all[(procedures_all['Procedure Type']=='ascitic-tap')|(procedures_all['Procedure Type']=='abdominal-paracentesis')]),
    len(procedures_all[procedures_all['Procedure Type']=='sengstacken-tube-placement']),
    len(procedures_all[procedures_all['Procedure Type']=='abdominal-ultrasound/fast']),
    len(procedures_all[procedures_all['Procedure Type']=='lumbar-puncture']),
    len(procedures_all[procedures_all['Procedure Type']=='brainstem-death-testing']),
]

procedures_total_local = [
    len(procedures_all_local[(procedures_all_local['Procedure Type']=='rsi')|(procedures_all_local['Procedure Type']=='emergency-intubation')|(procedures_all_local['Procedure Type']=='airway-protection')]),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='percutaneous-tracheostomy']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='bronchoscopy']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='intercostal-drain:seldinger']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='intercostal-drain:open']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='lung-ultrasound']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='arterial-cannulation']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='central-venous-access–internal-jugular']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='central-venous-access–subclavian']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='central-venous-access–femoral']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='pulmonary-artery-catheter']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='non-invasive-co-monitoring']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='echocardiogram']),
    len(procedures_all_local[(procedures_all_local['Procedure Type']=='ascitic-tap')|(procedures_all_local['Procedure Type']=='abdominal-paracentesis')]),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='sengstacken-tube-placement']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='abdominal-ultrasound/fast']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='lumbar-puncture']),
    len(procedures_all_local[procedures_all_local['Procedure Type']=='brainstem-death-testing']),
]

procedures_total_distant = [
    len(procedures_all_distant[(procedures_all_distant['Procedure Type']=='rsi')|(procedures_all_distant['Procedure Type']=='emergency-intubation')|(procedures_all_distant['Procedure Type']=='airway-protection')]),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='percutaneous-tracheostomy']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='bronchoscopy']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='intercostal-drain:seldinger']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='intercostal-drain:open']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='lung-ultrasound']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='arterial-cannulation']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='central-venous-access–internal-jugular']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='central-venous-access–subclavian']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='central-venous-access–femoral']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='pulmonary-artery-catheter']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='non-invasive-co-monitoring']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='echocardiogram']),
    len(procedures_all_distant[(procedures_all_distant['Procedure Type']=='ascitic-tap')|(procedures_all_distant['Procedure Type']=='abdominal-paracentesis')]),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='sengstacken-tube-placement']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='abdominal-ultrasound/fast']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='lumbar-puncture']),
    len(procedures_all_distant[procedures_all_distant['Procedure Type']=='brainstem-death-testing']),
]

#Procedures Table
Procedures = pd.DataFrame(
    data=[procedures_total_local, procedures_total_distant, procedures_total], 
    index= ['Local Supervision', 'Distant Supervision', 'Total'],
    columns= hier_index
)

#Transpose table
Procedures = Procedures.T
Procedures.index.names = (['System', 'Procedure'])


# Export to Excel
with pd.ExcelWriter(f"{name} FICM Logbook Summary {start_date} to {end_date}.xlsx") as writer:
    Events.to_excel(writer, sheet_name='Events')
    Procedures.to_excel(writer, sheet_name='Procedures')
