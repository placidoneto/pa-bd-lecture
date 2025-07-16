package com.clinicavet.petcare.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.clinicavet.petcare.model.Cirurgia;
import com.clinicavet.petcare.service.CirurgiaService;

@RestController
@RequestMapping("/api/cirurgias")
@CrossOrigin(origins = "*")
public class CirurgiaController {

    private final CirurgiaService cirurgiaService;

    public CirurgiaController(CirurgiaService cirurgiaService) {
        this.cirurgiaService = cirurgiaService;
    }

    @PostMapping
    public ResponseEntity<Cirurgia> salvar(@RequestBody Cirurgia cirurgia) {
        return ResponseEntity.ok(cirurgiaService.salvar(cirurgia));
    }

    @GetMapping
    public ResponseEntity<List<Cirurgia>> listarTodos() {
        return ResponseEntity.ok(cirurgiaService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Cirurgia> buscarPorId(@PathVariable Long id) {
        return cirurgiaService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Cirurgia> atualizar(@PathVariable Long id, @RequestBody Cirurgia cirurgia) {
        return ResponseEntity.ok(cirurgiaService.atualizar(id, cirurgia));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        cirurgiaService.deletar(id);
        return ResponseEntity.noContent().build();
    }
} 