from typing import Optional
import pandas as pd


def load_positions_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df = df.fillna(0)  # Replace NaN values with 0
        positions = []
        for d in df.to_dict(orient="records"):
            position = [int(i) for i in list(d.values())]  # Convert all but last value to int
            positions.append(position)
        return positions
    except Exception as e:
        print(f"Error loading positions from CSV: {e}")
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
                "gripper_closed": pos[5]
            })

        df = pd.DataFrame(datos)
        if file_path:
            df.to_csv(file_path, index=False)
        return df
    except Exception as e:
        print(f"Error saving positions to CSV: {e}")


if __name__ == "__main__":

    # positions = [
    #     [24000, 14500, 2500, 0, 0, True],
    # ]
    # df = save_positions_to_csv(positions, "kpr_positions.csv")
    print("Saved positions to CSV")
    read_positions = load_positions_from_csv("kpr_positions.csv")