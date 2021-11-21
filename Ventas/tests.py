from django.contrib.auth.models import User

from django.test import TestCase

import json

from rest_framework.test import APIClient
from rest_framework import status

class EcommerceCase(TestCase):

    def setUp(self):

        # Creamos un usuario y generamos el acceso a la api para hacer pruebas de forma general
        user = User(
            email='testing_login@clicoh.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('admin123')
        user.save()

        client = APIClient()
        response = client.post(
                '/api/token/', {
                'username': 'testing_login',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access']
        self.user = user

    def test_get_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/product')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/order')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orderdetail(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/orderdetail')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orderwithdetails(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get('/api/orderwithdetails')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unauthorized(self):

        client = APIClient()

        response = client.get('/api/product')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get('/api/order')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get('/api/orderdetail')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get('/api/orderwithdetails')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)

    def test_post_productNegativePrice(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": -5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese un Precio mayor o igual a Cero")

    def test_post_productNegativeStock(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": -300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese un stock mayor o igual a Cero")

    def test_post_productWithoutName(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Debe especificar el nombre")

    def test_post_productBlankName(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Debe ingresar un nombre")

    def test_post_productWithouStockPrice(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana"
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 0)
        self.assertEqual(result["stock"], 0)

    def test_update_productName(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana Update"
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana Update")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)

    def test_update_productPrice(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "price": 100.87
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 100.87)
        self.assertEqual(result["stock"], 300)

    def test_update_productStock(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "stock": 600
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 600)

    def test_update_productBlankName(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": ""
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Debe ingresar un nombre")

    def test_update_productNegativePrice(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "price": -5.0
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese un Precio mayor o igual a Cero")

    def test_update_productNegativeStock(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "stock": -300,
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese un stock mayor o igual a Cero")

    def test_post_multipleproduct(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)


        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 50)

    def test_update_multipleproduct(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "stock": 700
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera update",
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 700)


        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera update")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 50)


    def test_post_update_multipleproduct(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "stock": 700
                                    },
                                    {
                                        "id": "Cara-Mandarina",
                                        "name": "Caramelo Mandarina",
                                        "price": 5.0,
                                        "stock": 400
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 700)


        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 50)


        response = client.get('/api/product/Cara-Mandarina')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Mandarina")
        self.assertEqual(result["name"], "Caramelo Mandarina")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 400)

    def test_delete_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)

        response = client.delete('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["Respuesta"][0], "Se elimino el Producto")

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_productinOrder(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [{
                "id": "Cara-Manzana",
                "name": "Caramelo Manzana",
                "price": 5.0,
                "stock": 300
            }],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)


        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Manzana"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.delete('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No se puede eliminar un producto que exite en una Orden, elimine primero la Orden")

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_orderwithdetails(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["id"], 99)
        self.assertEqual(result["order"][0]["cuantity"], 10)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 10)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 290)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 40)

    def test_post_orderwithdetailsNonExistenProduct(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Manzana test"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No existe el producto Cara-Manzana test")

    def test_post_orderwithdetailsNegativeCuantity(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": -10,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese una Cantidad mayor a 0 (Cero)")

    def test_post_orderwithdetailsZeroCuantity(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 0,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese una Cantidad mayor a 0 (Cero)")

    def test_post_orderwithdetailsNoStock(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 301,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No posee el Stock suficiente en el producto Cara-Manzana")

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_orderwithdetailsAllStock(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 300,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post_orderwithdetails2products(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 20,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Manzana"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Productos duplicados Cara-Manzana")

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["stock"], 300)


        response = client.get('/api/product/order/99')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_orderwithdetailsAlreadyExists(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                                        {
                                            "id": 99,
                                            "date_time": "2021-11-20T22:03:18.892433",
                                        }
                                    ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 20,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ya existe la orden 99")

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["stock"], 300)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["stock"], 50)

        response = client.get('/api/orderwithdetails/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(len(result["order"]), 0)

    def test_delete_orderwithdetails(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
                '/api/product', [
                                    {
                                        "id": "Cara-Manzana",
                                        "name": "Caramelo Manzana",
                                        "price": 5.0,
                                        "stock": 300
                                    },
                                    {
                                        "id": "Cara-Pera",
                                        "name": "Caramelo Pera",
                                        "price": 5.0,
                                        "stock": 50
                                    }
                                ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
                '/api/orderwithdetails',    [
                                                {
                                                    "id": 99,
                                                    "date_time": "2021-11-20T22:03:18.892433",
                                                    "order": [
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Manzana"
                                                                },
                                                                {
                                                                    "cuantity": 10,
                                                                    "product": "Cara-Pera"
                                                                }
                                                             ]
                                                }
                                            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["id"], 99)
        self.assertEqual(result["order"][0]["cuantity"], 10)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 10)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 290)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 40)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["id"], 99)
        self.assertEqual(result["order"][0]["cuantity"], 10)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 10)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.delete('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 300)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 50)

    def test_post_order(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/order', [
                                        {
                                            "id": 99,
                                            "date_time": "2021-11-20T22:03:18.892433",
                                        }
                                    ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_orderdetail(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 20,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["order"][0]["cuantity"], 20)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 10)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 280)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 40)

    def test_post_orderdetailNegativeCuantity(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": -20,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese una Cantidad mayor a 0 (Cero)")

    def test_post_orderdetailZeroCuantity(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 0,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese una Cantidad mayor a 0 (Cero)")

    def test_post_orderdetailNonExistenProduct(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 20,
                                        "product": "Cara-Manzana Test"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No existe el producto")

    def test_post_orderdetailNonExistenOrder(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 100,
                                        "cuantity": 20,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No existe la orden")

    def test_post_orderdetailWithoutOrder(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "cuantity": 20,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "Ingrese una orden")

    def test_update_orderdetailMoreQuantity(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 20,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 50,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 30,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["order"][0]["cuantity"], 50)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 30)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 250)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 20)

    def test_update_orderdetailLessQuantity(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 50,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 30,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/orderwithdetails/99')
        result = json.loads(response.content)
        self.assertEqual(result["order"][0]["cuantity"], 10)
        self.assertEqual(result["order"][0]["product"], "Cara-Manzana")
        self.assertEqual(result["order"][1]["cuantity"], 10)
        self.assertEqual(result["order"][1]["product"], "Cara-Pera")


        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Manzana")
        self.assertEqual(result["name"], "Caramelo Manzana")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 290)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result["id"], "Cara-Pera")
        self.assertEqual(result["name"], "Caramelo Pera")
        self.assertEqual(result["price"], 5.0)
        self.assertEqual(result["stock"], 40)

    def test_update_orderdetailNoStock(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(
            '/api/product', [
                {
                    "id": "Cara-Manzana",
                    "name": "Caramelo Manzana",
                    "price": 5.0,
                    "stock": 300
                },
                {
                    "id": "Cara-Pera",
                    "name": "Caramelo Pera",
                    "price": 5.0,
                    "stock": 50
                }
            ],
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Manzana')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/product/Cara-Pera')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/order', [
                {
                    "id": 99,
                    "date_time": "2021-11-20T22:03:18.892433",
                }
            ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/order/99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(
            '/api/orderdetail', [
                                    {
                                        "order": 99,
                                        "cuantity": 301,
                                        "product": "Cara-Manzana"
                                    },
                                    {
                                        "order": 99,
                                        "cuantity": 10,
                                        "product": "Cara-Pera"
                                    }
                                 ],
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.content)
        self.assertEqual(result["Error"][0], "No posee el Stock suficiente en el producto")









































