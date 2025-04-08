#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import random
import requests

# --- Dictionnaire des indicatifs, préfixes, longueur et opérateurs pour certains pays ---
indicatifs = {
    "Afrique du Sud": {
        "code": "27",
        "prefixes_mobiles": ["6", "7", "8"],
        "longueur": 9,
        "operateurs": ["Vodacom", "MTN", "Cell C", "Telkom Mobile"]
    },
    "Albanie": {
        "code": "355",
        "prefixes_mobiles": ["6"],
        "longueur": 9,
        "operateurs": ["Vodafone", "ONE", "ALBtelecom"]
    },
    "Algérie": {
        "code": "213",
        "prefixes_mobiles": ["5", "6", "7"],
        "longueur": 9,
        "operateurs": ["Djezzy", "Mobilis", "Ooredoo"]
    },
    "Allemagne": {
        "code": "49",
        "prefixes_mobiles": ["15", "16", "17"],
        "longueur": 10,
        "operateurs": ["Telekom", "Vodafone", "O2"]
    },
    "Andorre": {
        "code": "376",
        "prefixes_mobiles": ["3"],
        "longueur": 6,
        "operateurs": ["Andorra Telecom"]
    },
    "Arabie saoudite": {
        "code": "966",
        "prefixes_mobiles": ["5"],
        "longueur": 9,
        "operateurs": ["STC", "Mobily", "Zain"]
    },
    "Argentine": {
        "code": "54",
        "prefixes_mobiles": ["15"],
        "longueur": 10,
        "operateurs": ["Movistar", "Personal", "Claro"]
    },
    "Arménie": {
        "code": "374",
        "prefixes_mobiles": ["91", "93", "94", "95", "96", "98", "99"],
        "longueur": 8,
        "operateurs": ["Viva-MTS", "Beeline", "Ucom"]
    },
    "Australie": {
        "code": "61",
        "prefixes_mobiles": ["4"],
        "longueur": 9,
        "operateurs": ["Telstra", "Optus", "Vodafone"]
    },
    "Autriche": {
        "code": "43",
        "prefixes_mobiles": ["6"],
        "longueur": 10,
        "operateurs": ["A1", "Magenta", "Drei"]
    },
    "Azerbaïdjan": {
        "code": "994",
        "prefixes_mobiles": ["40", "50", "51", "55", "70", "77"],
        "longueur": 9,
        "operateurs": ["Azercell", "Bakcell", "Nar"]
    },
    "Bahreïn": {
        "code": "973",
        "prefixes_mobiles": ["3", "6"],
        "longueur": 8,
        "operateurs": ["Batelco", "Zain", "stc"]
    },
    "Bangladesh": {
        "code": "880",
        "prefixes_mobiles": ["1"],
        "longueur": 10,
        "operateurs": ["Grameenphone", "Robi", "Banglalink", "Teletalk"]
    },
    "Belgique": {
        "code": "32",
        "prefixes_mobiles": ["4"],
        "longueur": 9,
        "operateurs": ["Proximus", "Orange", "BASE"]
    },
    "Bhoutan": {
        "code": "975",
        "prefixes_mobiles": ["17"],
        "longueur": 8,
        "operateurs": ["B-Mobile", "TashiCell"]
    },
    "Biélorussie": {
        "code": "375",
        "prefixes_mobiles": ["25", "29", "33", "44"],
        "longueur": 9,
        "operateurs": ["A1", "MTS", "life:)"]
    },
    "Bolivie": {
        "code": "591",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 8,
        "operateurs": ["Entel", "Tigo", "Viva"]
    },
    "Bosnie-Herzégovine": {
        "code": "387",
        "prefixes_mobiles": ["6"],
        "longueur": 8,
        "operateurs": ["BH Mobile", "Mtel", "HT Eronet"]
    },
    "Botswana": {
        "code": "267",
        "prefixes_mobiles": ["7"],
        "longueur": 7,
        "operateurs": ["Mascom", "Orange", "BTC Mobile"]
    },
    "Brésil": {
        "code": "55",
        "prefixes_mobiles": ["6", "7", "8", "9"],
        "longueur": 10,
        "operateurs": ["Vivo", "Claro", "TIM", "Oi"]
    },
    "Brunei": {
        "code": "673",
        "prefixes_mobiles": ["7", "8"],
        "longueur": 7,
        "operateurs": ["DST", "Progresif", "Imagine"]
    },
    "Bulgarie": {
        "code": "359",
        "prefixes_mobiles": ["87", "88", "89", "98"],
        "longueur": 8,
        "operateurs": ["A1", "Telenor", "Vivacom"]
    },
    "Canada": {
        "code": "1",
        "prefixes_mobiles": [],
        "longueur": 10,
        "operateurs": ["Rogers", "Bell", "Telus"]
    },
    "Cap-Vert": {
        "code": "238",
        "prefixes_mobiles": ["9"],
        "longueur": 7,
        "operateurs": ["CVMovel", "Unitel T+"]
    },
    "Chili": {
        "code": "56",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Entel", "Movistar", "Claro", "WOM"]
    },
    "Chine": {
        "code": "86",
        "prefixes_mobiles": ["1"],
        "longueur": 11,
        "operateurs": ["China Mobile", "China Unicom", "China Telecom"]
    },
    "Chypre": {
        "code": "357",
        "prefixes_mobiles": ["9"],
        "longueur": 8,
        "operateurs": ["Cyta", "Epic", "PrimeTel"]
    },
    "Colombie": {
        "code": "57",
        "prefixes_mobiles": ["3"],
        "longueur": 10,
        "operateurs": ["Claro", "Movistar", "Tigo"]
    },
    "Corée du Sud": {
        "code": "82",
        "prefixes_mobiles": ["10", "11", "16", "17", "18", "19"],
        "longueur": 10,
        "operateurs": ["SK Telecom", "KT", "LG U+"]
    },
    "Costa Rica": {
        "code": "506",
        "prefixes_mobiles": ["6", "7", "8"],
        "longueur": 8,
        "operateurs": ["Kolbi", "Movistar", "Claro"]
    },
    "Croatie": {
        "code": "385",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["A1", "T-Mobile", "Tele2"]
    },
    "Cuba": {
        "code": "53",
        "prefixes_mobiles": ["5"],
        "longueur": 8,
        "operateurs": ["Cubacel"]
    },
    "Danemark": {
        "code": "45",
        "prefixes_mobiles": ["2", "3", "4", "5"],
        "longueur": 8,
        "operateurs": ["TDC", "Telenor", "Telia"]
    },
    "Dominique": {
        "code": "1",
        "prefixes_mobiles": ["(767)"],
        "longueur": 7,
        "operateurs": ["Flow", "Digicel"]
    },
    "Égypte": {
        "code": "20",
        "prefixes_mobiles": ["10", "11", "12", "15"],
        "longueur": 10,
        "operateurs": ["Orange", "Vodafone", "Etisalat", "WE"]
    },
    "Émirats arabes unis": {
        "code": "971",
        "prefixes_mobiles": ["50", "52", "54", "55", "56"],
        "longueur": 9,
        "operateurs": ["Etisalat", "du"]
    },
    "Équateur": {
        "code": "593",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Claro", "Movistar", "CNT"]
    },
    "Espagne": {
        "code": "34",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 9,
        "operateurs": ["Movistar", "Vodafone", "Orange", "MásMóvil"]
    },
    "Estonie": {
        "code": "372",
        "prefixes_mobiles": ["5"],
        "longueur": 7,
        "operateurs": ["Telia", "Elisa", "Tele2"]
    },
    "Eswatini (Swaziland)": {
        "code": "268",
        "prefixes_mobiles": ["7"],
        "longueur": 8,
        "operateurs": ["MTN", "Eswatini Mobile"]
    },
    "États-Unis": {
        "code": "1",
        "prefixes_mobiles": [],
        "longueur": 10,
        "operateurs": ["Verizon", "AT&T", "T-Mobile"]
    },
    "Finlande": {
        "code": "358",
        "prefixes_mobiles": ["4", "5"],
        "longueur": 8,
        "operateurs": ["Elisa", "Telia", "DNA"]
    },
    "France": {
        "code": "33",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 9,
        "operateurs": ["Orange", "SFR", "Bouygues Telecom", "Free Mobile"]
    },
    "Gabon": {
        "code": "241",
        "prefixes_mobiles": ["0", "1", "2", "5", "6", "7"],
        "longueur": 7,
        "operateurs": ["Airtel", "Gabon Télécom", "Moov Africa"]
    },
    "Géorgie": {
        "code": "995",
        "prefixes_mobiles": ["5"],
        "longueur": 9,
        "operateurs": ["MagtiCom", "Silknet", "Veon (Beeline)"]
    },
    "Ghana": {
        "code": "233",
        "prefixes_mobiles": ["2", "5"],
        "longueur": 9,
        "operateurs": ["MTN", "Vodafone", "AirtelTigo"]
    },
    "Grèce": {
        "code": "30",
        "prefixes_mobiles": ["6"],
        "longueur": 10,
        "operateurs": ["Cosmote", "Vodafone", "Wind"]
    },
    "Grenade": {
        "code": "1",
        "prefixes_mobiles": ["(473)"],
        "longueur": 7,
        "operateurs": ["Flow", "Digicel"]
    },
    "Guatemala": {
        "code": "502",
        "prefixes_mobiles": ["4", "5"],
        "longueur": 8,
        "operateurs": ["Tigo", "Claro", "Movistar"]
    },
    "Guinée équatoriale": {
        "code": "240",
        "prefixes_mobiles": ["2", "5", "6", "7"],
        "longueur": 9,
        "operateurs": ["Getesa (Orange)", "Muni"]
    },
    "Guyana": {
        "code": "592",
        "prefixes_mobiles": ["6"],
        "longueur": 7,
        "operateurs": ["GTT", "Digicel"]
    },
    "Honduras": {
        "code": "504",
        "prefixes_mobiles": ["3", "7", "8", "9"],
        "longueur": 8,
        "operateurs": ["Tigo", "Claro", "Hondutel"]
    },
    "Hong Kong": {
        "code": "852",
        "prefixes_mobiles": ["5", "6", "9"],
        "longueur": 8,
        "operateurs": ["CSL", "SmarTone", "3 HK", "China Mobile HK"]
    },
    "Hongrie": {
        "code": "36",
        "prefixes_mobiles": ["20", "30", "31", "50", "70"],
        "longueur": 9,
        "operateurs": ["Magyar Telekom", "Telenor", "Vodafone"]
    },
    "Inde": {
        "code": "91",
        "prefixes_mobiles": ["6", "7", "8", "9"],
        "longueur": 10,
        "operateurs": ["Jio", "Airtel", "Vi"]
    },
    "Indonésie": {
        "code": "62",
        "prefixes_mobiles": ["8"],
        "longueur": 10,
        "operateurs": ["Telkomsel", "Indosat Ooredoo", "XL Axiata"]
    },
    "Irak": {
        "code": "964",
        "prefixes_mobiles": ["7"],
        "longueur": 10,
        "operateurs": ["Zain", "Asiacell", "Korek Telecom"]
    },
    "Iran": {
        "code": "98",
        "prefixes_mobiles": ["9"],
        "longueur": 10,
        "operateurs": ["MCI (Hamrah-e Aval)", "Irancell (MTN)", "RighTel"]
    },
    "Irlande": {
        "code": "353",
        "prefixes_mobiles": ["8"],
        "longueur": 9,
        "operateurs": ["Vodafone", "Three", "Eir"]
    },
    "Islande": {
        "code": "354",
        "prefixes_mobiles": ["6", "7", "8"],
        "longueur": 7,
        "operateurs": ["Síminn", "Vodafone", "Nova"]
    },
    "Israël": {
        "code": "972",
        "prefixes_mobiles": ["5"],
        "longueur": 9,
        "operateurs": ["Cellcom", "Partner (Orange)", "Pelephone"]
    },
    "Italie": {
        "code": "39",
        "prefixes_mobiles": ["3"],
        "longueur": 10,
        "operateurs": ["TIM", "Vodafone", "Wind Tre", "ILIAD"]
    },
    "Japon": {
        "code": "81",
        "prefixes_mobiles": ["70", "80", "90"],
        "longueur": 10,
        "operateurs": ["NTT Docomo", "KDDI au", "SoftBank"]
    },
    "Jordanie": {
        "code": "962",
        "prefixes_mobiles": ["77", "78", "79"],
        "longueur": 9,
        "operateurs": ["Zain", "Orange", "Umniah"]
    },
    "Kazakhstan": {
        "code": "7",
        "prefixes_mobiles": ["70", "77"],
        "longueur": 10,
        "operateurs": ["Beeline", "Kcell", "Tele2"]
    },
    "Kenya": {
        "code": "254",
        "prefixes_mobiles": ["7"],
        "longueur": 9,
        "operateurs": ["Safaricom", "Airtel", "Telkom"]
    },
    "Kirghizistan": {
        "code": "996",
        "prefixes_mobiles": ["70", "50", "55", "99"],
        "longueur": 9,
        "operateurs": ["Beeline", "MegaCom", "O!"]
    },
    "Kiribati": {
        "code": "686",
        "prefixes_mobiles": ["9"],
        "longueur": 5,
        "operateurs": ["Athena (Vodafone)"]
    },
    "Kosovo": {
        "code": "383",
        "prefixes_mobiles": ["43", "44", "45", "49"],
        "longueur": 8,
        "operateurs": ["Vala", "IPKO"]
    },
    "Koweït": {
        "code": "965",
        "prefixes_mobiles": ["5", "6", "9"],
        "longueur": 8,
        "operateurs": ["Zain", "STC", "Ooredoo"]
    },
    "Laos": {
        "code": "856",
        "prefixes_mobiles": ["20"],
        "longueur": 8,
        "operateurs": ["Unitel", "Lao Telecom", "Beeline"]
    },
    "Lettonie": {
        "code": "371",
        "prefixes_mobiles": ["2"],
        "longueur": 8,
        "operateurs": ["LMT", "Tele2", "Bite"]
    },
    "Liban": {
        "code": "961",
        "prefixes_mobiles": ["3", "70", "71", "76", "81"],
        "longueur": 8,
        "operateurs": ["Alfa", "touch"]
    },
    "Libye": {
        "code": "218",
        "prefixes_mobiles": ["91", "92", "94"],
        "longueur": 9,
        "operateurs": ["Libyana", "Al-Madar"]
    },
    "Lituanie": {
        "code": "370",
        "prefixes_mobiles": ["6"],
        "longueur": 8,
        "operateurs": ["Telia", "Bitė", "Tele2"]
    },
    "Luxembourg": {
        "code": "352",
        "prefixes_mobiles": ["6"],
        "longueur": 9,
        "operateurs": ["Orange", "POST", "Proximus"]
    },
    "Macédoine du Nord": {
        "code": "389",
        "prefixes_mobiles": ["70", "71", "72", "75", "76", "77", "78"],
        "longueur": 8,
        "operateurs": ["A1", "T-Mobile (Makedonski Telekom)", "Lycamobile"]
    },
    "Malaisie": {
        "code": "60",
        "prefixes_mobiles": ["1"],
        "longueur": 9,
        "operateurs": ["Maxis", "Celcom", "Digi", "U Mobile"]
    },
    "Maldives": {
        "code": "960",
        "prefixes_mobiles": ["7", "9"],
        "longueur": 7,
        "operateurs": ["Dhiraagu", "Ooredoo"]
    },
    "Malte": {
        "code": "356",
        "prefixes_mobiles": ["77", "79", "98", "99"],
        "longueur": 8,
        "operateurs": ["Vodafone (Epic)", "GO", "Melita"]
    },
    "Maroc": {
        "code": "212",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 9,
        "operateurs": ["Maroc Telecom", "Orange", "INWI"]
    },
    "Maurice": {
        "code": "230",
        "prefixes_mobiles": ["5"],
        "longueur": 7,
        "operateurs": ["my.t", "MTML (Chili)", "Emtel"]
    },
    "Mexique": {
        "code": "52",
        "prefixes_mobiles": ["1"],
        "longueur": 10,
        "operateurs": ["Telcel", "Movistar", "AT&T"]
    },
    "Micronésie": {
        "code": "691",
        "prefixes_mobiles": ["9"],
        "longueur": 7,
        "operateurs": ["FSMTC"]
    },
    "Moldavie": {
        "code": "373",
        "prefixes_mobiles": ["60", "61", "62", "69", "67", "68"],
        "longueur": 8,
        "operateurs": ["Orange", "Moldcell", "Unité"]
    },
    "Mongolie": {
        "code": "976",
        "prefixes_mobiles": ["5", "8", "9"],
        "longueur": 8,
        "operateurs": ["Mobicom", "Skytel", "Unitel", "G-Mobile"]
    },
    "Monténégro": {
        "code": "382",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 8,
        "operateurs": ["Crnogorski Telekom", "Telenor", "One"]
    },
    "Myanmar (Birmanie)": {
        "code": "95",
        "prefixes_mobiles": ["9"],
        "longueur": 8,
        "operateurs": ["MPT", "Telenor", "Ooredoo", "MyTel"]
    },
    "Namibie": {
        "code": "264",
        "prefixes_mobiles": ["81", "85"],
        "longueur": 9,
        "operateurs": ["MTC", "TN Mobile"]
    },
    "Népal": {
        "code": "977",
        "prefixes_mobiles": ["98", "97", "96"],
        "longueur": 10,
        "operateurs": ["Nepal Telecom", "Ncell", "SmartCell"]
    },
    "Nicaragua": {
        "code": "505",
        "prefixes_mobiles": ["8"],
        "longueur": 8,
        "operateurs": ["Claro", "Tigo"]
    },
    "Norvège": {
        "code": "47",
        "prefixes_mobiles": ["4", "9"],
        "longueur": 8,
        "operateurs": ["Telenor", "Telia", "Ice"]
    },
    "Nouvelle-Zélande": {
        "code": "64",
        "prefixes_mobiles": ["2"],
        "longueur": 8,
        "operateurs": ["Spark", "Vodafone", "2degrees"]
    },
    "Oman": {
        "code": "968",
        "prefixes_mobiles": ["9"],
        "longueur": 8,
        "operateurs": ["Omantel", "Ooredoo", "Vodafone Oman"]
    },
    "Ouzbékistan": {
        "code": "998",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Beeline", "UMS", "Ucell", "UzMobile"]
    },
    "Palestine": {
        "code": "970",
        "prefixes_mobiles": ["5"],
        "longueur": 9,
        "operateurs": ["Jawwal", "Ooredoo Palestine"]
    },
    "Panama": {
        "code": "507",
        "prefixes_mobiles": ["6"],
        "longueur": 8,
        "operateurs": ["Cable & Wireless", "Movistar", "Claro"]
    },
    "Paraguay": {
        "code": "595",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Tigo", "Personal", "Vox"]
    },
    "Pays-Bas": {
        "code": "31",
        "prefixes_mobiles": ["6"],
        "longueur": 9,
        "operateurs": ["KPN", "VodafoneZiggo", "T-Mobile"]
    },
    "Pérou": {
        "code": "51",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Movistar", "Claro", "Entel", "Bitel"]
    },
    "Philippines": {
        "code": "63",
        "prefixes_mobiles": ["9"],
        "longueur": 10,
        "operateurs": ["Globe", "Smart", "DITO"]
    },
    "Pologne": {
        "code": "48",
        "prefixes_mobiles": ["5", "6", "7"],
        "longueur": 9,
        "operateurs": ["Orange", "Play", "Plus", "T-Mobile"]
    },
    "Portugal": {
        "code": "351",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["MEO", "Vodafone", "NOS"]
    },
    "Qatar": {
        "code": "974",
        "prefixes_mobiles": ["3", "5", "6", "7"],
        "longueur": 8,
        "operateurs": ["Ooredoo", "Vodafone"]
    },
    "République dominicaine": {
        "code": "1",
        "prefixes_mobiles": ["(809)", "(829)", "(849)"],
        "longueur": 7,
        "operateurs": ["Claro", "Altice", "Viva"]
    },
    "République tchèque": {
        "code": "420",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 9,
        "operateurs": ["O2", "T-Mobile", "Vodafone"]
    },
    "Roumanie": {
        "code": "40",
        "prefixes_mobiles": ["7"],
        "longueur": 9,
        "operateurs": ["Orange", "Vodafone", "Telekom"]
    },
    "Royaume-Uni": {
        "code": "44",
        "prefixes_mobiles": ["7"],
        "longueur": 10,
        "operateurs": ["EE", "O2", "Vodafone", "Three"]
    },
    "Russie": {
        "code": "7",
        "prefixes_mobiles": ["9"],
        "longueur": 10,
        "operateurs": ["MTS", "Megafon", "Beeline", "Tele2"]
    },
    "Saint-Christophe-et-Niévès": {
        "code": "1",
        "prefixes_mobiles": ["(869)"],
        "longueur": 7,
        "operateurs": ["Flow", "Digicel"]
    },
    "Sainte-Lucie": {
        "code": "1",
        "prefixes_mobiles": ["(758)"],
        "longueur": 7,
        "operateurs": ["Flow", "Digicel"]
    },
    "Saint-Vincent-et-les-Grenadines": {
        "code": "1",
        "prefixes_mobiles": ["(784)"],
        "longueur": 7,
        "operateurs": ["Flow", "Digicel"]
    },
    "Salvador": {
        "code": "503",
        "prefixes_mobiles": ["6", "7"],
        "longueur": 8,
        "operateurs": ["Tigo", "Claro", "Movistar", "Digicel"]
    },
    "Sao Tomé-et-Principe": {
        "code": "239",
        "prefixes_mobiles": ["9"],
        "longueur": 7,
        "operateurs": ["CST", "Unitel"]
    },
    "Serbie": {
        "code": "381",
        "prefixes_mobiles": ["6"],
        "longueur": 9,
        "operateurs": ["Telekom Srbija (MTS)", "Telenor", "A1"]
    },
    "Seychelles": {
        "code": "248",
        "prefixes_mobiles": ["2"],
        "longueur": 7,
        "operateurs": ["Cable & Wireless", "Airtel"]
    },
    "Singapour": {
        "code": "65",
        "prefixes_mobiles": ["8", "9"],
        "longueur": 8,
        "operateurs": ["Singtel", "StarHub", "M1"]
    },
    "Slovaquie": {
        "code": "421",
        "prefixes_mobiles": ["9"],
        "longueur": 9,
        "operateurs": ["Orange", "Telekom", "O2", "4ka"]
    },
    "Slovénie": {
        "code": "386",
        "prefixes_mobiles": ["30", "40", "41", "51", "64", "68", "70"],
        "longueur": 8,
        "operateurs": ["A1", "Telekom Slovenije", "Telemach"]
    },
    "Sri Lanka": {
        "code": "94",
        "prefixes_mobiles": ["7"],
        "longueur": 9,
        "operateurs": ["Dialog", "Mobitel", "Airtel", "Hutch"]
    },
    "Suède": {
        "code": "46",
        "prefixes_mobiles": ["7"],
        "longueur": 9,
        "operateurs": ["Telia", "Telenor", "Tre (3)", "Tele2"]
    },
    "Suisse": {
        "code": "41",
        "prefixes_mobiles": ["7"],
        "longueur": 9,
        "operateurs": ["Swisscom", "Sunrise", "Salt"]
    },
    "Suriname": {
        "code": "597",
        "prefixes_mobiles": ["6", "7", "8"],
        "longueur": 7,
        "operateurs": ["Telesur (TeleG)", "Digicel"]
    },
    "Tadjikistan": {
        "code": "992",
        "prefixes_mobiles": ["50", "51", "52", "55", "90", "91", "92", "93", "98"],
        "longueur": 9,
        "operateurs": ["Babilon-M", "MegaFon", "Tcell", "Beeline"]
    },
    "Thaïlande": {
        "code": "66",
        "prefixes_mobiles": ["6", "8", "9"],
        "longueur": 9,
        "operateurs": ["AIS", "TrueMove H", "dtac"]
    },
    "Trinité-et-Tobago": {
        "code": "1",
        "prefixes_mobiles": ["(868)"],
        "longueur": 7,
        "operateurs": ["TSTT (bmobile)", "Digicel"]
    },
    "Tunisie": {
        "code": "216",
        "prefixes_mobiles": ["2", "9"],
        "longueur": 8,
        "operateurs": ["Orange", "Ooredoo", "Tunisie Télécom"]
    },
    "Turquie": {
        "code": "90",
        "prefixes_mobiles": ["5"],
        "longueur": 10,
        "operateurs": ["Turkcell", "Vodafone", "Türk Telekom"]
    },
    "Turkménistan": {
        "code": "993",
        "prefixes_mobiles": ["6"],
        "longueur": 8,
        "operateurs": ["TM Cell", "MTS"]
    },
    "Ukraine": {
        "code": "380",
        "prefixes_mobiles": ["39", "50", "63", "66", "67", "68", "73", "91", "92", "93", "94", "95", "96", "97", "98", "99"],
        "longueur": 9,
        "operateurs": ["Kyivstar", "Vodafone UA", "lifecell"]
    },
    "Uruguay": {
        "code": "598",
        "prefixes_mobiles": ["9"],
        "longueur": 8,
        "operateurs": ["Antel", "Movistar", "Claro"]
    },
    "Venezuela": {
        "code": "58",
        "prefixes_mobiles": ["4"],
        "longueur": 7,
        "operateurs": ["Movistar", "Movilnet", "Digitel"]
    },
    "Viêt Nam": {
        "code": "84",
        "prefixes_mobiles": ["3", "5", "7", "8", "9"],
        "longueur": 9,
        "operateurs": ["Viettel", "MobiFone", "Vinaphone"]
    }
}

