# Script         : Markdown to Jekyll Converter
#                  Recursively reads a directory containing markdown files, and prepares them for upload to a Jekyll blog
#                  Designed to work with the output of wp2md (see https://github.com/jonbeckett/wp2md)
# Author         : Jonathan Beckett
# Compatibility  : Python 3.x
# Pre-Requisites : None

# path where markdown files reside
source_path = "c:\\projects\\md2jekyll\\md"
output_path = "c:\\projects\\md2jekyll\\output"

# random images to inject

image_urls = ["0gkw_9fy0eQ","4v9Kk01mEbY","jpkvklXwt98","d34DtRp1bqo","-m88z7ily-w","qTpc0Vj4YoE","03UCoidYvXw","DWyRC2juMgs","X6cChncECA8","9ZQzrLWV52M","7QCBakMyDCE","LuQ2ex5HY3c","vP3pnOoCiYE","ZYYS1kapOm8","dUPDhdeCN84","l7dbl-sUg3k","Pll7AP6NFpY","_nRpqIBM40Q","di8ognBauG0","2aFp6EWWs58"]

# Import modules
import os
import os.path
import time
import re
import random

def get_valid_filename(fn):
	fn = str(fn).strip()
	return re.sub(r'(?u)[^-\w\ ]', '', fn)

for subdir, dirs, files in sorted(os.walk(source_path)):
	for file in sorted(files):
		if '.md' in file and 'README.md' not in file:

			print("Processing " + file)
			
			# Read the file contents
			markdown_file_full_path = os.path.join(subdir, file)
			markdown_file = open(markdown_file_full_path,'r',encoding="latin-1")
			markdown_text = markdown_file.read()
			markdown_file.close()

			# split the line into files, and chop the top 4 off
			# (to get rid of the title and date, as output by wp2md)
			markdown_text_lines = markdown_text.splitlines()
			hybrid_text_lines = []
			hybrid_text_lines += markdown_text_lines[4:]
			
			# build the post title and body
			post_title = markdown_text_lines[0].replace('# ','')			
			post_body = '\r\n'.join(hybrid_text_lines)
			
			# replace any strange characters
			post_body = post_body.replace( u'\U0001f499', '')
			post_body = post_body.replace( u'\U0001f49a', '')
			post_body = post_body.replace( u'\U0001f49b', '')
			post_body = post_body.replace( u'\U0001f49c', '')
			post_body = post_body.replace( u'\U0001f633', '')
			post_body = post_body.replace( u'\u2018', u'\'')
			post_body = post_body.replace( u'\u2019', u'\'')
			post_body = post_body.replace( u'\u201c', u'\'')
			post_body = post_body.replace( u'\u201d', u'\'')
			post_body = post_body.replace( u'\u2013', '-')
			post_body = post_body.replace( u'\u2026', '...')
			post_body = post_body.replace( u'\u2033', '\'')
			post_body = post_body.replace( u'\u2032', '\'')
			post_body = post_body.replace( u'\xd7', 'x')
			post_body = post_body.replace( u'\xc2', ' ')

			post_body = post_body.replace( '\xe2\x80\x98', '\'') # single curly quote
			post_body = post_body.replace( '\xe2\x80\x99', '\'') # single curly quote
			post_body = post_body.replace( '\xe2\x80\x9c', '\"') # double curly quote
			post_body = post_body.replace( '\xe2\x80\x9d', '\"') # double curly quote
			post_body = post_body.replace( '\xe2\x80\x93', '-') # hyphen
			post_body = post_body.replace( '\xe2\x80\x94', '-') # hyphen
			post_body = post_body.replace( '\xe2\x80\xa6', '...') # elipses
			post_body = post_body.replace(r"\r\n", r"\n") # carriage return
			
			post_body = re.sub("\r\n","\n",post_body)
			

			# Extract the date from the filename
			# (so we may use it to back-date the post into write.as)
			year = file[0:4]
			month = file[5:7]
			day = file[8:10]
			post_date = year + '-' + month + '-' + day

			output_filename = os.path.join(output_path,year + "-" + month + "-" + day + "-" + get_valid_filename(post_title.replace(" ","-")).lower() + ".md")

			image_url = "https://source.unsplash.com/" + image_urls[random.randint(0,len(image_urls)-1)] + "/1600x900"


			# write the output for jekyll
			post_file = open(output_filename, "w")
			
			post_file.write("---\n")
			post_file.write("title: " + post_title + "\n")
			post_file.write("tags:\n")
			post_file.write("  - Life\n")
			post_file.write("header:\n")
			post_file.write("  teaser: " + image_url + "\n")
			post_file.write("  image: " + image_url + "\n")
			post_file.write("  image_description: " + post_title + "\n")
			post_file.write("---\n\n")
			post_file.write(post_body);
			
			post_file.close()
			
			
