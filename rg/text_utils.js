function plural (x) {
  if (x.endsWith('power') || x.endsWith('replicanti')) {
    return x;
  } else if (x[x.length - 1] === 'y') {
    return x.slice(0, -1) + 'ies';
  } else {
    return x + 's';
  }
}

export {plural};
