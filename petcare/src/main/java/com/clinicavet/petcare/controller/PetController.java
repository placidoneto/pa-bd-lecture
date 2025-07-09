package com.clinicavet.petcare.controller;
import com.clinicavet.petcare.model.Pet;
import com.clinicavet.petcare.service.PetService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pets")
@CrossOrigin(origins = "*")
public class PetController {

    private final PetService petService;

    public PetController(PetService petService) {
        this.petService = petService;
    }

    @PostMapping
    public ResponseEntity<Pet> salvar(@RequestBody Pet pet) {
        return ResponseEntity.ok(petService.salvar(pet));
    }

    @GetMapping
    public ResponseEntity<List<Pet>> listarTodos() {
        return ResponseEntity.ok(petService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Pet> buscarPorId(@PathVariable Long id) {
        return petService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Pet> atualizar(@PathVariable Long id, @RequestBody Pet pet) {
        return ResponseEntity.ok(petService.atualizar(id, pet));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        petService.deletar(id);
        return ResponseEntity.noContent().build();
    }
}
