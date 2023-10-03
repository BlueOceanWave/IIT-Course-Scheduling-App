import json
import re

subjects ='Academic Training and Research (ATR)--\
Air Force Aerospace Studies (AS)--\
Architecture and Urbanism (AURB)--\
Architecture (ARCH)--\
Art and Architectural History (AAH)--\
Biology (BIOL)--\
Biomedical Engineering (BME)--\
Business (BUS)--\
Chemical Engineering (CHE)--\
Chemistry (CHEM)--\
Civil and Architectural Engr (CAE)--\
Communications (COM)--\
Computer Science (CS)--\
Computer Science Prof Master (CSP)--\
Data Science (DS)--\
Economics (ECON)--\
Electrical and Computer Engr (ECE)--\
Engineering Graphics (EG)--\
Engineering Management (EMGT)--\
English Language Program (ELP)--\
Environmental Engineering (ENVE)--\
Environmental Management and Sustainability (EMS)--\
Financial Markets Compliance (FMC)--\
Food Science and Nutrition (FDSN)--\
Game Design and Experiential Media (GEM)--\
General Engineering (ENGR)--\
History (HIST)--\
Humanities (HUM)--\
Industrial Tech and Mgmt (INTM)--\
Information Tech and Mgmt (ITM)--\
Institute of Design (ID)--\
Institute of Design (IDN)--\
Institute of Design (IDX)--\
Intellectual Prop Mgt and Mkts (IPMM)--\
Intensive English Program (IEP)--\
Interprofessional Project (IPRO)--\
ITM Development (ITMD)--\
ITM Management (ITMM)--\
ITM Operations (ITMO)--\
ITM Security (ITMS)--\
ITM Theory and Technology (ITMT)--\
Landscape Architecture (LA)--\
Law (LAW)--\
Lewis College (UG-LCHS)--\
Literature (LIT)--\
Management Science (MSC)--\
Marketing Analytics (MAX)--\
Master of Science in Finance (MSF)--\
Materials Science (MS)--\
Mathematics and Science Educ (MSED)--\
Mathematics (MATH)--\
MBA Business (MBA)--\
Mechl, Mtrls and Arspc Engrg (MMAE)--\
Military Science (MILS)--\
Naval Science (NS)--\
Philosophy (PHIL)--\
Physics (PHYS)--\
Political Science (PS)--\
Proficiency of English as a Second Language (PESL)--\
Psychology (PSYC)--\
Public Administration (PA)--\
Science (SCI)--\
Social Sciences (SSCI)--\
Sociology (SOC)--\
Statistics (STAT)--\
Stuart School of Business (SSB)--\
Sustainability Analytics and Management (SAM)--\
Sustainability Management (SMGT)--\
Technology (TECH)'

subjectList = []
for line in subjects.split('--'):
    # Use regular expression to extract portion in parenthesis
    pattern = r'\((.*?)\)'
    match = re.search(pattern, line)
    
    # Separate the two parts
    abbr = match.group(1)
    text = line[:match.start()]

    # Convert UG-LCHS to just LCHS
    if abbr == 'UG-LCHS':
        abbr = 'LCHS'

    # Add subject to list
    theSubject = {  "sID": abbr.strip(),
                    "lID": text.strip()
                 }
    subjectList.append(theSubject)

# Convert to JSON
fileName = "subjects.json" 
with open(fileName, 'w') as json_file: 
    json_string = json.dump(subjectList, json_file, indent = 4)

print('JSON file created')