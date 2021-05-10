const framacOutputDelimiter = '------------------------------------------------------------'


function parseFramacOutput(data) {
	sections = data['framac_output'].split(framacOutputDelimiter)
	sections = sections.map(section => section.trim())

	return {
		'sections': sections,
		'result': data['result_output']
	}
}

function preLoadEditorContent() {
	document.getElementById("grid-wrapper-editor").innerHTML = 'Waiting for server response...'
}

function preLoadFocusContent() {
	document.getElementById("grid-wrapper-elements").innerHTML = 'Running Frama-C...'
}

function preLoadResultContent() {
	document.getElementById("tab-result").innerHTML = 'Running Frama-C...'
}

function setErrorEditorContent() {
	document.getElementById("grid-wrapper-editor").innerHTML = 'There was an error.'
}

function setErrorFocusContent() {
	document.getElementById("grid-wrapper-elements").innerHTML = 'There was an error.'
}

function setErrorResultContent() {
	document.getElementById("tab-result").innerHTML = 'There was an error.'
}

function setEditorContent(fileContent) {
	document.getElementById("grid-wrapper-editor").innerHTML = fileContent
}

function setFocusContent(sections) {
	parent = document.getElementById("grid-wrapper-elements")
	parent.innerHTML = ''

	isHeader = true
	sections.map(section => {
		child = document.createElement('div')

		appendedChild = parent.appendChild(child)

		innerChild = document.createElement('p')
		innerChild.classList.add('text-container')
		innerChild.innerText = section

		appendedInnerChild = appendedChild.appendChild(innerChild)

		if (isHeader) {
			isHeader = false
			if (section.search(/Prover '[^']+' not found/) != -1)
				appendedInnerChild.classList.add('error')
		} else {
			if (section.search(/Valid/) != -1)
				appendedInnerChild.classList.add('valid')
			else if (section.search(/Unknown error/) != -1)
				appendedInnerChild.classList.add('unknown-error')
			else if (section.search(/Warning/) != -1)
				appendedInnerChild.classList.add('warning')
			else if (section.search(/Invalid/) != -1)
				appendedInnerChild.classList.add('error')
		}
	})
}

function setResultData(result) {
	document.getElementById("tab-result").innerText = result
}

function runFile(normalRun = false) {
	target = document.getElementsByClassName('file active')[0]
	if (target === undefined) {
		alert('No file selected.')
		return
	}

	preLoadEditorContent()
	preLoadFocusContent()
	preLoadResultContent()

	data = { 'file': target.innerText }
	if (normalRun) {
		data['normal_run'] = 'true'
	}

	$.ajax({
		type: 'GET',
		url: '/file',
		data: data,
		success: data => {
			setEditorContent(data['file_content'])
		},
		error: error => {
			setErrorEditorContent()
			console.log('GET /file Error occurred:', error)
		}
	})

	$.ajax({
		type: 'GET',
		url: '/run_file',
		data: data,
		success: data => {
			parsed_data = parseFramacOutput(data)
			setFocusContent(parsed_data['sections'])
			setResultData(parsed_data['result'])
		},
		error: error => {
			setErrorFocusContent()
			setErrorResultContent()
			console.log('GET /run_file Error occurred:', error)
		}
	})
}

function openFile(target) {
	files = document.getElementsByClassName("file")
	Array.prototype.map.call(files, file => {
		file.classList.remove("active")
	})
	target.classList.add("active")

	runFile(true)
}
