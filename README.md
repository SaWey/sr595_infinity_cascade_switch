# sr595_infinity_cascade_switch

Allows to configure switches using sr595_infinity_cascade shield on raspberry pi using wiringpi

A simple configuration could be:
```yaml
switch:
  - platform: sr595_infinity_cascade_switch
    devices:
    - address: 1
      name: Bathroom

```

An automation action can look like this:
```yaml
action: 
  service: switch.toggle
  entity_id: switch.bathroom

```

Optionally the pin configuration can be changed:
```yaml
switch:
  - platform: sr595_infinity_cascade_switch
    base_pin: 100
    pin_count: 32
    data_pin: 12
    clock_pin: 14
    latch_pin: 10
    devices:
    - address: 1
      name: Bathroom

```

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)