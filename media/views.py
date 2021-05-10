import subprocess

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from media.util import gen_file_struct, parse_file, update_sections

from .forms import *
from .models import Directory, File, User


def index(request):
	context = { 'file_sys': gen_file_struct() }
	return render(request, 'media/index.html', context)

def new_directory(request):
	if request.method == 'POST':
		form = AddDirectoryForm(request.POST)
		if form.is_valid():
			user = User.objects.first()
			timestamp = timezone.now()

			new_directory = Directory(
				owner=user,
				name=form.cleaned_data['name'],
				description=form.cleaned_data['description'],
				creation_date=timestamp,
				last_updated=timestamp,
			)
			new_directory.save()

			print('Successfully created a directory:', new_directory)

			return redirect('/')

	form = AddDirectoryForm()
	return render(request, 'media/add_directory.html', {'form': form})

def new_file(request):
	if request.method == 'POST':
		form = AddFileForm(request.POST, request.FILES)
		if form.is_valid():
			user = User.objects.first()
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

			parse_file(new_file, file_content)

			print('Successfully created a file:', new_file)

			return redirect('/')
		else:
			print('Invalid form')
	else:
		form = AddFileForm()

	return render(request, 'media/add_file.html', {'form': form})

def remove_directory(request):
	if request.method == 'POST':
		form = RemoveDirectoryForm(request.POST)
		if form.is_valid():
			directory = form.cleaned_data['directory']
			directory.validity_flag = False
			directory.save(update_fields=['validity_flag'])

			print('Removed directory:', directory)

			return redirect('/')
		else:
			print('Invalid form')

	form = RemoveDirectoryForm()
	return render(request, 'media/remove_directory.html', {'form': form})

def remove_file(request):
	if request.method == 'POST':
		form = RemoveFileForm(request.POST)
		if form.is_valid():
			file = form.cleaned_data['file']
			file.validity_flag = False
			file.save(update_fields=['validity_flag'])

			print('Removed file:', file)

			return redirect('/')
		else:
			print('Invalid form')

	form = RemoveFileForm()
	return render(request, 'media/remove_file.html', {'form': form})

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
		file_name = f'./uploads/{User.objects.first().name}/{request.GET["file"]}'

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
