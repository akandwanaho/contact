import os
from flask import Flask, request, redirect, render_template, jsonify, url_for, abort, send_from_directory, flash, make_response, session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime


import logging
# from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='/static')
submitted_questions_form1 = []  # List to store questions from form 1
submitted_questions_form2 = []  # List to store questions from form 2
submitted_answers_form1 = []  # List to store answers from form 1




# Define a global variable to store the access count
access_count = 0


# FAQs
faqs = {
    "When does semester one officially start?": "The semester commences on 29th July 2024. \nPlease review academic calendar for above mentioned dates and other key important dates.",
"When does semester two start?": "Semester two commences on 29th July 2024. \n<strong>Good Luck!</strong>.",
"When does semester 2 start?": "Semester two commences on 29th July 2024. \n<strong>Good Luck!</strong>.",
"When will semester 2 commence?": "Semester two commences on 29th July 2024. \n<strong>Good Luck!</strong>.",
    "Where do I access my fee statement?": "Fee statements can be accessed on iEnabler. \nOnce you have logged in, a drop down will appear, and you must select summarised statement of account. Your statement will then appear.",
    "Where can I get my academic record/ transcript?": "Academic record/transcript can be accessed on iEnabler. \nOnce you have logged in, you will click on student enquiry. \nA drop down will appear, and you must select academic transcript.",
"how do I access my academic transcript?": "Academic record/transcript can be accessed on iEnabler. \nOnce you have logged in, you will click on student enquiry. \nA drop down will appear, and you must select academic transcript.",
"how do I access my academic record?": "Academic record/transcript can be accessed on iEnabler. \nOnce you have logged in, you will click on student enquiry. \nA drop down will appear, and you must select academic transcript.",


"What is WIL?": "Work Integrated Learning entails practical hands-on experience received at the workplace which supports your learning experience and is part of your formal academic programme. \nAll final year students are required to conduct and complete their Work Integrated Learning. \nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform.",
"What is work integrated learning?": "Work Integrated Learning entails practical hands-on experience received at the workplace which supports your learning experience and is part of your formal academic programme. \nAll final year students are required to conduct and complete their Work Integrated Learning. \nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform.",
"Where do I do WIL?": " You can choose any company or organisation of your interest depending on your specialisation.\nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform. \nIf you cannot get a company, please contact Richfield through your administrator. \n<strong>Good Luck!</strong>",
"Where do I do work integrated learning?": " You can choose any company or organisation of your interest depending on your specialisation.\nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform. \nIf you cannot get a company, please contact Richfield through your administrator. \n<strong>Good Luck!</strong>",
"Where do I get a company for WIL?": " You can choose any company or organisation of your interest depending on your specialisation.\nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform. \nIf you cannot get a company, please contact Richfield through your administrator. \n<strong>Good Luck!</strong>",
"Where do I get a company for work integrated learning?": " You can choose any company or organisation of your interest depending on your specialisation.\nYou will be required to complete the WIL logbook and upload onto the Moodle platform. \nAll relevant documentation relating to WIL can be found on your Moodle platform. \nIf you cannot get a company, please contact Richfield through your administrator. \n<strong>Good Luck!</strong>",


"I cannot access ienabler": "To reset your iEnabler password, send an email to: moodlesupport@richfield.ac.za or contact your administrator.",
"I cant log in ienabler": "To reset your iEnabler password, send an email to: moodlesupport@richfield.ac.za or contact your administrator.",


"Hi": "Hi there, what information are you seeking today?.",
"Hello": "Hello, what information are you seeking today?.",

"How is the weather today?": "It is sunny and warm, but it is likely to rain in the evening",
"When is the assignment due date? assignments": "Assignments 1 & 2 due date is on 30 August 2024, \nAssignments 3 & 4 due date is on 30 August 2024, \nAssignments 5 & 6 due date is on 30 August 2024. \n<strong>Good Luck!</strong>",
"Who is the Dean?": "The Executive Dean is: Dr Stephen Akandwanaho (stephen.akandwanaho@growth-ten.com)",
"Who is the Director Distance Learning?": "Ms Ravika Sookraj (ravikas@richfield.ac.za)",
"Who is the Director Contact Learning?": "Mr Kegan Shunmugam (kegans@richfield.ac.za)",

"Who is the Managing Director Distance Learning?": "Ms Ravika Sookraj (ravikas@richfield.ac.za)",
"Who is the Managing Director Contact Learning?": "Mr Kegan Shunmugam (kegans@richfield.ac.za)",
"Who is the MD Distance Learning?": "Ms Ravika Sookraj (ravikas@richfield.ac.za)",
"Who is the MD Contact Learning?": "Mr Kegan Shunmugam (kegans@richfield.ac.za)",

"When is the exams?": "Semester exams run from 14th June to 3 July 2024.\n<strong>Good Luck!</strong>",
"exam dates?": "Semester exams run from 12th November to 2 December 2024.\n<strong>Good Luck!</strong>",
"exams dates?": "Semester exams run from 12th November to 2 December 2024.\n<strong>Good Luck!</strong>",
"When are the exams?": "Semester exams run from 12th November to 2 December 2024.\n<strong>Good Luck!</strong>",
"When does examination commence?": "Semester exams run from 12th November to 2 December 2024.\n<strong>Good Luck!</strong>",
"When are the examination exam?": "Semester exams run from 12th November to 2 December 2024.\n<strong>Good Luck!</strong>",
"When are the exams this semester?": "Semester exams run from 12th November to 2 December 2024. \n<strong>Good Luck!</strong>",

"When will results be released?": "Results will be released on 11 December 2024. \n<strong>Good Luck!</strong>",
"When will results be available?": "Results will be released on 11 December 2024. \n<strong>Good Luck!</strong>",
"How do I access my results?": "Results are accessed on iEnabler. \nPlease log into your iEnabler, \nSelect student inquiry and go to academic record. \n<strong>Good Luck!</strong>",
"How to access my results": "Results are accessed on iEnabler. \nPlease log into your iEnabler, \nSelect student inquiry and go to academic record. \n<strong>Good Luck!</strong>",
"When will results for semester 2 2024 be released?": "Results will be released on 11 December 2024. \n<strong>Good Luck!</strong>",


"When can I get my results?": "Results will be released on 11 December 2024. \n<bold>Good luck!<bold>",
"When are the institution holidays?": "Semester holidays run from 15 December 2024 to 22 February 2025. \n<bold>Enjoy your holidays!<bold>",
"holidays?": "Semester holidays run from 15 December 2024 to 22 February 2025. \n<bold>Enjoy your holidays!<bold>",


"Who is the registrar": "Dr Muni Kooblal(muni.kooblal@growth-ten.com)",
"Who is the Chief Academic Officer": "Ms Shireen Chengadu",
"Who is the CAO": "Ms Shireen Chengadu",
"Who is the CEO": "Mr Stefan Ferreira",
"Who is the Chief Executive Officer": "Mr Stefan Ferreira",
"Who is head of Data Analytics": "Arshad Suliman (arshad.suliman@growth-ten.com)",
"Why Richfield": "Richfield is the leading private higher education institution in South Africa with 8 premium campuses around the country and a world-class distance learning division",
"Which industry badges and certifications can I study": "Richfield partners with IBM, AWS Academy, Salesforce, Oracle, CISCO and CIMA. \nYou can choose any course of your interest that compliments your curriculum and obtain a badge and certification. \nThis will make you stand out and enhance your employability as a graduate of Richfield. \n<strong>Good luck!</strong>",

"How do I sign up for AWS": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"How do I signup for AWS": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"AWS": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",

"How do I access AWS": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"give me access to AWS": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"access to amazon": "In order to sign up for AWS, please complete this form from here: <a href='https://learning.richfield.ac.za/HET/mod/page/view.php?id=363438'>Moodle</a>.\nYou can also contact: jeminam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"How do I access IBM courses": "In order to sign up for Amazon, go to:<a href='https://www.ibm.com/academic/home'>IBM</a>.\n Create an account using your Richfield student email-address.\nLogin with your new credentials and then go to courses.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"give me access to IBM": "In order to sign up for IBM, go to:<a href='https://www.ibm.com/academic/home'>IBM</a>.\n Create an account using your Richfield student email-address.\nLogin with your new credentials and then go to courses.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"how do I signup for IBM": "In order to sign up for IBM, go to:<a href='https://www.ibm.com/academic/home'>IBM</a>.\n Create an account using your Richfield student email-address.\nLogin with your new credentials and then go to courses.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"how do I sign up for IBM": "In order to sign up for IBM, go to:<a href='https://www.ibm.com/academic/home'>IBM</a>.\n Create an account using your Richfield student email-address.\nLogin with your new credentials and then go to courses.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"IBM": "In order to sign up for IBM, go to:<a href='https://www.ibm.com/academic/home'>IBM</a>.\n Create an account using your Richfield student email-address.\nLogin with your new credentials and then go to courses.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",

"how do I signup for salesforce courses": "In order to sign up for Salesforce courses, go to:<a href='https://trailhead.salesforce.com/users/strailhead/trailmixes/get-started-with-trailhead-end-user'>Salesforce</a>.\n Signup and then select the course you are interested in.\nYou can get any number of badges.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"salesforce": "In order to sign up for Salesforce courses, go to:<a href='https://trailhead.salesforce.com/users/strailhead/trailmixes/get-started-with-trailhead-end-user'>Salesforce</a>.\n Signup and then select the course you are interested in.\nYou can get any number of badges.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"how do i access salesforce": "In order to sign up for Salesforce courses, go to:<a href='https://trailhead.salesforce.com/users/strailhead/trailmixes/get-started-with-trailhead-end-user'>Salesforce</a>.\n Signup and then select the course you are interested in.\nYou can get any number of badges.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",
"how do i get access to salesforce": "In order to sign up for Salesforce courses, go to:<a href='https://trailhead.salesforce.com/users/strailhead/trailmixes/get-started-with-trailhead-end-user'>Salesforce</a>.\n Signup and then select the course you are interested in.\nYou can get any number of badges.\nYou can also contact: <u>stephen.akandwanaho@growth-ten.com</u>.\n<strong>Good Luck!</strong>",




"When is the induction and orientation": "Induction and orientation runs from 22 to 23 February 2024",
"When is the English and Maths bootcamps": "Maths and English bootcamps run from 19 to 21 Feb 2024",
"When is Career Expo": "Career Expo is scheduled for 10 June 2024",
"Which campus is ": "Career Expo is scheduled for 10 June 2024",
"What campus is ": "Career Expo is scheduled for 10 June 2024",
"Richfield's banking details ": "<strong>Please use these banking details</strong>.\nLegal Entity Name: Richfield Graduate Institute of Technology(Pty), \nTrading as: Null, Reg No: 2000/000752/07:Account Name: RGI DISTANCE LEARNING, Type: Cheque: Number: 201901692, Branch: Tongaat, Code: 057729, Date account opended: 20130117, Swift Code:SBZAZAJJ; Universal branch code:051001",
"When do classes start?": "29 July 2024. \n<strong>Richfield wishes you a successful semester ahead</strong>",
"When do lectures start?": "29 July 2024. \n<strong>Richfield wishes you a successful semester ahead</strong>",
"When do classes commence?": "29 July 2024. \n<strong>Richfield wishes you a successful semester ahead</strong>",
"When do lectures commence?": "29 July 2024. \n<strong>Richfield wishes you a successful semester ahead</strong>",
"When is mental wellness?": "Mental Wellness is on 9 october 2024",
"When is Enterpreneurship Week?": "Enterpreneurship Week runs from 2 April to 5 April 2025",
"When is the hackathon?": "Hackathon runs from 30 May to 31 May 2025",
"When does the hackathon take place?": "Hackathon runs from 30 May to 31 May 2025",
"hackathon": "Hackathon runs from 30 May to 31 May 2025",

"When is the coding bootcamp?": "Bootcamps for first semester run from 15 to 16th April 2025",
"When are the bootcamps?": "Bootcamps for the second semester will take place on 4th October 2024",
"When are the boot camps?": "Bootcamps for the second semester will take place on 4th October 2024",
"What qualifications does Richfield offer": "Please find all this information and more on: <a href='https://www.richfield.ac.za/'> Richfield Website</a> ",
"Which qualifications does Richfield offer": "Please find all this information and more on: <a href='https://www.richfield.ac.za/'>Richfield Website</a> ",
"How many Faculties does Richfield have?": "Richfield has 2 Faculties: Faculty of IT and Faculty of Business and Management Sciences",
"Which Faculties does Richfield have?": "Richfield has 2 Faculties: Faculty of IT and Faculty of Business and Management Sciences",



"If I articulate to BSc IT from a Diploma, what will be the duration?": "You will take approximately 1 year to complete your BSc IT degree",
"If I complete the articulation to BSc IT what will reflect on my certificate?": "After completion of your BSc IT articulation you will have a bachelor's degree.",
"Will I be able to change the elective completed in my diploma when articulation to BSc IT?": "Unfortunately, you will not be able to change your elective.",
"If I get credited modules for articulation BSc IT would it be financial or academic credits?": "Articulation has a set price, therefore it is academic credit not financial credit.",
"How many modules do I need to complete to obtain my BSc IT?": "You will need to complete the modules as per the syllabus provided and electives registered.",
"After completion of badges or industry courses will I receive a certificate?": "You will receive a badge and certificate of completion and can be completed at your own pace.",
"Can I change my elective in Year 3?": "No.The elective that is chosen in Year 2 needs to be continued in Year 3.",
"Can they submit the IT project phases without the Software development system?": "Unfortunately not, you will need to have a running system to support your project phases.",
"After completing my qualification will I receive the certificate immediately?": "Unfortunately not, you get your certificate after graduation.",
"Is IT project and WIL compulsory?": "Yes, without completing your IT project and WIL you will not be able to graduate which will leave your qualification incomplete.",
"Whom can I contact about my fee statement?": "Contact your administrator to see which arrangement was chosen(upfront or 11 months).",
"How do we access our study guides?": "You will be able to access your study guide on Moodle. An electronic copy is provided to you via Moodle.",
"How do I access my study guide?": "You will be able to access your study guide on Moodle. An electronic copy is provided to you via Moodle.",
"How can I get my study guide?": "You will be able to access your study guide on Moodle. An electronic copy is provided to you via Moodle.",
"Where can I access my Workshops?": "You will be able to access your workshops on Ms Teams with your student login.",
"Workshop access": "You will be able to access your workshops on Ms Teams with your student login.",
"Where can I get the academic calendar?": "Your academic calendar has been sent to you by your administrator. If you do not have a copy, please contact your administrator.",
"If I am a Mid Year student, which semester do I follow on the academic calendar?": "You will follow the semester 1 dates on the academic calendar.",
"If I need to register for the next academic year, whom do I contact?": "You will need to contact your administrator. Your administrator will provide you with all documents required.",
"To register for the next academic year, whom do I contact?": "You will need to contact your administrator. Your administrator will provide you with all documents required.",
"Where will I be able to access my outstanding fee statement?": "You will be able to access the following via iEnabler.",
"How do I access my academic transcript with a stamp?": "You will be able to access your academic transcript on iEnabler under student enquiries.",
"If I am unable to submit the assignment, whom do I contact?": "Please contact your administrator for assistance on assignment submission",
"I am unable to submit the assignment": "Please contact your campus manager",
"I cannot submit the assignment": "Please contact your administrator for assistance on assignment submission",
"Where do I submit my assessments ?": "As a distance learning student you will need to submit via the moodle platform",
"How do I submit my assignments?": "As a distance learning student you will need to submit via the moodle platform",
"How many assessments do I complete?": "As a contact student you will need to complete 1 Assignment, 1 Online Test & 1 Online Examination. Good luck!",
"How many assessments?": "As a contact learning student you will need to complete 1 Assignment, 1 Online Test & 1 Online Examination. Good luck!",
"Who is the manager IT in Distance Learning?": "Jenitha Kara (jenithak@richfield.ac.za)",
"Who is the manager IT?": "Jenitha Kara (jenithak@richfield.ac.za)",
"Who is the manager BMS?": "Saphokazi Nxokweni(saphokazin@richfield.ac.za)",
"What is Lockdown Browser?": "Lockdown Browser is a proctoring software that Richfield uses to ensure assessments are safe for students. It identifies and prevents unauthorized access to other applications and websites during assessments. If your lockdown browser is not working after installation or in the middle of an assessment, please close and reopen your lockdown browser. If the problem still persists, please contact your distance leaning administrator. Good luck!",
"Lockdown Browser": "Lockdown Browser is a proctoring software that Richfield uses to ensure assessments are safe for students. \nIt identifies and prevents unauthorized access to other applications and websites during assessments. \nIf your lockdown browser is not working after installation or in the middle of an assessment, please close and reopen your lockdown browser. If the problem still persists, please contact your distance leaning administrator. Good luck!",
"Proctoring": "Lockdown Browser is a proctoring software that Richfield uses to ensure assessments are safe for students. \nIt identifies and prevents unauthorized access to other applications and websites during assessments. \nIf your lockdown browser is not working after installation or in the middle of an assessment, please close and reopen your lockdown browser. If the problem still persists, please contact your distance leaning administrator. Good luck!",
"Proctor": "Lockdown Browser is a proctoring software that Richfield uses to ensure assessments are safe for students. \nIt identifies and prevents unauthorized access to other applications and websites during assessments. \nIf your lockdown browser is not working after installation or in the middle of an assessment, please close and reopen your lockdown browser. If the problem still persists, please contact your distance leaning administrator. Good luck!",
"Proctored": "Lockdown Browser is a proctoring software that Richfield uses to ensure assessments are safe for students. \nIt identifies and prevents unauthorized access to other applications and websites during assessments. \nIf your lockdown browser is not working after installation or in the middle of an assessment, please close and reopen your lockdown browser. If the problem still persists, please contact your distance leaning administrator. Good luck!",
"How are my marks calculated": "Your marks are calculated as follows. Test: 50%, Assignment: 50%: Test and assignment are combined to Full Period Mark and calculated out of 40%. Exam is out of 60%. The final mark marks comes from full period mark and exam. You must obtain 40% and above in the full period mark to be eligible for exams. Good luck!",
"Weighting": "Your marks are calculated as follows. Test: 50%, Assignment: 50%: Test and assignment are combined to Full Period Mark and calculated out of 40%. Exam is out of 60%. The final mark marks comes from full period mark and exam. You must obtain 40% and above in the full period mark to be eligible for exams. Good luck!",
"Format of assignments": "Assignments must be uploaded on Moodle in PDF format.",
"Can I change from distance to contact?": "Yes, you can switch from distance to contact. Please contact your administrator to fill out the necessary documentation",
"Who is the manager MBA?": "Trusha Singh(trushas@richfield.ac.za)",
"Can I change my course?": "Yes, you can change your course. Please contact your administrator to fill out the necessary documentation",
"Who is the manager Postgraduate?": "Trusha Singh(trushas@richfield.ac.za)",
"Who is the manager BScHons?": "Trusha Singh(trushas@richfield.ac.za)",
"Who is the manager Hons?": "Trusha Singh(trushas@richfield.ac.za)",
"Who is the manager PGDM?": "Trusha Singh(trushas@richfield.ac.za)",
"How do I access Moodle": "Please access Moodle via this link:<a href='https://learning.richfield.ac.za/'> Student Moodle</a>",
"How do I access ienabler": "Please access ienabler via this link:<a href='https://rgitie.richfield.ac.za/pls/rgitp/w99pkg.mi_login'>Student iEnabler</a>",
"How do I access Library Resources?": "Library resources are accessed via Moodle.",

"Is Richfield recognised internationally?": "Richfield’s programmes are registered by SAQA which ensures international comparability.\nApplication to any institution nationally and internationally is subject to that institution’s own rules and regulations. \nMany of our students have pursued studies at national and international public institutions.",
"international recognition": "Richfield’s programmes are registered by SAQA which ensures international comparability.\nApplication to any institution nationally and internationally is subject to that institution’s own rules and regulations. \nMany of our students have pursued studies at national and international public institutions.",
"Who is the manager Postgraduate Diploma in Management?": "Trusha Singh(trushas@richfield.ac.za)",
"Who is eligible for supplementary examinations?": "Students that obtained 40-47% in the main exam (final mark) are eligible for supplementary examinations.",
"What is the cost of supplementary exam": "Supplementary fees cost R300",
"What is the cost of supp?": "Supplementary exam costs R300",
"How much does Supp exam cost?": "Supplementary exam costs R300",
"Supp fee?": "Supplementary exam costs R300",
"Richfield campuses": "<strong>Richfield campuses are as follows:</strong> \nPolokwane, \nNewtown in JHB, \n112 Long Street Cape Town, \nUmhlanga KZN, \nBryanston in JHB, \n291 Helen Joseph Pretoria, \nCenturion in JHB, \nMusgrave KZN, \nDistance Learning. \nYou can get more information from <a href='https://www.richfield.ac.za/'>Richfield website</a>. ",
"Richfield campus": "<strong>Richfield campuses are as follows:</strong> \nPolokwane, \nNewtown, \n112 Long Street Cape Town, \nUmhlanga KZN, \nBryanston in JHB, \n291 Helen Joseph Pretoria, \nCenturion in JHB, \nMusgrave KZN, \nDistance Learning. \nYou can get more information from <a href='https://www.richfield.ac.za/'>Richfield website</a>.",
"Where is Umhlanga Campus": "Centenary Boulevard, Park Square, 5-9 Park Avenue, Umhlanga",
"What are the different payment plan options toward my fees?": "Payment Options are: 11 Months and Upfront",
"What are the electives for Bachelor of Commerce?": "The electives for Bachelor of Commerce are: \nMarketing Management, Human Resource Management and Accounting. \n<strong>Choose only ONE!</strong>",
"What are the electives for BCOM?": "The electives for Bachelor of Commerce are: \nMarketing Management, Human Resource Management and Accounting. \n<strong>Choose only ONE!</strong>",

"What are the electives for Bachelor of Business Administration?": "The electives for BBA are: \nMarketing Management, Human Resource Management, Supply Chain Management and Accounting. \n<strong>Choose only ONE!</strong>",
"What are the electives for BBA?": "The electives for BBA are: \nMarketing Management, Human Resource Management, Supply Chain Management and Accounting. \n<strong>Choose only ONE!</strong>",

"What are the electives for Diploma in Business Management?": "The electives for DBA are: \nEconomics, Human Resource Management, Public Management and Supply Chain Management. \n<strong>Choose only ONE!</strong>",
"What are the electives for DBA?": "The electives for DBA are: \nEconomics, Human Resource Management, Public Management and Supply Chain Management. \n<strong>Choose only ONE!</strong>",

"What are the electives for Postgraduate Diploma in Management?": "The electives for PGDM are: \nPublic Sector Management, Operations Management and Enterpreneurship and Innovation. \n<strong>Choose only ONE!</strong>",
"What are the electives for PGDM?": "The electives for PGDM are: \nPublic Sector Management, Operations Management and Enterpreneurship and Innovation. \n<strong>Choose only ONE!</strong>",
"What are the electives for BSc IT?": "The electives for BSc IT are: \nProgramming, Emerging Technologies, IT Management and Network Engineering. \n<strong>Choose only ONE!</strong>",
"What are the electives for IT?": "The electives for BSc IT are: \nProgramming, Emerging Technologies, IT Management and Network Engineering. \n<strong>Choose only ONE!</strong>",
"What are the electives for Diploma in IT?": "The electives for DIT are: \nProgramming, Business Analysis and Network Engineering. \n<strong>Choose only ONE!</strong>",
"What are the electives for DIT?": "The electives for DIT are: \nProgramming, Business Analysis and Network Engineering. \n<strong>Choose only ONE!</strong>",
"who are the campus managers": "<strong>Richfield Campus Managers details are as follows:</strong> \nPolokwane campus (Innocent Shivambu: innocents@richfield.ac.za), \nNewtown Johannesburg Campus (Sagi Murali: sagi@richfield.ac.za), \nCape Town Campus (Genee Griffiths:genee.griffiths@growth-ten.com),\nCenturion Campus (Michelle Van Gelder: michellev@richfield.ac.za),\nUmhlanga Durban Campus (Sharen Singh:sharens@richfield.ac.za), \nMusgrave Durban Campus (Neroshen Govender:nerosheng@richfield.ac.za), \nPretoria Campus (Radha Varre: radhav@richfield.ac.za), \nBryanston Johannesburg Campus (Genee Griffiths:genee.griffiths@growth-ten.com). ",
"who is the campus manager": "<strong>Richfield Campus Managers details are as follows:</strong> \nPolokwane campus (Innocent Shivambu: innocents@richfield.ac.za), \nNewtown Johannesburg Campus (Sagi Murali: sagi@richfield.ac.za), \nCape Town Campus (Genee Griffiths:genee.griffiths@growth-ten.com),\nCenturion Campus (Michelle Van Gelder: michellev@richfield.ac.za),\nUmhlanga Durban Campus (Sharen Singh:sharens@richfield.ac.za), \nMusgrave Durban Campus (Neroshen Govender:nerosheng@richfield.ac.za), \nPretoria Campus (Radha Varre: radhav@richfield.ac.za),\nBryanston Johannesburg Campus (Genee Griffiths:genee.griffiths@growth-ten.com). ",
"How can I learn about all the DL courses and qualifications offered?": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed on: <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>.",
"Richfield Offerings": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9).\nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"Richfield courses": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"Richfield qualifications": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"Richfield course": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"What courses does Richfield offer?": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"What programmes are offered by Richfield?": "<strong>Richfield is accredited to offer the following courses:</strong> \nBSc in Information Technology, \nDiploma in Information Technology, \nHigher Certificate in Information Technology, \n Higher Certificate in Computer Forensics, \nBachelor of Science Honours in Information Technology (NQF Level 8), \nBachelor of Commerce, \nBachelor of Business Administration, \nDiploma in Business Administration, \nDiploma in Local Government Management, \nBachelor of Public Management, \nHigher Certificate in Office Administration, \nBachelor of Commerce SAICA Pathways \nHigher Certificate in Recognition of Prior Learning, \nPostgraduate Diploma in Management (NQF Level 8), \nMaster of Business Administration (MBA, NQF Level 9). \nMore details about the programmes can be accessed via <a href='https://www.richfield.ac.za/prospectus-and-pricelist/'>Richfield website</a>",
"How do I attend workshops": "All DL workshops are hosted via MS teams classrooms. \nPlease ensure you have access to your MS Teams classrooms. \nIf you don't have access, please contact your administrator.  Good luck!",
"attend workshops": "All DL workshops are hosted via MS teams classrooms. \nPlease ensure you have access to your MS Teams classrooms. \nIf you don't have access, please contact your administrator.  Good luck!",

