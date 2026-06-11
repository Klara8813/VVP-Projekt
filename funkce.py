import numpy as np
import json
from typing import Dict, Any
import random

def soubor_planet(filepath: str = "data/planets.json") -> Dict[str, Any]:
    """
    Načte data o planetách ze souboru JSON a převede pozice a rychlosti na numpy pole.

    Args:
        filepath (str): Cesta k JSON souboru s daty planet.

    Returns:
        Dict[str, Any]: Slovník s načtenými daty planet.
    """
    with open(filepath, "r") as f:
        planety = json.load(f)
    
    for nazev, p in planety.items():
        p["position"] = np.array(p["position"], dtype=float)
        p["velocity"] = np.array(p["velocity"], dtype=float)
        
    return planety

def vypocti_zrychleni(planety: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """
    Vypočítá zrychlení pro každou planetu na základě gravitační síly.
    Obsahuje ošetření proti dělení nulou při nulové vzdálenosti těles.

    Args:
        planety (Dict[str, Any]): Slovník planet s pozicemi a hmotnostmi.

    Returns:
        Dict[str, np.ndarray]: Slovník zrychlení pro každé těleso.
    """
    G = 6.67430e-11
    zrychleni = {nazev: np.array([0.0, 0.0]) for nazev in planety}
    
    for nazev_i, p_i in planety.items():
        for nazev_j, p_j in planety.items():
            if nazev_i == nazev_j:
                continue
                
            rozdil = p_j["position"] - p_i["position"]
            r = np.linalg.norm(rozdil)
            
            # Ošetření nulové vzdálenosti (prevence dělení nulou)
            if r == 0:
                continue
                
            velikost = G * p_j["mass"] / (r**2)
            sila = velikost * (rozdil / r)
        
            zrychleni[nazev_i] += sila
            
    return zrychleni

def simluj_planety(planety: Dict[str, Any], pocet_kroku: int, dt: float) -> Dict[str, list]:
    """
    Simuluje pohyb planet v čase a ukládá historii jejich pozic.

    Args:
        planety (Dict[str, Any]): Výchozí stav planet.
        pocet_kroku (int): Celkový počet kroků simulace.
        dt (float): Časový krok v sekundách.

    Returns:
        Dict[str, list]: Historie pozic pro každou planetu.
    """
    # Hluboká kopie, abychom nemodifikovali původní slovník
    import copy
    lokalni_planety = copy.deepcopy(planety)
    
    historie = {nazev: [] for nazev in lokalni_planety}
    
    for krok in range(pocet_kroku):
        zrychl = vypocti_zrychleni(lokalni_planety)
        
        for nazev, p in lokalni_planety.items():
            p["velocity"] += zrychl[nazev] * dt
            p["position"] += p["velocity"] * dt
            historie[nazev].append(p["position"].copy())
            
    return historie

def generuj_nahodny_scenar(pocet_planet : int) -> Dict[str, Any]:
    """
    Generuje náhodný scénář s daným počtem planet, včetně náhodných pozic, rychlostí a hmotností.

    Args:
        pocet_planet (int): Počet planet v simulaci.

    Returns:
        Dict[str, Any]: Slovník s náhodně generovanými planetami.
    """
    nahodne_planety = {}
    for i in range(pocet_planet):
        nazev = f"Planeta_{i+1}"
        nahodne_planety[nazev] = {
            "position": np.array([
                random.uniform(-2, 2),  # náhodná x poloha
                random.uniform(-2, 2)   # náhodná y poloha
            ], dtype=float),
            "velocity": np.array([
                random.uniform(-3000, 3000),  # náhodná x rychlost
                random.uniform(-3000, 3000)   # náhodná y rychlost
            ], dtype=float),
            "mass": random.uniform(1e23, 1e30)  # náhodná hmotnost
        }
    
    return nahodne_planety