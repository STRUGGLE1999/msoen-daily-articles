#!/usr/bin/env python3
"""Print today's Wuliuaou theme pack (Beijing date, 14-day rotation)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from zoneinfo import ZoneInfo

BEIJING = ZoneInfo("Asia/Shanghai")

THEMES = [
    {
        "id": "china-usa",
        "name": "China to USA shipping",
        "titles": [
            "How to Ship Goods from China to the USA: Complete Guide for Importers",
            "How Much Does Shipping from China to the USA Cost? Freight Rates and Pricing Guide",
            "How Long Does Shipping from China to the USA Take? Air, Sea and Express Transit Times",
            "What Documents Are Required to Ship Commercial Goods from China to the USA?",
            "China to USA Air Freight vs. Sea Freight: Which Shipping Method Is Better?",
            "How to Choose a Reliable China to USA Freight Forwarder for Your Business",
            "How to Ship Goods from China to the USA Door to Door with DDP Service",
            "How to Calculate the Total Cost of Shipping from China to the USA",
            "How Does Customs Clearance Work When Importing Goods from China to the USA?",
            "China to USA Door-to-Door Shipping: Complete Guide for Importers",
        ],
    },
    {
        "id": "furniture-nz",
        "name": "China furniture shipping to New Zealand",
        "titles": [
            "How to Ship Furniture from China to New Zealand: Complete Guide for Importers",
            "How Much Does It Cost to Ship Furniture from China to New Zealand?",
            "How Long Does Furniture Shipping from China to New Zealand Take?",
            "What Documents Do You Need to Ship Furniture from China to New Zealand?",
            "Best Ways to Ship Furniture from China to New Zealand: Sea Freight vs. Air Freight",
            "How to Choose a Reliable China-to-New Zealand Furniture Shipping Company",
            "China Furniture Shipping to New Zealand: DDP, Door-to-Door, and Port Delivery Explained",
            "How to Reduce the Cost of Shipping Furniture from China to New Zealand",
            "How to Import Furniture from China to New Zealand Without Unexpected Costs",
            "China to New Zealand Furniture Shipping: Costs, Transit Times, and Customs Guide",
        ],
    },
    {
        "id": "lcl",
        "name": "LCL sea freight from China",
        "titles": [
            "How Much Does LCL Shipping from China Cost? Ocean Freight Rates and Hidden Fees Explained",
            "How Long Does LCL Shipping from China Take? Transit Times by Country",
            "LCL vs FCL from China: What Should You Choose for Small and Large Shipments?",
            "How to Reduce China LCL Shipping Costs: Practical Ways to Save Money",
            "What Documents Are Required for LCL Shipping from China?",
            "How to Prevent Damage and Loss When Shipping LCL from China",
            "How to Ship LCL from China to the USA: Costs, Transit Times, and Door-to-Door Options",
            "How to Ship LCL from China to Europe: Costs, Transit Times, and Customs",
            "How to Choose a Reliable China LCL Freight Forwarder",
            "How to Ship Small Quantities from China Overseas: A Complete LCL Guide",
        ],
    },
    {
        "id": "ddp",
        "name": "DDP and door-to-door shipping from China",
        "titles": [
            "China DDP Shipping Explained: How Door-to-Door Delivery from China Works",
            "How to Ship from China DDP: Customs, Duties, Delivery and Cost Guide",
            "China DDP vs. DDU Shipping: What Is the Difference and Which Option Should You Choose?",
            "How to Import from China Without Unexpected Customs Costs Using DDP",
            "China Door-to-Door Shipping: How to Import Goods from China to Your Warehouse",
            "What Is Included in a China DDP Freight Quote?",
            "How Long Does DDP Shipping from China Take?",
            "How Much Does DDP Shipping from China Cost?",
            "How to Choose a Reliable China DDP Freight Forwarder",
            "DDP Shipping from China: Costs, Transit Times, Customs and Door-to-Door Delivery",
        ],
    },
    {
        "id": "battery-dg",
        "name": "Lithium battery and dangerous goods from China",
        "titles": [
            "How to Ship Lithium Batteries from China by Sea: Rules, Documents, and LCL Options",
            "China Lithium Battery LCL Shipping Freight Forwarder Guide",
            "What Documents Are Required to Export Lithium Batteries from China?",
            "How Long Does Lithium Battery Shipping from China Take?",
            "How Much Does It Cost to Ship Lithium Batteries from China?",
            "Dangerous Goods Battery Shipping from China by Sea: What Importers Should Know",
            "How to Choose a Reliable China Battery Dangerous Goods Freight Forwarder",
            "China DG Battery LCL Sea Freight: Packaging, Labeling, and Booking Checklist",
            "Can You Ship Lithium Batteries from China Door to Door with DDP?",
            "China Lithium Battery Export Sea Freight: Costs, Transit Times, and Compliance Guide",
        ],
    },
    {
        "id": "europe",
        "name": "China to Europe shipping",
        "titles": [
            "How to Ship from China to Europe: Air Freight, Sea Freight, Rail Freight and DDP",
            "How Much Does It Cost to Ship Goods from China to Europe?",
            "How Long Does Shipping from China to Europe Take? Sea, Air and DDP Transit Times",
            "What Documents Are Required to Ship from China to Europe?",
            "China to Europe Air Freight vs. Sea Freight: Which Method Is Better?",
            "How to Choose a Reliable China to Europe Freight Forwarder",
            "How to Ship from China to Europe DDP: Customs, VAT, Duties and Delivery",
            "How to Reduce Shipping Costs from China to Europe",
            "China to Europe LCL Shipping: Costs, Transit Times and Door-to-Door Options",
            "China to Europe Shipping Guide: Transit Time, Cost, Customs and Delivery Options",
        ],
    },
    {
        "id": "choose-forwarder",
        "name": "How to choose a China freight forwarder",
        "titles": [
            "How to Choose a Reliable China Freight Forwarder for International Shipping",
            "How to Find a Reliable China Freight Forwarder",
            "What to Look for in a China Freight Forwarder With Good Customer Service",
            "How a Professional China Freight Forwarder Makes International Shipping Easier",
            "China Freight Forwarder for Reliable Air, Sea, Rail, and Express Shipping",
            "How to Evaluate a Trustworthy Freight Forwarder in China Before You Ship",
            "What Makes a Great China Freight Forwarder Stand Out",
            "How to Choose a China Freight Forwarder With Reliable Service",
            "China Freight Forwarding Services With Transparent Pricing and Shipment Support",
            "Your Guide to Working with a Dependable Freight Forwarder Based in China",
        ],
    },
    {
        "id": "cars",
        "name": "China car and vehicle export shipping",
        "titles": [
            "How to Ship Cars from China: RoRo, Container and Door-to-Door Options",
            "How Much Does It Cost to Ship a Car from China?",
            "How Long Does Car Shipping from China Take?",
            "What Documents Are Required to Export Vehicles from China?",
            "RoRo vs Container Shipping for Chinese Cars: Which Option Is Better?",
            "How to Choose a Reliable China Auto Export Freight Forwarder",
            "China Vehicle Export Logistics: Customs Clearance and Delivery Guide",
            "How to Reduce the Cost of Shipping Cars from China",
            "End-to-End Logistics Solutions for Chinese Automotive Exports",
            "Professional Freight Forwarding Services for Chinese Car Exports to Global Markets",
        ],
    },
    {
        "id": "middle-east",
        "name": "China to Middle East shipping",
        "titles": [
            "China to Saudi Arabia Freight Forwarder: Door-to-Door Shipping Guide for Importers",
            "China to UAE Freight Forwarder: Cost, Shipping Time and Customs Clearance Guide",
            "How to Ship from China to Aqaba (Jordan): FCL, LCL and DDP Door-to-Door",
            "How Much Does Shipping from China to the Middle East Cost?",
            "How Long Does Sea Freight from China to Saudi Arabia Take?",
            "What Documents Are Required to Ship from China to the UAE?",
            "China to Middle East DDP Shipping: Customs, Duties and Door-to-Door Delivery",
            "How to Choose a Reliable China to Middle East Freight Forwarder",
            "China to Aqaba LCL Sea Freight: A Guide for Small and Medium Exporters",
            "FCL Container Shipping from China to Jeddah, Jebel Ali and Aqaba",
        ],
    },
    {
        "id": "air-vs-sea",
        "name": "Air freight vs sea freight from China",
        "titles": [
            "Air Freight vs. Sea Freight from China: Which Shipping Method Is Better for Your Cargo?",
            "Is It Cheaper to Ship by Air or Sea from China?",
            "How to Choose the Best Shipping Method from China",
            "How Air Freight from China Is Calculated: Chargeable Weight, Rates and Surcharges",
            "How Sea Freight from China Works: From Factory to Destination Port",
            "When Should You Use Air Freight Instead of Sea Freight from China?",
            "How Long Does Air Freight from China Take Compared With Sea Freight?",
            "How to Reduce International Shipping Costs When Importing from China",
            "China FCL vs. LCL Shipping: Which Option Is Better for Your Cargo?",
            "China Shipping Guide: How to Choose Sea Freight, Air Freight, and Express Shipping",
        ],
    },
    {
        "id": "documents",
        "name": "Shipping documents and customs from China",
        "titles": [
            "What Documents Are Needed to Ship Goods from China?",
            "International Shipping Documents Guide: Everything Importers Need to Know",
            "How Does Customs Clearance Work When Importing from China?",
            "China Customs Clearance Guide: Avoid Delays and Extra Import Costs",
            "What Information Do You Need to Get an Accurate Freight Quote from China?",
            "Commercial Invoice, Packing List and Bill of Lading: A Practical Importer Guide",
            "How to Avoid Customs Delays When Shipping from China",
            "How HS Codes Affect Shipping Costs and Clearance from China",
            "What Documents Are Required for DDP Shipping from China?",
            "China Export Customs Clearance: Step-by-Step Guide for Global Buyers",
        ],
    },
    {
        "id": "ecommerce-fba",
        "name": "Amazon FBA and e-commerce shipping from China",
        "titles": [
            "Amazon FBA Shipping from China: Complete Logistics Guide for Sellers",
            "Best China Logistics Provider for Amazon FBA and E-Commerce Sellers",
            "How to Ship from China to Amazon FBA: Costs, Transit Times and Labeling",
            "How Much Does Amazon FBA Shipping from China Cost?",
            "How Long Does FBA Shipping from China Take?",
            "What Documents Are Required for Amazon FBA Shipments from China?",
            "China to Amazon FBA: Air Freight vs Sea Freight vs Express",
            "How to Reduce Amazon FBA Shipping Costs from China",
            "China Consolidation Shipping Service for E-Commerce and Wholesale Buyers",
            "How to Choose a Reliable China Freight Forwarder for Amazon FBA",
        ],
    },
    {
        "id": "usa-ddp",
        "name": "China to USA DDP door-to-door",
        "titles": [
            "How to Ship Goods from China to the USA Door to Door: A Complete Guide for Importers",
            "How to Ship Products from China to the USA with DDP Service",
            "China to USA DDP Shipping: Costs, Customs and Door-to-Door Delivery",
            "How Much Does Door-to-Door Shipping from China to the USA Cost?",
            "How Long Does DDP Shipping from China to the USA Take?",
            "What Documents Are Required for DDP Shipments from China to the USA?",
            "China to USA Door-to-Door vs Port-to-Port Shipping: Which Should You Choose?",
            "How to Import from China to the USA Without Unexpected Customs Costs",
            "How to Choose a Reliable China to USA DDP Freight Forwarder",
            "China to USA Door-to-Door Shipping Guide: Sea Freight, Air Freight and DDP",
        ],
    },
    {
        "id": "fcl",
        "name": "FCL container shipping from China",
        "titles": [
            "China FCL Shipping Services: How Businesses Save Money on Full Container Shipping",
            "How Much Does a Container from China Cost? FCL Rates and Surcharges Explained",
            "How Long Does FCL Shipping from China Take?",
            "FCL vs LCL from China: Which Container Option Is Better?",
            "What Documents Are Required for FCL Shipments from China?",
            "How to Choose Between 20ft and 40ft Containers When Shipping from China",
            "How to Reduce FCL Shipping Costs from China",
            "How to Book FCL Sea Freight from China: From Factory Pickup to Destination Port",
            "How to Choose a Reliable China FCL Freight Forwarder",
            "Shipping Container from China Guide: FCL vs LCL, Costs, and Best Practices",
        ],
    },
]


def beijing_today(now: dt.datetime | None = None) -> dt.date:
    if now is None:
        now = dt.datetime.now(tz=BEIJING)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=BEIJING)
    else:
        now = now.astimezone(BEIJING)
    return now.date()


def theme_for(day: dt.date) -> dict:
    idx = day.toordinal() % len(THEMES)
    pack = dict(THEMES[idx])
    pack["beijing_date"] = day.isoformat()
    pack["index"] = idx
    pack["count"] = len(pack["titles"])
    return pack


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="YYYY-MM-DD in Beijing time")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.date:
        day = dt.date.fromisoformat(args.date)
    else:
        day = beijing_today()
    pack = theme_for(day)
    if args.json:
        json.dump(pack, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    print(f"Beijing date: {pack['beijing_date']}")
    print(f"Theme {pack['index'] + 1}/{len(THEMES)}: {pack['name']} ({pack['id']})")
    print("Publish 10 titles:")
    for i, title in enumerate(pack["titles"], 1):
        print(f"  {i:02d}. {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
