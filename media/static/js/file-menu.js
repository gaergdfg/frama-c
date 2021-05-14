const emptyOptionValue = '-----'


function populateFileList(files) {
	list = $('#file-list-delete')[0]

	option = document.createElement('option')
	option.value = emptyOptionValue
	option.innerText = emptyOptionValue

	list.appendChild(option)

	files.map(file => {
		option = document.createElement('option')
		option.value = file.pk
		option.innerText = file.pk

		list.appendChild(option)
	})
}

function populateDirectoryList(directories) {
	list = $('#directory-list-delete')[0]

	option = document.createElement('option')
	option.value = emptyOptionValue
	option.innerText = emptyOptionValue

	list.appendChild(option)

	directories.map(directory => {
		option = document.createElement('option')
		option.value = directory.fields.name
		option.innerText = directory.fields.name

		list.appendChild(option)
	})
}

async function populateDeleteMenu() {
	let { files, directories } = await getFilesDirectories()

	populateFileList(files)
	populateDirectoryList(directories)
}


function deleteFile() {
	file = document.getElementById('file-list-delete').value
	if (file == emptyOptionValue)
		return

	csrfToken = getScrfToken()
	if (csrfToken === null)
		return

	$.ajax({
		type: 'POST',
		url: '/remove_file/',
		data: {
			'csrfmiddlewaretoken': csrfToken,
			'file': file
		},
		success: () => {
			loadFileSystemData()
			populateDeleteMenu()
		},
		error: error => {
			alert('There was an error.')
			console.log(error)
		},
		complete: () => {
			document.getElementById('file-list-delete').value = emptyOptionValue
		}
	})
}

function deleteDirectory() {
	directory = document.getElementById('directory-list-delete').value
	if (directory == emptyOptionValue)
		return

	csrfToken = getScrfToken()
	if (csrfToken === null)
		return

	$.ajax({
		type: 'POST',
		url: '/remove_directory/',
		data: {
			'csrfmiddlewaretoken': csrfToken,
			'directory': directory
		},
		success: () => {
			loadFileSystemData()
			populateDeleteMenu()
		},
		error: error => {
			alert('There was an error.')
			console.log(error)
		},
		complete: () => {
			document.getElementById('directory-list-delete').value = emptyOptionValue
		}
	})
}


$(document).ready(() => {
	populateDeleteMenu()
})
