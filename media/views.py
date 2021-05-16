import subprocess

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core import serializers

from media.util import get_files, get_directories, parse_file, update_sections

from .forms import *
from .models import Directory, File, User


def index(request):
	try:
		request.session['login']
	except KeyError:
		return redirect('login/')

	return render(request, 'media/index.html', {})


def login(request):
	if request.method == 'POST':
		form = GetUserForm(request.POST)
		if form.is_valid():
			user = User.objects.filter(
				login=form.cleaned_data['login'],
				password=form.cleaned_data['password']
			).first()

			if user == None:
				form = GetUserForm()
				return render(request, 'media/login.html', { 'form': form })

			request.session['login'] = request.POST['login']

			return redirect('/')

	form = GetUserForm()
	return render(request, 'media/login.html', { 'form': form })

def logout(request):
	try:
		del request.session['login']
	except KeyError:
		pass

	return redirect('/login/')


def new_directory(request):
	if request.method == 'POST':
		form = AddDirectoryForm(request.POST)
		if form.is_valid():
			user = User.objects.filter(login=request.session['login']).first()
			timestamp = timezone.now()

			new_directory = Directory(
				owner=user,
				name=form.cleaned_data['name'],
				description=form.cleaned_data['description'],
				creation_date=timestamp,
				last_updated=timestamp,
			)
			new_directory.save()

			return redirect('/')

	form = AddDirectoryForm()
	return render(request, 'media/add_directory.html', { 'form': form })

def new_file(request):
	if request.method == 'POST':
		form = AddFileForm(request.POST, request.FILES, login=request.session['login'])
		if form.is_valid():
			user = User.objects.filter(login=request.session['login']).first()
			timestamp = timezone.now()

			file_content = request.FILES['source'].read().decode('utf-8')

			new_file = File(
				owner=user,
				directory=form.cleaned_data['parent_directory'],
				name=form.cleaned_data['name'],
				description=form.cleaned_data['description'],
				source=request.FILES['source'],
				creation_date=timestamp,
				last_updated=timestamp,
			)
			new_file.save()

			parse_file(new_file, file_content, user)

			return redirect('/')
	else:
		form = AddFileForm(login=request.session['login'])

	return render(request, 'media/add_file.html', { 'form': form })

def remove_directory(request):
	if request.method == 'POST':
		directory_name = request.POST['directory']

		directory = Directory.objects.filter(name=directory_name).first()
		if directory == None:
			return JsonResponse({}, status=200)

		directory.validity_flag = False
		directory.save(update_fields=['validity_flag'])

		return JsonResponse({}, status=200)

	return JsonResponse({}, status=400)

def remove_file(request):
	if request.method == 'POST':
		file_name = request.POST['file']

		file = File.objects.filter(name=file_name).first()
		if file == None:
			return JsonResponse({}, status=200)

		file.validity_flag = False
		file.save(update_fields=['validity_flag'])

		return JsonResponse({}, status=200)

	return JsonResponse({}, status=400)

def get_user(request):
	if request.method == 'GET':
		try:
			return JsonResponse({ 'login': request.session['login'] })
		except:
			pass

	return JsonResponse({}, status=400) 

def get_user_directories(request):
	if request.method == 'GET':
		try:
			directories = get_directories(request.session['login'])
		except KeyError:
			return JsonResponse({}, status=400)

		return JsonResponse(serializers.serialize('json', directories), status=200, safe=False)

	return JsonResponse({}, status=400)

def get_user_files(request):
	if request.method == 'GET':
		try:
			files = get_files(request.session['login'])
		except KeyError:
			return JsonResponse({}, status=400)

		return JsonResponse(serializers.serialize('json', files), status=200, safe=False)

	return JsonResponse({}, status=400)

def get_file(request):
	if request.method == 'GET':
		file_name = request.GET['file']
		file = File.objects.filter(name=file_name).first()

		file_content = file.source.read().decode('utf-8')

		return JsonResponse({ 'file_content': file_content })
	else:
		return JsonResponse({}, status=400)

def run_file(request):
	if request.method == 'GET':
		username = User.objects.filter(login=request.session['login']).first().name
		file_name = f'./uploads/{username}/{request.GET["file"]}'

		normal_run = False
		try:
			if request.GET['normal_run'] == 'true':
				normal_run = True
		except KeyError:
			pass

		args = ['frama-c', '-wp', '-wp-prover']

		try:
			args.append(request.session['prover'])
		except KeyError:
			args.append('Z3')
			pass

		if not normal_run:
			try:
				if request.session['wp-rte-flag'] == 'true':
					args.append('-wp-rte')
			except KeyError:
				pass

			wp_prop = '-wp-prop='
			try:
				wp_prop += request.session['invariant-flag']
				wp_prop += request.session['variant-flag']
				wp_prop += request.session['assert-flag']
				wp_prop += request.session['precondition-flag']
				wp_prop += request.session['postcondition-flag']

				args.append(wp_prop)
			except KeyError:
				pass

		normal_args = args
		if normal_run:
			normal_args.append('-wp-print')
		normal_args.append(file_name)

		output = subprocess.run(normal_args, capture_output=True)

		result_args = args
		result_args.append('-wp-log=r:result.txt')
		result_args.append(file_name)

		subprocess.run(result_args)

		result = subprocess.run(['cat', 'result.txt'], capture_output=True)
		subprocess.run(['rm', 'result.txt'])

		if normal_run:
			update_sections(request.GET['file'], output.stdout.decode('utf-8'))

		return JsonResponse({
			'framac_output': output.stdout.decode('utf-8'),
			'result_output': result.stdout.decode('utf-8')
		})
	else:
		return JsonResponse({}, status=400)

def set_prover(request):
	if request.method == 'POST':
		request.session['prover'] = request.POST['prover']

		return JsonResponse({})
	else:
		return JsonResponse({}, status=400)

def set_vcs(request):
	if request.method == 'POST':
		config = request.POST

		for flag in config:
			if flag != 'csrfmiddlewaretoken':
				request.session[flag] = config[flag]

		return JsonResponse({})
	else:
		return JsonResponse({}, status=400)