# --- Fonction pour récupérer l'indicatif via l'API RestCountries pour les pays non présents dans notre dictionnaire ---
def fetch_country_calling_code(pays):
    url = f"https://restcountries.com/v3.1/name/{pays}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list):
            idd = data[0].get("idd", {})
            root = idd.get("root", "")
            suffixes = idd.get("suffixes", [])
            if root:
                code = root + (suffixes[0] if suffixes else "")
                return code.lstrip('+')
    except Exception as e:
        print(f"Erreur lors de l'appel API pour {pays} : {e}")
    return None

# --- Fonction de génération d'un numéro de téléphone ---
def generer_numero(pays, operateur=None):
    # Si le pays figure dans notre dictionnaire
    if pays in indicatifs:
        info = indicatifs[pays]
        code = info["code"]
        prefixes = info["prefixes_mobiles"]
        longueur = info["longueur"]
        ops = info["operateurs"]
        # Si un opérateur est spécifié (et différent de "Aléatoire")
        if operateur and operateur != "Aléatoire":
            # Si le nombre de préfixes correspond exactement au nombre d'opérateurs,
            # on considère qu'il y a une correspondance directe.
            if len(prefixes) == len(ops) and operateur in ops:
                idx = ops.index(operateur)
                prefix = prefixes[idx]
            else:
                # Sinon, on choisit aléatoirement un préfixe parmi ceux disponibles.
                prefix = random.choice(prefixes) if prefixes else ""
        else:
            prefix = random.choice(prefixes) if prefixes else ""
        nb_chiffres = longueur - len(prefix)
        nb_chiffres = nb_chiffres if nb_chiffres > 0 else 0
        numero_local = "".join(random.choices("0123456789", k=nb_chiffres))
        return f"+{code}{prefix}{numero_local}"
    else:
        # Pour les pays non présents dans le dictionnaire : appel API et génération par défaut.
        code = fetch_country_calling_code(pays)
        if not code:
            print(f"Aucun indicatif trouvé pour {pays}. Utilisation de l'indicatif '00'.")
            code = "00"
        prefix = random.choice(["6", "7", "8", "9"])
        nb_chiffres = 9 - len(prefix)
        nb_chiffres = nb_chiffres if nb_chiffres > 0 else 0
        numero_local = "".join(random.choices("0123456789", k=nb_chiffres))
        return f"+{code}{prefix}{numero_local}"

