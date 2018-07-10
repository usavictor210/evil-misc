import {savePlayer, loadPlayer, setupAutoSave} from './save_and_load.js';
import {stats} from './stats.js';
import {setupTabs, resetShownData} from './tabs.js';
import {a} from './basic_html.js';
import {decToStr, percentToStr} from './num_display_utils.js';
import {getNew, capMaxedOut, getReplicateChance} from './game_utils.js';

function setupSaveAndLoad(setPlayer, getPlayer) {
  a('saveButton').onclick = function () {
    savePlayer(getPlayer());
    a('saveArea').focus();
    a('saveArea').select();
    try {
      document.execCommand('copy');
    } catch (e) {
      alert('Copy to clipboard failed!');
    }
    a('saveArea').blur();
  }
  a('loadButton').onclick = function () {
    loadPlayer(prompt('Enter save to load:'), setPlayer);
    savePlayer(getPlayer());
  }
  setupAutoSave(getPlayer);
}

let html = {
	replicanti: a("replicanti"),
	replicateChance: a("replicateChance"),
  replicateNum: a("replicateNum"),
	replicateCap: a("replicateCap")
};

function setReset (f) {
  a('resetButton').onclick = f;
}

function fillInHtml () {
  for (let i of stats) {
    html['replicate' + i + 'UpgradeButton'] = a('replicate' + i + 'Upgrade');
		html['replicate' + i + 'MaxUpgradeButton'] = a('replicate' + i + 'Max');
    html['replicate' + i + 'UpgradeDescription'] = a('replicate' + i + 'Description');
  }
}

fillInHtml();

function setUpdate(player) {
  html.update = function () {
  	this.replicanti.innerHTML = decToStr(player.replicanti);
  	this.replicateChance.innerHTML = percentToStr(getReplicateChance(player)) + '%';
  	this.replicateNum.innerHTML = (player.replicatePlus + 1) + '';
  	this.replicateCap.innerHTML = decToStr(player.replicateCap);

  	for (let i of stats) {
  		this['replicate' + i + 'UpgradeButton'].innerHTML = decToStr(player['replicate' + i + 'Upgrade']) + " replicanti";
  	}
  	this.replicateChanceUpgradeDescription.innerHTML = "Increase the replicate fraction by 1%.<br/>(from " + getNew(player, 'replicateChance') + "% to " + (getNew(player, 'replicateChance') + 1) + "%)";
  	if (capMaxedOut(player)) {
  		this.replicateCapUpgradeDescription.innerHTML = "Replicanti cap increase maxed out.";
  	} else {
  		this.replicateCapUpgradeDescription.innerHTML = "Increase the replicanti cap by 2x.<br/>(from " + decToStr(getNew(player, 'replicateCap')) + " to " + decToStr(getNew(player, 'replicateCap').times(2)) + ")";
  	}
  	this.replicateDivideUpgradeDescription.innerHTML = "Replicanti produce 1 more replicanti when replicated.<br/>(from " + (getNew(player, 'replicatePlus') + 1) + " to " + (getNew(player, 'replicatePlus') + 2) + ")";
  }
}

function displayUpdate () {
  html.update();
}

function displayOnReflection () {
  resetShownData();
}

function displayOnOverflow () {
  resetShownData();
}

function setupReplicantiUpdate (f) {
	window.setInterval(function() {
		f();
		displayUpdate();
	}, 1000);
}

function setOnclick (type, f) {
  html['replicate' + type + 'UpgradeButton'].onclick = f;
	html['replicate' + type + 'MaxUpgradeButton'].onclick = function () {
		while (f()) {};
	}
}

function setChanceOnclick (f) {
  return setOnclick('Chance', f)
}

function setCapOnclick (f) {
  return setOnclick('Cap', f)
}

function setDivideOnclick (f) {
  return setOnclick('Divide', f)
}

function setSoftenOnclick (f) {
  return setOnclick('Soften', f)
}

function done (player) {
  // This is primarily a hook to allow replacing this file with, for example,
  // an automatic tester,
  // which might use this function to start a loop which acts automatically
  // based on the values of the player.
  // However, it can also generally be used for finalizing stuff.
  setupTabs(player);
  resetShownData();
}

export {setUpdate, setReset, displayUpdate, setupReplicantiUpdate, setupSaveAndLoad,
setChanceOnclick, setCapOnclick, setDivideOnclick, setSoftenOnclick, done};
