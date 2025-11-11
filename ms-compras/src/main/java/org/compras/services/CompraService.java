package org.compras.services;

import org.compras.models.Compra;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Service
public class CompraService {

    private final List<Compra> compras = new ArrayList<>();
    private final Random random = new Random();

    public int realizarCompra(Compra compra) {
        int status = random.nextBoolean() ? 200 : 409;

        if (status == 200) {
            compras.add(compra);
        }
        return status;
    }

    public int compensarCompra(Compra compra) {
        compras.removeIf(c -> c.getId().equals(compra.getId()));
        return 200;
    }

    public List<Compra> listarCompras() {
        return compras;
    }
}
