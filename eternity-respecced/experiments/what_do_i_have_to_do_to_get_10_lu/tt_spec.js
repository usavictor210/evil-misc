let [ip, timeshards, tt, galPower, secondsInInfinity] = process.argv.slice(2).map(x => +x);

let getGalaxies = function (x) {
  return Math.floor((getEighths(x) - 10) / 60);
}

let getBoosts = function (x) {
  return 5 + Math.floor((getEighths(x) - 10) / 15);
}

let eighthMemo = {};

let getEighths = function (x) {
  if (x in eighthMemo) {
    return eighthMemo[x];
  }
  let am = getAM(x);
  let gotten = 0;
  let cost = 24;
  let inc = 15;
  let inf = Math.log10(2) * 1024;
  while (am >= cost) {
    gotten += 10;
    cost += inc;
    if (cost > inf) {
      inc += Math.log10(3);
    }
  }
  eighthMemo[x] = gotten;
  return gotten;
}

let getAM = function (x) {
  // seems about right
  return x * 205;
}

let getBaseSac = function (x) {
  // yes, I know, not exactly 7 / 8 but this is an approximation.
  return getAM(x) * .012 * (7 / 8);
}

function get_c (st) {
  return Math.pow(4 / 3, 1 / (1 + st / 10))
}

function getTotalTickGained (timeshards, st) {
  if (timeshards < 1) {
    return 0;
  }
  let timeshardLn = Math.log(timeshards);
  let c = get_c(st);
  // we know that ln(1.001) * (x - 1) * x / 2 + ln(c) * x <= timeshardLn
  // so ln(1.001) / 2 * x^2 + (ln(c) - ln(1.001) / 2) * x - timeshardLn <= 0
  let a = Math.log(1.001) / 2;
  let b = Math.log(c) - a;
  let solution = (-b + Math.sqrt(Math.pow(b, 2) + 4 * a * timeshardLn)) / (2 * a);
  let realSolution = Math.floor(solution) + 1
  return realSolution;
}

let getRG = function (x) {
  let c = 170;
  let n = 0;
  while (c <= x) {
    c += 5 * (n + 5);
    n += 1;
  }
  return n;
}

let getTickPower = function (x) {
  return Math.log10(1 / 0.965) * (getGalaxies(x) + getRG(x)) * 3.3
}

let getTSPower = [null, null, null, null, null, null];

getTSPower[0] = function (x, sh, s, st) {
  return getBaseSac(x) * Math.log(1 + st / 10) / 8;
}

getTSPower[1] = function (x, sh, s, st) {
  return getTickPower(x) * (getTotalTickGained(sh, st) - getTotalTickGained(sh, 0));
}

getTSPower[2] = function (x, sh, s, st) {
  return Math.log10(2 ** (galPower * 5)) * 56 * st;
}

getTSPower[3] = function (x, sh, s, st) {
  return getBoosts(x) * Math.log10(1 + st / 4);
}

// I think infinity power and infinity points are fairly close, usually.
getTSPower[4] = function (x, sh, s, st) {
  return (5 - Math.log(s) / Math.log(10)) * 1.1 * 56 * st;
}

getTSPower[5] = function (x, sh, s, st) {
  return Math.log(s) / Math.log(10) * 1.1 * 56 * st;
}

let cartPow = function (l, n) {
  if (n === 0) {
    return [[]];
  } else {
    let r = cartPow(l, n - 1)
    return [].concat(...l.map((i) => r.map((j) => [i].concat(j))))
  }
}

let l = [];
let h = {};
for (let i of cartPow([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 6)) {
  if (i.map((x) => x * (x + 1) / 2).reduce((a, b) => a + b) <= tt) {
    l.push(i.join(' '));
    h[i.join(' ')] = i.map((x, i) => getTSPower[i](ip, timeshards, secondsInInfinity, x)).reduce(
      (a, b) => a + b);
  }
}

l.sort((a, b) => h[b] - h[a]);

console.log(l.slice(0, 5).map((x) => [x, h[x]]));
