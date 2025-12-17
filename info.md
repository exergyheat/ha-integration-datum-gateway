# DATUM Gateway Integration

Monitor your DATUM Gateway Bitcoin mining operations directly in Home Assistant.

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

## Configuration

After installation, add the integration via:

**Settings** → **Devices & Services** → **Add Integration** → Search for "DATUM Gateway"

### Required Settings
- **Gateway URL**: Full HTTPS URL to your DATUM Gateway dashboard
  - Example: `https://your-gateway.local`
  - Example: `https://192.168.1.100`

### Optional Settings  
- **Verify SSL**: Enable/disable SSL certificate verification
  - Set to `false` for self-signed certificates (recommended for local gateways)

## Requirements

- Home Assistant 2023.1 or newer
- DATUM Gateway with accessible web dashboard
- Network connectivity between HA and gateway

## Support

- **Integration Issues**: [GitHub Issues](https://github.com/exergyheat/ha-integration-datum-gateway/issues)
- **DATUM Gateway**: https://github.com/OCEAN-xyz/datum_gateway
- **Ocean Mining Pool**: https://ocean.xyz