"Who are the Deans of Business and Management Sciences and IT?": "Dr Raj Tulsee(rajt@richfield.ac.za) is the Dean of BMS.\nDr Stephen Akandwanaho (stephen.akandwanaho@growth-ten.com) is the Dean of IT & Research",
"Who is the Dean of Business and Management Sciences?": "Dr Raj Tulsee(rajt@richfield.ac.za) is the Dean of BMS.",
"Who is the Dean of Information Technology?": "Dr Stephen Akandwanaho (stephen.akandwanaho@growth-ten.com) is the Dean of IT & Research.",
"Who is the Dean of IT?": "Dr Stephen Akandwanaho (stephen.akandwanaho@growth-ten.com) is the Dean of IT & Research.",
"Who is the Dean of BMS?": "Dr Raj Tulsee(rajt@richfield.ac.za) is the Dean of BMS Faculty.",

"What happens if I fail the mid-year exam?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",
"What happens if I fail exams?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",
"What happens if I fail exam?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",
"fail exam?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",
"learn coding?": "Please look out for the coding bootcamps that are scheduled for this semester. \nIf you are not sure of the dates, you can ask this bot when they are due.\nYou will be trained on coding and immerse yourself in the experience. \nYou can also use this website to study on coding: <a href='https://www.geeksforgeeks.org/how-to-learn-programming/'>Coding Website</a> ",
"How do I learn coding?": "Please look out for the coding bootcamps that are scheduled for this semester. \nIf you are not sure of the dates, you can ask this bot when they are due.\nYou will be trained on coding and immerse yourself in the experience. \nYou can also use this website to study on coding: <a href='https://www.geeksforgeeks.org/how-to-learn-programming/'>Coding Website</a> ",
"What happens if I fail the exam?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",
"What happens if I fail the exams?": "If your final mark is 40% and above, there is a chance for you to sit the supplementary exam. \nThe supplementary exam costs R500. \n<strong>Good Luck!</strong>",


