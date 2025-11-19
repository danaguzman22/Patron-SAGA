from fastapi import FastAPI, Response, status
import random

app = FastAPI()

@app.get("/inventario")
def verificar_inventario():
  stock = random.choice([True, False])

  if stock:
        return Response(
            content='{"mensaje": "Hay stock disponible"}',
            media_type="application/json",
            status_code=status.HTTP_200_OK
        )
  else:
      return Response(
          content='{"mensaje": "Sin stock"}',
          media_type="application/json",
          status_code=status.HTTP_409_CONFLICT
      )
      
#sugerencias de edicion en inventario (ayuda)
"""El enunciado dice que todos los microservicios que participan de la transacción deben tener:

✔ 1. Un endpoint de transacción

→ en inventario sería: reservar stock

✔ 2. Un endpoint de compensación

→ en inventario sería: revertir reserva de stock

Y además:

✔ 3. Inventario debe devolver 200 o 409 aleatorio

(Que ya se hace, pero solo en un endpoint)

Pero esto NO sirve para Saga, porque:

Falta un endpoint para realizar la acción real (reservar)

Falta un endpoint para compensar (compensar)

Falta usar POST para ambas operaciones

El orquestador que NO puede funcionar con este inventario"""

# from fastapi import FastAPI, Response, status
# import random
# import time

# app = FastAPI()

# @app.post("/inventario/reservar")
# def reservar_inventario():
#     """
#     Intenta reservar inventario.
#     Devuelve 200 si hay stock, 409 si no hay.
#     """
#     time.sleep(random.uniform(0.2, 1.0))  # Simula latencia

#     exito = random.choice([True, False])

#     if exito:
#         return Response(
#             content='{"mensaje": "Inventario reservado"}',
#             media_type="application/json",
#             status_code=status.HTTP_200_OK
#         )

#     return Response(
#         content='{"mensaje": "Sin stock disponible"}',
#         media_type="application/json",
#         status_code=status.HTTP_409_CONFLICT
#     )


# @app.post("/inventario/compensar")
# def compensar_inventario():
#     """
#     Compensa la reserva (si otro microservicio falló).
#     Siempre retorna 200.
#     """
#     time.sleep(random.uniform(0.1, 0.6))  # Simula latencia

#     return Response(
#         content='{"mensaje": "Reserva revertida"}',
#         media_type="application/json",
#         status_code=status.HTTP_200_OK
#     )
