from parsing.nmap_parser import (
    parse_nmap_file,
    parse_target_info,
    parse_nmap_hosts
)

from security.analyzer import analyze_findings
from security.attack_paths import generate_attack_paths
from security.action_plan import create_action_plan
from security.management_intelligence import calculate_infralens_security_index
from security.executive_actions import create_executive_actions

from infrastructure.network_analysis import analyze_network
from infrastructure.host_inventory import create_host_inventory
from infrastructure.topology import generate_topology_notes
from infrastructure.asset_discovery import discover_assets
from infrastructure.asset_inventory import create_asset_inventory
from infrastructure.scan_context import filter_scanner_from_assets

from compliance.nis2_mapper import (
    map_findings_to_nis2,
    calculate_nis2_statistics
)


def run_analysis(input_path, scan_context, enable_nis2=True):
    findings = parse_nmap_file(input_path)
    hosts = parse_nmap_hosts(input_path)

    if not findings:
        return None

    target_info = parse_target_info(input_path)
    analyzed_findings = analyze_findings(findings)
    attack_paths = generate_attack_paths(analyzed_findings)
    network_analysis = analyze_network(target_info)

    host_inventory = create_host_inventory(
        target_info,
        analyzed_findings
    )

    assets = discover_assets(
        analyzed_findings,
        target_info
    )

    raw_asset_inventory = create_asset_inventory(hosts)

    asset_inventory = filter_scanner_from_assets(
        raw_asset_inventory,
        scan_context
    )

    action_plan = create_action_plan(asset_inventory)

    executive_actions = create_executive_actions(action_plan)

    management_intelligence = calculate_infralens_security_index(
        asset_inventory,
        action_plan
    )

    topology_notes = generate_topology_notes(
        target_info,
        host_inventory
    )

    if enable_nis2:
        nis2_mapping = map_findings_to_nis2(
            analyzed_findings,
            attack_paths,
            network_analysis,
            host_inventory
        )

        nis2_statistics = calculate_nis2_statistics(
            nis2_mapping
        )
    else:
        nis2_mapping = None
        nis2_statistics = None

    return {
        "findings": findings,
        "analyzed_findings": analyzed_findings,
        "target_info": target_info,
        "attack_paths": attack_paths,
        "network_analysis": network_analysis,
        "host_inventory": host_inventory,
        "assets": assets,
        "asset_inventory": asset_inventory,
        "action_plan": action_plan,
        "executive_actions": executive_actions,
        "management_intelligence": management_intelligence,
        "topology_notes": topology_notes,
        "nis2_mapping": nis2_mapping,
        "nis2_statistics": nis2_statistics
    }