"how much marks does assignment carry": "The assignment carries 50% and the test carries 50%.",
"what is the weighting for assignments": "The assignment carries 50% and the test carries 50%.",
"what is the weighting for assignment": "The assignment carries 50% and the test carries 50%.",
"what is the weighting for formative assessments": "The assignment carries 50% and the test carries 50%.\nBoth the assignment and test are converted to 40%.\nExam is out of 100% and then converted to 60%",
"what is the assessment weighting": "The assignment carries 50% and the test carries 50%.\nBoth the assignment and test are converted to 40%.\nExam is out of 100% and then converted to 60%",
"how are marks calculated?": "The assignment carries 50% and the test carries 50%.\nBoth the assignment and test are converted to 40%.\nExam is out of 100% and then converted to 60%",



"What is the policy on late submission of assignments": "The assignments must be submitted as per the due dates. \nAny submission 2 weeks after the due date will attract a penalty of 10% from the total assignment marks.\nNo submission will be accepted 2 weeks after the due date. Good Luck!",
"late submission of assignments": "The assignments must be submitted as per the due dates. \nAny submission 2 weeks after the due date will attract a penalty of 10% from the total assignment marks.\nNo submission will be accepted 2 weeks after the due date. Good Luck!",
"Can I submit the assignment after the due date?": "The assignments must be submitted as per the due dates. \nAny submission 2 weeks after the due date will attract a penalty of 10% from the total assignment marks.\nNo submission will be accepted 2 weeks after the due date. Good Luck!",
"Can assignments be submitted after due dates?": "The assignments must be submitted as per the due dates. \nAny submission 2 weeks after the due date will attract a penalty of 10% from the total assignment marks.\nNo submission will be accepted 2 weeks after the due date. Good Luck!",
"What if I submit the assignment after the due date?": "The assignments must be submitted as per the due dates. \nAny submission 2 weeks after the due date will attract a penalty of 10% from the total assignment marks.\nNo submission will be accepted 2 weeks after the due date. Good Luck!",

