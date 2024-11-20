import logging

def transform_s3_data(data):
    """
    Transform the nested JSON data into a flat format with required fields.

    Args:
        data (list): List of raw JSON objects.

    Returns:
        list: Transformed data as a list of dictionaries.
    """
    transformed = []
    for row in data:
        try:
            country_name = row.get("name", {}).get("common", "")
            official_name = row.get("name", {}).get("official", "")
            native_name = (
                list(row.get("name", {}).get("nativeName", {}).values())[0].get("common", "")
                if row.get("name", {}).get("nativeName")
                else ""
            )
            independence = row.get("independent", None)
            un_member = row.get("unMember", None)
            start_of_week = row.get("startOfWeek", "")
            currencies = row.get("currencies", {})
            currency_code = next(iter(currencies.keys()), "")
            currency = currencies.get(currency_code, {})
            currency_name = currency.get("name", "")
            currency_symbol = currency.get("symbol", "")
            idd_root = row.get("idd", {}).get("root", "")
            idd_suffix = next(iter(row.get("idd", {}).get("suffixes", [])), "")
            country_code = f"{idd_root}{idd_suffix}".strip()
            capital = next(iter(row.get("capital", [])), "")
            region = row.get("region", "")
            sub_region = row.get("subregion", "")
            languages = ", ".join(row.get("languages", {}).values())
            area = row.get("area", None)
            population = row.get("population", None)
            continents = ", ".join(row.get("continents", []))

            transformed.append({
                "country_name": country_name,
                "official_name": official_name,
                "native_name": native_name,
                "independence": independence,
                "un_member": un_member,
                "start_of_week": start_of_week,
                "currency_code": currency_code,
                "currency_name": currency_name,
                "currency_symbol": currency_symbol,
                "country_code": country_code,
                "capital": capital,
                "region": region,
                "sub_region": sub_region,
                "languages": languages,
                "area": area,
                "population": population,
                "continents": continents,
            })
        except Exception as e:
            logging.error(f"Error transforming row: {row}, Error: {e}")
    return transformed
