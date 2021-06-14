import sys, json, numpy as np

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    lines = read_in()

    #!/usr/bin/env python
    # coding: utf-8

    #  

    # In[1]:

    from io import StringIO
    import re
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser

    output_string = StringIO()
    with open('C:/Users/ASUS/Downloads/Profile.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    str1 = output_string.getvalue()
    str1 = str1.replace("Page 1 of 2", "")
    str1 = str1.replace("Page 2 of 2", "")
    str2 = re.sub(r'(\n\s*)+\n+', '\n\n', str1)


    # In[2]:


    email = re.search(r'[\w\.-]+@[\w\.-]+', str2)
    email_var = email.group(0)


    # In[3]:


    summary = re.search('(?<=Summary\n)([^.])*',str2)
    summary_var = summary.group(0)


    # In[5]:


    name = re.search('(?<=\n\n)[A-Za-z]{4,25} [A-Za-z]{2,25}', str2)
    namelist = name.group(0).split()

    if len(namelist) == 2:
        fname = namelist[0]
        lname = namelist[1]
    else:
        fname = namelist[0]
        mname = namelist[1]
        lname = namelist[2]


    # In[6]:


    skills = re.search('(?<=Top Skills)(?:\r?\n(?!\r?\n).*)*', str2)
    skills_var = skills.group(0)


    # In[7]:


    a, b = str2.find('Experience\n'), str2.find('Education')
    experience_var = str2[a+10:b]


    # In[8]:


    certifications = re.search('(?<=Certifications)(?:\r?\n(?!\r?\n).*)*', str2)
    certifications_var = certifications.group(0)


    # In[9]:


    education = re.search('(?<=Education)([^$]*)', str2)
    education_var = education.group(0)


    # In[10]:


    skills = skills_var.lstrip()
    skills = skills.split("\n")


    # In[11]:


    experience_var = experience_var.lstrip()
    experience_var = experience_var.rstrip()
    experience = experience_var.split("\n\n")


    # In[12]:


    education_var = education_var.lstrip()
    education_var = education_var.rstrip()
    education = education_var.split("\n\n")


    # In[13]:


    certifications_var = certifications_var.lstrip()
    certifications = certifications_var.split("\n")


    # In[18]:


    # User record
    import firebase_admin
    from firebase_admin import credentials

    cred_object = firebase_admin.credentials.Certificate(r'D:\Kavya\online studies\winlysis\project-3-winlysis-firebase-adminsdk-mi6d1-32ff71caa0.json')
    default_app = firebase_admin.initialize_app(cred_object)
    from firebase_admin import firestore
    db = firestore.client()
    #default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':'https://console.firebase.google.com/u/0/project/project-3-winlysis/firestore/data~2Fuser~2FEQ02tXKrDFe6vlM4IHOGkvqPrA52'}, name="user")

    doc_ref = db.collection(u'user').document(lines[1])
    doc_ref.set({
        u'fname': fname,
        u'lname': lname,
        u'email': email_var,
        u'profile_overview': summary_var,
        u'skills': skills,
    }, merge=True)


    # In[20]:


    # Certifications record
    import firebase_admin
    from firebase_admin import credentials

    cred_object = firebase_admin.credentials.Certificate(r'D:\Kavya\online studies\winlysis\project-3-winlysis-firebase-adminsdk-mi6d1-32ff71caa0.json')
    default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':'https://console.firebase.google.com/u/0/project/project-3-winlysis/firestore/data~2Fcertificates-record~2FOt6LAo49VMfxAlbONNKV'}, name="certificates-record")
    from firebase_admin import firestore
    db = firestore.client()


    # In[21]:


    for c in certifications:
        import random
        n = random.randint(0,10)
        doc_ref = db.collection(u'certificates-record').document(str(lines[1]))
        doc_ref.set({
            u'certificate_description': "",
            u'certificate_id':"",
            u'certificate_name':c,
            u'certificate_organization':"",
            u'certificate_url':"",
            u'userid':lines[0]
    })


    # In[23]:


    # Employment Record
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    cred_object = firebase_admin.credentials.Certificate(r'D:\Kavya\online studies\winlysis\project-3-winlysis-firebase-adminsdk-mi6d1-32ff71caa0.json')
    default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':'https://console.firebase.google.com/u/0/project/project-3-winlysis/firestore/data~2Femployment_record~2Femp-8e534fe0-f66d-46fd-8238-92e1c6230847'}, name = "employment_record")
    db = firestore.client()


    # In[24]:


    for e in experience:
        employment_name = re.search(".*", e)
        try:
            employment_name = employment_name.group(0)
        except:
            employment_name = ""
            
        employment_from_month = re.search(".+?(?=[0-9]{4})", e)
        try:
            employment_from_month = employment_from_month.group(0)
        except:
            employment_from_month = ""
            
        employment_to_month = re.search("(?<=-\s)(\w*)", e)
        try:
            employment_to_month = employment_to_month.group(0)
        except:
            employment_to_month = ""
            
        employment_city = re.search("(?m)(?<=\)\n)\w*(?=,)", e)
        try:
            employment_city = employment_city.group(0)
        except:
            employment_city = ""
            
        employment_title = re.search("(?m)(?<=\n).*", e)
        try:
            employment_title = employment_title.group(0)
        except:
            employment_title = ""
            
        employment_from_year = re.search("\d{4}", e)
        try:
            employment_from_year = employment_from_year.group(0)
        except:
            employment_from_year = ""
    
        #employment_to_year
        temp = re.search("(?m)(?<=\d{4}\s-\s).*(\d{4})", e)
        try:
            temp = temp.group(0)
        except:
            temp = ""
        employment_to_year = re.search("\d{4}", str(temp))
        try:
            employment_to_year = employment_to_year.group(0)
        except:
            employment_to_year = ""

        
        #employment_country 
        ec = re.search("(?<=, )(?=\w+,).*", e)
        try:
            ec = ec.group(0)
        except:
            ec = ""
        employment_country = re.search("(?<=, ).*", str(ec))
        try:
            employment_country = employment_country.group(0)
        except:
            employment_country = ""
        
        import random
        n = random.randint(0,10)
        doc_ref = db.collection(u'employment_record').document(str(n))
        doc_ref.set({
            u'employment_name': employment_name,
            u'employment_from_month': employment_from_month,
            u'employment_to_month': employment_to_month,
            u'employment_city': employment_city,
            u'employment_title': employment_title,
            u'employment_from_year': employment_from_year,     
            u'employment_to_year': employment_to_year,
            u'employment_country': employment_country
        })


    # In[26]:


    # Education Record
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    cred_object = firebase_admin.credentials.Certificate(r'D:\Kavya\online studies\winlysis\project-3-winlysis-firebase-adminsdk-mi6d1-32ff71caa0.json')
    default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':'https://console.firebase.google.com/u/0/project/project-3-winlysis/firestore/data~2Feducation_record~2FWtElIxG7i4ksXF4RnlRi'}, name="education_record")
    db = firestore.client()


    # In[27]:


    for ed in education:
        college_name =  re.search(".*", ed)
        try:
            college_name = college_name.group(0)
        except:
            college_name = ""
            
        dates_from = re.search("(?<=\()\w{4}", ed)
        try:
            dates_from = dates_from.group(0)
        except:
            dates_from = ""
            
        dates_to = re.search("(?<=-\s)\w{4}", ed)
        try:
            dates_to = dates_to.group(0)
        except:
            dates_to = ""
            
        degree = re.search("(?m)(?<=\n).*(?=,)", ed)
        try:
            degree = degree.group(0)
        except:
            degree = ""
            
        study_area = re.search("(?m)(?<=,\s).*(?=\(\d)", ed)
        try:
            study_area = study_area.group(0)
        except:
            study_area = ""
            
        study_description = re.search("(?m)(?=\)\n)", ed)
        try:
            study_description = study_description.group(0)
        except:
            study_description = ""
        
        
        import random
        n = random.randint(0,10)
        doc_ref = db.collection(u'education_record').document(str(n))
        doc_ref.set({
            u'college_name': college_name,
            u'dates_from': dates_from,
            u'dates_to': dates_to,
            u'degree': degree,
            u'study_area': study_area,
            u'study_description': study_description
        })

    print("Done")
    var="complete"
    # In[ ]:






    uid = "This is UID "+lines[1]

    #return the string to the output stream
    print(uid)

#start process
if __name__ == '__main__':
    main()
   

