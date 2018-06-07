import {Decimal} from './decimal.js';

function gainedReplicanti (player) {
  return player.replicanti.times(getReplicateChance(player).div(100)).times(player.replicatePlus);
}

function getReplicateChance (player) {
  return Decimal.pow(2, -Math.max(getSoftnessOver(player), 0)).times(player.replicateChance);
}

function getSoftnessOver (player) {
  if (player.replicateSoftness === 0) {
    return 0;
  } else {
    return (player.replicanti.ln() / player.replicateCap.ln() - 1) * 16 / player.replicateSoftness;
  }
}

function getNew (player, x) {
	if (x in player.new) {
		return player.new[x];
	} else {
		return player[x];
	}
}

function capMaxedOut (player) {
	return getNew(player, 'replicateCap').gt(Decimal.pow(2, 1024).times(1 - 1e-6));
}

export {getReplicateChance, gainedReplicanti, getNew, capMaxedOut};
