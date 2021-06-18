from django.test import RequestFactory, tag, TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from media.models import *
from media.views import *
from media.forms import *
from media.util import *


##################### MODEL TESTS #####################


@tag('model')
class UserModelTests(TestCase):
	def test_user_correct_data(self):
		user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()
		try:
			user.full_clean()
		except ValidationError:
			self.fail()

	def test_user_too_long_name(self):
		user = User(
			name=('a' * 201),
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()
		with self.assertRaises(ValidationError):
			user.full_clean()


@tag('model')
class DirectoryModelTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

	def test_directory_correct_data(self):
		directory = Directory(
			owner=self.user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		directory.save()
		try:
			directory.full_clean()
		except ValidationError:
			self.fail()

	def test_directory_too_long_name(self):
		directory = Directory(
			owner=self.user,
			name=('a' * 201),
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		directory.save()
		with self.assertRaises(ValidationError):
			directory.full_clean()

	def test_directory_no_owner(self):
		directory = Directory(
			owner=None,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			directory.save()


@tag('model')
class FileModelTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

		self.directory = Directory(
			owner=self.user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		self.directory.save()

		self.source = SimpleUploadedFile(
			"test_name.test",
			b"test_file_content"
		)

	def test_file_correct_data(self):
		file = File(
			owner=self.user,
			directory=self.directory,
			name='test_name.test',
			source=self.source,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file.save()
		try:
			file.full_clean()
		except ValidationError:
			self.fail()

	def test_file_too_long_name(self):
		file = File(
			owner=self.user,
			directory=self.directory,
			name=('a' * 201),
			source=self.source,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file.save()
		with self.assertRaises(ValidationError):
			file.full_clean()


@tag('model')
class SectionCategoryTests(TestCase):
	def test_section_category_correct_data(self):
		section_category = SectionCategory(
			category=1,
			last_updated=timezone.now()
		)
		section_category.save()
		try:
			section_category.full_clean()
		except ValidationError:
			self.fail()

	def test_section_category_categorynr_out_of_upper_bound(self):
		section_category = SectionCategory(
			category=255,
			last_updated=timezone.now()
		)
		section_category.save()
		with self.assertRaises(ValidationError):
			section_category.full_clean()

	def test_section_category_categorynr_out_of_lower_bound(self):
		section_category = SectionCategory(
			category=0,
			last_updated=timezone.now()
		)
		section_category.save()
		with self.assertRaises(ValidationError):
			section_category.full_clean()


@tag('model')
class StatusTests(TestCase):
	def test_status_correct_data(self):
		status = Status(
			status=1,
			last_updated=timezone.now()
		)
		status.save()
		try:
			status.full_clean()
		except ValidationError:
			self.fail()

	def test_status_statusnr_out_of_upper_bound(self):
		status = Status(
			status=255,
			last_updated=timezone.now()
		)
		status.save()
		with self.assertRaises(ValidationError):
			status.full_clean()

	def test_status_statusnr_out_of_lower_bound(self):
		status = Status(
			status=0,
			last_updated=timezone.now()
		)
		status.save()
		with self.assertRaises(ValidationError):
			status.full_clean()


@tag('model')
class StatusDataTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

	def test_status_data_correct_data(self):
		status_data = StatusData(
			user=self.user,
			status_data='test_status_data',
			last_updated=timezone.now()
		)
		status_data.save()
		try:
			status_data.full_clean()
		except ValidationError:
			self.fail()

	def test_status_data_no_user(self):
		status_data = StatusData(
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			status_data.save()


@tag('model')
class FileSectionTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

		self.directory = Directory(
			owner=self.user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		self.directory.save()

		self.source = SimpleUploadedFile(
			"test_name.test",
			b"test_file_content"
		)

		self.file = File(
			owner=self.user,
			directory=self.directory,
			name='test_name.test',
			source=self.source,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		self.file.save()

		self.category = SectionCategory(
			category=1,
			last_updated=timezone.now()
		)
		self.category.save()

		self.status = Status(
			status=1,
			last_updated=timezone.now()
		)
		self.status.save()

		self.status_data = StatusData(
			user=self.user,
			status_data='test_status_data',
			last_updated=timezone.now()
		)
		self.status_data.save()

	def test_file_section_correct_data(self):
		file_section = FileSection(
			file=self.file,
			category=self.category,
			status=self.status,
			status_data=self.status_data,
			name='test_name',
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file_section.save()
		try:
			file_section.full_clean()
		except ValidationError:
			self.fail()

	def test_file_section_no_file(self):
		file_section = FileSection(
			file=None,
			category=self.category,
			status=self.status,
			status_data=self.status_data,
			name='test_name',
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			file_section.save()

	def test_file_section_no_category(self):
		file_section = FileSection(
			file=self.file,
			category=None,
			status=self.status,
			status_data=self.status_data,
			name='test_name',
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			file_section.save()

	def test_file_section_no_status(self):
		file_section = FileSection(
			file=self.file,
			category=self.category,
			status=None,
			status_data=self.status_data,
			name='test_name',
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			file_section.save()

	def test_file_section_no_status_data(self):
		file_section = FileSection(
			file=self.file,
			category=self.category,
			status=self.status,
			status_data=None,
			name='test_name',
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		with self.assertRaises(IntegrityError):
			file_section.save()

	def test_file_section_too_long_name(self):
		file_section = FileSection(
			file=self.file,
			category=self.category,
			status=self.status,
			status_data=self.status_data,
			name=('a' * 201),
			line=1,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file_section.save()
		with self.assertRaises(ValidationError):
			file_section.full_clean()

	def test_file_section_no_line_number(self):
		file_section = FileSection(
			file=self.file,
			category=self.category,
			status=self.status,
			status_data=self.status_data,
			name='test_name',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file_section.save()
		with self.assertRaises(ValidationError):
			file_section.full_clean()


##################### VIEW TESTS #####################


@tag('view')
class IndexViewTests(TestCase):
	def test_index_status_code_logged_out(self):
		response = self.client.get('/')
		self.assertEquals(response.status_code, 302)


@tag('view')
class LoginViewTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

	def test_login_correct_data(self):
		data = {
			'login': self.user.login,
			'password': self.user.password
		}
		response = self.client.post('/login/', data=data)
		self.assertRedirects(
			response,
			'/',
			status_code=302,
			target_status_code=200,
			fetch_redirect_response=True
		)

	def test_login_incorrect_method(self):
		data = {
			'login': self.user.login,
			'password': self.user.password
		}
		response = self.client.get('/login/', data=data)
		self.assertEqual(response.status_code, 200)

	def test_login_incorrect_data(self):
		data = {
			'login': 'incorrect_login',
			'password': 'incorrect_password'
		}
		response = self.client.post('/login/', data=data)
		self.assertEqual(response.status_code, 200)


@tag('view')
class LogoutViewTests(TestCase):
	def test_logout_logged_out(self):
		response = self.client.get('/logout/')
		self.assertRedirects(
			response,
			'/login/',
			status_code=302,
			target_status_code=200,
			fetch_redirect_response=True
		)


@tag('view')
class NewDirectoryViewTests(TestCase):
	def setUp(self):
		self.session = self.client.session
		self.session['login'] = 'test_login'
		self.session.save()

		user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()

	def test_new_directory_incorrect_method(self):
		response = self.client.get('/new_directory/')
		self.assertEquals(response.status_code, 200)

	def test_new_directory_incorrect_data(self):
		response = self.client.post('/new_directory/', data={})
		self.assertEquals(response.status_code, 200)

	def test_new_directory_correct_data(self):
		data = {
			'name': 'test_name',
			'description': 'test_description',
		}

		response = self.client.post('/new_directory/', data=data)
		self.assertRedirects(
			response,
			'/',
			status_code=302,
			target_status_code=200,
			fetch_redirect_response=True
		)

		created_dir = Directory.objects.filter(name='test_name')
		self.assertEquals(len(created_dir), 1)


@tag('view')
class NewFileViewTests(TestCase):
	def setUp(self):
		self.session = self.client.session
		self.session['login'] = 'test_login'
		self.session.save()

	def test_new_file_incorrect_method(self):
		response = self.client.get('/new_file/')
		self.assertEquals(response.status_code, 200)

	def test_new_file_incorrect_data(self):
		response = self.client.post('/new_file/', data={})
		self.assertEquals(response.status_code, 200)

# TODO: fix this test (redirect returns 200 code)
	# def test_new_file_correct_data(self):
	# 	user = User(
	# 		name='test_name',
	# 		login='test_login',
	# 		password='test_password',
	# 		last_updated=timezone.now()
	# 	)
	# 	user.save()

	# 	directory = Directory(
	# 		owner=user,
	# 		name='test_name',
	# 		description='test_description',
	# 		creation_date=timezone.now(),
	# 		last_updated=timezone.now()
	# 	)
	# 	directory.save()

	# 	source = SimpleUploadedFile(
	# 		"test_name.test",
	# 		b"test_file_content"
	# 	)

	# 	data = {
	# 		'parent_directory': directory,
	# 		'name': 'test_name',
	# 		'description': 'test_description',
	# 		'source': source
	# 	}

	# 	response = self.client.post('/new_file/', data=data)
	# 	self.assertRedirects(
	# 		response,
	# 		'/',
	# 		status_code=302,
	# 		target_status_code=200,
	# 		fetch_redirect_response=True
	# 	)

	# 	created_file = File.objects.filter(name='test_name')
	# 	self.assertEquals(len(created_file), 1)


@tag('view')
class RemoveDirectoryViewTests(TestCase):
	def test_remove_directory_correct_data(self):
		user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()

		directory = Directory(
			owner=user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		directory.save()

		data = { 'directory': directory.name }
		response = self.client.post('/remove_directory/', data=data)
		self.assertEqual(response.status_code, 200)

	def test_remove_directory_incorrect_data(self):
		data = { 'directory': 'incorrect_name' }
		response = self.client.post('/remove_directory/', data=data)
		self.assertEqual(response.status_code, 200)

	def test_remove_directory_incorrect_method(self):
		response = self.client.get('/remove_directory/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class GetUserDirectoriesViewTests(TestCase):
	def test_get_user_directories_incorrect_method(self):
		response = self.client.post('/user_directories/')
		self.assertEqual(response.status_code, 400)

	def test_get_user_directories_correct_user(self):
		self.session = self.client.session
		self.session['login'] = 'test_login'
		self.session.save()

		response = self.client.get('/user_directories/')
		self.assertEqual(response.status_code, 200)

	def test_get_user_directories_incorrect_user(self):
		response = self.client.get('/user_directories/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class GetUserFilesViewTests(TestCase):
	def test_get_user_files_incorrect_method(self):
		response = self.client.post('/user_files/')
		self.assertEqual(response.status_code, 400)

	def test_get_user_files_correct_user(self):
		self.session = self.client.session
		self.session['login'] = 'test_login'
		self.session.save()

		response = self.client.get('/user_files/')
		self.assertEqual(response.status_code, 200)

	def test_get_user_files_incorrect_user(self):
		response = self.client.get('/user_files/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class GetFileViewTests(TestCase):
	def test_get_file_correct_data(self):
		user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()

		directory = Directory(
			owner=user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		directory.save()

		source = SimpleUploadedFile(
			"test_name.test",
			b"test_file_content"
		)

		file = File(
			owner=user,
			directory=directory,
			name='test_name.test',
			source=source,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file.save()

		data = { 'file': 'test_name.test' }
		response = self.client.get('/file/', data=data)
		self.assertEquals(response.status_code, 200)

	def test_get_file_incorrect_method(self):
		response = self.client.post('/file/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class RunFileViewTests(TestCase):
	def setUp(self):
		self.session = self.client.session
		self.session['login'] = 'test_login'
		self.session.save()

	def test_run_file_correct_data(self):
		user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		user.save()

		directory = Directory(
			owner=user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		directory.save()

		source = SimpleUploadedFile(
			"test_name.test",
			b"test_file_content"
		)

		file = File(
			owner=user,
			directory=directory,
			name='test_name.test',
			source=source,
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		file.save()

		data = { 'file': 'test_name.test' }
		response = self.client.get('/run_file/', data=data)
		self.assertEquals(response.status_code, 200)

	def test_run_file_incorrect_method(self):
		response = self.client.post('/run_file/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class SetProverViewTests(TestCase):
	def test_set_prover_incorrect_method(self):
		response = self.client.get('/set_prover/')
		self.assertEqual(response.status_code, 400)


@tag('view')
class SetVCsViewTests(TestCase):
	def test_set_vcs_incorrect_method(self):
		response = self.client.get('/set_vcs/')
		self.assertEqual(response.status_code, 400)


##################### FORM TESTS #####################


@tag('form')
class GetUserFormTests(TestCase):
	def test_get_user_form_correct_data(self):
		data = {
			'login': 'test_login',
			'password': 'test_password'
		}
		form = GetUserForm(data)
		self.assertTrue(form.is_valid())

	def test_get_user_form_too_long_name(self):
		data = {
			'login': ('a' * 201),
			'password': 'test_password'
		}
		form = GetUserForm(data)
		self.assertFalse(form.is_valid())

	def test_get_user_form_no_data(self):
		form = GetUserForm({})
		self.assertFalse(form.is_valid())


@tag('form')
class AddDirectoryFormTests(TestCase):
	def test_get_user_form_correct_data(self):
		data = { 'name': 'test_name' }
		form = AddDirectoryForm(data)
		self.assertTrue(form.is_valid())

	def test_get_user_form_too_long_name(self):
		data = { 'login': ('a' * 201) }
		form = AddDirectoryForm(data)
		self.assertFalse(form.is_valid())

	def test_get_user_form_no_data(self):
		form = AddDirectoryForm({})
		self.assertFalse(form.is_valid())


@tag('form')
class AddFileFormTests(TestCase):
	def setUp(self):
		self.user = User(
			name='test_name',
			login='test_login',
			password='test_password',
			last_updated=timezone.now()
		)
		self.user.save()

		self.directory = Directory(
			owner=self.user,
			name='test_name',
			description='test_description',
			creation_date=timezone.now(),
			last_updated=timezone.now()
		)
		self.directory.save()

		self.source = SimpleUploadedFile(
			"test_name.test",
			b"test_file_content"
		)

# TODO: fix these two tests (self.source invalidates the forms)
	# def test_get_user_form_correct_data(self):
	# 	data = {
	# 		'name': 'test_name',
	# 		'parent_directory': Directory.objects.first(),
	# 		'source': self.source
	# 	}
	# 	form = AddFileForm(data)
	# 	self.assertTrue(form.is_valid())

	# def test_get_user_form_too_long_name(self):
	# 	data = {
	# 		'name': ('a' * 201),
	# 		'parent_directory': Directory.objects.first(),
	# 		'source': self.source
	# 	}
	# 	form = AddFileForm(data)
	# 	self.assertFalse(form.is_valid())

	def test_get_user_form_no_data(self):
		with self.assertRaises(KeyError):
			AddFileForm({})


##################### UTIL TESTS #####################


@tag('util')
class utilTests(TestCase):
	def test_count_lines(self):
		example = '\n\n\r\n \n'
		self.assertEquals(count_lines(example), 4)
