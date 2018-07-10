function openTab(baseTabName) {
  // Get all elements with class="tabcontent" and hide them
  let tabs = document.getElementsByClassName("tabcontent");
  for (let tab of tabs) {
      tab.style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  let links = document.getElementsByClassName('tablinks');
  for (let link of links) {
      link.classList.remove('active');
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(baseTabName + 'Tab').style.display = 'block';
  document.getElementById(baseTabName + 'TabButton').classList.add('active');
}

function setupTabs(player) {
  let showReplicantiTabNeeded = false;
  let links = document.getElementsByClassName('tablinks');
  for (let link of links) {
    let reflectionsOk = !link.classList.contains('reflectionTabButton') ||
    player.reflections > 0;
    let overflowsOk = !link.classList.contains('overflowTabButton') ||
    player.overflows > 0;
    if (reflectionsOk && overflowsOk) {
      link.style.display = 'default';
    } else {
      link.style.display = 'none';
      if (link.classList.contains('active')) {
        showReplicantiTabNeeded = true;
      }
    }
  }
  if (showReplicantiTabNeeded) {
    openTab('replicanti');
  }
  for (let i of document.getElementsByClassName('reflectionData')) {
    if (player.reflections > 0) {
      i.style.display = 'default';
    } else {
      i.style.display = 'none';
    }
  }
  for (let i of document.getElementsByClassName('overflowData')) {
    if (player.overflows > 0) {
      i.style.display = 'default';
    } else {
      i.style.display = 'none';
    }
  }
}

function resetShownData () {
  let links = document.getElementsByClassName('tablinks');
  for (let link of links) {
    let tabName = link.id.split('TabButton')[0];
    link.onclick = function () {
      openTab(tabName);
    }
  }
  openTab('replicanti');
}

export {setupTabs, resetShownData};
