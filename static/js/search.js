function myFunction() {
	var checkbox = document.getElementById('downloaded');
  if (checkbox.checked != false)
  {
    let maps
	let mapsPromise = fetch('http://127.0.0.1:5757/maplist')
  .then(response => response.json())
  .catch(error => {
    // Handle any errors
    console.error(error);
  });
  mapsPromise.then(data => {
  // Handle the response data
  const maps = data;
  console.log(maps);

  // Continue with your code that depends on the fetched data
  // ...
  // maps.includes(nodes[i].id) && nodes[i].innerText.toLowerCase().includes(filter)
  var input = document.getElementById("Search");
  var filter = input.value.toLowerCase();
  var nodes = document.getElementsByClassName('grid-container');
  for (i = 0; i < nodes.length; i++) {
    if (maps.includes(nodes[i].id) && nodes[i].innerText.toLowerCase().includes(filter)) {
      nodes[i].style.display = "block";
    } else {
      nodes[i].style.display = "none";
    }
  }
  window.scrollTo(0,0);
  });
				   } else 
  {
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
  }
}
function displayDownloaded() {
	var checkbox = document.getElementById('downloaded');
  if (checkbox.checked != false)
  {
    let maps
	let mapsPromise = fetch('http://127.0.0.1:5757/maplist')
  .then(response => response.json())
  .catch(error => {
    // Handle any errors
    console.error(error);
  });
  mapsPromise.then(data => {
  // Handle the response data
  const maps = data;
  console.log(maps);

  // Continue with your code that depends on the fetched data
  // ...
  var nodes = document.getElementsByClassName('grid-container');
  for (i = 0; i < nodes.length; i++) {
    if (maps.includes(nodes[i].id)) {
      nodes[i].style.display = "block";
    } else {
      nodes[i].style.display = "none";
    }
  }
  window.scrollTo(0,0);
  });
  } else {
	  var nodes = document.getElementsByClassName('grid-container');
	  var input = document.getElementById("Search");
	  console.log(input);
	  var filter = input.value.toLowerCase();
	  console.log(filter == '');
  for (i = 0; i < nodes.length; i++) {
	  if (filter != "") {
    if (maps.includes(nodes[i].id) && nodes[i].innerText.toLowerCase().includes(filter)) {
      nodes[i].style.display = "block";
    } else {
      nodes[i].style.display = "none";
    }
		  
	} else {
    nodes[i].style.display = "block";
	}
   }
  }

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