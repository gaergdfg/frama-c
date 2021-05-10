import os

from django.db import models


def get_filename(instance, filename):
	return os.path.join(f'uploads/{instance.owner.name}/', instance.name)


class User(models.Model):
	name = models.CharField(primary_key = True, unique = True, max_length = 200)
	login = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')


class Directory(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	parent_directory = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)

	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 1000, blank = True, default = '')
	creation_date = models.DateTimeField('created')

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')

	def __str__(self):
		return self.name


class File(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	directory = models.ForeignKey(Directory, on_delete = models.CASCADE)

	name = models.CharField(primary_key = True, unique = True, max_length = 200)
	description = models.CharField(max_length = 1000, blank = True, default = '')
	source = models.FileField(upload_to=get_filename, null = True)
	creation_date = models.DateTimeField('created')

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')

	def __str__(self):
		return self.name


class SectionCategory(models.Model):
	INVARIANT = 1
	VARIANT = 2
	ASSERT = 3
	REQUIRES = 4
	ENSURES = 5
	STATUS = (
		(INVARIANT, 'Invariant section'),
		(VARIANT, 'Variant section'),
		(ASSERT, 'Assertion section'),
		(REQUIRES, 'Precondition section'),
		(ENSURES, 'Postcondition section')
	)
	category = models.PositiveSmallIntegerField(choices = STATUS)

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')


class Status(models.Model):
	PROVED = 1
	INVALID = 2
	COUNTEREXAMPLE = 3
	ERROR = 4
	UNCHECKED = 5
	STATUS = (
		(PROVED, 'Proved'),
		(INVALID, 'Invalid'),
		(COUNTEREXAMPLE, 'Counterexample'),
		(ERROR, 'Error'),
		(UNCHECKED, 'Unchecked')
	)
	status = models.PositiveSmallIntegerField(choices = STATUS)

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')


class StatusData(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	status_data = models.CharField(max_length = 1000, default='')

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')


class FileSection(models.Model):
	parent_section = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)
	file = models.ForeignKey(File, on_delete = models.CASCADE)
	category = models.OneToOneField(SectionCategory, models.CASCADE)
	status = models.OneToOneField(Status, models.CASCADE)
	status_data = models.OneToOneField(StatusData, models.CASCADE)

	name = models.CharField(max_length = 200, blank = True, default = '')
	description = models.CharField(max_length = 1000, blank = True, default = '')
	line = models.IntegerField(null=True)
	creation_date = models.DateTimeField('created')

	validity_flag = models.BooleanField(default = True)
	last_updated = models.DateTimeField('modified')
