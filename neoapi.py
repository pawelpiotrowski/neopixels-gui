import re

__author__ = 'pawelpiotrowski'


def validate_command(cmd_str):
	limiter = 255
	cmd_fallback = '-1,0,0,0'
	cmd_suffix = '\n'
	cmd_fallback += cmd_suffix
	cmd_pattern = re.compile('-?\d+,\d+,\d+,\d+')
	if cmd_pattern.match(cmd_str):
		cmd_split = cmd_str.split(',')
		for index, cmd_piece in enumerate(cmd_split):
			if index > 0:
				piece_as_number = int(float(cmd_piece))
				if piece_as_number > limiter:
					cmd_split[index] = '0'
		return ','.join(cmd_split) + cmd_suffix
	return cmd_fallback
