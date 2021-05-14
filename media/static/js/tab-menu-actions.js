function setProver() {
	csrfToken = getScrfToken()
	if (csrfToken === null)
		return

	options = document.getElementsByClassName('prover-choice-radio')

	for (let i = 0; i < options.length; i++) {
		if (options[i].checked) {
			$.ajax({
				type: 'POST',
				url: '/set_prover/',
				data: {
					'csrfmiddlewaretoken': csrfToken,
					'prover': options[i].value
				},
				success: () => {
					alert('Successfully set the prover.')
				},
				error: error => {
					alert('There was an error.')
					console.log(error)
				},
				complete: () => {
					options[i].checked = false
				}
			})

			return
		}
	}
}

function setVCs() {
	csrfToken = getScrfToken()
	if (csrfToken === undefined) {
		alert('There was an error.')
		return;
	}

	options = document.getElementsByClassName('vc-choice-checkbox')
	config = { 'csrfmiddlewaretoken' : csrfToken }

	for (let i = 0; i < options.length; i++) {
		config[options[i].value] = options[i].checked ? '-@' + options[i].value.slice(0, -5) : ''
	}

	$.ajax({
		type: 'POST',
		url: '/set_vcs/',
		data: config,
		success: () => {
			alert('Successfully set the VCs.')
		},
		error: error => {
			alert('There was an error.')
			console.log(error)
		},
		complete: () => {
			for (let i = 0; i < options.length; i++) {
				options[i].checked = false
			}
		}
	})
}
