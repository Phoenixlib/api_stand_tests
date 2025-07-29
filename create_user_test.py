import sender_stand_request
import data

def possitive_assert(first_name):
    # La versión actualizada del cuerpo de solicitud con el nombre "Aa" se guarda en la variable "user_body"
    user_body = get_user_body(first_name)
    # El resultado de la solicitud relevante se guarda en la variable "user_response"
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()
    # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

def negative_assert(first_name):
    # La versión actualizada del cuerpo de solicitud con el nombre "Aa" se guarda en la variable "user_body"
    user_body = get_user_body(first_name)
    # El resultado de la solicitud relevante se guarda en la variable "user_response"
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 400
    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert user_response.json()["code"] == 400
    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert user_response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."
    print(user_response.json())

def negative_assert_no_firstname(user_body):
    # Guarda el resultado de llamar a la función a la variable "response"
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si la respuesta contiene el código 400
    assert response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400

    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

# esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

def test_create_user_2_letter_in_first_name_get_success_response():
    possitive_assert("aa")
def test_create_user_15_letter_in_first_name_get_success_response():
    possitive_assert("aasdfgtretrecd")
def test_create_user_1_letter_in_first_name_get_success_response():
    negative_assert("a")
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert("aadfrteqwiokfjdi")
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert("A Aaa")
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("\"№%@\",")
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert("123")
# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)
# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)