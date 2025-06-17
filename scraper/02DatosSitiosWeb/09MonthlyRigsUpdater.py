import pandas as pd
import math
import hashlib

def recalculate_first_row(hist_df):
    hist_df["Last"] = hist_df["Last"].astype(float).round(0)

    if len(hist_df) > 1:
        hist_df.at[0, "Change"] = round(hist_df.at[0, "Last"] - hist_df.at[1, "Last"], 2)
        hist_df.at[0, "%Chg"] = round((hist_df.at[0, "Change"] / hist_df.at[1, "Last"] * 100), 1) if hist_df.at[1, "Last"] != 0 else None
    else:
        hist_df.at[0, "Change"] = None
        hist_df.at[0, "%Chg"] = None

    try:
        current_anio = int(hist_df.at[0, "Anio"])
        current_mes = hist_df.at[0, "Mes"]
        match = hist_df[(hist_df["Anio"] == str(current_anio - 1)) & (hist_df["Mes"] == current_mes)]
        if not match.empty:
            previous_value = float(match.iloc[0]["Last"])
            change = round(hist_df.at[0, "Last"] - previous_value, 2)
            percent = round((change / previous_value) * 100, 1) if previous_value != 0 else None
            hist_df.at[0, "YearChange"] = change
            hist_df.at[0, "Year%Chg"] = percent
        else:
            hist_df.at[0, "YearChange"] = None
            hist_df.at[0, "Year%Chg"] = None
    except:
        hist_df.at[0, "YearChange"] = None
        hist_df.at[0, "Year%Chg"] = None

    return hist_df

def dataframe_checksum(df):
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def analyze_worldwide_rig_data():
    hist_path = "scraper/01HistoricalDatabase/12WorldWideRigMensual.csv"
    hist_df = pd.read_csv(hist_path, dtype=str)
    original_checksum = dataframe_checksum(hist_df)

    anio = hist_df.loc[0, "Anio"]
    mes = hist_df.loc[0, "Mes"]
    last = int(round(float(hist_df.loc[0, "Last"])))

    current_data = [anio, mes, last]
    print("Current historical data:", current_data)

    new_path = "scraper/02DatosSitiosWeb/csv/WorldWide_Rig_Count.csv"
    new_df = pd.read_csv(new_path, dtype=str)
    new_df["Rig Count Value"] = new_df["Rig Count Value"].astype(float).round(0).astype(int)

    filtered = new_df[(new_df["Year"] == anio) & (new_df["Month"] == mes)]
    if filtered.empty:
        print("❌ No matching data found for the given year and month.")
        return

    total_rig_count = filtered["Rig Count Value"].sum()
    print(f"🔎 Total Rig Count for {mes}/{anio}: {total_rig_count}")

    updated_hist_df = hist_df.copy()

    if total_rig_count == last:
        print("✅ No changes. Looking for next month...")
    else:
        print("⚠️ Rig Count has changed. Updating historical value...")
        updated_hist_df.at[0, "Last"] = float(round(total_rig_count, 0))
        updated_hist_df = recalculate_first_row(updated_hist_df)

    anio_int = int(anio)
    mes_int = int(mes)
    if mes_int == 12:
        next_anio = str(anio_int + 1)
        next_mes = "01"
    else:
        next_anio = anio
        next_mes = str(mes_int + 1).zfill(2)

    next_filtered = new_df[(new_df["Year"] == next_anio) & (new_df["Month"] == next_mes)]
    if not next_filtered.empty:
        print("📈 New month data encountered. Adding to historical file...")
        next_total = float(round(next_filtered["Rig Count Value"].sum(), 0))
        new_row = pd.DataFrame([[next_anio, next_mes, next_total]], columns=["Anio", "Mes", "Last"])
        updated_hist_df = pd.concat([new_row, updated_hist_df], ignore_index=True)
        updated_hist_df = recalculate_first_row(updated_hist_df)
    else:
        print("📉 No new month data available.")

    updated_checksum = dataframe_checksum(updated_hist_df)
    if updated_checksum != original_checksum:
        updated_hist_df.to_csv(hist_path, index=False)
        print("✅ Historical file updated with recalculated fields.")
    else:
        print("🟡 No changes detected. File was not modified.")

if __name__ == "__main__":
    analyze_worldwide_rig_data()
