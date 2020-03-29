#!/usr/bin/env python3
import os
import argparse
import configparser

def run(line_start, line_end, remote, local, filelist, bat_filename):
	batch = []
	batch.append(f'@echo off\n')
	batch.append(f'echo Tiedostoja kopioitu:\n')
	batch.append(f'echo.\n') #tyhjä rivi

	with open(filelist, 'r') as file:
		lines = map(lambda x: x.strip("\n"), file.readlines())
	
	for line in lines:
		if line.strip() and not line.startswith("#"):
			(source, filename) = line.rsplit("\\", 1)
			target = source.replace(remote, local)

			line1 = f'{line_start} "{os.path.join(target, filename)}" "{source}" {line_end}\n'
			line2 = f'{line_start} "{os.path.join(source, filename)}" "{target}\\" {line_end}\n\n'

			batch.append(f'echo Verkkolevylle:\n')
			batch.append(line1)
			batch.append(f'echo.\n') #tyhjä rivi
			batch.append(f'echo Koneelle:\n')
			batch.append(line2)
			batch.append(f'echo.\n') #tyhjä rivi

	batch.append(f'pause') #jätä ikkuna auki
	write_batchfile(batch, bat_filename)

def write_batchfile(batch, bat_filename):
	with open(bat_filename, 'w') as f:
		for item in batch:
			f.write(item)

if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.read('config.ini')
	
	parser = argparse.ArgumentParser(description='arguments for profile selection')
	parser.add_argument('-p', default='default', required=False)
	args = parser.parse_args()

	if args.p in config:
		print (f"using profile [{args.p}]")
		profile = args.p
	else:
		print ("unknown profile argument, using [default] profile instead")
		profile = 'default'

	line_start = config[profile]['line_start']
	line_end   = config[profile]['line_end']
	remote     = config[profile]['remote']
	local      = config[profile]['local']
	filelist   = config[profile]['filelist']
	bat_filename   = config[profile]['filename']

	run(line_start, line_end, remote, local, filelist, bat_filename)