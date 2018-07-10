import {Decimal} from './decimal.js';
import {a} from './basic_html.js'

function makeSave (x) {
  if (Array.isArray(x)) {
    return x.map(makeSave);
  } else if (x === null || typeof x !== 'object') {
    return x;
  } else if (x instanceof Decimal) {
    return Decimal.save(x);
  } else {
    let r = {};
    for (let i in x) {
      r[i] = makeSave(x[i]);
    }
    return r;
  }
}

function loadSave (x) {
  if (Array.isArray(x)) {
    return x.map(loadSave);
  } else if (x === null || typeof x !== 'object') {
    return x;
  } else if ('e' in x) {
    return Decimal.load(x);
  } else {
    let r = {};
    for (let i in x) {
      r[i] = loadSave(x[i]);
    }
    return r;
  }
}

function savePlayer (player) {
  let saveText = btoa(JSON.stringify(makeSave(player)));
  a('saveArea').value = saveText;
  localStorage.setItem('save', saveText);
}

function loadPlayer (p, setPlayer) {
  if (p === undefined || p === null) {
    p = localStorage.getItem('save');
  }
  if (p) {
    try {
      let loaded = loadSave(JSON.parse(atob(p)));
      if (loaded) {
        setPlayer(loaded);
      }
    } catch (e) {
      // Something went wrong.
      alert('Issue with loading!');
    }
  }
}

function setupAutoSave (getPlayer) {
  window.setInterval(function () {
    savePlayer(getPlayer())
  }, 10000);
}

export {loadPlayer, savePlayer, setupAutoSave};