# --- Classe de l'application Tkinter ---
class PhoneGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Générateur de numéros de téléphone")
        self.geometry("400x550")
        self.resizable(False, False)

        # Zone de recherche
        tk.Label(self, text="Rechercher un pays :").pack(pady=(10, 0))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_listbox)
        self.search_entry = tk.Entry(self, textvariable=self.search_var, width=40)
        self.search_entry.pack(pady=5)

        # Listbox affichant la liste des pays filtrés
        self.listbox = tk.Listbox(self, height=8, width=40)
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.countries = sorted(list(indicatifs.keys()))
        self.update_listbox()

        # Zone d'affichage ou de saisie du pays sélectionné
        tk.Label(self, text="Pays sélectionné :").pack(pady=(10, 0))
        self.selected_country_var = tk.StringVar()
        self.selected_country_entry = tk.Entry(self, textvariable=self.selected_country_var, width=40)
        self.selected_country_entry.pack(pady=5)

        # Combobox pour choisir l'opérateur
        tk.Label(self, text="Opérateur :").pack(pady=(10, 0))
        self.operator_var = tk.StringVar()
        self.operator_combo = ttk.Combobox(self, textvariable=self.operator_var, state="readonly", width=37)
        self.operator_combo['values'] = ["Aléatoire"]
        self.operator_combo.current(0)
        self.operator_combo.pack(pady=5)

        # Nombre de numéros à générer
        tk.Label(self, text="Nombre de numéros :").pack(pady=(10, 0))
        self.nombre_var = tk.IntVar(value=1)
        self.nombre_entry = tk.Entry(self, textvariable=self.nombre_var, width=40)
        self.nombre_entry.pack(pady=5)

        # Nom du fichier de sortie
        tk.Label(self, text="Nom du fichier de sortie :").pack(pady=(10, 0))
        self.output_var = tk.StringVar(value="numeros.txt")
        self.output_entry = tk.Entry(self, textvariable=self.output_var, width=40)
        self.output_entry.pack(pady=5)

        # Bouton de génération
        self.generate_button = tk.Button(self, text="Générer", command=self.generate_numbers)
        self.generate_button.pack(pady=20)

    def update_listbox(self, *args):
        search_term = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        for country in self.countries:
            if search_term in country.lower():
                self.listbox.insert(tk.END, country)

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            country = event.widget.get(index)
            self.selected_country_var.set(country)
            self.update_operator_choices(country)

    def update_operator_choices(self, country):
        # Met à jour la liste des opérateurs en fonction du pays
        if country in indicatifs:
            ops = indicatifs[country].get("operateurs", [])
            # On ajoute une option "Aléatoire" pour choisir aléatoirement un opérateur
            values = ["Aléatoire"] + ops if ops else ["Aléatoire"]
            self.operator_combo['values'] = values
            self.operator_combo.current(0)
        else:
            self.operator_combo['values'] = ["Aléatoire"]
            self.operator_combo.current(0)

    def generate_numbers(self):
        country = self.selected_country_var.get().strip()
        if not country:
            messagebox.showerror("Erreur", "Veuillez sélectionner ou saisir un pays.")
            return
        try:
            nombre = int(self.nombre_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de numéros doit être un entier.")
            return
        output_file = self.output_var.get().strip()
        if not output_file:
            messagebox.showerror("Erreur", "Veuillez fournir un nom de fichier de sortie.")
            return

        # Récupère l'opérateur sélectionné dans la combobox (si "Aléatoire", on transmet None)
        operateur = self.operator_var.get()
        if operateur == "Aléatoire":
            operateur = None

        numeros = []
        for _ in range(nombre):
            numero = generer_numero(country, operateur)
            numeros.append(numero)

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for numero in numeros:
                    f.write(numero + "\n")
            messagebox.showinfo("Succès", f"{nombre} numéros ont été générés dans le fichier '{output_file}'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'écriture dans le fichier : {e}")

if __name__ == "__main__":
    app = PhoneGeneratorApp()
    app.mainloop()
