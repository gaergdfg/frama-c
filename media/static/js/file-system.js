async function getFilesDirectories() {
	let files, directories

	await $.ajax({
		type: 'GET',
		url: 'user_files/',
		data: {},
		success: data => {
			files = JSON.parse(data)
		},
		error: error => {
			alert('There was an error.')
			console.log('GET user_files/ error:', error.statusText)
		}
	})

	await $.ajax({
		type: 'GET',
		url: 'user_directories/',
		data: {},
		success: data => {
			directories = JSON.parse(data)
		},
		error: error => {
			alert('There was an error.')
			console.log('GET user_directories/ error:', error.statusText)
		}
	})

	return { files: files, directories: directories }
}

async function getFileSystem() {
	let fileSystem = {}
	let directoryMapping = {}
	let { files, directories } = await getFilesDirectories()

	directories.map(directory => {
		directoryMapping[directory.pk] = directory.fields.name
		fileSystem[directory.fields.name] = []
	})

	files.map(file => {
		fileSystem[directoryMapping[file.fields.directory]].push(file.pk)
	})

	return fileSystem
}


function preLoadSystemData() {
	document.getElementById('grid-wrapper-file-system').innerHTML = 'Loading files...'
}

function setFileSystemData(fileSystem) {
	parent = document.getElementById('grid-wrapper-file-system')
	parent.innerHTML = ''

	for (let [directory, fileList] of Object.entries(fileSystem)) {
		button = document.createElement('div')
		button.classList.add('file-sys-element', 'directory')
		button.innerText = directory + '/'

		parent.appendChild(button)

		fileList.map(file => {
			fileButton = document.createElement('button')
			fileButton.classList.add('file-sys-element', 'file')
			fileButton.innerText = file

			button.appendChild(fileButton)

			fileButton.onclick = () => {
				openFile(file)
			}
		})
	}
}

async function loadFileSystemData() {
	preLoadSystemData()

	let fileSystem = await getFileSystem()

	setFileSystemData(fileSystem)
}

$(document).ready(async () => {
	loadFileSystemData()
})
