package com.clinicavet.petcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicavet.petcare.model.Veterinario;

public interface VeterinarioRepository extends JpaRepository<Veterinario, Long> {
}
