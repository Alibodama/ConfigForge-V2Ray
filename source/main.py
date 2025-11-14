import os
import re
import json
import socket
import random
import asyncio
import logging
import base64
import requests
import httpx
import urllib3
import zoneinfo
import ipaddress
from urllib.parse import quote, urlsplit, urlunsplit, unquote
from datetime import datetime
from functools import lru_cache
from collections import defaultdict

# ============================== Configuration ==============================

URLS = [
    "https://raw.githubusercontent.com/MrAbolfazlNorouzi/iran-configs/refs/heads/main/configs/working-configs.txt",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    "https://www.v2nodes.com/subscriptions/country/all/?key=CCAD69583DBA2BF",
    "https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt",
]

OUTPUT_DIR = "configs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

ZONE = zoneinfo.ZoneInfo("Asia/Tehran")

# ============================== Base64 / Geo ===============================

geo_cache: dict[str, str] = {}

def b64_decode(s: str) -> str:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s + pad).decode(errors="ignore")

def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

def b64url_decode(s: str) -> bytes:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(s + pad)

def b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

def country_flag(code: str) -> str:
    if not code:
        return "🏳️"
    c = code.strip().upper()
    if len(c) != 2 or not c.isalpha():
        return "🏳️"
    return chr(ord(c[0]) + 127397) + chr(ord(c[1]) + 127397)

def get_country_by_ip(ip: str) -> str:
    if ip in geo_cache:
        return geo_cache[ip]
    try:
        r = requests.get(f"https://ipwhois.app/json/{ip}", timeout=5)
        if r.status_code == 200:
            code = r.json().get("country_code", "unknown").lower()
            geo_cache[ip] = code
            return code
    except Exception as e:
        logging.warning(f"Geolocation lookup failed for {ip}: {e}")
    geo_cache[ip] = "unknown"
    return "unknown"

# ============================== Fetch / Decode =============================

