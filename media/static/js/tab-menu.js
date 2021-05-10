function openTab(target, tabName) {
	tabsContent = document.getElementsByClassName("tab-content")
	Array.prototype.map.call(tabsContent, tab => {
		tab.style.display = "none"
	})

	tabLinks = document.getElementsByClassName("tab-link")
	Array.prototype.map.call(tabLinks, tabLink => {
		tabLink.classList.remove("active")
	})

	currTab = document.getElementById(tabName)
	currTab.style.display = "block";
	target.classList.add("active")
}

document.getElementById("tab-data-default").click()
