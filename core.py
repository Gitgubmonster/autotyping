def github_raw_url(path):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"

def fetch_text(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8")

def check_updates():
    print("[ОБНОВЛЕНИЕ] Проверка обновлений на GitHub...")
    try:
        manifest = json.loads(fetch_text(github_raw_url("manifest.json")))
    except Exception as e:
        print(f"[ОБНОВЛЕНИЕ] Не удалось проверить (нет сети или ошибка URL): {e}")
        print("-" * 50)
        return False

    remote_ver = manifest.get("version", "0.0.0")
    local_ver = globals().get("__version__", "0.0.0")

    if remote_ver == local_ver:
        print(f"[ОБНОВЛЕНИЕ] У вас актуальная версия ({local_ver}). Обновлений нет.")
        print("-" * 50)
        return False

    print(f"[ОБНОВЛЕНИЕ] Найдена новая версия: {local_ver} -> {remote_ver}")
    ans = input("Скачать и установить? (y/n): ").strip().lower()
    if ans != "y":
        print("[ОБНОВЛЕНИЕ] Обновление отменено пользователем.")
        print("-" * 50)
        return False

    script_dir = os.path.dirname(os.path.abspath(__file__))
    protected = set(UPDATE_PROTECTED)
    downloaded = []

    print("[ОБНОВЛЕНИЕ] Начинаю скачивание файлов...")
    try:
        for fname in manifest.get("files", []):
            if fname in protected:
                print(f"  - {fname} (защищен, пропущен)")
                continue
            print(f"  - Скачиваю {fname}...", end="", flush=True)
            url = github_raw_url(fname)
            data = fetch_text(url).encode("utf-8")
            tmp_path = os.path.join(script_dir, fname + ".new")
            with open(tmp_path, "wb") as f:
                f.write(data)
            downloaded.append((tmp_path, os.path.join(script_dir, fname)))
            print(" ОК")
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось скачать файлы: {e}")
        for tmp, _ in downloaded:
            try: os.remove(tmp)
            except: pass
        print("-" * 50)
        return False

    if not downloaded:
        print("[ОБНОВЛЕНИЕ] Нечего обновлять (все файлы в защищенном списке).")
        print("-" * 50)
        return False

    print(f"\n[ОБНОВЛЕНИЕ] Успешно скачано файлов: {len(downloaded)}")
    
    self_path = os.path.abspath(__file__)
    self_updated = any(dst == self_path for _, dst in downloaded)

    if not self_updated:
        print("[ОБНОВЛЕНИЕ] Применяю изменения...")
        for tmp, dst in downloaded:
            os.replace(tmp, dst)
        print("[ОБНОВЛЕНИЕ] Готово! Перезапустите скрипт, чтобы применить изменения.")
        print("-" * 50)
        return True

    # Если обновляется сам core.py
    bat_path = os.path.join(script_dir, "_update.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("timeout /t 2 /nobreak >nul\n")
        for tmp, dst in downloaded:
            f.write(f'move /Y "{tmp}" "{dst}"\n')
        f.write(f'start "" "{sys.executable}" "{self_path}"\n')
        f.write("del \"%~f0\"\n")

    print("\n[ОБНОВЛЕНИЕ] Скачивание завершено. Скрипт перезапустится для применения...")
    print("-" * 50)
    time.sleep(1.5)
    os.startfile(bat_path)
    sys.exit(0)