def fetch_data(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": CHROME_UA}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, verify=False)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.error(f"Download error for {url}: {e}")
        return ""

def maybe_base64_decode(s: str) -> str:
    s = s.strip()
    try:
        decoded = b64_decode(s)
        if "://" in decoded:
            return decoded.strip()
    except Exception:
        pass
    return s

# ============================== Parsing / Netloc ===========================

def normalize_proto(proto: str) -> str:
    p = proto.lower()
    if p in ("ss", "shadowsocks"):
        return "shadowsocks"
    if p in ("hy2", "hysteria2"):
        return "hysteria2"
    if p.startswith("hysteria"):
        return "hysteria"
    return p

def detect_protocol(link: str) -> str:
    m = re.match(r"([a-z0-9+.-]+)://", link.strip().lower())
    if not m:
        return "unknown"
    return normalize_proto(m.group(1))

def is_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False

def split_host_port(raw_hostport: str) -> tuple[str, str]:
    """
    Extract host and port from a netloc or 'host:port' string.
    - Strips userinfo if present (user:pass@host:port)
    - Handles IPv6 with or without brackets
    - Returns (host, port_or_empty)
    """
    hp = unquote(raw_hostport.strip())
    if "@" in hp:
        hp = hp.split("@", 1)[1]
    if hp.startswith("["):
        m = re.match(r"^\[(.+?)\](?::(\d+))?$", hp)
        if m:
            return m.group(1), (m.group(2) or "")
    if hp.count(":") > 1:
        return hp, ""  # likely raw IPv6 without port
    if ":" in hp:
        h, p = hp.rsplit(":", 1)
        return h, p
    return hp, ""

def format_hostport(host: str, port: str | int | None) -> str:
    """Build a valid netloc host:port, adding brackets for IPv6."""
    p = str(port) if port else "443"
    h = f"[{host}]" if (":" in host and not host.startswith("[")) else host
    return f"{h}:{p}"

def extract_host(link: str, proto: str) -> str:
    """
    Return 'host:port' (no userinfo) if possible, else ''.
    Handles vmess/ss/ssr explicitly; falls back to URL parsing for URL-like schemes.
    """
    try:
        if proto == "vmess":
            cfg = json.loads(b64_decode(link.split("://", 1)[1]))
            host = str(cfg.get("add", "")).strip()
            port_val = cfg.get("port", "")
            port = str(port_val).strip() if port_val != "" else ""
            return f"{host}:{port}" if host and port else host or ""

        if proto == "shadowsocks":
            body = link.split("ss://", 1)[1]
            if "#" in body:
                body = body.split("#", 1)[0]
            if "@" in body:
                _creds, hostport = body.split("@", 1)
                return hostport
            try:
                decoded = b64_decode(body)
                if "@" in decoded and ":" in decoded.split("@", 1)[0]:
                    _creds, hostport = decoded.split("@", 1)
                    return hostport
            except Exception:
                pass
            return ""

        if proto == "ssr":
            raw = link.split("ssr://", 1)[1]
            decoded = b64url_decode(raw).decode(errors="ignore")
            main = decoded.split("/?", 1)[0]
            parts = main.split(":")
            if len(parts) >= 2:
                return f"{parts[0]}:{parts[1]}"
            return ""

        p = urlsplit(link)
        netloc = p.netloc
        if "@" in netloc:
            netloc = netloc.split("@", 1)[1]
        return netloc
    except Exception as e:
        logging.debug(f"extract_host error for [{proto}] {link}: {e}")
        return ""

# ============================== Async Ping =================================

_connection_limit = asyncio.Semaphore(10)

def _has_ok(data: dict) -> bool:
    """True if any node entry contains at least one OK measurement.
    Accept both shapes: entries[0] = [[status, time, *opt], ...] or list of dicts.
    """
    if not isinstance(data, dict):
        return False
    for entries in data.values():
        try:
            if not entries:
                continue
            first = entries[0]
            if isinstance(first, (list, tuple)):
                for row in first:
                    if isinstance(row, (list, tuple)) and row and row[0] == "OK":
                        return True
            for row in entries:
                if isinstance(row, dict) and row.get("status") == "OK":
                    return True
        except Exception:
            continue
    return False

async def run_ping_once(client: httpx.AsyncClient, host: str, timeout: int = 45, retries: int = 3) -> dict:
    """
    Ping a host via check-host.net with retries.
    Returns a dict: {"results": <node->entries map>, "node_cc": <node->cc map>}
    Host must be plain (no userinfo/port).
    """
    if not host:
        return {}
    base = "https://check-host.net"

    async with _connection_limit:
        for attempt in range(1, retries + 1):
            try:
                r1 = await client.get(
                    f"{base}/check-ping",
                    params={"host": host},
                    headers={"Accept": "application/json"},
                    timeout=timeout,
                )
                if r1.status_code in (429, 503):
                    wait = random.uniform(2, 5)
                    logging.warning(f"{r1.status_code} for {host}, retry {attempt}/{retries} after {wait:.1f}s")
                    await asyncio.sleep(wait)
                    continue

                r1.raise_for_status()
                j1 = r1.json()
                req_id = j1.get("request_id")
                if not req_id:
                    return {}

                # Build node->cc map from this specific check-ping response
                nodes_map: dict[str, str] = {}
                nodes_json = j1.get("nodes", {}) or {}
                for node, arr in nodes_json.items():
                    cc = None
                    try:
                        if isinstance(arr, (list, tuple)) and arr:
                            cc = str(arr[0]).lower()
                    except Exception:
                        pass
                    base_node = node.split("/", 1)[0].split(":", 1)[0].lower()
                    if cc:
                        nodes_map[base_node] = cc

                # initial wait
                await asyncio.sleep(4)

                max_polls = 45  # ~135s with sleep=3
                got_partial_any = False
                last_data = {}
                for _ in range(max_polls):
                    await asyncio.sleep(3)
                    try:
                        r2 = await client.get(
                            f"{base}/check-result/{req_id}",
                            headers={"Accept": "application/json"},
                            timeout=timeout,
                        )
                        if r2.status_code in (429, 503):
                            await asyncio.sleep(3 + random.random() * 2)
                            continue
                        r2.raise_for_status()
                        data = r2.json() or {}
                        if data:
                            got_partial_any = True
                            last_data = data
                            if _has_ok(data):
                                return {"results": data, "node_cc": nodes_map}
                    except httpx.ReadTimeout:
                        continue
                    except Exception as e:
                        logging.debug(f"check-result error for {host}: {e}")
                        continue

                if got_partial_any:
                    return {"results": last_data, "node_cc": nodes_map}
                break

            except Exception as e:
                logging.error(f"Ping error for {host} (attempt {attempt}): {e}")
                await asyncio.sleep(2)

    return {}

# --- entries parsing that tolerates alternate shapes ---

def _iter_ok_pings(entries):
    """Yield ping times (seconds) for OK rows across both API shapes."""
    if entries is None:
        return
    # classic/list shape under entries[0]
    try:
        seq = entries[0]
        if isinstance(seq, (list, tuple)):
            for row in seq:
                if isinstance(row, (list, tuple)) and row and row[0] == "OK":
                    if len(row) >= 2:
                        try:
                            yield float(row[1])
                        except Exception:
                            continue
        return
    except Exception:
        pass
    # list-of-dicts fallback
    try:
        for row in entries:
            if isinstance(row, dict) and row.get("status") == "OK":
                t = row.get("time")
                if t is not None:
                    try:
                        yield float(t)
                    except Exception:
                        continue
    except Exception:
        return

# ============================== Node Maps / Latency ========================

async def get_nodes_by_country(client: httpx.AsyncClient) -> dict[str, list[str]]:
    """
    Fetch check-host nodes and group them by country code.
    (Used to decide which country folders to emit; per-host mapping comes from check-ping.)
    """
    url = "https://check-host.net/nodes/hosts"
    try:
        r = await client.get(url, headers={"Accept": "application/json"}, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        logging.error(f"Error fetching nodes list: {e}")
        return {}

    mapping: dict[str, list[str]] = {}
    for node, info in data.get("nodes", {}).items():
        loc = info.get("location", [])
        if isinstance(loc, list) and loc:
            mapping.setdefault(str(loc[0]).lower(), []).append(node)
    return mapping

def _derive_cc_from_node(node: str) -> str:
    node = node.split("/", 1)[0].split(":", 1)[0].lower()
    first = node.split(".", 1)[0]
    m = re.match(r"^([a-z]{2})", first)
    return m.group(1) if m else ""

def latencies_by_cc_from_results(results: dict, node_to_cc: dict[str, str]) -> dict[str, float]:
    """Average latency per country-code from a single host's results.
    Prefer explicit node_to_cc mapping from the same request; fall back to deriving from node id.
    """
    pings_by_cc: dict[str, list[float]] = defaultdict(list)
    for node, entries in (results or {}).items():
        base_node = node.split("/", 1)[0].split(":", 1)[0]
        cc = node_to_cc.get(base_node)
        if not cc:
            cc = _derive_cc_from_node(base_node)
        if not cc:
            continue
        for ping in _iter_ok_pings(entries):
            pings_by_cc[cc].append(ping)
    return {cc: (sum(v)/len(v)) if v else float("inf") for cc, v in pings_by_cc.items()}

def extract_latency_global(results: dict) -> float:
    """Compute global average latency across all nodes for a single host."""
    pings: list[float] = []
    for node, entries in (results or {}).items():
        for ping in _iter_ok_pings(entries):
            pings.append(ping)
    return (sum(pings) / len(pings)) if pings else float("inf")

# ============================== Output =====================================

def save_to_file(path: str, lines: list[str]):
    """Save a list of configuration lines to a file."""
    if not lines:
        logging.warning(f"No lines to save: {path}")
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logging.info(f"Saved: {path} ({len(lines)} lines)")

# ============================== Renaming ===================================

def _build_tag(ip: str) -> str:
    country = get_country_by_ip(ip)
    flag = country_flag(country)
    return f"{flag} Alibodama {random.randint(100000, 999999)}"

def is_valid_hostname(label: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9.-]+", label or "") is not None

def _resolve_host(host: str) -> str:
    host = host.strip()
    if not host:
        return host
    if is_ip(host):
        return host
    if not is_valid_hostname(host):
        logging.warning(f"Skip resolve invalid host: {host}")
        return host
    try:
        return socket.gethostbyname(host)
    except (socket.gaierror, UnicodeError) as e:
        logging.warning(f"DNS lookup failed for {host}: {e}")
        return host

def rename_vmess(link: str, ip: str, port: str, tag: str) -> str:
    try:
        raw = link.split("://", 1)[1]
        cfg = json.loads(b64_decode(raw))
        cfg.update({"add": ip, "port": int(port) if port else 443, "ps": tag})
        new_b64 = b64_encode(json.dumps(cfg, ensure_ascii=False))
        return f"vmess://{new_b64}#{quote(tag)}"
    except Exception as e:
        logging.debug(f"vmess rename error: {e}")
        return link

def rename_shadowsocks(link: str, ip: str, port: str, tag: str) -> str:
    try:
        body = link.split("ss://", 1)[1]
        if "#" in body:
            body = body.split("#", 1)[0]
        method = pwd = None
        if "@" in body:
            creds_part, _hostport = body.split("@", 1)
            try:
                method, pwd = b64_decode(creds_part).split(":", 1)
            except Exception:
                method, pwd = creds_part.split(":", 1)
        else:
            try:
                decoded = b64_decode(body)
                if "@" in decoded and ":" in decoded.split("@", 1)[0]:
                    creds, _hp = decoded.split("@", 1)
                    method, pwd = creds.split(":", 1)
                else:
                    method, pwd = decoded.split(":", 1)
            except Exception:
                pass
        if not (method and pwd):
            return link
        new_creds = b64_encode(f"{method}:{pwd}")
        hp = format_hostport(ip, port or "443")
        return f"ss://{new_creds}@{hp}#{quote(tag)}"
    except Exception as e:
        logging.debug(f"shadowsocks rename error: {e}")
        return link

def rename_ssr(link: str, ip: str, port: str, tag: str) -> str:
    try:
        if ":" in ip and not ip.startswith("["):
            logging.debug("SSR IPv6 host detected; skipping rename to avoid ambiguity.")
            return link
        raw = link.split("ssr://", 1)[1]
        decoded = b64url_decode(raw).decode(errors="ignore")
        parts = decoded.split("/?", 1)
        main = parts[0]
        tail = "/?" + parts[1] if len(parts) > 1 else ""
        fields = main.split(":")
        if len(fields) < 6:
            return link
        fields[0] = ip
        fields[1] = str(port or "443")
        new_main = ":".join(fields)
        new_decoded = new_main + tail
        new_link = "ssr://" + b64url_encode(new_decoded.encode())
        return f"{new_link}#{quote(tag)}"
    except Exception as e:
        logging.debug(f"ssr rename error: {e}")
        return link

def rename_url_like(link: str, ip: str, port: str, tag: str) -> str:
    try:
        p = urlsplit(link)
        hostport = p.netloc
        hp = format_hostport(ip, port or "443")
        if "@" in hostport:
            userinfo, _hp = hostport.split("@", 1)
            new_netloc = f"{userinfo}@{hp}"
        else:
            new_netloc = hp
        new_frag = quote(tag)
        return urlunsplit((p.scheme, new_netloc, p.path, p.query, new_frag))
    except Exception as e:
        logging.debug(f"rename_url_like error: {e}")
        return link

@lru_cache(maxsize=100_000)
def _rename_cached(link: str, ip: str, port: str, tag: str, proto: str) -> str:
    if proto == "vmess":
        return rename_vmess(link, ip, port, tag)
    if proto == "shadowsocks":
        return rename_shadowsocks(link, ip, port, tag)
    if proto == "ssr":
        return rename_ssr(link, ip, port, tag)
    return rename_url_like(link, ip, port, tag)

def rename_line(link: str) -> str:
    proto = detect_protocol(link)
    host_port = extract_host(link, proto)
    if not host_port:
        return link
    host, port = split_host_port(host_port)
    if not port:
        port = "443"
    ip = _resolve_host(host)
    tag = _build_tag(ip)
    return _rename_cached(link, ip, port, tag, proto)

# ============================== Main Flow ==================================

def group_by_protocol(links: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for l in links:
        out.setdefault(detect_protocol(l), []).append(l)
    return out

async def main_async():
    now = datetime.now(ZONE).strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{now}] Starting download and processing…")

    async with httpx.AsyncClient() as client:
        # 1) Discover nodes per country (used to decide which country folders to emit)
        country_nodes = await get_nodes_by_country(client)

        # 2) Fetch all raw configs and collect (link, host) pairs
        all_pairs: list[tuple[str, str]] = []
        for url in URLS:
            blob = maybe_base64_decode(fetch_data(url))
            configs = re.findall(r"[a-zA-Z][\w+.-]*://[^\s]+", blob)
            logging.info(f"Fetched {url} → {len(configs)} configs")
            for link in configs:
                proto = detect_protocol(link)
                hostport = extract_host(link, proto)
                if not hostport:
                    continue
                host, _port = split_host_port(hostport)
                if not host:
                    continue
                all_pairs.append((link, host))

        if not all_pairs:
            logging.warning("No links parsed; abort.")
            return

        # 3) Deduplicate hosts and ping them once
        hosts = sorted({h for _, h in all_pairs if h})
        tasks = [run_ping_once(client, h) for h in hosts]
        ping_results = await asyncio.gather(*tasks)

        results_by_host: dict[str, dict] = {}
        node_cc_by_host: dict[str, dict] = {}
        for h, item in zip(hosts, ping_results):
            if isinstance(item, dict) and ("results" in item or "node_cc" in item):
                results_by_host[h] = item.get("results") or {}
                node_cc_by_host[h] = item.get("node_cc") or {}
            else:
                # backward compatibility: treat entire item as results
                results_by_host[h] = item or {}
                node_cc_by_host[h] = {}

        # Helper: map host -> global avg latency
        host_global_lat: dict[str, float] = {
            h: extract_latency_global(results_by_host.get(h, {})) for h in hosts
        }

        # 4) --------- GLOBAL OUTPUTS ----------
        link_global_lat: dict[str, float] = {}
        for link, host in all_pairs:
            lat = host_global_lat.get(host, float("inf"))
            link_global_lat[link] = min(link_global_lat.get(link, float("inf")), lat)

        sorted_global_links = [l for l, _ in sorted(link_global_lat.items(), key=lambda x: x[1])]
        renamed_global = [rename_line(l) for l in sorted_global_links]

        grouped_global = group_by_protocol(sorted_global_links)

        save_to_file(os.path.join(OUTPUT_DIR, "all.txt"), renamed_global)
        save_to_file(os.path.join(OUTPUT_DIR, "light.txt"), renamed_global[:30])

        for proto, proto_links in grouped_global.items():
            save_to_file(
                os.path.join(OUTPUT_DIR, f"{proto}.txt"),
                [rename_line(l) for l in proto_links]
            )

        for missing in ["vless", "vmess", "shadowsocks", "trojan", "unknown"]:
            path = os.path.join(OUTPUT_DIR, f"{missing}.txt")
            if not os.path.exists(path):
                save_to_file(path, [])

        # 5) --------- COUNTRY OUTPUTS ----------
        # Use per-host node->cc maps from the corresponding check-ping request for precise matching.
        for country, _nodes in country_nodes.items():
            logging.info(f"Processing country: {country}")
            link_country_lat: dict[str, float] = {}
            for link, host in all_pairs:
                per_cc = latencies_by_cc_from_results(
                    results_by_host.get(host, {}),
                    node_cc_by_host.get(host, {}),
                )
                lat = per_cc.get(country, float("inf"))
                if lat == float("inf"):
                    lat = host_global_lat.get(host, float("inf"))
                prev = link_country_lat.get(link, float("inf"))
                if lat < prev:
                    link_country_lat[link] = lat

            sorted_links = [l for l, _ in sorted(link_country_lat.items(), key=lambda x: x[1]) if link_country_lat[l] != float("inf")]

            dest_dir = os.path.join(OUTPUT_DIR, country)
            os.makedirs(dest_dir, exist_ok=True)

            if not sorted_links:
                logging.warning(f"No lines to save: {os.path.join(dest_dir, 'all.txt')}")
                continue

            grouped = group_by_protocol(sorted_links)
            for proto, proto_links in grouped.items():
                save_to_file(
                    os.path.join(dest_dir, f"{proto}.txt"),
                    [rename_line(l) for l in proto_links]
                )

            renamed_all_country = [rename_line(l) for l in sorted_links]
            save_to_file(os.path.join(dest_dir, "all.txt"), renamed_all_country)
            save_to_file(os.path.join(dest_dir, "light.txt"), renamed_all_country[:30])

if __name__ == "__main__":
    asyncio.run(main_async())
