import {Decimal} from './decimal.js';

import {setUpdate, setReset, displayUpdate, setupReplicantiUpdate, setupSaveAndLoad,
setChanceOnclick, setCapOnclick, setDivideOnclick, setSoftenOnclick, done} from './display.js';

import {loadPlayer} from './save_and_load.js';

import {stats} from './stats.js';

import {getReplicateChance, gainedReplicanti, getNew, capMaxedOut} from './game_utils.js';

let initialPlayer = {
  replicanti: new Decimal(1),
  replicateChance: 10,
  replicatePlus: 1,
  replicateCap: new Decimal(256),
  replicateChanceUpgrade: new Decimal(16),
  replicateChanceIncrease: 1,
  replicateCapUpgrade: new Decimal(256),
  replicateDivideUpgrade: Decimal.pow(16, 8),
  replicateSoftenUpgrade: Decimal.pow(16, 16),
  replicateSoftness: 0,
	new: {},
	zeroed: {},
  reflections: 0,
  overflows: 0
};

let player = {};

function makePlayer () {
	for (let i in initialPlayer) {
		player[i] = initialPlayer[i];
	}
}

makePlayer();

loadPlayer(null, function (x) {
  player = x;
});

function reset () {
	for (let i in player.new) {
		player[i] = player.new[i];
	}
	for (let i in player.zeroed) {
		player[i] = initialPlayer[i];
	}
	player.new = {};
	player.zeroed = {};
	player.replicanti = new Decimal(1);
}

setReset(reset);

setUpdate(player);

displayUpdate();

setupSaveAndLoad(function (x) {
  console.log(x);
  player = x;
}, function () {
  return player;
});

setupReplicantiUpdate(function() {
  player.replicanti = player.replicanti.plus(gainedReplicanti(player));
  if (player.replicateSoftness === 0) {
    player.replicanti = player.replicanti.min(player.replicateCap);
  }
});

function pay (cost, multiplier, effect, cond) {
  return function () {
		let safeReset = false;
		if (cond && !cond()) {
			return false;
		}
    // first branch: we're far over cost
		// second branch: we're probably just at cost, it's just a precision issue
		// third branch: we're under cost
		let replicantiCostRatio = player.replicanti.div(player[cost]);
    if (replicantiCostRatio.gte(1 + 1e-6)) {
      player.replicanti = player.replicanti.minus(player[cost]);
		} else if (replicantiCostRatio.gte(1 - 1e-6)) {
      player.replicanti = new Decimal(1);
			if (Object.keys(player.zeroed).length === 0) {
				// Nothing will be zeroed, we might as well reset automatically for the player.
				safeReset = true;
			}
		} else {
			// Purchase failed.
			return false;
		}
		// Purchase succeeded.
    effect();
    player[cost] = player[cost].times(
      typeof multiplier === 'function' ? multiplier() : multiplier)
		if (safeReset) {
			reset();
		}
    displayUpdate();
		return true;
  }
}

let replicateChanceUpgrade = pay(
  'replicateChanceUpgrade', 2, function () {
    player.new.replicateChance = getNew(player, 'replicateChance') + player.replicateChanceIncrease;
  }
);

let replicateCapUpgrade = pay(
  'replicateCapUpgrade', 2, function () {
    player.new.replicateCap = getNew(player, 'replicateCap').times(2);
  }, function () {
		return !capMaxedOut(player);
	}
);

let replicateDivideUpgrade = pay(
  'replicateDivideUpgrade', Decimal.pow(16, 4), function () {
    player.new.replicatePlus = getNew(player, 'replicatePlus') + 1;
  }
);

let zeroOnSoften = ['replicateChance', 'replicateChanceUpgrade', 'replicateCap',
'replicateCapUpgrade', 'replicatePlus', 'replicateDivideUpgrade'];

let replicateSoftenUpgrade = pay(
  'replicateSoftenUpgrade', function () {
    return Decimal.pow(16, 16 * (1 + 2 * getNew(player, 'replicateSoftness')));
  }, function () {
    player.new.replicateSoftness = getNew(player, 'replicateSoftness') + 1;
		for (let i of zeroOnSoften) {
			player.zeroed[i] = true;
		}
  }
);

setChanceOnclick(replicateChanceUpgrade);
setCapOnclick(replicateCapUpgrade);
setDivideOnclick(replicateDivideUpgrade);
setSoftenOnclick(replicateSoftenUpgrade);

done(player);
