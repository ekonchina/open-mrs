import json
import pytest
import requests
from requests.auth import HTTPBasicAuth


BASE_URL = "http://localhost/openmrs/ws/rest/v1"
USERNAME = "admin"
PASSWORD = "Admin123"


# ----------------------------
# HTTP helpers
# ----------------------------
def api_post_person(payload: dict) -> requests.Response:
    return requests.post(
        f"{BASE_URL}/person",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        data=json.dumps(payload),
    )


def api_get_person(person_uuid: str, v: str = "full") -> requests.Response:
    return requests.get(
        f"{BASE_URL}/person/{person_uuid}",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Accept": "application/json"},
        params={"v": v},
    )


def pretty(obj) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)
    except Exception:
        return str(obj)


# ----------------------------
# Assertions: common structures
# ----------------------------
def assert_is_non_empty_str(value, field_name: str):
    assert isinstance(value, str) and value.strip(), f"{field_name} must be non-empty string, got: {value!r}"


def assert_links_structure(obj: dict, allow_full: bool = True):
    links = obj.get("links")
    assert isinstance(links, list), f"links must be list, got: {type(links)}; body={pretty(obj)}"
    assert links, f"links must be non-empty list; body={pretty(obj)}"

    for link in links:
        assert isinstance(link, dict), f"each link must be dict, got: {type(link)}; link={link}"
        assert_is_non_empty_str(link.get("rel"), "link.rel")
        # resourceAlias иногда есть, иногда нет — но в OpenMRS обычно есть
        if "resourceAlias" in link:
            assert_is_non_empty_str(link.get("resourceAlias"), "link.resourceAlias")
        assert_is_non_empty_str(link.get("uri"), "link.uri")

    # Часто присутствует self, а full может быть в create-ответе тоже
    rels = {l.get("rel") for l in links if isinstance(l, dict)}
    assert "self" in rels, f"Expected 'self' link; rels={rels}; body={pretty(obj)}"
    if allow_full:
        # не всегда обязано быть, но у тебя оно есть — пусть будет мягко:
        pass


def assert_boolean_field(obj: dict, field: str):
    assert field in obj, f"{field} missing; body={pretty(obj)}"
    assert isinstance(obj[field], bool), f"{field} must be bool, got {type(obj[field])}; body={pretty(obj)}"


# ----------------------------
# Assertions: create response (default rep)
# ----------------------------
def assert_create_person_response(created: dict, expected_gender: str):
    assert isinstance(created, dict), f"Response must be dict, got {type(created)}"

    # id fields
    assert_is_non_empty_str(created.get("uuid"), "uuid")
    assert_is_non_empty_str(created.get("display"), "display")

    # gender
    assert created.get("gender") == expected_gender, f"gender mismatch: {pretty(created)}"

    # flags / standard fields
    assert_boolean_field(created, "voided")
    assert created["voided"] is False, f"Expected voided=False; body={pretty(created)}"

    # resourceVersion may exist (у тебя есть)
    if "resourceVersion" in created:
        assert_is_non_empty_str(created.get("resourceVersion"), "resourceVersion")

    # preferredName structure in default rep (у тебя есть)
    pref = created.get("preferredName")
    assert isinstance(pref, dict), f"preferredName missing/not dict: {pretty(created)}"
    assert_is_non_empty_str(pref.get("uuid"), "preferredName.uuid")
    if "display" in pref:
        assert_is_non_empty_str(pref.get("display"), "preferredName.display")
    if "links" in pref:
        assert_links_structure(pref, allow_full=False)

    # links structure on person
    assert_links_structure(created)


