JHOVE DigiSpecs

\-Patrick Wadley



1. Run JHOVE and input this command:



jhove -h xml -k "*filelocation*" -o "*outputlocation\\filename.xml*"



2\. Paste the below python code into the terminal. Remember to enter the "input\_location\\filename.xml" and "output\_location\\filename.csv". You may have to launch python with the "python" command.



3\. You should see your (mostly) formatted digital specifications in the terminal, along with a non-formatted .csv file of the same data in our output location.



4\. Copy and paste the digispecs into your word processor or spreadsheet. Remove the file extensions with "find and replace" with an empty "replace" box.



5\. Edit formatting as necessary and look for errors before populating metadata worksheets.



..........................................................................................



from urllib.parse import unquote

import os

import xml.etree.ElementTree as ET

import csv



\# Do Not Forget to Add Filepaths!!!

xml\_file = r"input\_location\\filename.xml"

output\_csv = r"output\_location\\filname.csv"



\# JHOVE namespace

ns = {

&#x20;   "jhove": "http://schema.openpreservation.org/ois/xml/ns/jhove",

&#x20;   "mix": "http://www.loc.gov/mix/v20"

}



tree = ET.parse(xml\_file)

root = tree.getroot()



rows = \[]



\# Loop start

for rep in root.findall("jhove:repInfo", ns):

&#x20;   # Uri and filename isolation

&#x20;   uri = rep.get("uri")

&#x20;   filename = os.path.basename(unquote(uri))

&#x20;

&#x20;   # Filesize

&#x20;   size\_elem = rep.find("jhove:size", ns)

&#x20;   size = size\_elem.text if size\_elem is not None else ""

&#x20;

&#x20;   # Checksum

&#x20;   md5 = ""

&#x20;   checksums = rep.find("jhove:checksums", ns)



&#x20;   if checksums is not None:

&#x20;       for checksum in checksums.findall("jhove:checksum", ns):

&#x20;           if checksum.get("type") == "MD5":

&#x20;               md5 = checksum.text

&#x20;               break

&#x20;

&#x20;   # Width and Height

&#x20;   width\_elem = rep.find(".//mix:imageWidth", ns)

&#x20;   height\_elem = rep.find(".//mix:imageHeight", ns)



&#x20;   width = width\_elem.text if width\_elem is not None else ""

&#x20;   height = height\_elem.text if height\_elem is not None else ""

&#x20;

&#x20;   # Csv columns

&#x20;   rows.append(\[filename, size, width, height, md5])



with open(output\_csv, "w", newline="", encoding="utf-8") as f:

&#x20;   writer = csv.writer(f)

&#x20;   writer.writerow(\["Filename", "Size", "ImageWidth", "ImageHeight", "MD5"])

&#x20;   writer.writerows(rows)



\# User notification and formatted output

print(f"Extracted {len(rows)} records:")



for filename, size, width, height, md5 in rows:

&#x20;   print(f"{filename}: {size} bytes, {width} x {height}, MD5: {md5};")



..........................................................................................

*Deprecated*



1. Run JHOVE and input this command:



jhove -h xml -k "*filelocation*" -o "*outputlocation*"



2\. Then run the below python code in the terminal. You may have to launch python with the "python" command.



3\. Find your resulting .csv file and open it in excel, it should delineate automatically, otherwise you can run "text to columns".



4\. Clean up the uri using "find and replace" with an empty "replace" box.



5\. Finish formatting as necessary.





import xml.etree.ElementTree as ET

import csv



xml\_file = r\*"filename"\*

output\_csv = r\*"output.\*csv"



\# JHOVE namespace

ns = {

&#x20;   "jhove": "http://schema.openpreservation.org/ois/xml/ns/jhove",

&#x20;   "mix": "http://www.loc.gov/mix/v20"

}



tree = ET.parse(xml\_file)

root = tree.getroot()



rows = \[]



for rep in root.findall("jhove:repInfo", ns):

&#x20;   uri = rep.get("uri")



&#x20;   size\_elem = rep.find("jhove:size", ns)

&#x20;   size = size\_elem.text if size\_elem is not None else ""



&#x20;   md5 = ""

&#x20;   checksums = rep.find("jhove:checksums", ns)



&#x20;   if checksums is not None:

&#x20;       for checksum in checksums.findall("jhove:checksum", ns):

&#x20;           if checksum.get("type") == "MD5":

&#x20;               md5 = checksum.text

&#x20;               break



&#x20;   width\_elem = rep.find(".//mix:imageWidth", ns)

&#x20;   height\_elem = rep.find(".//mix:imageHeight", ns)



&#x20;   width = width\_elem.text if width\_elem is not None else ""

&#x20;   height = height\_elem.text if height\_elem is not None else ""



&#x20;   rows.append(\[uri, size, width, height, md5])



with open(output\_csv, "w", newline="", encoding="utf-8") as f:

&#x20;   writer = csv.writer(f)

&#x20;   writer.writerow(\["uri", "size", "imageWidth", "imageHeight", "md5"])

&#x20;   writer.writerows(rows)



print(f"Extracted {len(rows)} records")

