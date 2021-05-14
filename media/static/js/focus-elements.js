function getNextOfClass(element, targetClass) {
	let next = element

	do {
		next = next.nextElementSibling
	} while (!next.classList.contains(targetClass))

	return next
}

function setFocusElementsOnClick() {
	elements = document.getElementsByClassName('collapsible')

	Array.prototype.map.call(elements, element => {
		element.addEventListener('click', event => {
			content = getNextOfClass(event.target, 'collapsible-content')
			
			event.target.innerText = content.style.display == 'block' ? '+' : '-'
			content.style.display = content.style.display == 'block' ? 'none' : 'block'
		})
	})
}