"how is the student performance evaluated?": "The student performance is evaluated based on the grades that the student obtains in the formative and summative assessments. \nThe weighting is 40% formative and 60% summative.\nThe student attendance and participation in class also have a bearing on the performance.",


"Who is the business analytics for Richfield": "Arshad Suliman (arshad.suliman@growth-ten.com)",
"Who is the head data analytics for Richfield ": "Arshad Suliman (arshad.suliman@growth-ten.com)",


"My email is not working": "If your e-mail is not working, go to <a href='https://www.office.com/'>Office.com</a> \nUse your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"I cannot access my email": "If your e-mail is not working, go to <a href='https://www.office.com/'>Office.com</a>\nUse your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"How do I access my e-mail": "To access your e-mail, go to <a href='https://www.office.com/'>Office.com</a> use your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"How do I access my email": "To access your e-mail, go to <a href='https://www.office.com/'>Office.com</a> use your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"I cannot access my e-mail": "If your e-mail is not working, go to <a href='https://www.office.com/'>Office.com</a>\nUse your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"I cannot get into my email": "If your e-mail is not working, go to <a href='https://www.office.com/'>Office.com</a>\nUse your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",
"My e-mail is not working": "If your e-mail is not working, go to <a href='https://www.office.com/'>Office.com</a>\nUse your studentnumber@my.richfield.ac.za. Password is: Richfield@2024 \nYou can also contact your administrator.",




"Where do I submit my proposal and concept": "If you are a postgraduate student, submit your research concept or proposal to Londiwes@richfield.ac.za.\nPlease copy stephen.akandwanaho@growth-ten.com",

"Where do I submit my concept?": "If you are a postgraduate student, submit your research concept or proposal to Londiwes@richfield.ac.za.\nPlease copy stephen.akandwanaho@growth-ten.com.\nIf you are not a postgraduate student, please contact your administrator.\nYou can ask me who your administrator is.",
"Where do I submit my proposal?": "If you are a postgraduate student, submit your research concept or proposal to Londiwes@richfield.ac.za.\nPlease copy stephen.akandwanaho@growth-ten.com.\nIf you are not a postgraduate student, please contact your administrator.\nYou can ask me who your administrator is.",
"Where do I submit my research proposal?": "If you are a postgraduate student, submit your research concept or proposal to Londiwes@richfield.ac.za.\nPlease c.c. stephen.akandwanaho@growth-ten.com.\nIf you are not a postgraduate student, please contact your administrator.\nYou can ask me who your administrator is.",

