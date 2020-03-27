#!/usr/bin/env python3
import os
import configparser

def run():
	config = configparser.ConfigParser()
	config.read('config.ini')
	project    = config['run']['profile']
	
	line_start = config[project]['line_start']
	line_end   = config[project]['line_end']
	remote     = config[project]['remote']
	local      = config[project]['local']
	filelist   = config[project]['filelist']
	bat_name   = config[project]['filename']
	
	batch = []
	with open(filelist, 'r') as file:
		for line in file.readlines():
			(path, filename) = line.rsplit("\\", 1)

			#poistetaan rivinvaihdot
			filename = filename.strip("\n")
			nline = path.replace(remote, local).strip("\n")
			line_stripped = path.strip("\n")

			s = f'{line_start}\n  "{os.path.join(nline, filename)}"\n  "{line_stripped}"\n  {line_end}\n'
			s2 = f'{line_start}\n  "{os.path.join(line_stripped, filename)}"\n  "{nline}"\n  {line_end}\n'

			batch.append(s)
			batch.append(s2)

	write_batchfile(batch, bat_name)

def write_batchfile(batch, bat_filename):
	with open(bat_filename, 'w') as f:
		for item in batch:
			f.write(item)

if __name__ == "__main__":
	run()
