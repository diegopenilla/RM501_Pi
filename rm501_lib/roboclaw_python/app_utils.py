from typing import Optional
import pandas as pd
import streamlit as st

def load_positions_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return [[int(i) for i in list(d.values())] for d in df.to_dict(orient="records")]
    except Exception as e:
        st.error(f"Error loading positions from CSV: {e}")
        return []


def save_positions_to_csv(data: list[list[int]], file_path: Optional[str] = "positions.csv"):
    try:
        datos = list()
        for pos in data:
            datos.append({
                "pos0": pos[0],
                "pos1": pos[1],
                "pos2": pos[2],
                "pos3": pos[3],
                "pos4": pos[4],
            })

        df = pd.DataFrame(datos)
        if file_path:
            df.to_csv(file_path, index=False)
        return df
    except Exception as e:
        st.error(f"Error saving positions to CSV: {e}")


if __name__ == "__main__":

    positions = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15]
    ]
    df = save_positions_to_csv(positions, "kpr_positions.csv")
    print("Saved positions to CSV")
    read_positions = load_positions_from_csv("positions.csv")