"What sections should be in a proposal?": "<strong>The postgraduate research proposal should have these sections:</strong>\nBackground,\nIntroduction,\nResearch Aim & Objectives,\nResearch Questions,\nLiterature Review,\nProblem Statement,\nHypothesis (Optional),\nSignficance of Study,\nResearch Timeframe,\nConclusion,\nReferences.\nEnsure that you consult many articles, books, journals and other sources. \nThe proposal should have more than 20 references.\nThe references should not be more than 5 years old.\n<strong>Good Luck!</strong>",
"How should a proposal be written?": "<strong>The postgraduate research proposal should have these sections:</strong>\nBackground,\nIntroduction,\nResearch Aim & Objectives,\nResearch Questions,\nLiterature Review,\nProblem Statement,\nHypothesis (Optional),\nSignficance of Study,\nResearch Timeframe,\nConclusion,\nReferences.\nEnsure that you consult many articles, books, journals and other sources. \nThe proposal should have more than 20 references.\nThe references should not be more than 5 years old.\n<strong>Good Luck!</strong>",
"Give me the structure of the proposal?": "<strong>The postgraduate research proposal should have these sections:</strong>\nBackground,\nIntroduction,\nResearch Aim & Objectives,\nResearch Questions,\nLiterature Review,\nProblem Statement,\nHypothesis (Optional),\nSignficance of Study,\nResearch Timeframe,\nConclusion,\nReferences.\nEnsure that you consult many articles, books, journals and other sources. \nThe proposal should have more than 20 references.\nThe references should not be more than 5 years old.\n<strong>Good Luck!</strong>",
"How is the proposal structured?": "<strong>The postgraduate research proposal should have these sections:</strong>\nBackground,\nIntroduction,\nResearch Aim & Objectives,\nResearch Questions,\nLiterature Review,\nProblem Statement,\nHypothesis (Optional),\nSignficance of Study,\nResearch Timeframe,\nConclusion,\nReferences.\nEnsure that you consult many articles, books, journals and other sources. \nThe proposal should have more than 20 references.\nThe references should not be more than 5 years old.\n<strong>Good Luck!</strong>",
"Give me sections of the proposal?": "<strong>The postgraduate research proposal should have these sections:</strong>\nBackground,\nIntroduction,\nResearch Aim & Objectives,\nResearch Questions,\nLiterature Review,\nProblem Statement,\nHypothesis (Optional),\nSignficance of Study,\nResearch Timeframe,\nConclusion,\nReferences.\nEnsure that you consult many articles, books, journals and other sources. \nThe proposal should have more than 20 references.\nThe references should not be more than 5 years old.\n<strong>Good Luck!</strong>",



"What chapters should be in a BSc Hons IT dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic).\n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"What chapters should be in a PGDM dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic).\n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"What chapters should be in a Postgraduate Diploma in Management dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic).\n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"Give me the structure of the BSc Hons IT dissertation": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic). \n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"Give me the structure of the Postgraduate Diploma in Management dissertation": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic). \n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"Give me the structure of the PGDM dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic). \n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"what is the structure of the PGDM dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic). \n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",
"what is the structure of the BSc Hons dissertation?": "The dissertation for PGDM & BSc Hons IT should have a minimum of 80 pages and a maximum of 120 pages.\n<strong>The dissertation should be structured as follows:</strong> \nThe preamble should have a Richfield Logo, Title Page (Topic, Fullname, Student Number, Course, Supervisor, Month and Year).\nAcknowledgements.\nDeclaration.\nList of Figures and Tables.\nAbbreviations.\nAbstract (100 words)\nTable of Contents (Automatic). \n<strong>The chapters for the main body are:</strong> \n<strong>Chapter 1:Introduction</strong>\nBackground\nIntroduction\nAim and Objectives\nResearch Objectives\nResearch Questions\nLiterature Review\nProblem Statement\nSignificance of Study\nHypothesis(Otional)\nTheoretical Framework\nStructure of the Dissertation\nConclusion\n<strong>Chapter 2:Literature Review</strong>\nUse a thematic approach\n<strong>Chapter 3: Problem Statement</strong>\nIntroduction\nProblem\nConclusion\n<strong>Chapter 4:Research Methodology</strong>\nIntroduction\nResearch Design\nTarget Population\nData Collection and Instrument used\nData Analysis\nEthical Consideration\nLimitations\nSummary\n<strong>Chapter 5:Presentation of Results</strong>\nIntroduction\nResponse Rate\nResults\nConclusion\n<strong>Chapter 6:Conclusion</strong>\nSummary\nMain Findings\nContributions\nImplications\nLimitations\nRecommendations\nSuggestions for future research\nReferences (Harvard Style).\nAppendices.\nEnsure that references are not more than 5 years old\n<strong>Good Luck!</strong>",


"when is the dissertation due?": "Please make sure you submit your dissertation before semester exams. \nRemember to send your dissertation to Dr Stephen (stephen.akandwanaho@growth-ten.com) to send for external proof-reading. The cost is only R2500. \nGood Luck!",
"what is the submission date for Dissertation?": "Please make sure you submit your dissertation before semester exams. \nRemember to send your dissertation to Dr Stephen (stephen.akandwanaho@growth-ten.com) to send for external proof-reading. The cost is only R2500. \nGood Luck!",
"Give me the due date for the dissertation": "Please make sure you submit your dissertation before semester exams. \nRemember to send your dissertation to Dr Stephen (stephen.akandwanaho@growth-ten.com) to send for external proof-reading. The cost is only R2500. \nGood Luck!",

"where do I submit my dissertation": "The dissertation must be submitted on <a href = 'https://learning.richfield.ac.za/HET/login/index.php'>Moodle</a>. \nRemember to send your dissertation to Dr Stephen (stephen.akandwanaho@growth-ten.com) to send for external proof-reading. The cost is only R2500. \nGood Luck!",
"How do I submit my dissertation": "The dissertation must be submitted on <a href = 'https://learning.richfield.ac.za/HET/login/index.php'>Moodle</a>. \nRemember to send your dissertation to Dr Stephen (stephen.akandwanaho@growth-ten.com) to send for external proof-reading. The cost is only R2500. \nGood Luck!",


"What is the extension due date for Dissertation chapters 1, 2 & 3": "The due date for chapters 1, 2 & 3 submission is 3rd October 2024. \n<strong>Good Luck!</strong> ",
"due date for Dissertation chapters 1, 2 & 3": "The due date for chapters 1, 2 & 3 submission is 3rd October 2024.\n<strong>Good Luck!</strong> ",
"when do we submit chapters 1, 2 & 3 of the dissertation": "The due date for chapters 1, 2 & 3 submission is 3rd October 2024.\n<strong>Good Luck!</strong> ",
"give me the due date for chapters 1, 2 & 3": "The due date for chapters 1, 2 & 3 submission is 3rd October 2024.\n<strong>Good Luck!</strong> ",


"Do you offer online classes?": "Yes, Richfield offers online classes via Distance Learning modality. \nPlease contact your administrator for details.",
"Does Richfield offer online classes?": "Yes, Richfield offers online classes via Distance Learning modality.\nPlease contact your administrator for details.",
"How can I get recordings?": "To get workshop recordings, go to your class on Teams and download the recording. \nPlease contact your administrator if you experience any difficulty. \n<strong>Good Luck!<strong>",
"How can I access class recordings?": "To get workshop recordings, go to your class on Teams and download the recording. \nPlease contact your administrator if you experience any difficulty. \n<strong>Good Luck!<strong>",
"How can I access workshop recordings?": "To get workshop recordings, go to your class on Teams and download the recording. \nPlease contact your administrator if you experience any difficulty. \n<strong>Good Luck!<strong>",

"recordings?": "To get workshop recordings, go to your class on Teams and download the recording. \nPlease contact your administrator if you experience any difficulty. \n<strong>Good Luck!<strong>",


