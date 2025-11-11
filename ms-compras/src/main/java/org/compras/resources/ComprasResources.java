package org.compras.resources;

import org.compras.models.Compra;
import org.compras.services.CompraService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/compras")
public class ComprasResources {

    @Autowired
    private CompraService compraService;

    @PostMapping("/realizar")
    public ResponseEntity<String> realizarCompra(@RequestBody Compra compra) {
        int status = compraService.realizarCompra(compra);

        if (status == 200) return ResponseEntity.ok("Compra Registrada");
        else return ResponseEntity.status(400).body("Error registrando compra");
    }

    @PostMapping("compensar")
    public ResponseEntity<String> compensarCompra(@RequestBody Compra compra) {
        compraService.compensarCompra(compra);
        return ResponseEntity.ok("Compra revertida");
    }

    @GetMapping("/listar")
    public ResponseEntity<?> listarCompras() {
        return ResponseEntity.ok(compraService.listarCompras());
    }
}
