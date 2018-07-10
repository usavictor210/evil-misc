import {Decimal} from './decimal.js';

// Use this to calculate RP and OP gains, and to calculate mirrors.
function decFloor (n) {
  let v = n.toNum();
  if (Math.abs(v) < 1e100) {
    return new Decimal(Math.floor(v + 1e-9));
  } else {
    // No one will even notice.
    return v;
  }
}

function log2Bonus (x) {
  if (x.lt(2) {
    return new Decimal(1);
  } else {
    return x.decLog(2);
  }
}

export {decFloor};