"I cannot log onto Turnitin": "Please ensure you are using your Richfield student e-mail address to login and access your class on Turnitin. \nPlease contact nompumelelom@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com should you still be unable to use Turnitin. \n<strong>Good Luck!</strong>",
"I cannot access Turnitin": "Please ensure you are using your Richfield student e-mail address to login and access your class on Turnitin. \nPlease contact nompumelelom@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com should you still be unable to use Turnitin. \n<strong>Good Luck!</strong>",
"How do I access Turnitin": "Please ensure you are using your Richfield student e-mail address to login and access your class on Turnitin. \nPlease contact nompumelelom@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com should you still be unable to use Turnitin. \n<strong>Good Luck!</strong>",
"Give me ID and enrolment key for Turnitin": "Please ensure you are using your Richfield student e-mail address to login and access your class on Turnitin. \nPlease contact nompumelelom@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com should you still be unable to use Turnitin. \n<strong>Good Luck!</strong>",
"ID and enrolment key": "Please ensure you are using your Richfield student e-mail address to login and access your class on Turnitin. \nPlease contact nompumelelom@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com should you still be unable to use Turnitin. \n<strong>Good Luck!</strong>",


"Give me Moodle credentials": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"Moodle credentials": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"How do I access Moodle credentials": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"Give me Moodle access": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"I want Moodle credentials": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"How do I change my moodle password": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"change moodle password": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"my moodle password is not working": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"log into moodle": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"I cannot log into moodle": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"How do I reset my moodle password?": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"I cannot access moodle": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"I can't log into moodle": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",
"how do i get moodle login": "Moodle credentials are as follows:\n<strong>Username:</strong>[9-digit student number].\n<strong>Password:</strong>R1chfield#2024\nYou can access the portal on:<a href='https://learning.richfield.ac.za/HET'>Moodle</a>.\nYou will be forced to change your password once you use the above credentials. \nPlease follow the steps to change your password, \nyou will then see all registered modules on your dashboard.\n<strong>Good Luck!</strong>",



"where do I submit my topic?": "Please submit your research topic to londiwes@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"how do I submit the topic?": "Please submit your research topic to londiwes@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"where do I submit my research topic?": "Please submit your research topic to londiwes@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",
"how do I submit my research topic?": "Please submit your research topic to londiwes@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.\n<strong>Good Luck!</strong>",


"Who can help me with my IT issue?": "If you have a technical problem with your computer, operating system (Microsoft) or anything IT related, please contact:vinoliam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.",
"Whom can i contact about my laptop": "If you have a technical problem with your computer, operating system (Microsoft) or anything IT related, please contact:vinoliam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.",
"who is the IT guy?": "If you have a technical problem with your computer, operating system (Microsoft) or anything IT related, please contact:vinoliam@richfield.ac.za and cc stephen.akandwanaho@growth-ten.com.",


"When is the entrepreneurship week?": "The enterpreneurship week runs from 02 April to 05 April 2025. \nThis is an opportunity for students to showcase their innovations and attract funding.\nPitch presentations will be attended by industry representatives who will determine the viability and creativity of your innovation.\nPlease ensure that your ideas are aimed to solve an intractable problem in industry. \nSend your details to your administrator for consideration. \n<strong>Good Luck!</strong>",
"How do i take part in the entrepreneurship week?": "The enterpreneurship week runs from 02 April to 05 April 2025. \nThis is an opportunity for students to showcase their innovations and attract funding.\nPitch presentations will be attended by industry representatives who will determine the viability and creativity of your innovation.\nPlease ensure that your ideas are aimed to solve an intractable problem in industry. \nSend your details to your administrator for consideration. \n<strong>Good Luck!</strong>",
"entrepreneurship week?": "The enterpreneurship week runs from 02 April to 05 April 2025. \nThis is an opportunity for students to showcase their innovations and attract funding.\nPitch presentations will be attended by industry representatives who will determine the viability and creativity of your innovation.\nPlease ensure that your ideas are aimed to solve an intractable problem in industry. \nSend your details to your administrator. \n<strong>Good Luck!</strong>",
"Who takes part in the entrepreneurship week?": "The enterpreneurship week runs from 02 April to 05 April 2025. \nThis is an opportunity for students to showcase their innovations and attract funding.\nPitch presentations will be attended by industry representatives who will determine the viability and creativity of your innovation.\nPlease ensure that your ideas are aimed to solve an intractable problem in industry. \nSend your details to your administrator. \n<strong>Good Luck!</strong>",


"How does one qualify to graduate?": "To qualify for graduation, the below requirements must be met: \nAll modules must be successfully completed. \nFees must be paid up. \nWIL/Dissertation/ IT project must be submitted and marked.",
"Do I qualify to graduate?": "To qualify for graduation, the below requirements must be met: \nAll modules must be successfully completed. \nFees must be paid up. \nWIL/Dissertation/ IT project must be submitted and marked.",
"How do I qualify to graduate?": "To qualify for graduation, the below requirements must be met: \nAll modules must be successfully completed. \nFees must be paid up. \nWIL/Dissertation/ IT project must be submitted and marked.",
"Who graduates?": "To qualify for graduation, the below requirements must be met: \nAll modules must be successfully completed. \nFees must be paid up. \nWIL/Dissertation/ IT project must be submitted and marked.",
"who is eligible for graduation?": "To qualify for graduation, the below requirements must be met: \nAll modules must be successfully completed. \nFees must be paid up. \nWIL/Dissertation/ IT project must be submitted and marked.",

"How do I apply for richfield bursary": "You can apply for the richfield bursary using this link <a href='https://www.richfield.ac.za/bursaries/'>Richfield Bursary</a>.\n<strong>Good Luck!<strong>",
"richfield bursary": "You can apply for the richfield bursary using this link <a href='https://www.richfield.ac.za/bursaries/'>Richfield Bursary</a>.\n<strong>Good Luck!<strong>",
"bursary": "You can apply for the richfield bursary using this link <a href='https://www.richfield.ac.za/bursaries/'>Richfield Bursary</a>.\n<strong>Good Luck!<strong>",



"How do I submit my assignments on Moodle?": "First you must convert the word document to pdf. \nLogin to Moodle, Go to the module you want to submit/upload. \nScroll to Assignment and there will be a section that shows you can submit. \nFollow the steps there and submit.",

"Is There any cash transactions allowed on campus?":"No cash transactions are allowed on campus.",
"Who are the senior lecturers for my campus?": "We need to list the senior lecturer’s names with the campuses.",

"Who is the Campus Administrator at the Musgrave Campus?": "Mrs Simone Govender.",
"Who is the Campus Manager at the Musgrave Campus?": "Mr Neroshen Govender.",
"Who is the IT Technician at the Musgrave Campus?": "Mr Preven Naidoo.",
"Who is my lecturer for Fundamentals of Accounting?": "Mr Bonginkosi Ngcobo.",
"Who is my lecturer for Accounting 511?": "Mr Bonginkosi Ngcobo.",
"Who is my lecturer for Auditing and Assurance?": "Mr Bonginkosi Ngcobo.",
"Who is my lecturer for Information Systems in Business Studies?": "Mr Bonginkosi \n Ngcobo.",
"Who is my lecturer for Taxation?": "Mr Bonginkosi Ngcobo.",
"Who is my lecturer for Auditing and Assurance?": "Mr Bonginkosi Ngcobo.",
"Who is my lecturer for Supply Chain Management?": "Mr Russell Makhanya.",
"Who is my lecturer for Total Quality Management 731?": "Mr Russell Makhanya.",




"How do I access the electronic Richfield library?": "You can access the electronic library through Moodle using your student credentials. \n Navigate to the library section to search for resources, \n journals, and databases. \nIf you are still failing to get what you are looking for, please ask for assistance from your Campus Librarian.",
"How do I do reference?": "Richfield offers guidance using Harvard referencing style. \nYou can find referencing guides and support materials in the library or through academic support services.",
"is the campus open on Saturdays?": "Yes, the Richfield campuses are open on Saturdays. \nThey open at 07h45 and close at 13h00.",
"How do I know if my assignment has been submitted?": "After submitting your assignment on Moodle, \nyou should receive a confirmation message or email indicating that it has been successfully submitted. \n You can also check your submission history on Moodle.",
"What do I do when my assignment did not upload correctly?": "If your assignment fails to upload correctly, \ntry re-submitting it. \nIf the issue persists, contact your lecturer or\n the IT support for assistance.",

