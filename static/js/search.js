function myFunction() {
  var input = document.getElementById("Search");
  var filter = input.value.toLowerCase();
  var nodes = document.getElementsByClassName('grid-container');
  for (i = 0; i < nodes.length; i++) {
    if (nodes[i].innerText.toLowerCase().includes(filter)) {
      nodes[i].style.display = "block";
    } else {
      nodes[i].style.display = "none";
    }
  }
  window.scrollTo(0,0);
}
function key_down(e)
{
    e = e || window.event;
    if (e.keyCode == 13)
    {
        myFunction();
        return false;
    }
    return true;
}
function removeOverlay() {
	const element = document.getElementById("overlay");
  element.remove();
}