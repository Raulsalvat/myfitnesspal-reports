import pandas as pd

def process_myfitnesspal_csv():
    # Carga el archivo CSV (asegúrate de que la ruta sea correcta)
    df = pd.read_csv("myfitnesspal - Hoja-1.csv")

    # Renombra las columnas largas a nombres limpios
    df.rename(columns={
        "Date": "date",
        "Meal": "meal",
        "Time": "time",
        "Calories": "calories",
        "Fat (g)": "fat_g",
        "Saturated Fat": "fat_saturated",
        "Polyunsaturated Fat": "fat_poly",
        "Monounsaturated Fat": "fat_mono",
        "Trans Fat": "fat_trans",
        "Cholesterol": "cholesterol",
        "Sodium (mg)": "sodium_mg",
        "Potassium": "potassium",
        "Carbohydrates (g)": "carbs_g",
        "Fiber": "fiber",
        "Sugar": "sugar",
        "Protein (g)": "protein_g",
        "Vitamin A": "vitamin_a",
        "Vitamin C": "vitamin_c",
        "Calcium": "calcium",
        "Iron": "iron",
        "Note": "note"
    }, inplace=True)

    return df
