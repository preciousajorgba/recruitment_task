import csv
import json
from hashlib import sha256


sum = 0
start=0
end=19
dlist=[]
teams=[]
jsonfiles_list=[]
list_csv=[]
hash_list=[]
count=0


# define function for generating hash key
def shakey(jsonfile):
    dkey = sha256(jsonfile.encode('utf-8')).hexdigest()
    return dkey



#Open the original csv file and append each row as a dict to a list while taking count of the rows
with open('HNGi9_CSV.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for csv_customer in reader:
            dlist.append(csv_customer)
            count+=1

#create a 21 length list containg the names of the teams
for i in range(21):
    teams.append(dlist[sum]["TEAM NAMES"])
    sum = sum + 20

#using the list generated above, update the value of the "TEAMS NAMES" pair for each Team
for i in teams:
    for y in range(start,end+1):
        dlist[y]["TEAM NAMES"]=i
    start = start + 20
    end = end + 20
    
# Create a dict and append it as JSON Strings to a list
for dicts in dlist:
        if dicts["Series Number"].isnumeric():
            dict_customer = {
                "format":"CHIP-0007",
                "filename":dicts["Filename"],
                "name":dicts["Name"],
                "description":dicts["Description"],
                "minting_tool":dicts["TEAM NAMES"],
                "sensitive_content": False,
                "series_number":int(dicts["Series Number"]),
                "series_total":count,
                'attributes': dicts["Attributes"].replace(".",";").lower(),
                "UUID":dicts["UUID"],
                "hash":" ",
                "collection":{
                    "name":"Zuri NFT Tickets for Free Lunch",
                    "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                    "attributes": [
                            {
                                "type": "description",
                                "value": "Rewards for accomplishments during HNGi9"
                            }
                        ]
                }
                
            }           
            jsonfiles_list.append(json.dumps(dict_customer, indent=2))



# For each Json string, create a hash key and append it to a list which is then appended to each json string. Then create several JSON files that has a hash key-value pair 
for dfile in jsonfiles_list:
    filesha=shakey(dfile)
    hash_list.append(filesha)
    jfile=json.loads(dfile)
    jfile["hash"]= filesha
    filename=jfile["name"]+".json"
    json_string = json.dumps(jfile, indent=4)
    jsonfile=open(filename,"w")
    jsonfile.write(json_string)

# Create a new CSV File that  have a hash key column
with open('HNGi9_CSV.csv','r') as csvinput:
    with open('HNGi9_CSV.output .csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('HASH')
        all.append(row)

        for row, i in zip(reader,hash_list):
            row.append(i)
            all.append(row)

        writer.writerows(all)
