import re
from django.utils import timezone

from media.models import *


def get_directories():
	return Directory.objects.filter(validity_flag=True)

def get_files():
	return File.objects.filter(validity_flag=True)

def gen_file_struct():
	res = {}
	directories = get_directories()

	for directory in directories:
		res[directory] = File.objects.filter(validity_flag=True, directory=directory)

	return res


section_regex = r' ((?:requires|ensures|assert|invariant|variant)[^;]*;)'
section_type_regex = r'(requires|ensures|assert|invariant|variant)'

def count_lines(preffix):
	return len(re.findall(r'\n', preffix))

def parse_file(new_file, file_content):
	line = 1
	while True:
		match = re.search(section_regex, file_content)
		if match == None:
			return

		preffix = file_content[:match.start() - 1]
		line += count_lines(preffix)

		section_type = re.search(section_type_regex, match.group()).group()
		timestamp = timezone.now()
		mapping = {
			'requires': 4,
			'ensures': 5,
			'assert': 3,
			'invariant': 1,
			'variant': 2
		}

		section_category = SectionCategory(category=mapping[section_type], last_updated=timestamp)
		status = Status(status=5, last_updated=timestamp)
		status_data = StatusData(user=User.objects.first(), last_updated=timestamp)
		section_category.save()
		status.save()
		status_data.save()

		file_section = FileSection(
			file=new_file, category=section_category, status=status, status_data=status_data,
			line=line, creation_date=timestamp,
			last_updated=timestamp
		)
		file_section.save()

		line += count_lines(match.group())
		file_content = file_content[match.end():-1]

delimiter = '------------------------------------------------------------'
section_feedback_regex = r'Goal [^ ]+ \(file [^,]+, line (\d+)\)'

def update_sections(file_name, output):
	file = File.objects.filter(name=file_name).first()
	output = re.split(delimiter, output)
	output = list(map(lambda feed: feed.strip(), output))
	timestamp = timezone.now()
	
	for block in output:
		match = re.search(section_feedback_regex, block)

		if match != None:
			line = match.group(1)
			file_section = FileSection.objects.filter(file=file, line=line).first()

			if file_section != None:
				status = file_section.status

				if re.search('Valid', block):
					status.status = 1
				elif re.search('Invalid', block):
					status.status = 2
				elif re.search('Counterexample', block):
					status.status = 3
				else:
					status.status = 4

				status.last_updated = timestamp
				status.save(update_fields=['status', 'last_updated'])

				file_section.last_updated = timestamp
				file_section.save(update_fields=['status', 'last_updated'])

	file_sections = FileSection.objects.filter(file=file)

	for file_section in file_sections:
		section_status = file_section.status
		if section_status.last_updated != timestamp:
			section_status.last_updated = timestamp
			section_status.status = 4

			status.save(update_fields=['status', 'last_updated'])
