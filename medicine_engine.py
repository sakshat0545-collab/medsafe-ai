import pandas as pd
from fuzzywuzzy import process


class MedicineEngine:
    def __init__(self, csv_path="data/medicines.csv"):
        """
        Initialize the medicine engine and load the dataset.
        """
        self.data = pd.read_csv(csv_path)

        # Create a unified searchable list of all medicines
        self.all_medicines = list(
            set(
                self.data["medicine"].astype(str).tolist()
                + self.data["interacts_with"].astype(str).tolist()
            )
        )

    def match_medicine(self, input_name):
        """
        Perform fuzzy matching to find the closest medicine name.
        """
        if not input_name:
            return None

        match = process.extractOne(input_name, self.all_medicines)

        # Only accept reasonably confident matches
        if match and match[1] >= 70:
            return match[0]

        return None

    def check_interactions(self, medicines):
        """
        Check pairwise interactions between provided medicines.
        Returns a list of interaction dictionaries.
        """
        interactions = []

        for i in range(len(medicines)):
            for j in range(i + 1, len(medicines)):

                med1 = medicines[i]
                med2 = medicines[j]

                # Check both directions
                row = self.data[
                    (
                        (self.data["medicine"] == med1)
                        & (self.data["interacts_with"] == med2)
                    )
                    |
                    (
                        (self.data["medicine"] == med2)
                        & (self.data["interacts_with"] == med1)
                    )
                ]

                if not row.empty:
                    interaction_info = row.iloc[0]

                    interactions.append(
                        {
                            "medicine_1": med1,
                            "medicine_2": med2,
                            "risk": interaction_info["risk"],
                            "drug_class": interaction_info.get("drug_class", ""),
                            "description": interaction_info.get("description", ""),
                        }
                    )

        return interactions