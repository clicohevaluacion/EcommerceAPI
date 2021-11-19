![alt text](https://play-lh.googleusercontent.com/jUVC_febXM8dxgLuhOkvT4acVl7x6pYngNtEHkCnWeSBQRNPcTon4YOSiixjsOlt4EQ)

#Sistema de Ecommerce para evaluacion de postulante en Clicoh

El sistema esta en produccion en heroku https://clicohevaluacion.herokuapp.com/api

#Obtener token

El token se obtiene con el metodo "POST" en "https://clicohevaluacion.herokuapp.com/api/token/" donde se debe ingresar las credenciales

    {"username": "   ",
    "password": "    "}

donde se obtendra el refresh y el access

    {
        "refresh": "",
        "access": ""
    }

#Productos

Se pude listar todos los productos con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/product

Se puede crear o editar los productos de manera simultanea con el metodo "POST" en https://clicohevaluacion.herokuapp.com/api/product de la siguente manera

     [
            {
                "id": "Cara-Frutilla",
                "name": "Caramelo Frutilla",
                "price": 5.0,
                "stock": 189
            },
            {
                "id": "Cara-Limon",
                "name": "Caramelo Limon",
                "price": 5.0,
                "stock": 103
            }
    ]

Si el id del producto existe se modificara los datos enviados.
Si el id no existe se creara el producto

Con el metodo "DELETE" se puede eliminar un producto introduciendo a continuacion de https://clicohevaluacion.herokuapp.com/api/product/{pk} donde {pk} es el id del producto

Por ejemplo https://clicohevaluacion.herokuapp.com/api/product/Cara-Limon

Solo se podra borrar productos que no se encuentren en un detalle de una orden

Con el metodo "GET" se puede obtener un producto introduciendo a continuacion de https://clicohevaluacion.herokuapp.com/api/product/{pk} donde {pk} es el id del producto

Por ejemplo https://clicohevaluacion.herokuapp.com/api/product/Cara-Limon

#Orden

Se puede listar todas las ordenes con su detalles incluidos con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/orderwithdetails

Se puede obtener una orden con su detalles incluidos con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/orderwithdetails/{pk} donde {pk} es el id de la orden

Se puede listar todas las cabeceras de las ordenes con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/order

Se puede obtener una cabecera de una orden con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/order/{pk} donde {pk} es el id de la orden


Se puede cargar una orden completa con sus detalles con el metodo "POST" en https://clicohevaluacion.herokuapp.com/api/orderwithdetails

    [
        {
            "id": 3,
            "date_time": "2021-11-20T22:03:18.892433",
            "order": [
                {
                    "cuantity": 10,
                    "product": "Cara-Frutilla"
                },
                {
                    "cuantity": 10,
                    "product": "Cara-Limon"
                }
            ]
        }
    ]

Se puede modificar y agregar una cabeceras de una orden con el metodo "POST" en https://clicohevaluacion.herokuapp.com/api/order

    [
        {
            "id": 1,
            "date_time": "2021-11-20T22:03:18.892433"
        },
        {
            "id": 2,
            "date_time": "2021-11-18T01:37:35.047252"
        }
    ]



Se puede obtener una cabecera de una orden con el metodo "GET" en https://clicohevaluacion.herokuapp.com/api/order/{pk} donde {pk} es el id de la orden

Se puede eliminar una orden con el metodo "DELETE" en https://clicohevaluacion.herokuapp.com/api/order/{pk} donde {pk} es el id de la orden

Por ejemplo: https://clicohevaluacion.herokuapp.com/api/order/4

#Ordenes detalles 

Se pude modificar y agregar detalles de ordenes con el metodo "POST" en https://clicohevaluacion.herokuapp.com/api/orderdetail

Si la orden y producto ya existe solo se modificara la cantidad introducida

#Totales de venta

Se puede obtener el todal de la venta en https://clicohevaluacion.herokuapp.com/api/order/{pk}/get_total donde {pk} es el id de la orden

por ejemplo: https://clicohevaluacion.herokuapp.com/api/order/1/get_total

De igual manera se puede obtener el total en dolar blue en https://clicohevaluacion.herokuapp.com/api/order/{pk}/get_total_usd donde {pk} es el id de la orden

por ejemplo: https://clicohevaluacion.herokuapp.com/api/order/1/get_total_usd