# Prep

!pip install -r "requirements ejercicio 2.txt"

import time, re
import pandas as pd
from bs4 import BeautifulSoup

# Selenium (renderiza JS)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://www.bumeran.com.pe"
START_URL = "https://www.bumeran.com.pe/en-lima/empleos-area-tecnologia-sistemas-y-telecomunicaciones-subarea-programacion-full-time-publicacion-menor-a-15-dias.html"

# ---------- Configurar navegador ----------
opts = Options()
opts.add_argument("--headless=new")       # si algo falla, prueba "--headless" o comenta esta línea
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-gpu")
opts.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 12)

def accept_cookies_if_present():
    """Clic en el banner de cookies si aparece (texto en ES/EN)."""
    try:
        for txt in ["Aceptar", "Acepto", "De acuerdo", "Accept", "I agree"]:
            # busca botones o enlaces con ese texto
            els = driver.find_elements(By.XPATH, f"//*[self::button or self::a][contains(., '{txt}')]")
            for el in els:
                try:
                    el.click()
                    time.sleep(0.5)
                    return
                except:
                    pass
    except:
        pass

def get_soup_js(url: str) -> BeautifulSoup:
    driver.get(url)
    accept_cookies_if_present()
    # Espera a que carguen tarjetas o el contenedor principal
    try:
        wait.until(EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article, [data-testid='job-card'], .job-card")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "main, section"))
        ))
    except:
        pass
    # Scroll por si hay carga diferida
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    except:
        pass
    return BeautifulSoup(driver.page_source, "html.parser")

def parse_cards(soup: BeautifulSoup):
    rows = []
    cards = soup.select("article, .list-item, .sc-card, .job-card, [data-testid='job-card']")
    for c in cards:
        a = c.select_one("a[href*='/empleo/'], a[href*='/trabajo/'], a[href*='/oferta/'], a[href*='/job/']")
        if not a:
            continue
        url = a.get("href")
        if url and url.startswith("/"):
            url = BASE + url
        title = (a.get_text(strip=True) or "").replace("\n", " ")
        company_node = c.select_one(".company, .sc-company, .card-company, [data-testid='company-name'], [class*='empresa']")
        company = company_node.get_text(strip=True) if company_node else ""
        location_node = c.select_one(".location, .sc-location, [data-testid='job-location'], [class*='ubicacion']")
        location = location_node.get_text(strip=True) if location_node else ""
        if url and title:
            rows.append({"title": title, "url": url, "company": company, "location": location})
    return rows

def build_page_url(start_url: str, page_number: int) -> str:
    # Soporta ...-p2.html o ?page=2
    if page_number == 1:
        return start_url
    if start_url.endswith(".html"):
        return start_url[:-5] + f"-p{page_number}.html"
    if "page=" in start_url:
        return re.sub(r"page=\\d+", f"page={page_number}", start_url)
    sep = "&" if "?" in start_url else "?"
    return f"{start_url}{sep}page={page_number}"

def crawl_all_pages_js(start_url: str, max_pages: int = 50) -> pd.DataFrame:
    all_rows = []
    for p in range(1, max_pages + 1):
        urlp = build_page_url(start_url, p)
        soup = get_soup_js(urlp)
        page_rows = parse_cards(soup)
        print(f"p{p}: {len(page_rows)} avisos")
        if p > 1 and len(page_rows) == 0:
            print("Sin tarjetas -> corto")
            break
        all_rows.extend(page_rows)
        time.sleep(1.0)
    return pd.DataFrame(all_rows).drop_duplicates(subset=["url"]).reset_index(drop=True)
