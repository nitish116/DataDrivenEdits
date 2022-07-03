import os
import re
from pprint import pprint
import csv


def writeToCSV(fields, rows, filepath):
	with open(filepath, 'w') as csvfile: 
		csvwriter = csv.writer(csvfile) 
		csvwriter.writerow(fields) 
		csvwriter.writerows(rows)
		pass

def fetch_episode_details(filename):
	if len(filename.split('.')) > 5:
		SxEy = filename.split(".")[1]
		season = int(SxEy.split("e")[0].split("s")[1])
		episode = int(SxEy.split("e")[1])

		return {
			"season" : season,
			"episode" : episode,
		}
	else:
		SxEy = filename.split("-")[1].rstrip().strip()
		season = int(SxEy.split("x")[0])
		episode = int(SxEy.split("x")[1])
		return {
			"season" : season,
			"episode" : episode,
		}



data_dir = "data/"
cnt = 0

isTimeStamp = re.compile(r'\b-->\b')

def isIndexLine(cur_line):
	isIndex = re.compile(r'\d+$')
	return isIndex.match(cur_line)

def isTimeStampLine(cur_line):
	if "-->" in cur_line:
		return True
	return False


data = [] 
cur_index = -1
cur_timestamp = 'NONE'
cur_text = ''


fields = ["season","episode","index","timestamp","text"]
for cur_season_dir in os.listdir(data_dir):
	for cur_file in os.listdir(data_dir + "/" + cur_season_dir + "/"):
		if cur_file.split(".")[-1] == "srt":#cnt < 1:
			cur_file_path = data_dir + "/" + cur_season_dir + "/" + cur_file

			try:
				SE = fetch_episode_details(cur_file)
				season = SE["season"]
				episode = SE["episode"]
				print(SE)

			except Exception as e:
				print("could not fetch details ", cur_file)
			
			if 1:#season == 2:
			

				for cur_line in open(cur_file_path).readlines():
					if isIndexLine(cur_line):

						cur_index = int(cur_line)
						if cur_index!= -1:
							# data.append({
							# 	"season" : season,
							# 	"episode" : episode,
							# 	"index" : cur_index,
							# 	"timestamp" : cur_timestamp,
							# 	"text" : cur_text
							# })
							data.append([season,episode,cur_index, cur_timestamp, cur_text.strip().rstrip()])
							# print(data[-1])
						cur_text = ""


					elif isTimeStampLine(cur_line):
						cur_timestamp = cur_line.strip().rstrip()
					else:
						stripped_line = cur_line.strip().rstrip()
						if len(stripped_line) > 0: 
							cur_text+= stripped_line.replace('\n','-NL-')
		cnt+=1

writeToCSV(fields,data,"friends_subtitles.csv")