# ----------------------------
# Assertions: full response (v=full)
# ----------------------------
def assert_full_person_response(full: dict, expected: dict):
    assert isinstance(full, dict), f"Full response must be dict, got {type(full)}"

    # core fields
    assert_is_non_empty_str(full.get("uuid"), "uuid")
    assert_is_non_empty_str(full.get("display"), "display")
    assert full.get("gender") in ("M", "F", "U"), f"Unexpected gender in full: {full.get('gender')}; body={pretty(full)}"

    # presence of common fields in full (как правило есть всегда)
    for field in [
        "attributes",
        "birthdateEstimated",
        "dead",
        "deathdateEstimated",
        "voided",
    ]:
        assert field in full, f"{field} missing in full; body={pretty(full)}"

    assert isinstance(full["attributes"], list), f"attributes must be list; body={pretty(full)}"
    assert_boolean_field(full, "birthdateEstimated")
    assert_boolean_field(full, "dead")
    assert_boolean_field(full, "deathdateEstimated")
    assert_boolean_field(full, "voided")
    assert full["voided"] is False, f"Expected voided=False; body={pretty(full)}"

    # death fields consistency (мягкая проверка)
    if full.get("dead") is False:
        # когда dead=False, causeOfDeath/deathDate часто None
        pass

    # preferredName and preferredAddress can be None/obj
    pref = full.get("preferredName")
    assert isinstance(pref, dict), f"preferredName missing/not dict in full; body={pretty(full)}"
    assert_is_non_empty_str(pref.get("uuid"), "preferredName.uuid")
    if "display" in pref:
        assert_is_non_empty_str(pref.get("display"), "preferredName.display")

    # names should be present in v=full
    names = full.get("names")
    assert isinstance(names, list) and names, f"names missing/empty in full; body={pretty(full)}"
    for n in names:
        assert isinstance(n, dict), f"name item must be dict; got {type(n)}"
        # minimal expected fields in name
        assert_is_non_empty_str(n.get("uuid"), "name.uuid")
        assert_boolean_field(n, "voided")
        # given/family may exist depending on how name stored, but usually there
        # делаем мягко: хотя бы display обязан быть
        assert_is_non_empty_str(n.get("display"), "name.display")

    # verify expected name exists (точная проверка given+family)
    exp_given = expected["givenName"]
    exp_family = expected["familyName"]
    found_exact = any(
        (n.get("givenName") == exp_given and n.get("familyName") == exp_family and n.get("voided") is False)
        for n in names
        if isinstance(n, dict)
    )
    assert found_exact, (
        f"Expected exact name not found: {exp_given} {exp_family}\n"
        f"names={pretty(names)}\nfull={pretty(full)}"
    )

    # verify gender matches expectation
    if "gender" in expected:
        assert full.get("gender") == expected["gender"], f"gender mismatch in full; body={pretty(full)}"

    # birthdate / age checks (учитываем формат даты в ответе)
    if "birthdate" in expected:
        bd = full.get("birthdate")
        assert bd, f"birthdate missing in full; body={pretty(full)}"
        assert isinstance(bd, str), f"birthdate must be str; got {type(bd)}; body={pretty(full)}"
        assert bd.startswith(expected["birthdate"]), f"birthdate mismatch: got {bd}; expected prefix {expected['birthdate']}"

    if "age" in expected:
        # age может быть int или None в зависимости от сборки/конфига,
        # но если сервер возвращает age — проверим.
        if full.get("age") is not None:
            assert full.get("age") == expected["age"], f"age mismatch; body={pretty(full)}"

    # links in full
    assert_links_structure(full)


# ----------------------------
# Positive tests
# ----------------------------
@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            {"names": [{"givenName": "John", "familyName": "Doe"}], "gender": "M"},
            {"givenName": "John", "familyName": "Doe", "gender": "M"},
        ),
        (
            {"names": [{"givenName": "Alice", "familyName": "Smith"}], "gender": "F", "age": 30},
            {"givenName": "Alice", "familyName": "Smith", "gender": "F", "age": 30},
        ),
        (
            {"names": [{"givenName": "Bob", "familyName": "Brown"}], "gender": "M", "birthdate": "1990-01-15"},
            {"givenName": "Bob", "familyName": "Brown", "gender": "M", "birthdate": "1990-01-15"},
        ),
        (
            # middleName просто как дополнительное поле (в exact match проверяем given+family)
            {"names": [{"givenName": "Ivan", "middleName": "Petrovich", "familyName": "Sidorov"}], "gender": "M"},
            {"givenName": "Ivan", "familyName": "Sidorov", "gender": "M"},
        ),
        (
            # multiple names: проверяем, что хотя бы первый реально есть
            {"names": [{"givenName": "Maria", "familyName": "Garcia"}, {"givenName": "Masha", "familyName": "Garcia"}], "gender": "F"},
            {"givenName": "Maria", "familyName": "Garcia", "gender": "F"},
        ),
    ],
)
def test_create_person_full_validation(payload, expected):
    # 1) CREATE
    create_resp = api_post_person(payload)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.status_code}\n{create_resp.text}"
    created = create_resp.json()

    # (опционально) полный вывод в лог pytest:
    print("CREATE RESPONSE JSON:\n", pretty(created))

    # 2) validate create response (default rep)
    assert_create_person_response(created, expected_gender=expected["gender"])

    person_uuid = created["uuid"]

    # 3) GET FULL
    full_resp = api_get_person(person_uuid, v="full")
    assert full_resp.status_code == 200, f"Get full failed: {full_resp.status_code}\n{full_resp.text}"
    full = full_resp.json()

    print("FULL RESPONSE JSON:\n", pretty(full))

    # 4) validate full response deeply
    assert_full_person_response(full, expected)


