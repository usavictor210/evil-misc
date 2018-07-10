function decToStr (x) {
  if (x.lt(1000)) {
    return Math.round(x.toNum()) + '';
  } else {
    return x.toStr(2);
  }
}

function percentToStr (x) {
  if (x.gte(10 - 1e-6)) {
    return Math.round(x.toNum()) + '';
  } else if (x.gte(1)) {
    return x.toStr(2).split('e')[0];
  } else {
    return x.toStr(2);
  }
}

export {decToStr, percentToStr};
