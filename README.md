# Stal-Out

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![Stars](https://img.shields.io/github/stars/ReyGall/Stal-Out?style=flat-square&color=gold)
![Contributors](https://img.shields.io/github/contributors/ReyGall/Stal-Out?style=flat-square&color=blue)
![Forks](https://img.shields.io/github/forks/ReyGall/Stal-Out?style=flat-square&color=lightgrey)
![Issues](https://img.shields.io/github/issues/ReyGall/Stal-Out?style=flat-square&color=red)

A terminal-based RPG engine featuring modular logic and SQLite database integration.

## Overview
This project is a technical demonstration of Python-based game mechanics. It focuses on persistent data management, modularity, and inventory systems. The core logic is separated from data assets to ensure scalability and ease of maintenance.

## Key Features
* **Data Persistence:** Integration with SQLite for loot tables and player statistics.
* **Modular Architecture:** Distinct separation between the game engine core and data processing.
* **Save System:** Implementation of JSON-based player state serialization.
* **Administrative Tools:** Scripts for database management and balance adjustments.

## Project Structure
* `core/` - Main game engine mechanics and trade logic.
* `data/` - SQLite databases and persistent storage files.
* `Icons/` - Graphic assets for UI/GUI development.
* `Main.py` - Application entry point.

## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/ReyGall/Stal-Out.git](https://github.com/ReyGall/Stal-Out.git)

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
Developed for educational purposes to demonstrate Python backend and database management skills.