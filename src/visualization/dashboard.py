import pandas as pd

def build_event_impact_table(results):
    """
    Create a table summarizing the impacts of political, economic, business, and technological factors.
    """
    rows = []
    for result in results:
        if result:
            # Приклад обробки відповідей, додаючи фактори в таблицю
            impact = result.get("impact", {})
            rows.append({
                "Factor": impact.get("factor", "Unknown"),
                "Description": impact.get("description", ""),
                "Cryptocurrency": impact.get("cryptocurrency", ""),
                "Impact on Price": impact.get("price_impact", "")
            })
    df = pd.DataFrame(rows)
    return df
