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
      
