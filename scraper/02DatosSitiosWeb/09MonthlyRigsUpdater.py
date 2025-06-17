import pandas as pd
import math

def analyze_worldwide_rig_data():
    # Step 1: Read the historical CSV and get the first row values
    hist_path = "scraper/01HistoricalDatabase/12WorldWideRigMensual.csv"
    hist_df = pd.read_csv(hist_path, dtype=str)
    
    anio = hist_df.loc[0, "Anio"]
    mes = hist_df.loc[0, "Mes"]
    last = int(round(float(hist_df.loc[0, "Last"])))

    # Store into a vector
    current_data = [anio, mes, last]
    print("Current historical data:", current_data)

    # Step 2: Read the new CSV to compare against
    new_path = "scraper/02DatosSitiosWeb/csv/WorldWide_Rig_Count.csv"
    new_df = pd.read_csv(new_path, dtype=str)

    # Ensure numeric fields are converted
    new_df["Rig Count Value"] = new_df["Rig Count Value"].astype(float).round(0).astype(int)

    # Step 3: Filter based on Year and Month from the vector
    filtered = new_df[(new_df["Year"] == anio) & (new_df["Month"] == mes)]

    if filtered.empty:
        print("❌ No matching data found for the given year and month.")
        return

    total_rig_count = filtered["Rig Count Value"].sum()
    print(f"🔎 Total Rig Count for {mes}/{anio}: {total_rig_count}")

    if total_rig_count == last:
        print("✅ No changes. Looking for next month...")
    else:
        print("⚠️ Rig Count has changed. Updating historical value...")
        hist_df.at[0, "Last"] = total_rig_count
        hist_df.to_csv(hist_path, index=False)
        print(f"✅ Updated 'Last' value to {total_rig_count} in historical file.")

    # Step 4: Look for the next month
    anio_int = int(anio)
    mes_int = int(mes)
    if mes_int == 12:
        next_anio = str(anio_int + 1)
        next_mes = "01"
    else:
        next_anio = anio
        next_mes = str(mes_int + 1)

    next_filtered = new_df[(new_df["Year"] == next_anio) & (new_df["Month"] == next_mes)]

    if not next_filtered.empty:
        print("📈 New month data encountered. Adding to historical file...")
        next_total = next_filtered["Rig Count Value"].sum()
        new_row = pd.DataFrame([[next_anio, next_mes, next_total]], columns=["Anio", "Mes", "Last"])
        updated_hist_df = pd.concat([new_row, hist_df], ignore_index=True)
        updated_hist_df.to_csv(hist_path, index=False)
        print(f"✅ Added new row: [{next_anio}, {next_mes}, {next_total}] to historical file.")
    else:
        print("📉 No new month data available.")

if __name__ == "__main__":
    analyze_worldwide_rig_data()