"What do I do if I have submitted the incorrect assignment?": "Contact your lecturer immediately to explain the situation and request guidance on how to proceed.",
"Where do I find my student card?": "Richfield offers virtual student cards, and these are accessible through I enabler. But should you require a physical student card, \n you need to talk to your Campus Manager or Campus Administrator and a R100 fee is required.",
"I cannot access the turnstiles. Who do I go to for help?": "Contact the campus security office or the administration office for assistance with accessing the turnstiles.",
"What do I do if I miss an assessment?": "Contact your Lecturer or Campus Manager as soon as possible to explain the circumstances. \n They can advise you on the next steps and any possible implications.",
"Where do I find the banking details to pay my fees?": "You can find the banking details for fee payments on the Richfield website, \n on the Richfield’s marketing flyer or leaflet or by contacting Sales or Finance department directly.",
"What do I do if I cannot pay my fees this month?": "Contact your Campus Manager or Campus Administrator to discuss your situation and explore possible options for payment arrangements or financial assistance.",


"Who is my student adviser?": "Your student adviser or academic mentor is typically assigned to you upon enrolment. \n Contact your Regional Sales Manager for information on your adviser.",
"How do I apply for admission?": "You can apply for admission to Richfield Graduate Institute of Technology online through the admissions portal on the Richfield’s official website or you can visit your nearest Richfield Campus.",

"What resources are available for academic support?": "Richfield offers various academic support services, including tutoring, \nstudy groups, and workshops.",
"What are the application deadlines?": "Application deadlines vary depending on the programme and intake. \n Check the Richfield website or contact the Sales department for specific deadlines.",
"What financial aid options are available?": "Richfield offers various financial aid options, including bursaries, and student loans. \n Contact the financial aid office for information on available options and eligibility criteria.",
"What career opportunities are available for IT or business qualifications?": "Graduates of IT or Business programmes from Richfield have opportunities in various industries, \n including technology firms, \n finance, \n consulting, and entrepreneurship.",

"What are the entry requirements for programmes in the Faculty of Information Technology?": "Entry requirements vary depending on the programme. \n Check the Richfield website or contact admissions for specific entry requirements.",
"Can I apply for an IT programme if I don't have a background in IT?": "Yes, some IT programmes at Richfield may accept students without a background in IT. \n Check the programme requirements or Regional Sales Manager or Sales Advisors for guidance.",
"What career opportunities are available after completing programmes in the Faculty of Information Technology?": "Graduates of IT programs at Richfield have opportunities in roles such as software developer, \n network administrator, cybersecurity analyst, and IT consultant.",
"Do I need prior coding experience for programmes like Programming and Emerging Technologies?": "Prior coding experience may be beneficial but is not always \n required. \n Programming and Emerging Technologies programmes at Richfield provide instruction \n from foundational to advanced coding skills.",
"Are there opportunities for practical experience or internships during the program?": "Yes, Richfield encourages students to participate in practical experience  (Work Integrated Learning) as part of their programme.",
"Can I pursue postgraduate studies after completing undergraduate programs?": "Yes, Richfield offers postgraduate programmes for students who have completed undergraduate programmes. \n Check the Richfield website or contact Regional Sales Manager or Sales Advisors for guidance for information on postgraduate offerings.",
"What support services are available for students within the faculties at our institution?": "Richfield offers various support services, including academic advising, counselling, disability services, and career development. \n Contact your campus manager, lecturer, Regional Sales Manager or Sales Advisors for guidance.",
"Are there opportunities for international students to study at Richfield?": "Yes, Richfield welcomes international students and offers support services tailored to their needs. \n Contact the international student office or admissions for information on international student admissions.",
"What is the process for changing a major or program of study?": "You can contact your campus manager, campus administrator, regional sale manager or student advisors for assistance with this.",

"I am transferring from another tertiary institution. How do I apply for subject module credits?": "You can contact your campus manager or campus administrator for assistance with this. \n<strong>Welcome to Richfield!<strong>",


"What is the cost of adding modules or discontinuing my qualification?": "You can contact your campus manager, campus administrator, regional sale manager or student advisors for assistance with this.",
"How do I make an arrangement for outstanding fees?": "Please contact your Campus Manager or Campus Administrator to discuss your situation and explore possible options for payment arrangements or financial assistance.\n<strong>Good Luck!<strong>",
"Are there health services available on campus?": "Yes, Richfield typically provides health services on campus to support the well-being of its students and staff. These health services include: \nSickbay: The campuses have sickbay for both staff or students who are too ill, or who require medical attention. \n Counselling Services: Mental health counselling services may be available on campus to provide support for students dealing with stress, anxiety, depression, or other mental health issues. \n Health Education Workshops: The institution may offer health education workshops or talks on topics such as good health, nutrition, or fitness.",



"how many failed modules can I carry to another year?": "You are only allowed to carry a maximum of 2 failed modules to another year.",
"If I am carrying 1st year modules, am I allowed to continue to 2nd year?": "You are only allowed to carry a maximum of 2 failed modules to another year.",

"Do we have a semester break?": "Yes. The semester break for mid-year is 23 September to 27 September 2024.\n<strong>Enjoy your break</strong>",
"semester break?": "The semester break for mid-year is 23 September to 27 September 2024.\n<strong>Enjoy your break</strong>",
"Do we offer extramural activities?": "Please check with your campus manager.",
"Are there any security cameras around campus?": "Yes. There are security cameras around the campus",
"How influential is SRC?": "Richfield has a strong SRC body. \nEach campus has an active SRC committee and participates in the insitution's decisiona making processes.",
"does richfield have SRC?": "Richfield has a strong SRC body. \nEach campus has an active SRC committee and participates in the insitution's decisiona making processes.",
"is there SRC?": "Richfield has a strong SRC body. \nEach campus has an active SRC committee and participates in the insitution's decisiona making processes.",
"SRC": "Richfield has a strong SRC body. \nEach campus has an active SRC committee and participates in the insitution's decisiona making processes.",



"SEB": "The SEB is the proctoring software that we use for all our assessments, for both distance and contact learning students. \nIt contains facial detection and video analytics capabilities.\n You can download the guide from this site by navigating to the top right corner, just after the ‘Pay Fees’ link, where you will find the download link.”.",
"Safe Exam Browser": "The SEB is the proctoring software that we use for all our assessments, for both distance and contact learning students. \nIt contains facial detection and video analytics capabilities.\n You can download the guide from this site by navigating to the top right corner, just after the ‘Pay Fees’ link, where you will find the download link.”.",
"proctoring software": "The SEB is the proctoring software that we use for all our assessments, for both distance and contact learning students. \nIt contains facial detection and video analytics capabilities.\n You can download the guide from this site by navigating to the top right corner, just after the ‘Pay Fees’ link, where you will find the download link.”.",
"proctoring tool": "The SEB is the proctoring software that we use for all our assessments, for both distance and contact learning students. \nIt contains facial detection and video analytics capabilities.\n You can download the guide from this site by navigating to the top right corner, just after the ‘Pay Fees’ link, where you will find the download link.”.",






}

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(list(faqs.keys()))


