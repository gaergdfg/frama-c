const csrfTokenCookieRegex = /csrftoken=([a-zA-Z0-9]+);/


function getScrfToken() {
	let csrfToken = csrfTokenCookieRegex.exec(document.cookie)[1]
	if (csrfToken === undefined) {
		alert('There was an error.')
		return null
	}

	return csrfToken
}
