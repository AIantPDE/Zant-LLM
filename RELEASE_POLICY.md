# Release Policy

A version successor is not accepted from the delivery package alone. v1.6R uses gate-aware successor input hydration and actual successor resolution.

Required before accepting the next stage:

1. local validation green;
2. stdlib tests green;
3. gate report complete;
4. receipt seal valid;
5. successor input values are concrete booleans;
6. resolver-selected actual successor is present;
7. runtime authority remains false;
8. provider dispatch remains false.