def get_answer(user_question):
    # Lowercase the user question for case-insensitive matching
    lower_question = user_question.lower()

    # Define keywords or phrases that indicate the user is asking for an admin or assistance
    admin_keywords = ["who is my admin", "get assistance", "assist", "who can help", "how can i be helped", "whom to contact", "contact", "who is my administrator","who can assist me", "administrator details","my administrator details"]

    # Check if any of the keywords or phrases are in the user's question
    if any(keyword in lower_question for keyword in admin_keywords):
        # Expanded structured response with a complete list of administrators
        admins = [
            {"name": "Khanyi Ngcobo", "email": "khanyisilen@richfield.ac.za", "responsibility": "BSc Year 2 Semester 3 & BSc Year 3"},
            {"name": "Sthembile Mpanza", "email": "smpanza@richfield.ac.za", "responsibility": "DIT Year 2 & 3"},
            {"name": "Zamakhanya Gcwabaza", "email": "zamakhanyaz@richfield.ac.za", "responsibility": "BSc Articulation and Year 2 Semester 4"},
            {"name": "Fortunate Sibiya", "email": "fortunaten@richfield.ac.za", "responsibility": "DIT Year 1"},
            {"name": "Ndumiso Mbambo", "email": "ndumisoN@richfied.ac.za", "responsibility": "HCIT & HCCF Year 1"},
            {"name": "Sihle Mthembu", "email": "sihlem@richfield.ac.za", "responsibility": "BSc Year 1 Full year reg (Jan reg)"},
            {"name": "Amiel Moodley", "email": "AmielM@richfield.ac.za", "responsibility": "BSc Year 1 Midyear reg (July reg)"},
            {"name": "Vinisha Sundarparsad", "email": "vinishas@richfield.ac.za", "responsibility": "BCOM 1st year/BBA ART/PDAB"},
            {"name": "Shorne Mdadane", "email": "mdadanen@richfield.ac.za", "responsibility": "DBA"},
            {"name": "Simangele Ndimande", "email": "sndimande@richfield.ac.za", "responsibility": "HCBA"},
            {"name": "Cynthia Mtshali", "email": "czakwe@richfield.ac.za", "responsibility": "BCOM Year 2/3"},
            {"name": "Nerisha Baldeo", "email": "nerisha@richfield.ac.za", "responsibility": "BPM/DLGM/HCLGM"},
            {"name": "Lethokuhle Msweli", "email": "lethokuhlem@richfield.ac.za", "responsibility": "BBA 1st Year/ BBA ART"},
            {"name": "Nicole Zondi", "email": "nicolez@richfield.ac.za", "responsibility": "BBA 2nd/3rd year"},
            {"name": "Urisha Roopnund", "email": "UrishaR@richfield.ac.za", "responsibility": "MBA"},
            {"name": "Nompumelelo Mjwara", "email": "NompumeleloM@richfield.ac.za", "responsibility": "PGDM, BSc Hons"},
            # Ensure all names and email addresses are accurate and up to date
        ]
        return {"type": "admin_list", "data": admins}

    elif lower_question in ["give me the class timetable", "give me my class timetable", "how do i get my timetable",
                            "class timetable", "give me class timetable","give me a workshop timetable", "give me a class timetable", "workshop timetable","give me the workshop timetable","give me my workshop timetables", "workshop timetables", "give me my timetable","timetable"]:

        timetable_data = [
            {"MODULES": "Quantitative Techniques 600", "SEMESTER": "S1", "LECTURER": "Silas Toperesu",
             "DATE": "16th March 2024", "TIME": "11:30"},
            {"MODULES": "Software Engineering 600", "SEMESTER": "S1", "LECTURER": "Eugene Innocent",
             "DATE": "16th March 2024", "TIME": "08:30"},
            {"MODULES": "Networks 631", "SEMESTER": "S1", "LECTURER": "Njabulo Mavundla", "DATE": "16th March 2024",
             "TIME": "09:30"},
            {"MODULES": "Programming 631", "SEMESTER": "S1", "LECTURER": "Raymond Shamba", "DATE": "16th March 2024",
             "TIME": "10:30"},
            {"MODULES": "Operating Systems 600", "SEMESTER": "S2", "LECTURER": "Taelo Molefe", "DATE": "16th March 2024",
             "TIME": "08:30"},
            {"MODULES": "Networks 632", "SEMESTER": "S2", "LECTURER": "Njabulo Mavundla", "DATE": "16th March 2024",
             "TIME": "12:30"},
            {"MODULES": "Programming 632", "SEMESTER": "S2", "LECTURER": "Raymond Shamba", "DATE": "16th March 2024",
             "TIME": "11:30"}
        ]

    # Assuming the return statement is part of a larger function, adjust as necessary for your context.
        return {"type": "timetable", "data": timetable_data}

    elif lower_question in ["give me 2024 graduation dates","When is 2024 graduation and what are the times","When is the graduation ceremony","2024 graduation","give me graduation dates","graduation dates","when is graduation for 2024","when is graduation for 2024?","when is graduation?","graduation venue","where is graduation in 2024","where is 2024 graduation?","when is 2024 graduation?","where is graduation","give me dates for 2024 graduation","when is graduation","when is 2024 graduation","where will 2024 graduation take place","where will 2024 graduation take place?","where will graduation take place in 2024?","where will graduation take place in 2024?","where will graduation take place","when is graduation 2024", "graduation dates 2024","when are graduations","when are 2024 graduations"]:

        graduation_data = [
        {"event": "Richfield CapeTown", "date": "04-05-2025", "venue": "Fountains Hotel"},
        {"event": "Johannesburg", "date": "11-05-2025", "venue": "Linder Auditorium"},
        {"event": "KwaZulu-Natal", "date": "18-05-2025", "venue": "Greyville Race Course"},
        {"event": "Pretoria", "date": "23-05-2025", "venue": "State Theatre"},
        {"event": "Polokwane", "date": "25-05-2025", "venue": "Merupa Sun"}

        ]

    # Assuming the return statement is part of a larger function, adjust as necessary for your context.
        return {"type": "graduation", "data": graduation_data}

    else:
        # Proceed with the original logic if the question doesn't match the special cases
        user_question_vec = vectorizer.transform([user_question])
        cosine_similarities = cosine_similarity(user_question_vec, vectorizer.transform(list(faqs.keys())))

        threshold = 0.5  # Adjust this threshold value as needed

        if np.max(cosine_similarities) < threshold:
            return {"type": "text", "data": "Sorry, the answer for this question is not yet available."}

        else:
            most_similar_question_idx = np.argmax(cosine_similarities)
            return {"type": "text", "data": list(faqs.values())[most_similar_question_idx]}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_answer', methods=['POST'])
def answer():
    user_question = request.form.get('question', '')
    response = get_answer(user_question)

    # Check if the response is a dictionary and contains 'type'. If not, it's a regular FAQ answer
    if isinstance(response, dict) and 'type' in response:
        # For admin list or any other structured response
        answer_context = response
    else:
        # For regular FAQ answers
        answer_context = {"type": "text", "data": response}

    # Append the submitted answer to the global list
    if 'data' in answer_context:
        submitted_answers_form1.append(answer_context['data'])
    else:
        # If the answer context doesn't contain data, it means the response is not available
        answer_context = {"type": "text", "data": "Sorry, the answer for this question is not yet available."}

    return render_template('index.html', question=user_question, answer=answer_context)



@app.route('/get_admin_list', methods=['GET'])
def admin_list():
    response = get_answer(request.args.get('question', ''))
    if 'type' in response and response['type'] == 'admin_list':
        return jsonify(response['data'])
    else:
        return jsonify({"error": "No admin list available for this question."})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit-question', methods=['POST'])
def submit_question():
    # Extract the question from the form data
    question = request.form.get('unanswered_question')

    # Append the submitted question to the global list
    submitted_questions_form2.append(question)

    # Redirect back to the index page
    return redirect(url_for('index'))


@app.route('/feedback')
def feedback():
    return render_template('feedback.html', submitted_questions=submitted_questions_form2)


# @app.route('/admin-view')
# def admin_view():
#  return render_template('feedback.html', submitted_questions=submitted_questions)

"""
@app.route('/admin-view', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'POST':
        submitted_password = request.form.get('password')
        if submitted_password == 'execdean8':
            return render_template('feedback.html', submitted_questions=submitted_questions_form2)
        else:
            return redirect(url_for('incorrect_password'))
    return render_template('feedback.html', password_prompt=True)


@app.route('/incorrect-password')
def incorrect_password():
    return render_template('incorrect_password.html')


# Route for admin view
@app.route('/admin-view-form1', methods=['GET', 'POST'])
def admin_view_form1():
    password_correct = False
    website_access_data = {}

    if request.method == 'POST':
        submitted_password = request.form.get('password')
        if submitted_password == 'execdean9':
            password_correct = True
            # Retrieve access data
            website_access_data = get_access_data()
        else:
            return redirect(url_for('incorrect_password'))

    return render_template('admin_view.html', password_correct=password_correct,
                           website_access_data=website_access_data, submitted_answers=submitted_answers_form1)


# Function to retrieve access data
def get_access_data():
    global access_count
    requested_url = request.url
    if requested_url.startswith('https://richfield.onrender.com'):
        access_count += 1
    return {'count': access_count, 'date': datetime.now().strftime('%Y-%m-%d')}

"""

@app.route('/api/faq')
def get_faq_data():
    # Return the actual FAQ data
    return jsonify(faqs)







if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=8000)