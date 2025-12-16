"""API Client for DATUM Gateway."""
import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Any

_LOGGER = logging.getLogger(__name__)


class DatumGatewayAPI:
    """DATUM Gateway API client."""

    def __init__(self, host: str, verify_ssl: bool = False) -> None:
        """Initialize the API client."""
        self.host = host.rstrip("/")
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        
    def _get_page(self, endpoint: str) -> str:
        """Fetch a page from the gateway."""
        url = f"{self.host}{endpoint}"
        try:
            response = self.session.get(url, verify=self.verify_ssl, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as err:
            _LOGGER.error(f"Error fetching {url}: {err}")
            raise
    
    def _extract_text_by_label(self, soup: BeautifulSoup, label: str) -> str:
        """Extract text value for a given label from table."""
        try:
            label_td = soup.find("td", class_="label", string=lambda text: label in text if text else False)
            if label_td:
                value_td = label_td.find_next_sibling("td")
                if value_td:
                    return value_td.get_text(strip=True)
        except Exception as err:
            _LOGGER.debug(f"Error extracting {label}: {err}")
        return None
    
    def get_status(self) -> dict[str, Any]:
        """Get status data from main dashboard."""
        html = self._get_page("/")
        soup = BeautifulSoup(html, "html.parser")
        
        data = {}
        
        # Extract total hashrate
        hashrate_text = self._extract_text_by_label(soup, "Estimated Hashrate:")
        if hashrate_text:
            match = re.search(r"([0-9.]+)\s*Th/sec", hashrate_text)
            if match:
                data["total_hashrate"] = float(match.group(1))
        
        # Extract shares accepted
        shares_accepted_text = self._extract_text_by_label(soup, "Shares Accepted:")
        if shares_accepted_text:
            match = re.search(r"^([0-9]+)", shares_accepted_text)
            if match:
                data["shares_accepted"] = int(match.group(1))
            # Extract difficulty
            diff_match = re.search(r"\(([0-9]+)\s+diff\)", shares_accepted_text)
            if diff_match:
                data["difficulty_accepted"] = int(diff_match.group(1))
        
        # Extract shares rejected
        shares_rejected_text = self._extract_text_by_label(soup, "Shares Rejected:")
        if shares_rejected_text:
            match = re.search(r"^([0-9]+)", shares_rejected_text)
            if match:
                data["shares_rejected"] = int(match.group(1))
            # Extract difficulty
            diff_match = re.search(r"\(([0-9]+)\s+diff\)", shares_rejected_text)
            if diff_match:
                data["difficulty_rejected"] = int(diff_match.group(1))
        
        # Calculate acceptance rate
        if "shares_accepted" in data and "shares_rejected" in data:
            total = data["shares_accepted"] + data["shares_rejected"]
            if total > 0:
                data["acceptance_rate"] = round((data["shares_accepted"] / total) * 100, 2)
        
        # Extract pool status
        status_text = self._extract_text_by_label(soup, "Status:")
        if status_text:
            data["pool_status"] = "connected" if "Connected and Ready" in status_text else "disconnected"
        
        # Extract pool host
        pool_host = self._extract_text_by_label(soup, "Pool Host:")
        if pool_host:
            data["pool_host"] = pool_host
        
        # Extract miner tag
        miner_tag = self._extract_text_by_label(soup, "Secondary/Miner Tag:")
        if miner_tag:
            data["miner_tag"] = miner_tag.strip('"')
        
        # Extract uptime
        uptime = self._extract_text_by_label(soup, "Process uptime:")
        if uptime:
            data["uptime"] = uptime
        
        # Extract active threads
        threads_text = self._extract_text_by_label(soup, "Active Threads:")
        if threads_text:
            match = re.search(r"([0-9]+)", threads_text)
            if match:
                data["active_threads"] = int(match.group(1))
        
        # Extract total connections
        connections_text = self._extract_text_by_label(soup, "Total Connections:")
        if connections_text:
            match = re.search(r"([0-9]+)", connections_text)
            if match:
                data["total_connections"] = int(match.group(1))
        
        # Extract block height
        block_height_text = self._extract_text_by_label(soup, "Block Height:")
        if block_height_text:
            match = re.search(r"([0-9]+)", block_height_text)
            if match:
                data["block_height"] = int(match.group(1))
        
        # Extract block value
        block_value_text = self._extract_text_by_label(soup, "Block Value:")
        if block_value_text:
            match = re.search(r"([0-9.]+)\s*BTC", block_value_text)
            if match:
                data["block_value"] = float(match.group(1))
        
        # Extract transaction count
        txn_count_text = self._extract_text_by_label(soup, "Txn Count:")
        if txn_count_text:
            match = re.search(r"([0-9]+)", txn_count_text)
            if match:
                data["transaction_count"] = int(match.group(1))
        
        # Extract pool minimum difficulty
        mindiff_text = self._extract_text_by_label(soup, "Pool Current MinDiff:")
        if mindiff_text:
            match = re.search(r"([0-9]+)", mindiff_text)
            if match:
                data["pool_mindiff"] = int(match.group(1))
        
        return data
    
    def get_threads(self) -> dict[str, Any]:
        """Get thread data from threads page."""
        html = self._get_page("/threads")
        soup = BeautifulSoup(html, "html.parser")
        
        data = {"threads": []}
        
        # Find all table rows
        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                # Check if first cell is a number (TID)
                tid_text = cells[0].get_text(strip=True)
                if tid_text.isdigit():
                    thread_data = {
                        "tid": int(tid_text),
                        "connections": int(cells[1].get_text(strip=True)),
                        "subscriptions": int(cells[2].get_text(strip=True)),
                    }
                    
                    # Extract hashrate
                    hashrate_text = cells[3].get_text(strip=True)
                    match = re.search(r"([0-9.]+)\s*Th/s", hashrate_text)
                    if match:
                        thread_data["hashrate"] = float(match.group(1))
                    
                    data["threads"].append(thread_data)
        
        return data
