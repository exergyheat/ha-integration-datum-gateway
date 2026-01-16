# Exergy - DATUM Gateway Custom Integration for Home Assistant

A custom Home Assistant integration for monitoring DATUM Gateway Bitcoin mining operations.

## Features

### Mining Performance Sensors
- **Total Hashrate** - Real-time combined hashrate (TH/s)
- **Per-Thread Hashrate** - Individual miner/thread performance
- **Shares Accepted** - Counter of accepted shares
- **Shares Rejected** - Counter of rejected shares
- **Acceptance Rate** - Calculated success percentage

### Pool Status
- **Pool Status** - Connection state (connected/disconnected)
- **Pool Host** - Current pool endpoint
- **Miner Tag** - Your configured mining tag

### System Monitoring
- **Active Threads** - Number of active mining threads
- **Total Connections** - Connected miners count
- **Uptime** - Gateway process uptime

### Block Template Info
- **Block Height** - Current block being mined
- **Block Value** - Current block reward (BTC)
- **Transaction Count** - Transactions in current template

## Installation

### Method 1: Manual Installation

1. Copy the `custom_components/datum_gateway` folder to your Home Assistant `custom_components` directory:
   ```
   config/
     custom_components/
       datum_gateway/
         __init__.py
         config_flow.py
         const.py
         datum_api.py
         manifest.json
         sensor.py
         strings.json
   ```

2. Restart Home Assistant

3. Go to **Settings** → **Devices & Services** → **Add Integration**

4. Search for "Exergy - DATUM Gateway"

5. Enter your DATUM Gateway URL (e.g., `https://your-datum-gateway-url.local` or '197.16.0.100')

6. Uncheck "Verify SSL certificate" if using self-signed certificate

7. Click Submit

### Method 2: HACS (Future)

_This integration will be submitted to HACS for easier installation._

## Configuration

### Required Settings
- **Gateway URL**: Full HTTPS URL to your DATUM Gateway dashboard
  - Example: `https://your-gateway.local`
  - Example: `https://192.168.1.100`

### Optional Settings  
- **Verify SSL**: Enable/disable SSL certificate verification
  - Set to `false` for self-signed certificates (recommended for local gateways)

## Supported DATUM Gateway Versions

- ✅ DATUM Gateway v0.4.0-beta and newer
- ⚠️ Older versions may work but are untested

## Sensors Created

After setup, the following sensors will be available:

| Entity ID | Description | Unit | Type |
|-----------|-------------|------|------|
| `sensor.datum_gateway_total_hashrate` | Total mining hashrate | TH/s | Measurement |
| `sensor.datum_gateway_shares_accepted` | Total shares accepted | - | Counter |
| `sensor.datum_gateway_shares_rejected` | Total shares rejected | - | Counter |
| `sensor.datum_gateway_acceptance_rate` | Share acceptance percentage | % | Measurement |
| `sensor.datum_gateway_pool_status` | Pool connection status | - | State |
| `sensor.datum_gateway_pool_host` | Pool hostname | - | Diagnostic |
| `sensor.datum_gateway_miner_tag` | Your miner tag | - | Diagnostic |
| `sensor.datum_gateway_active_threads` | Active mining threads | - | Measurement |
| `sensor.datum_gateway_total_connections` | Connected miners | - | Measurement |
| `sensor.datum_gateway_uptime` | Gateway uptime | - | Diagnostic |
| `sensor.datum_gateway_block_height` | Current block height | - | Measurement |
| `sensor.datum_gateway_block_value` | Current block reward | BTC | Measurement |
| `sensor.datum_gateway_transaction_count` | Transactions in template | - | Measurement |
| `sensor.datum_gateway_thread_0_hashrate` | Thread 0 hashrate | TH/s | Measurement |
| `sensor.datum_gateway_thread_1_hashrate` | Thread 1 hashrate | TH/s | Measurement |

## Usage Examples

### Create Automations

```yaml
automation:
  - alias: "Alert on Pool Disconnect"
    trigger:
      - platform: state
        entity_id: sensor.datum_gateway_pool_status
        to: "disconnected"
        for:
          minutes: 2
    action:
      - service: notify.mobile_app
        data:
          title: "Mining Pool Disconnected"
          message: "DATUM Gateway lost connection to pool"
```

### Dashboard Card

```yaml
type: entities
title: Mining Performance
entities:
  - entity: sensor.datum_gateway_total_hashrate
    name: Hashrate
  - entity: sensor.datum_gateway_acceptance_rate
    name: Success Rate
  - entity: sensor.datum_gateway_pool_status
    name: Pool
  - entity: sensor.datum_gateway_shares_accepted
    name: Accepted Shares
```

### Lovelace Gauge

```yaml
type: gauge
entity: sensor.datum_gateway_total_hashrate
name: Mining Hashrate
min: 0
max: 100
needle: true
```

## Troubleshooting

### Sensors Show "Unavailable"

1. **Check Gateway URL**: Ensure the URL is correct and accessible from Home Assistant
2. **Test Connection**: Try accessing the URL in a browser
3. **SSL Certificate**: If using self-signed cert, ensure "Verify SSL" is unchecked
4. **Network Access**: Verify Home Assistant can reach the gateway IP
5. **Check Logs**: Review Home Assistant logs for specific errors

### Connection Errors

```bash
# Test from Home Assistant host
curl -k https://your-gateway-url/
```

If this fails, check:
- Gateway is running and accessible
- Firewall rules allow access
- DNS resolution (try IP address instead of hostname)

### Data Not Updating

- Default update interval: 30 seconds
- Check Home Assistant logs for errors
- Verify gateway dashboard loads correctly in browser
- Restart the integration: Settings → Devices & Services → Exergy - DATUM Gateway → Reload

## Requirements

- Home Assistant 2023.1 or newer
- DATUM Gateway with accessible web dashboard
- Network connectivity between HA and gateway

## Development

### Dependencies
- `beautifulsoup4>=4.12.2` - HTML parsing
- `requests` - HTTP client (included in HA)

### Testing Locally

1. Clone this repository
2. Copy to HA `custom_components` directory
3. Restart HA and configure via UI

### Contributing

Contributions welcome! Please:
1. Test changes with your DATUM Gateway
2. Follow Home Assistant development guidelines
3. Update documentation for new features

## Support

- **DATUM Gateway Issues**: https://github.com/OCEAN-xyz/datum_gateway/issues
- **Integration Issues**: https://github.com/exergyheat/ha-integration-datum-gateway/issues
- **Ocean Mining Pool**: https://ocean.xyz

## Credits

- **DATUM Gateway**: Created by OCEAN.xyz and Bitcoin Ocean, LLC
- **Integration**: Developed by Exergy

## License

MIT License - See LICENSE file for details
