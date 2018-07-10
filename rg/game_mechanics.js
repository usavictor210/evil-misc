import {Decimal} from './decimal.js';

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

// New stuff.

function increaseReplicanti () {
  player.replicanti = player.replicanti.times(gainedReplicantiFraction().plus(1).pow(
    getReplicantiIncreasesPerTick()));
}

function getGalaxyPower () {
  if (player.overflowUpgrades.includes(128)) {
    return 2;
  } else {
    return 1;
  }
}

function getReplicantiGalaxies () {
  let result = player.replicantiGalaxies;
  if (player.overflowUpgrades.includes(4096)) {
    result += player.capUpgrades;
  }
  return result;
}

function getReplicantiIncreasesPerTick () {
  return 1 + getReplicantiGalaxies() * getGalaxyPower();
}

function gainedReplicantiFraction (player) {
  return getReplicateChance(player).div(100).times(getReplicatePlus(player));
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

function squareReflection (x) {
  if (player.overflowUpgrades.includes(4)) {
    return x.pow(2);
  } else {
    return x;
  }
}

function getReplicatePlus (player) {
  let res = player.replicatePlus;
  res = res.times(getMirrors().plus(1));
  if (player.reflectionUpgrades.includes(256)) {
    res = res.times(squareReflection(player.reflections));
  }
  if (player.reflectionUpgrades.includes(2 ** 16)) {
    res = res.times(squareReflection(
      decFloor(log2Bonus(player.reflectionPoints))));
  }
  if (player.reflectionUpgrades.includes(2 ** 32)) {
    res = res.times(squareReflection(player.mirrorPower.max(1)));
  }
  return res;
}

function getMirrors () {
  return decFloor(player.mirrorPower.minus(1).plus(
    Decimal.pow(1 + player.replicateChance / 100, player.mirrorPower)));
}

function getCapDimensionMultiplier (i) {
  let result = player.capDimension[i].power;
  if (i === 1 && player.overflowUpgrades.includes(16)) {
    result = result.times(log2Bonus(log2Bonus(player.replicanti)));
  }
  if (i === 2 && player.overflowUpgrades.includes(32)) {
    result = result.times(log2Bonus(log2Bonus(player.reflectionPoints)));
  }
  if (player.overflowUpgrades.includes(256)) {
    result = result.times(player.overflows);
  }
  if (player.overflowUpgrades.includes(2 ** 24)) {
    result = result.times(log2Bonus(player.capPower));
  }
  return result;
}

function increaseCapUpgrades () {
  while (player.capUpgradeThreshold.lt(player.capPower.times(1 + 1e-6))) {
    player.capUpgrades += 1;
    player.capUpgradeThreshold = player.capUpgradeThreshold.times(
      player.capUpgradeMultiplier);
    if (player.capUpgradeThreshold.gt(Decimal.pow(2, 64))) {
      player.capUpgradeMultiplier = player.capUpgradeMultiplier.times(257 / 256);
    }
  }
}

function increaseCapDimensions () {
  player.capPower = player.capPower.plus(player.capDimension[1].amount.times(
    getCapDimensionMultiplier(1)))
  for (let i = 1; i <= 4; i++) {
    player.capDimension[i].amount = player.capDimension[i].amount.plus(
      player.capDimension[i + 1].amount.times(
        getCapDimensionMultiplier(i + 1)));
  }
  increaseCapUpgrades();
}

// TODO functions to buy and reset stuff

// there are 10 types of autobuyer purchases and resets

// there are also cap dimensions and overflow upgrades,
// which are not among those ten.

// We thus probably need 12 functions to buy stuff.

function runAutobuyers () {
  // TODO
}

function tick (player) {
  increaseReplicanti();
  increaseCapDimensions();
  runAutobuyers();
}

export {getReplicateChance, gainedReplicanti, getNew, capMaxedOut};
