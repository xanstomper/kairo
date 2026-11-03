# KAIRO — Offensive Hardware Batteries (five planes)

Decisive tests per plane. Every probe: minimal, non-destructive, documented-PoC
adaptation only. Score before running (family E/I/L/R/N × time-weight inside 3AM
engagements). Ledger every negative with its exact test. A positive triggers the
control proof (read-only) then the crown-jewel question: **what does this device
reach?**

Kit baseline: logic analyzer (OpenBench logic sniffer/Saleae-class), USB-UART
(CP2102/CH340), SPI/NAND flash clip or SOIC-8 probes, Bus Pirate/FT2232H-class
multiprotocol, SDR (HackRF/RTL-SDR), YubiKey-class NFC reader, shielded enclosure
for RF work, hot air + soldering (destructive ops require per-device opt-in).

## Plane 1 — Firmware & storage

| Probe | Test | Confirmed-when |
|---|---|---|
| Extraction (SPI) | `flashrom -p ch341a_spi -r fw.bin` on pinned flash (owned board) | full image read |
| Extraction (eMMC/NAND) | footprint/`nanddump` on owned inline-eMMC dev boards | userspace files visible |
| Filesystem carve | `binwalk -Me fw.bin` → squashfs/cpio/ubifs | filesystem mounts |
| String sweep | `strings -n 6 fw.bin` + targeted grep (`passwd`, `key`, `token`, `192.168`, `/dev/tty`) | credentials/keys/hosts in image |
| Update package | capture OTA (`mitmproxy` on own update endpoint) → sign/format inspect | unencrypted or unsigned payload |
| Signature check | extract pubkey (`openssl x509`/`uefi-firmware-parser`), test rollback of OLD signed version (owned device) | old image accepted = rollback open |
| Secure boot chain | `cbmem`/UEFI vars/`sbctl status`-class read on owned device | chain config identifies trust root |

Typical yields: plaintext credentials, hardcoded API/cloud keys, hidden debug UART
configs, unsigned OTA → arbitrary firmware (confirmation via one shell command on the
owned device, then STOP).

## Plane 2 — Interfaces

| Probe | Test | Confirmed-when |
|---|---|---|
| UART discovery | 4-pin header detection (GND sweep) → `minicom` @ 115200/57600 | bootloader/root shell banner |
| UART login | `root`/empty/`admin`/vendor defaults at the serial prompt | shell or `$` prompt |
| JTAG/SWD | `openocd -f interface/ftdi.cfg` on owned board; `jtagscan`-class pin find | debug access or IDCODE read |
| Bus sniffing | logic analyzer on SPI/I²C to crypto IC / flash on owned board | key material or plaintext on the bus |
| USB | `lsusb` descriptors, `usbhid-dump` on owned device, DFU mode check | hidden DFU/update mode exposed |
| Crypto/Secure element | MITM the element's bus (owned board); read-back attempt | key read or bus-level bypass |

## Plane 3 — Radio & wireless

| Probe | Test | Confirmed-when |
|---|---|---|
| WiFi WPS | `reaver`/`wash` on OWN AP (lab) — WPS enabled + no lockout | WPS active, no rate-limit |
| WiFi handshake | `airmon-ng` own AP capture → PMKID check (owned infra) | PMKID present = offline attack feasible |
| BLE GATT | `bluetoothctl`/`gatttool` scan + services on OWN device | writable characteristic without auth |
| BLE pairing | legacy pairing (no MITM) on owned peripheral | Just-Works pairing accepted |
| RFID/NFC | `libnfc`/Proxmark read of OWN badge; identify tag type + locks | tag readable / rolling code pattern observed |
| ISM/SDR | HackRF capture of own remote's 433/868MHz frames → decode/replay feasibility | frame structure + fixed code (or rolling with sync) |
| Zigbee/Z-Wave | SDR/Conbee scan of own network keys exchange | network key captured on own coordinator |

RF rule: transmit ONLY against operator-owned hardware in the operator's own lab;
document frequency/power before any tx.

## Plane 4 — Protocol & logic

| Probe | Test | Confirmed-when |
|---|---|---|
| Vendor protocol fuzz-lite | grammar probe of a single field on owned device (one malformed packet) | crash/exception observed (documented-PoC) |
| MQTT | connect to OWN broker with empty creds; subscribe `#` | topics stream without auth |
| Modbus/DNP3 | read-only register/coil read on OWN PLC/RTU test rig | values returned without auth |
| Cloud-device trust | MITM device↔app TLS (own cert) on owned device; inspect API calls | device token/key visible in transit |
| Update channel | intercept own device's update check; serve unsigned modified image in LAB | device applies it |
| Dongle/license | USB capture of OWN dongle protocol → replay analysis | auth token replayable |

## Plane 5 — Physical & supply

| Probe | Test | Confirmed-when |
|---|---|---|
| Tamper/documentation | visual + silkscreen review (no opening if not owned) | exposed debug headers, test points |
| Default credentials | documented vendor default lists vs device login (declared estate) | login with default |
| OEM/ODM surface | firmware strings/manufacturer portal enumeration (public) | OEM image/backdoor suspicion documented |
| Implant analysis | on OWN device: PCB review, unknown-component identification | unexpected modem/crypto/logging IC |
| Supply-chain image | hash + sign comparison of shipped image vs vendor published (owned) | image mismatch |

## Control proof & crown jewels

Confirmed plane finding → one read-only proof (shell `id`, bus byte read, key
extraction hash) → STOP. Then chain: what does the device reach? (cloud API, adjacent
network, OTA server, other devices). Record the chain per 3AM/T1–T7 style:
`uart-shell→firmware-keys→cloud-api:TAKEOVER` where the final hop is proven read-only.

## Negatives & decay

- Negatives are results — exact test string in the ledger, never re-probed without a
  change (firmware version, access level, new kit).
- Findings decay: firmware updates kill rollback findings; radio state drifts; cloud
  trust changes. Re-verify before citing.

## Kit honesty

Missing kit is not a blocker — it is a named gap: `HYPOTHESIS + exact unlock
condition` (e.g. "needs logic analyzer on SPI bus of owned board"). Ship the gap, buy
the probe, re-run.