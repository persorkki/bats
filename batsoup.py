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

	batch.append(f'@echo off\n')
	batch.append(f'echo Tiedostoja kopioitu:\n')
	batch.append(f'echo.\n') #tyhjä rivi

	with open(filelist, 'r') as file:
		for line in file.readlines():
			if not line.startswith('\n'):
				(path, filename) = line.rsplit("\\", 1)

				#poistetaan rivinvaihdot
				filename = filename.strip("\n")
				nline = path.replace(remote, local).strip("\n")
				line_stripped = path.strip("\n")

				line1 = f'{line_start} "{os.path.join(nline, filename)}" "{line_stripped}" {line_end}\n'
				line2 = f'{line_start} "{os.path.join(line_stripped, filename)}" "{nline}" {line_end}\n\n'

				batch.append(f'echo Verkkolevylle:\n')
				batch.append(line1)
				batch.append(f'echo.\n') #tyhjä rivi
				batch.append(f'echo Koneelle:\n')
				batch.append(line2)
				batch.append(f'echo.\n') #tyhjä rivi

	batch.append(f'pause') #jätä ikkuna auki

	write_batchfile(batch, bat_name)

def write_batchfile(batch, bat_filename):
	with open(bat_filename, 'w') as f:
		for item in batch:
			f.write(item)

if __name__ == "__main__":
	run()
